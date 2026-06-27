#!/usr/bin/env python3
"""Validate Wave 1 pre-execution environment readiness evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

PACKS = [
    "WAVE1-WAES-LINT-RUNTIME-001",
    "WAVE1-GFIS-REAL-SOR-001",
    "WAVE1-GPC-EXTERNAL-RUNTIME-001",
    "WAVE1-BRAIN-HUMAN-REVIEW-001",
    "WAVE1-GPCF-POST-SCHEME-REVIEW-001",
]

REQUIRED_TOKENS = [
    "project_group_wave1_pre_execution_environment_readiness_20260626 = controlled",
    "checked_pack_count = 5",
    "repo_path_check = pass",
    "package_script_check = pass",
    "gpcf_validator_check = pass",
    "local_script_discovery = pass",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "authorization_granted = false",
    "action_executed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "validate_project_group_wave1_execution_command_pack_20260626.py",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    board = read(BOARD, failures)

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing token in Wave 1 readiness: {token}")

    for pack in PACKS:
        if pack not in doc:
            failures.append(f"missing Wave 1 readiness pack: {pack}")

    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in Wave 1 readiness: {token}")

    if "globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md" not in board:
        failures.append("governance board missing Wave 1 readiness reference")

    result = {
        "gate": "project_group_wave1_pre_execution_environment_readiness_20260626",
        "status": "pass" if not failures else "fail",
        "checked_pack_count": len(PACKS),
        "failures": failures,
        "warnings": [
            "This validates only pre-execution entry readiness; it does not run Wave 1 commands, modify code, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
