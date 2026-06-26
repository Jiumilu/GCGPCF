#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "execution_entry_id",
    "execution_scope",
    "execution_target",
    "execution_owner",
    "execution_window_start_at",
    "execution_window_expires_at",
    "receipt_id",
    "authorized_by",
    "authorized_at",
    "record_count",
    "expected_execution_count",
    "expected_error_count",
    "rollback_triggered_expected",
    "rollback_evidence",
    "rollback_entry",
    "failure_exit",
    "forbidden_claims",
    "intake_status",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
]

PENDING_PREFIX = "PENDING_"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-external-execution-integration-intake.pending.json",
    )
    parser.add_argument(
        "--require-complete-intake",
        action="store_true",
        help="Require all pending execution parameters to be replaced with concrete values.",
    )
    args = parser.parse_args()

    path = Path(args.input)
    data = json.loads(path.read_text(encoding="utf-8"))

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    pending = [
        field
        for field in [
            "execution_target",
            "execution_owner",
            "execution_window_start_at",
            "execution_window_expires_at",
            "receipt_id",
        ]
        if str(data.get(field, "")).startswith(PENDING_PREFIX)
    ]

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
    )

    status = data.get("intake_status")
    if args.require_complete_intake:
        intake_complete = not pending
        status_ok = status == "ready_for_external_execution_validation"
        result = "pass_complete" if not missing and intake_complete and bool_gate_ok and status_ok else "fail"
    else:
        intake_complete = not pending
        status_ok = status in {
            "pending_user_supplied_execution_parameters",
            "ready_for_external_execution_validation",
        }
        result = "pass_pending" if not missing and bool_gate_ok and status_ok else "fail"

    print(
        "cognee_external_execution_integration_intake="
        f"{result} missing_required_field_count={len(missing)} "
        f"pending_field_count={len(pending)} "
        f"intake_complete={str(intake_complete).lower()} "
        f"intake_status={status} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()}"
    )

    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
