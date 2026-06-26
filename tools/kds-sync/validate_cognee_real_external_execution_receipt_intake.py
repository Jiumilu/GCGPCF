#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "receipt_intake_id",
    "receipt_intake_scope",
    "source_readiness_rollup",
    "source_receipt_template",
    "expected_execution_entry_id",
    "expected_execution_target",
    "expected_execution_owner",
    "required_receipt_fields",
    "received_receipt_ref",
    "received_receipt_id",
    "received_at",
    "received_by",
    "receipt_validation_status",
    "record_count",
    "execution_count",
    "error_count",
    "rollback_triggered",
    "gap_001_ready",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

PENDING_VALUES = {
    "PENDING_REAL_EXTERNAL_EXECUTION_RECEIPT",
    "PENDING_REAL_RECEIPT_ID",
    "PENDING_REAL_RECEIPT_RECEIVED_AT",
    "PENDING_RECEIVER",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-real-external-execution-receipt-intake.pending.json",
    )
    parser.add_argument(
        "--require-real-receipt",
        action="store_true",
        help="Require a real receipt reference and non-zero execution counts.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    pending_count = sum(
        1
        for field in ["received_receipt_ref", "received_receipt_id", "received_at", "received_by"]
        if data.get(field) in PENDING_VALUES
    )

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    required_shape_ok = isinstance(data.get("required_receipt_fields"), list) and len(data.get("required_receipt_fields", [])) >= 10
    count_shape_ok = (
        isinstance(data.get("record_count"), int)
        and isinstance(data.get("execution_count"), int)
        and isinstance(data.get("error_count"), int)
    )

    if args.require_real_receipt:
        status_ok = data.get("receipt_validation_status") == "real_receipt_recorded"
        receipt_ok = pending_count == 0 and data.get("record_count", 0) > 0 and data.get("execution_count", 0) > 0
        gap_ok = data.get("gap_001_ready") is True
        result = (
            "pass_real"
            if not missing and bool_gate_ok and required_shape_ok and count_shape_ok and status_ok and receipt_ok and gap_ok
            else "fail"
        )
    else:
        status_ok = data.get("receipt_validation_status") in {
            "pending_real_receipt",
            "real_receipt_recorded",
        }
        result = (
            "pass_pending"
            if not missing and bool_gate_ok and required_shape_ok and count_shape_ok and status_ok
            else "fail"
        )

    print(
        "cognee_real_external_execution_receipt_intake="
        f"{result} missing_required_field_count={len(missing)} "
        f"pending_field_count={pending_count} "
        f"receipt_validation_status={data.get('receipt_validation_status')} "
        f"gap_001_ready={str(data.get('gap_001_ready')).lower()} "
        f"record_count={data.get('record_count')} execution_count={data.get('execution_count')} "
        f"error_count={data.get('error_count')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
