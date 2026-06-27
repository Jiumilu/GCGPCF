#!/usr/bin/env python3
"""Validate the next-stage authorization human fill request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md"
DECISION_BOARD = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"
EXAMPLE_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md"
RECORDING_PROCEDURE = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md"

AUTH_IDS = [
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001",
    "project_group_next_stage_authorization_human_fill_request_20260627 = prepared",
    "next_stage_authorization_human_fill_request_ready",
    "fill_item_count | `7`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
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
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "authorized_for_recording_only",
    "deferred_pending_more_context",
    "rejected_keep_pending",
    "建议填写顺序",
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "5.3 KDS 单仓核对卡",
    "5.5.1 AAAS delegated wrapper 单仓核对卡",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡",
    "5.5.3 SOP delegated wrapper 单仓核对卡",
    "4.2 A 项确认后状态传导摘要",
    "5.4 KDS 确认后状态传导摘要",
    "5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "A-E 最小核对单",
    "7.3 C-E 项 delegated wrapper review",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "cleanup_allowed = true",
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
    doc_text = read(DOC, failures)
    refs_text = "\n".join(
        [
            read(DECISION_BOARD, failures),
            read(EXAMPLE_PACK, failures),
            read(RECORDING_PROCEDURE, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in human fill request: {token}")

    for auth_id in AUTH_IDS:
        if auth_id not in doc_text:
            failures.append(f"missing auth id in human fill request: {auth_id}")
        if auth_id not in refs_text:
            failures.append(f"missing auth id in supporting refs: {auth_id}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_next_stage_authorization_human_fill_request_20260627",
        "status": "pass" if not failures else "fail",
        "fill_item_count": len(AUTH_IDS),
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates the next-stage human fill request only; it does not record authorization, execute actions, or grant accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
