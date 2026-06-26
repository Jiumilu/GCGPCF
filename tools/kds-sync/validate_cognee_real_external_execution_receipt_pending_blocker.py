#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "blocker_id",
    "blocker_scope",
    "source_submission_request",
    "source_update_patch_plan",
    "blocked_gap_id",
    "blocked_reason",
    "required_unblock_artifacts",
    "unblock_commands",
    "blocker_status",
    "gap_001_ready",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

REQUIRED_ARTIFACTS = {
    "REAL_RECEIPT_REF",
    "REAL_RECEIPT_ID",
    "EXECUTED_AT",
    "EXECUTION_COUNTS",
    "ROLLBACK_STATUS",
    "OPERATOR_NOTE",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-real-external-execution-receipt-pending-blocker.json",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]

    bool_gate_ok = (
        data.get("gap_001_ready") is False
        and data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    artifact_ok = set(data.get("required_unblock_artifacts", [])) == REQUIRED_ARTIFACTS
    command_ok = set(data.get("unblock_commands", [])) == {
        "python3 tools/kds-sync/validate_cognee_real_external_execution_receipt_intake.py --require-real-receipt",
        "python3 tools/kds-sync/validate_cognee_full_run_readiness_rollup.py",
    }
    blocker_ok = (
        data.get("blocked_gap_id") == "COGNEE-FULL-RUN-GAP-001"
        and data.get("blocked_reason") == "real_external_execution_receipt_not_received"
        and data.get("blocker_status") == "blocked_pending_real_receipt"
    )

    result = "pass_blocked" if not missing and bool_gate_ok and artifact_ok and command_ok and blocker_ok else "fail"

    print(
        "cognee_real_external_execution_receipt_pending_blocker="
        f"{result} missing_required_field_count={len(missing)} "
        f"blocked_gap_id={data.get('blocked_gap_id')} "
        f"blocker_status={data.get('blocker_status')} "
        f"gap_001_ready={str(data.get('gap_001_ready')).lower()} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
