#!/usr/bin/env python3
"""Validate the current KDS diff-check blocker evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-kds-diffcheck-blocker-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

REQUIRED_EVIDENCE_TOKENS = [
    "GPCF-KDS-DIFFCHECK-BLOCKER-20260626-001",
    "project_group_kds_diffcheck_blocker_20260626 = controlled",
    "kds_diffcheck_blocker_controlled",
    "blocker_count | `1`",
    "blocked_repo | `GlobalCloud KDS`",
    "blocked_file | `wiki/log.md`",
    "blocker_type | `trailing_whitespace`",
    "diff_check_failed_repos | `GlobalCloud KDS`",
    "gate | `blocked`",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
    "project_group_git_clean=false",
    "auto_fix_executed=false",
    "kds_write_executed=false",
    "commit_executed=false",
    "push_executed=false",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-KDS-DIFFCHECK-BLOCKER-20260626-001",
    "globalcloud-project-group-kds-diffcheck-blocker-20260626.md",
    "validate_project_group_kds_diffcheck_blocker_20260626.py",
    "project_group_kds_diffcheck_blocker_20260626 = controlled",
    "kds_diffcheck_blocker_controlled",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
]

FORBIDDEN_TOKENS = [
    "project_group_git_clean=true",
    "auto_fix_executed=true",
    "kds_write_executed=true",
    "commit_executed=true",
    "push_executed=true",
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
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


def main() -> int:
    failures: list[str] = []
    evidence_text = read(EVIDENCE, failures)
    governance_text = "\n".join(
        [
            read(BOARD, failures),
            read(CORE_REGISTER, failures),
            read(TASK_PACKS, failures),
        ]
    )

    require_tokens("evidence", evidence_text, REQUIRED_EVIDENCE_TOKENS, failures)
    require_tokens("governance", governance_text, REQUIRED_GOVERNANCE_TOKENS, failures)

    combined = evidence_text + "\n" + governance_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_kds_diffcheck_blocker_20260626",
        "status": "pass" if not failures else "fail",
        "blocked_repo": "GlobalCloud KDS",
        "blocked_file": "wiki/log.md",
        "blocker_type": "trailing_whitespace",
        "auto_fix_executed": False,
        "failures": failures,
        "warnings": [
            "This validates blocker governance only; it does not edit KDS, clean whitespace, stage, commit, push, or grant acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
