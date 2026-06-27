#!/usr/bin/env python3
"""Validate the project-group authorization pre-execution command pack."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md"
RECEIPT_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

AUTH_IDS = [
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-GPC-REVIEW-20260626",
    "AUTH-PVAOS-REVIEW-20260626",
    "AUTH-STUDIO-REVIEW-20260626",
    "AUTH-GPCF-GOVERNANCE-REVIEW-20260626",
    "AUTH-KDS-OWNER-DECISION-20260626",
    "AUTH-SOP-OWNER-DECISION-20260626",
]

REQUIRED_COMMAND_PACK_TOKENS = [
    "GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "globalcloud-project-group-first-execution-authorization-request-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-template-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md",
    "project_group_authorization_pre_execution_command_pack_20260626 = controlled",
    "authorization_pre_execution_command_pack_ready",
    "command_pack_count | `7`",
    "receipt_record_count | `0`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "A 项 WAS 单仓核对卡",
    "4.1 A 项单仓核对卡",
    "4.2 A 项确认后状态传导摘要",
    "command_pack_count=7",
    "receipt_record_count=0",
    "authorization_granted_count=0",
    "action_executed_count=0",
    "review_boundary_repo_count=6",
    "noise_cleanup_repo_count=1",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md",
    "validate_project_group_authorization_pre_execution_command_pack_20260626.py",
    "project_group_authorization_pre_execution_command_pack_20260626 = controlled",
    "authorization_pre_execution_command_pack_ready",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
]

REQUIRED_COMMAND_TOKENS_BY_AUTH = {
    "AUTH-WAS-DELETE-DS-STORE-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系",
        "git status --short --untracked-files=all",
        "git diff --check",
        "was-ds-store-noise-cleanup-receipt-*",
        "noise_decision_required",
    ],
    "AUTH-GPC-REVIEW-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC",
        "npm run quality:repo",
        "npm run test:e2e",
        "validate_gpc_evidence_browser_repair.py",
        "gpc-review-receipt-*",
    ],
    "AUTH-PVAOS-REVIEW-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS",
        "npm run release:gate:local",
        "validate_pvaos_release_gate_repair.py",
        "validate_pvaos_release_review.py",
        "pvaos-review-receipt-*",
    ],
    "AUTH-STUDIO-REVIEW-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio",
        "npm run harness:check",
        "validate_studio_workflow_release_boundary.py",
        "validate_studio_workflow_permissions_hardening.py",
        "studio-review-receipt-*",
    ],
    "AUTH-GPCF-GOVERNANCE-REVIEW-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF",
        "validate_project_group_real_execution_governance_board.py",
        "validate_core_chain_real_evidence_register.py",
        "validate_project_group_execution_authorization_receipt_ledger_20260626.py",
        "gpcf-governance-review-receipt-*",
    ],
    "AUTH-KDS-OWNER-DECISION-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS",
        "git diff --name-status",
        "validate_kds_brain_report_hold_review.py",
        "KDS TOKEN gate",
        "kds-owner-decision-receipt-*",
    ],
    "AUTH-SOP-OWNER-DECISION-20260626": [
        "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud SOP",
        "validate_sop_assets.py",
        "run_smoke_test.py",
        "validate_sop_scenario_owner_review.py",
        "sop-owner-decision-receipt-*",
    ],
}

FORBIDDEN_TOKENS = [
    "authorization_granted | `true`",
    "action_executed | `true`",
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "authorization_granted=true",
    "action_executed=true",
    "review_allowed=true",
    "stage_allowed=true",
    "commit_allowed=true",
    "push_allowed=true",
    "delete_allowed=true",
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
]

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing token: {token}")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    command_pack_text = read(COMMAND_PACK, failures)
    receipt_ledger_text = read(RECEIPT_LEDGER, failures)
    board_text = read(BOARD, failures)
    core_register_text = read(CORE_REGISTER, failures)
    task_packs_text = read(TASK_PACKS, failures)
    status_matrix_text = read(STATUS_MATRIX, failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    require_tokens("command pack", command_pack_text, REQUIRED_COMMAND_PACK_TOKENS, failures)

    for auth_id in AUTH_IDS:
        if auth_id not in receipt_ledger_text:
            failures.append(f"receipt ledger missing auth id: {auth_id}")
        if auth_id not in command_pack_text:
            failures.append(f"command pack missing auth id: {auth_id}")
        require_tokens(f"command pack {auth_id}", command_pack_text, REQUIRED_COMMAND_TOKENS_BY_AUTH[auth_id], failures)

    if command_pack_text.count("| `AUTH-") != len(AUTH_IDS):
        failures.append("command pack must have exactly 7 AUTH table rows")

    for token in FORBIDDEN_TOKENS:
        if token in command_pack_text:
            failures.append(f"command pack contains forbidden granted/executed token: {token}")

    for label, text in [
        ("board", board_text),
        ("core register", core_register_text),
        ("task packs", task_packs_text),
        ("status matrix", status_matrix_text),
    ]:
        require_tokens(label, text, REQUIRED_GOVERNANCE_TOKENS, failures)

    result = {
        "gate": "project_group_authorization_pre_execution_command_pack_20260626",
        "status": "pass" if not failures else "fail",
        "command_pack_count": len(AUTH_IDS),
        "receipt_record_count": 0,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates command-pack control only; it does not grant authorization or execute project actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
