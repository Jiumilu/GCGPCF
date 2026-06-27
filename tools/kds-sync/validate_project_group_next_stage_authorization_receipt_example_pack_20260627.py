#!/usr/bin/env python3
"""Validate the next-stage authorization receipt example pack."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md"
DECISION_BOARD = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"
PRE_WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"
POST_SCHEME_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md"
EXECUTION_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md"
COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-pre-execution-command-pack-20260626.md"

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
    "GPCF-NEXT-STAGE-AUTHORIZATION-RECEIPT-EXAMPLE-PACK-20260627-001",
    "project_group_next_stage_authorization_receipt_example_pack_20260627 = controlled",
    "next_stage_authorization_receipt_example_pack_ready",
    "example_receipt_count | `7`",
    "recorded_receipt_count | `0`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "review_boundary_repos_current | `GlobalCloud AAAS`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP`",
    "noise_cleanup_repo_current | `WAS世界资产体系(.DS_Store)`",
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
    "example_only_not_recorded",
    "noise_cleanup_decision_registration_only",
    "human_review_and_conclusion_registration_only",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "单仓核对卡 / 状态传导复用入口",
    "5.5.1 AAAS delegated wrapper 单仓核对卡",
    "5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡",
    "5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡",
    "5.6.3 SOP delegated wrapper 确认后状态传导摘要",
]

REFERENCE_TOKENS = [
    "globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md",
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
    "recording_status | `recorded`",
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
            read(PRE_WAVE1, failures),
            read(POST_SCHEME_LEDGER, failures),
            read(EXECUTION_LEDGER, failures),
            read(COMMAND_PACK, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in receipt example pack: {token}")

    for auth_id in AUTH_IDS:
        if auth_id not in doc_text:
            failures.append(f"missing auth id in receipt example pack: {auth_id}")
        if auth_id not in refs_text:
            failures.append(f"missing auth id in supporting references: {auth_id}")

    for token in REFERENCE_TOKENS:
        if token not in doc_text:
            failures.append(f"missing reference token in receipt example pack: {token}")

    example_rows = [
        line
        for line in doc_text.splitlines()
        if line.startswith("| ")
        and "EXAMPLE" in line
        and any(line.startswith(f"| {label} |") for label in ["A", "B", "C", "D", "E", "F", "G"])
    ]
    if len(example_rows) != len(AUTH_IDS):
        failures.append(f"expected 7 example receipt rows, found {len(example_rows)}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_next_stage_authorization_receipt_example_pack_20260627",
        "status": "pass" if not failures else "fail",
        "example_receipt_count": len(AUTH_IDS),
        "recorded_receipt_count": 0,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates receipt examples only; it does not record authorization, execute review or cleanup, or grant accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
