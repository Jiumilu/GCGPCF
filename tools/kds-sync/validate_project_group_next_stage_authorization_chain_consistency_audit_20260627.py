#!/usr/bin/env python3
"""Validate the next-stage authorization chain consistency audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md"
DECISION_BOARD = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"
EXAMPLE_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md"
RECORDING_PROCEDURE = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md"
HUMAN_FILL = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md"
EXECUTION_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md"
POST_SCHEME_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md"
PRE_WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"

AUTH_IDS = [
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

POST_SCHEME_AUTH_IDS = AUTH_IDS[1:]

REQUIRED_TOKENS = [
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001",
    "project_group_next_stage_authorization_chain_consistency_audit_20260627 = controlled",
    "next_stage_authorization_chain_consistency_audit_ready",
    "chain_node_count | `7`",
    "auth_count | `7`",
    "execution_ledger_auth_count | `1`",
    "post_scheme_ledger_auth_count | `6`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "wave1_entry_blocked_by_pre_review | `true`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "单仓核对卡 / 状态传导对齐",
    "5.5.1 AAAS delegated wrapper 单仓核对卡",
    "5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡",
    "5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡",
    "5.6.3 SOP delegated wrapper 确认后状态传导摘要",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
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
    audit_text = read(AUDIT, failures)
    refs = {
        "decision_board": read(DECISION_BOARD, failures),
        "example_pack": read(EXAMPLE_PACK, failures),
        "recording_procedure": read(RECORDING_PROCEDURE, failures),
        "human_fill": read(HUMAN_FILL, failures),
        "execution_ledger": read(EXECUTION_LEDGER, failures),
        "post_scheme_ledger": read(POST_SCHEME_LEDGER, failures),
        "pre_wave1": read(PRE_WAVE1, failures),
    }

    for token in REQUIRED_TOKENS:
        if token not in audit_text:
            failures.append(f"missing token in consistency audit: {token}")

    for auth_id in AUTH_IDS:
        for label, text in refs.items():
            if label == "execution_ledger" and auth_id != "AUTH-WAS-DELETE-DS-STORE-20260626":
                continue
            if label == "post_scheme_ledger" and auth_id == "AUTH-WAS-DELETE-DS-STORE-20260626":
                continue
            if label == "pre_wave1" and auth_id == "AUTH-WAS-DELETE-DS-STORE-20260626":
                continue
            if auth_id not in text:
                failures.append(f"{label} missing auth id: {auth_id}")

    if "AUTH-WAS-DELETE-DS-STORE-20260626" not in refs["execution_ledger"]:
        failures.append("execution ledger missing next-stage WAS auth item")
    for auth_id in POST_SCHEME_AUTH_IDS:
        if auth_id in refs["execution_ledger"]:
            failures.append(f"execution ledger must not contain post-scheme next-stage auth id: {auth_id}")

    for auth_id in POST_SCHEME_AUTH_IDS:
        if auth_id not in refs["post_scheme_ledger"]:
            failures.append(f"post-scheme ledger missing auth id: {auth_id}")

    combined = audit_text + "\n" + "\n".join(refs.values())
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_next_stage_authorization_chain_consistency_audit_20260627",
        "status": "pass" if not failures else "fail",
        "auth_count": len(AUTH_IDS),
        "execution_ledger_auth_count": 1,
        "post_scheme_ledger_auth_count": len(POST_SCHEME_AUTH_IDS),
        "failures": failures,
        "warnings": [
            "This validates next-stage authorization chain consistency only; it does not record authorization or execute any actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
