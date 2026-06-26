#!/usr/bin/env python3
"""Validate the project-group execution authorization receipt ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md"
AUTH_REQUEST = ROOT / "docs/harness/evidence/globalcloud-project-group-first-execution-authorization-request-20260626.md"
RECEIPT_TEMPLATE = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-template-20260626.md"
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

REQUIRED_LEDGER_TOKENS = [
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "globalcloud-project-group-first-execution-authorization-request-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-template-20260626.md",
    "project_group_execution_authorization_receipt_ledger_20260626 = controlled",
    "execution_authorization_receipt_ledger_ready",
    "receipt_record_count | `0`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "pending_authorization_items | `7`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "receipt_record_count=0",
    "authorization_granted_count=0",
    "action_executed_count=0",
    "pending_authorization_items=7",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md",
    "validate_project_group_execution_authorization_receipt_ledger_20260626.py",
    "project_group_execution_authorization_receipt_ledger_20260626 = controlled",
    "execution_authorization_receipt_ledger_ready",
]

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
    ledger_text = read(LEDGER, failures)
    auth_request_text = read(AUTH_REQUEST, failures)
    receipt_template_text = read(RECEIPT_TEMPLATE, failures)
    board_text = read(BOARD, failures)
    core_register_text = read(CORE_REGISTER, failures)
    task_packs_text = read(TASK_PACKS, failures)
    status_matrix_text = read(STATUS_MATRIX, failures)

    require_tokens("ledger", ledger_text, REQUIRED_LEDGER_TOKENS, failures)

    for auth_id in AUTH_IDS:
        if auth_id not in auth_request_text:
            failures.append(f"auth request missing auth id: {auth_id}")
        if auth_id not in receipt_template_text:
            failures.append(f"receipt template missing auth id: {auth_id}")
        if auth_id not in ledger_text:
            failures.append(f"ledger missing auth id: {auth_id}")

    if ledger_text.count("pending_confirmation") != len(AUTH_IDS):
        failures.append("ledger must keep all 7 auth rows as pending_confirmation")
    if ledger_text.count("| `none` | `pending_confirmation` | `false` | `false` |") != len(AUTH_IDS):
        failures.append("ledger auth rows must have none receipt_id, pending status, and false authorization/action")

    for token in FORBIDDEN_TOKENS:
        if token in ledger_text:
            failures.append(f"ledger contains forbidden granted/executed token: {token}")

    for label, text in [
        ("board", board_text),
        ("core register", core_register_text),
        ("task packs", task_packs_text),
        ("status matrix", status_matrix_text),
    ]:
        require_tokens(label, text, REQUIRED_GOVERNANCE_TOKENS, failures)

    result = {
        "gate": "project_group_execution_authorization_receipt_ledger_20260626",
        "status": "pass" if not failures else "fail",
        "auth_items_checked": len(AUTH_IDS),
        "receipt_record_count": 0,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates the receipt ledger only; it does not grant authorization or execute project actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
