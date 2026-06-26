#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "rollup_id",
    "rollup_scope",
    "source_admission_package",
    "gap_results",
    "ready_gap_count",
    "total_gap_count",
    "readiness_status",
    "next_required_action",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

EXPECTED_GAPS = {
    "COGNEE-FULL-RUN-GAP-001",
    "COGNEE-FULL-RUN-GAP-002",
    "COGNEE-FULL-RUN-GAP-003",
    "COGNEE-FULL-RUN-GAP-004",
    "COGNEE-FULL-RUN-GAP-005",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-full-run-readiness-rollup.json",
    )
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Require every full-run gap to be ready.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    gaps = data.get("gap_results", [])
    gap_ids = {gap.get("gap_id") for gap in gaps if isinstance(gap, dict)}
    ready_gap_count = sum(1 for gap in gaps if isinstance(gap, dict) and gap.get("ready") is True)

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    gap_shape_ok = (
        isinstance(gaps, list)
        and gap_ids == EXPECTED_GAPS
        and data.get("total_gap_count") == len(EXPECTED_GAPS)
        and data.get("ready_gap_count") == ready_gap_count
    )

    if args.require_ready:
        status_ok = data.get("readiness_status") == "ready" and ready_gap_count == len(EXPECTED_GAPS)
        result = "pass_ready" if not missing and bool_gate_ok and gap_shape_ok and status_ok else "fail"
    else:
        status_ok = data.get("readiness_status") in {"not_ready", "ready"}
        result = "pass_not_ready" if not missing and bool_gate_ok and gap_shape_ok and status_ok else "fail"

    print(
        "cognee_full_run_readiness_rollup="
        f"{result} missing_required_field_count={len(missing)} "
        f"ready_gap_count={ready_gap_count} total_gap_count={data.get('total_gap_count')} "
        f"readiness_status={data.get('readiness_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
