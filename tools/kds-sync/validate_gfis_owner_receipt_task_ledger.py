#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.json"


REQUIRED_TASK_KEYS = [
    "customer_requirement_platform_order_source_of_record",
    "customer_requirement_platform_order_dispatch_confirmation",
    "waes_confirmation",
    "kds_write_receipt",
    "runtime_primary_key",
]


def fail(message: str) -> None:
    raise SystemExit(f"gfis_owner_receipt_task_ledger=fail reason={message}")


def main() -> None:
    if not LEDGER.exists():
        fail("ledger_missing")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    tasks = ledger.get("tasks", [])
    if ledger.get("task_count") != 5 or len(tasks) != 5:
        fail("task_count_must_be_5")
    keys = [task.get("task_key") for task in tasks]
    if keys != REQUIRED_TASK_KEYS:
        fail("task_keys_or_order_invalid")
    if ledger.get("completed_task_count") != 0:
        fail("completed_task_count_must_be_0")
    for gate_name in ["review_queue", "runtime_intake", "waes_review", "verified"]:
        if ledger.get(gate_name) != 0:
            fail(f"{gate_name}_must_remain_0")
    non_claims = ledger.get("non_claims", {})
    for key, value in non_claims.items():
        if value is not False:
            fail(f"non_claim_must_be_false:{key}")
    for task in tasks:
        if not task.get("required_fields"):
            fail(f"required_fields_missing:{task.get('task_key')}")
        if not task.get("source_evidence"):
            fail(f"source_evidence_missing:{task.get('task_key')}")
        if "completed" in str(task.get("state", "")):
            fail(f"task_state_must_not_claim_completion:{task.get('task_key')}")
    print(
        "gfis_owner_receipt_task_ledger=pass "
        f"tasks={ledger.get('task_count')} completed={ledger.get('completed_task_count')} "
        f"runtime_sop_e2e={ledger.get('runtime_sop_e2e')}"
    )


if __name__ == "__main__":
    main()
