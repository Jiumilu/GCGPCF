#!/usr/bin/env python3
"""Validate the post-scheme-recognition pre-execution command pack."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-pre-execution-command-pack-20260626.md"
RECEIPT_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

AUTH_IDS = [
    "AUTH-AAAS-SCHEME-REVIEW-20260626",
    "AUTH-BRAIN-SCHEME-REVIEW-20260626",
    "AUTH-WAS-SCHEME-REVIEW-20260626",
    "AUTH-XIAOC-SCHEME-REVIEW-20260626",
    "AUTH-WAES-SCHEME-REVIEW-20260626",
    "AUTH-GPC-SCHEME-REVIEW-20260626",
    "AUTH-STUDIO-SCHEME-REVIEW-20260626",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-XWAIL-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-MMC-SCHEME-REVIEW-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-XIAOG-SCHEME-REVIEW-20260626",
    "AUTH-PVAOS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-SCHEME-REVIEW-20260626",
    "AUTH-PKC-SCHEME-REVIEW-20260626",
    "AUTH-XGD-SCHEME-REVIEW-20260626",
]

REQUIRED_COMMAND_PACK_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md",
    "globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md",
    "project_group_post_scheme_recognition_pre_execution_command_pack_20260626 = controlled",
    "post_scheme_recognition_pre_execution_command_pack_ready",
    "command_pack_count | `17`",
    "receipt_record_count | `0`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "cleanup_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "command_pack_count=17",
    "receipt_record_count=0",
    "authorization_granted_count=0",
    "action_executed_count=0",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "globalcloud-project-group-post-scheme-recognition-pre-execution-command-pack-20260626.md",
    "validate_project_group_post_scheme_recognition_pre_execution_command_pack_20260626.py",
    "project_group_post_scheme_recognition_pre_execution_command_pack_20260626 = controlled",
    "post_scheme_recognition_pre_execution_command_pack_ready",
]

REQUIRED_COMMON_COMMAND_TOKENS = [
    "git status --short --untracked-files=all",
    "git diff --check",
    "validate_project_group_scheme_recognition_rules_20260626.py",
    "receipt ledger gate",
    "不声明项目群 Git 全量 clean",
]

FORBIDDEN_TOKENS = [
    "authorization_granted | `true`",
    "action_executed | `true`",
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "cleanup_allowed | `true`",
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
    "cleanup_allowed=true",
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
    command_pack_text = read(COMMAND_PACK, failures)
    receipt_ledger_text = read(RECEIPT_LEDGER, failures)
    refs_text = "\n".join([read(BOARD, failures), read(CORE_REGISTER, failures), read(TASK_PACKS, failures)])

    require_tokens("command pack", command_pack_text, REQUIRED_COMMAND_PACK_TOKENS, failures)
    require_tokens("command pack common commands", command_pack_text, REQUIRED_COMMON_COMMAND_TOKENS, failures)

    for auth_id in AUTH_IDS:
        if auth_id not in receipt_ledger_text:
            failures.append(f"receipt ledger missing auth id: {auth_id}")
        if auth_id not in command_pack_text:
            failures.append(f"command pack missing auth id: {auth_id}")
    if command_pack_text.count("| `AUTH-") != len(AUTH_IDS):
        failures.append("command pack must have exactly 17 AUTH table rows")

    require_tokens("governance", refs_text, REQUIRED_GOVERNANCE_TOKENS, failures)

    combined = command_pack_text + "\n" + refs_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden granted/executed token: {token}")

    result = {
        "gate": "project_group_post_scheme_recognition_pre_execution_command_pack_20260626",
        "status": "pass" if not failures else "fail",
        "command_pack_count": len(AUTH_IDS),
        "receipt_record_count": 0,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates post-scheme command-pack control only; it does not grant authorization or execute project actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
