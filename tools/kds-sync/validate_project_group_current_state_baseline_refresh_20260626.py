#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group current-state baseline refresh evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

PROJECTS = [
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
]

REQUIRED_TOKENS = [
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "project_count = 17",
    "git_gate = partial",
    "dirty_repo_count = 17",
    "pass_repo_count = 0",
    "ahead_repos = 0",
    "behind_repos = 0",
    "sensitive_repos = 0",
    "diff_check = pass",
    "auto_ready_for_review_upgrade = false",
    "authorization_granted = false",
    "action_executed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "WAES-LINT-RUNTIME-001",
    "GFIS-REAL-SOR-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
]

FORBIDDEN_TOKENS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "auto_ready_for_review_upgrade = true",
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
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
            failures.append(f"missing token in current baseline refresh: {token}")

    for project in PROJECTS:
        if project not in doc:
            failures.append(f"missing project in current baseline refresh: {project}")

    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in current baseline refresh: {token}")

    if "globalcloud-project-group-current-state-baseline-refresh-20260626.md" not in board:
        failures.append("governance board missing current-state baseline refresh reference")

    result = {
        "gate": "project_group_current_state_baseline_refresh_20260626",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "failures": failures,
        "warnings": [
            "This validates current-state baseline refresh evidence only; it does not execute tasks, clean repos, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
