#!/usr/bin/env python3
"""Validate read-only environment readiness for authorization command packs."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-pre-execution-environment-readiness-20260626.md"
COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

REPOS = {
    "AUTH-WAS-DELETE-DS-STORE-20260626": PROJECT_ROOT / "WAS世界资产体系",
    "AUTH-GPC-REVIEW-20260626": PROJECT_ROOT / "GlobalCloud GPC",
    "AUTH-PVAOS-REVIEW-20260626": PROJECT_ROOT / "GlobalCloud PVAOS",
    "AUTH-STUDIO-REVIEW-20260626": PROJECT_ROOT / "GlobalCloud Studio",
    "AUTH-GPCF-GOVERNANCE-REVIEW-20260626": ROOT,
    "AUTH-KDS-OWNER-DECISION-20260626": PROJECT_ROOT / "GlobalCloud KDS",
    "AUTH-SOP-OWNER-DECISION-20260626": PROJECT_ROOT / "GlobalCloud SOP",
}

PACKAGE_SCRIPTS = {
    "AUTH-GPC-REVIEW-20260626": {
        "package": PROJECT_ROOT / "GlobalCloud GPC/package.json",
        "scripts": ["quality:repo", "test:e2e"],
    },
    "AUTH-PVAOS-REVIEW-20260626": {
        "package": PROJECT_ROOT / "GlobalCloud PVAOS/package.json",
        "scripts": ["release:gate:local"],
    },
    "AUTH-STUDIO-REVIEW-20260626": {
        "package": PROJECT_ROOT / "GlobalCloud Studio/package.json",
        "scripts": ["harness:check", "test", "build"],
    },
}

TARGET_FILES = [
    PROJECT_ROOT / "GlobalCloud Studio/scripts/validate_studio_workflow_release_boundary.py",
    PROJECT_ROOT / "GlobalCloud Studio/scripts/validate_studio_workflow_permissions_hardening.py",
    PROJECT_ROOT / "GlobalCloud SOP/scripts/validate_sop_assets.py",
    PROJECT_ROOT / "GlobalCloud SOP/scripts/run_smoke_test.py",
]

GPCF_VALIDATORS = [
    ROOT / "tools/kds-sync/check_document_pollution.py",
    ROOT / "tools/kds-sync/validate_project_group_real_execution_governance_board.py",
    ROOT / "tools/kds-sync/validate_core_chain_real_evidence_register.py",
    ROOT / "tools/kds-sync/loop_document_gate.py",
    ROOT / "tools/kds-sync/validate_project_group_execution_authorization_receipt_ledger_20260626.py",
    ROOT / "tools/kds-sync/validate_project_group_authorization_pre_execution_command_pack_20260626.py",
    ROOT / "tools/kds-sync/validate_gpc_evidence_browser_repair.py",
    ROOT / "tools/kds-sync/validate_pvaos_release_gate_repair.py",
    ROOT / "tools/kds-sync/validate_pvaos_release_review.py",
    ROOT / "tools/kds-sync/validate_kds_brain_report_hold_review.py",
    ROOT / "tools/kds-sync/validate_sop_scenario_owner_review.py",
]

REQUIRED_EVIDENCE_TOKENS = [
    "GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001",
    "project_group_authorization_pre_execution_environment_readiness_20260626 = controlled",
    "authorization_pre_execution_environment_ready",
    "repo_path_check_count | `7`",
    "repo_path_check_pass | `7`",
    "package_script_check_pass | `6`",
    "target_file_check_pass | `4`",
    "gpcf_validator_check_pass | `11`",
    "command_execution_allowed | `false`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001",
    "globalcloud-project-group-authorization-pre-execution-environment-readiness-20260626.md",
    "validate_project_group_authorization_pre_execution_environment_readiness_20260626.py",
    "project_group_authorization_pre_execution_environment_readiness_20260626 = controlled",
    "authorization_pre_execution_environment_ready",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def is_git_repo(path: Path) -> bool:
    if not path.exists():
        return False
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def package_has_script(package_path: Path, script_name: str) -> bool:
    text = package_path.read_text(encoding="utf-8") if package_path.exists() else ""
    return f'"{script_name}"' in text


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing token: {token}")


def main() -> int:
    failures: list[str] = []
    evidence_text = read(EVIDENCE, failures)
    command_pack_text = read(COMMAND_PACK, failures)
    board_text = read(BOARD, failures)
    core_register_text = read(CORE_REGISTER, failures)
    task_packs_text = read(TASK_PACKS, failures)
    status_matrix_text = read(STATUS_MATRIX, failures)

    repo_results = {auth_id: is_git_repo(path) for auth_id, path in REPOS.items()}
    for auth_id, ok in repo_results.items():
        if not ok:
            failures.append(f"repo path is not an existing git repo: {auth_id} -> {REPOS[auth_id]}")

    script_results: dict[str, bool] = {}
    for auth_id, spec in PACKAGE_SCRIPTS.items():
        for script in spec["scripts"]:
            key = f"{auth_id}:{script}"
            script_results[key] = package_has_script(spec["package"], script)
            if not script_results[key]:
                failures.append(f"missing package script: {key}")

    target_file_results = {str(path): path.exists() for path in TARGET_FILES}
    for path, ok in target_file_results.items():
        if not ok:
            failures.append(f"missing target file: {path}")

    validator_results = {str(path): path.exists() for path in GPCF_VALIDATORS}
    for path, ok in validator_results.items():
        if not ok:
            failures.append(f"missing GPCF validator: {path}")

    require_tokens("evidence", evidence_text, REQUIRED_EVIDENCE_TOKENS, failures)
    require_tokens("command pack", command_pack_text, ["authorization_pre_execution_command_pack_ready"], failures)

    for label, text in [
        ("board", board_text),
        ("core register", core_register_text),
        ("task packs", task_packs_text),
        ("status matrix", status_matrix_text),
    ]:
        require_tokens(label, text, REQUIRED_GOVERNANCE_TOKENS, failures)

    result = {
        "gate": "project_group_authorization_pre_execution_environment_readiness_20260626",
        "status": "pass" if not failures else "fail",
        "repo_path_check_pass": sum(1 for ok in repo_results.values() if ok),
        "repo_path_check_count": len(repo_results),
        "package_script_check_pass": sum(1 for ok in script_results.values() if ok),
        "package_script_check_count": len(script_results),
        "target_file_check_pass": sum(1 for ok in target_file_results.values() if ok),
        "target_file_check_count": len(target_file_results),
        "gpcf_validator_check_pass": sum(1 for ok in validator_results.values() if ok),
        "gpcf_validator_check_count": len(validator_results),
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates read-only environment readiness only; it does not execute authorization command packs.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
