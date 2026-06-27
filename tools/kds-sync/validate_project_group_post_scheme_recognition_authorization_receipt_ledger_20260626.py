#!/usr/bin/env python3
"""Validate the post-scheme-recognition authorization receipt ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md"
AUTH_REQUEST = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md"
RECEIPT_TEMPLATE = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-template-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

AUTH_IDS = [
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_LEDGER_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-template-20260626.md",
    "project_group_post_scheme_recognition_authorization_receipt_ledger_20260626 = controlled",
    "post_scheme_recognition_authorization_receipt_ledger_ready",
    "receipt_record_count | `0`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "live_dirty_repo_count | `7`",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "pending_authorization_items | `6`",
    "excluded_noise_cleanup_items | `1`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "cleanup_allowed | `false`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repos_current | `GlobalCloud AAAS`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP`",
    "noise_cleanup_repo_current | `WAS世界资产体系(.DS_Store)`",
    "B 项 KDS 落账回放摘要",
    "C/D/G delegated wrapper 落账回放摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "authorized_action = human_review_and_conclusion_registration_only",
    "receipt_status_before = pending_confirmation",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "receipt_record_count=0",
    "authorization_granted_count=0",
    "action_executed_count=0",
    "pending_authorization_items=6",
    "review_boundary_repo_count=6",
    "noise_cleanup_repo_count=1",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md",
    "validate_project_group_post_scheme_recognition_authorization_receipt_ledger_20260626.py",
    "project_group_post_scheme_recognition_authorization_receipt_ledger_20260626 = controlled",
    "post_scheme_recognition_authorization_receipt_ledger_ready",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
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
    ledger_text = read(LEDGER, failures)
    auth_request_text = read(AUTH_REQUEST, failures)
    receipt_template_text = read(RECEIPT_TEMPLATE, failures)
    refs_text = "\n".join([read(BOARD, failures), read(CORE_REGISTER, failures), read(TASK_PACKS, failures)])

    require_tokens("ledger", ledger_text, REQUIRED_LEDGER_TOKENS, failures)

    for auth_id in AUTH_IDS:
        if auth_id not in auth_request_text:
            failures.append(f"auth request missing auth id: {auth_id}")
        if auth_id not in ledger_text:
            failures.append(f"ledger missing auth id: {auth_id}")
    if "globalcloud-project-group-execution-authorization-receipt-template-20260626.md" not in ledger_text:
        failures.append("ledger must reference the receipt template")

    if ledger_text.count("| `none` | `pending_confirmation` | `false` | `false` |") != len(AUTH_IDS):
        failures.append("ledger auth rows must have none receipt_id, pending status, and false authorization/action")

    require_tokens("governance", refs_text, REQUIRED_GOVERNANCE_TOKENS, failures)

    combined = ledger_text + "\n" + refs_text + "\n" + receipt_template_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden granted/executed token: {token}")

    result = {
        "gate": "project_group_post_scheme_recognition_authorization_receipt_ledger_20260626",
        "status": "pass" if not failures else "fail",
        "auth_items_checked": len(AUTH_IDS),
        "receipt_record_count": 0,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates the post-scheme receipt ledger only; it does not grant authorization or execute project actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
