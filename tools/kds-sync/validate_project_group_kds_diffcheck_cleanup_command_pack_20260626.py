#!/usr/bin/env python3
"""Validate the KDS diff-check cleanup command pack."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-kds-diffcheck-cleanup-command-pack-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

REQUIRED_DOC_TOKENS = [
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
    "project_group_kds_diffcheck_cleanup_command_pack_20260626 = controlled",
    "kds_diffcheck_cleanup_command_pack_ready",
    "command_pack_count | `1`",
    "recheck_date | `2026-06-27`",
    "target_repo | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS`",
    "target_path | `.env.production.example`",
    "current_live_git_gate | `blocked`",
    "current_blocker | `sensitive_path_review_required`",
    "authorization_granted | `false`",
    "cleanup_executed | `false`",
    "kds_api_sync_executed | `false`",
    "commit_executed | `false`",
    "push_executed | `false`",
    "precheck",
    "classify",
    "cleanup",
    "verify",
    "project_group_gate",
    "receipt",
    "sensitive path review / optional cleanup command pack",
    "sensitive path cleanup gate",
    "receipt ledger gate",
    "authorization_granted=false",
    "cleanup_executed=false",
    "kds_api_sync_executed=false",
    "commit_executed=false",
    "push_executed=false",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001",
    "globalcloud-project-group-kds-diffcheck-cleanup-command-pack-20260626.md",
    "validate_project_group_kds_diffcheck_cleanup_command_pack_20260626.py",
    "project_group_kds_diffcheck_cleanup_command_pack_20260626 = controlled",
    "kds_diffcheck_cleanup_command_pack_ready",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
]

FORBIDDEN_TOKENS = [
    "authorization_granted=true",
    "cleanup_executed=true",
    "kds_api_sync_executed=true",
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
    doc_text = read(DOC, failures)
    governance_text = "\n".join(
        [
            read(BOARD, failures),
            read(CORE_REGISTER, failures),
            read(TASK_PACKS, failures),
        ]
    )

    require_tokens("command pack", doc_text, REQUIRED_DOC_TOKENS, failures)
    require_tokens("governance", governance_text, REQUIRED_GOVERNANCE_TOKENS, failures)

    combined = doc_text + "\n" + governance_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_kds_diffcheck_cleanup_command_pack_20260626",
        "status": "pass" if not failures else "fail",
        "authorization_item": "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
        "target_file": ".env.production.example",
        "cleanup_executed": False,
        "failures": failures,
        "warnings": [
            "This validates command-pack readiness only; it does not edit KDS, clean whitespace, stage, commit, push, or grant acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
