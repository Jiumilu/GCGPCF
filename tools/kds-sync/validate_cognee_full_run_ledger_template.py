#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "ledger_id",
    "ledger_scope",
    "source_admission_package",
    "source_external_execution_receipt",
    "batch_count",
    "record_count",
    "successful_record_count",
    "failed_record_count",
    "excluded_record_count",
    "coverage_summary",
    "batches",
    "exception_records",
    "full_run_ledger_status",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-full-run-ledger-template.json",
    )
    parser.add_argument(
        "--require-real-ledger",
        action="store_true",
        help="Require a real full-run ledger instead of a template-only ledger.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    coverage = data.get("coverage_summary", {})
    coverage_shape_ok = {
        "object_coverage_ready",
        "scenario_coverage_ready",
        "coverage_basis",
    }.issubset(set(coverage))
    batches_shape_ok = isinstance(data.get("batches"), list) and len(data.get("batches", [])) >= 1

    if args.require_real_ledger:
        status_ok = data.get("full_run_ledger_status") == "real_ledger_recorded"
        count_ok = data.get("batch_count", 0) > 0 and data.get("record_count", 0) > 0
        result = (
            "pass_real"
            if not missing and bool_gate_ok and coverage_shape_ok and batches_shape_ok and status_ok and count_ok
            else "fail"
        )
    else:
        status_ok = data.get("full_run_ledger_status") in {
            "template_only",
            "real_ledger_recorded",
        }
        result = (
            "pass_template"
            if not missing and bool_gate_ok and coverage_shape_ok and batches_shape_ok and status_ok
            else "fail"
        )

    print(
        "cognee_full_run_ledger_template="
        f"{result} missing_required_field_count={len(missing)} "
        f"batch_count={data.get('batch_count')} record_count={data.get('record_count')} "
        f"ledger_status={data.get('full_run_ledger_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
