#!/usr/bin/env python3
"""Validate the 2026-06-27 project-group authorization layer matrix."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-AUTHORIZATION-LAYER-MATRIX-001.md"
GPCF_REVIEW = ROOT / "docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

REQUIRED_TOKENS = [
    "authorization_layer_matrix = prepared",
    "authorization_layer_count = 4",
    "DEV-AUTH-20260627",
    "REVIEW-AUTH-20260627",
    "RUNTIME-AUTH-20260627",
    "ACCEPTANCE-AUTH-20260627",
    "REVIEW-AUTH-GPCF-WORKTREE-20260627",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-DECISION-BOARD-20260626-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001",
    "pre_wave1_review_authorization_status = prepared_pending_confirmation",
    "next_stage_authorization_package_status = prepared_pending_confirmation",
    "next_stage_authorization_chain_loop_round_status = prepared_pending_confirmation",
    "review_auth_first_entry = GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "review_auth_second_entry = GPCF-NEXT-STAGE-AUTHORIZATION-DECISION-BOARD-20260626-001",
    "review_auth_third_entry = GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "review_auth_fourth_entry = GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001",
    "git_gate_current = blocked",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "sensitive_repos_current = GlobalCloud KDS(.env.production.example)",
    "dev_auth_status = active_for_local_dev",
    "review_auth_status = prepared_pending_confirmation",
    "runtime_auth_status = blocked_pending_business_input",
    "acceptance_auth_status = blocked_pending_human_acceptance",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "runtime_write_allowed = false",
    "schema_migrate_allowed = false",
    "real_api_write_allowed = false",
    "accepted_allowed = false",
    "integrated_allowed = false",
    "production_ready_allowed = false",
    "customer_accepted_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

FORBIDDEN_TRUE_TOKENS = [
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "runtime_write_allowed = true",
    "schema_migrate_allowed = true",
    "real_api_write_allowed = true",
    "accepted_allowed = true",
    "integrated_allowed = true",
    "production_ready_allowed = true",
    "customer_accepted_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_git_gate(failures: list[str]) -> str:
    result = run(["python3", str(GIT_GATE), "--root", str(PROJECT_ROOT), "--allow-non-pass-exit-zero"])
    if result.returncode != 0:
        failures.append(f"project group git gate failed: {result.returncode}")
        return "unknown"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"project group git gate JSON parse failed: {exc}")
        return "unknown"
    gate = str(payload.get("gate", "unknown"))
    summary = payload.get("summary", {})
    if gate != "blocked":
        failures.append(f"git gate not blocked: {gate}")
    if summary.get("dirty_repos") != ["GlobalCloud AAAS", "WAS世界资产体系", "GlobalCoud GPCF", "GlobalCloud XWAIL", "GlobalCloud GFIS", "GlobalCloud KDS", "GlobalCloud SOP"]:
        failures.append(f"unexpected dirty repos: {summary.get('dirty_repos')}")
    for key in ["missing_repos", "ahead_repos", "behind_repos"]:
        if summary.get(key) != []:
            failures.append(f"{key} present: {summary.get(key)}")
    if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
        failures.append(f"sensitive_repos present: {summary.get('sensitive_repos')}")
    for repo in payload.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"repo diff-check not pass: {repo.get('name')}")
    return gate


def main() -> int:
    failures: list[str] = []
    evidence = read(EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)
    gpcf_review = read(GPCF_REVIEW, failures)

    for token in REQUIRED_TOKENS:
        if token not in evidence:
            failures.append(f"missing authorization matrix token: {token}")
    for token in FORBIDDEN_TRUE_TOKENS:
        if token in evidence:
            failures.append(f"forbidden true authorization token: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")
    for token in ["gpcf_worktree_review_packages = pass", "review_package_count = 7", "GPCF-RP7"]:
        if token not in gpcf_review:
            failures.append(f"missing GPCF review prerequisite token: {token}")
    for token in [
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "validate_project_group_pre_wave1_review_authorization_request_20260627.py",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "validate_project_group_next_stage_authorization_decision_board_20260626.py",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "validate_project_group_next_stage_authorization_package_20260627.py",
    "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "validate_project_group_next_stage_authorization_chain_loop_round_20260627.py",
    ]:
        if token not in evidence:
            failures.append(f"missing pre-wave1 authorization token: {token}")

    gate = validate_git_gate(failures)
    result = {
        "project_group_authorization_layer_matrix": "pass" if not failures else "fail",
        "authorization_layer_count": 4,
        "review_auth_first_entry": "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
        "git_gate": gate,
        "review_allowed": False,
        "stage_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "runtime_write_allowed": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "customer_accepted": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
