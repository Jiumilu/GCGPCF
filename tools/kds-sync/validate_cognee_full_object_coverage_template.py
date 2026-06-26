#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "coverage_id",
    "coverage_scope",
    "source_admission_package",
    "source_full_run_ledger",
    "object_inventory_source",
    "total_object_count",
    "in_scope_object_count",
    "excluded_object_count",
    "covered_object_count",
    "uncovered_object_count",
    "coverage_rate",
    "coverage_basis",
    "object_groups",
    "exclusion_records",
    "coverage_status",
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
        default="fixtures/cognee/cognee-full-object-coverage-template.json",
    )
    parser.add_argument(
        "--require-real-coverage",
        action="store_true",
        help="Require real object inventory and non-zero coverage.",
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
    groups_shape_ok = isinstance(data.get("object_groups"), list) and len(data.get("object_groups", [])) >= 1
    count_shape_ok = (
        isinstance(data.get("total_object_count"), int)
        and isinstance(data.get("in_scope_object_count"), int)
        and isinstance(data.get("covered_object_count"), int)
        and isinstance(data.get("uncovered_object_count"), int)
        and isinstance(data.get("coverage_rate"), (int, float))
    )

    if args.require_real_coverage:
        status_ok = data.get("coverage_status") == "real_coverage_recorded"
        coverage_ok = data.get("total_object_count", 0) > 0 and data.get("in_scope_object_count", 0) > 0
        result = (
            "pass_real"
            if not missing and bool_gate_ok and groups_shape_ok and count_shape_ok and status_ok and coverage_ok
            else "fail"
        )
    else:
        status_ok = data.get("coverage_status") in {"template_only", "real_coverage_recorded"}
        result = (
            "pass_template"
            if not missing and bool_gate_ok and groups_shape_ok and count_shape_ok and status_ok
            else "fail"
        )

    print(
        "cognee_full_object_coverage_template="
        f"{result} missing_required_field_count={len(missing)} "
        f"total_object_count={data.get('total_object_count')} "
        f"covered_object_count={data.get('covered_object_count')} "
        f"coverage_rate={data.get('coverage_rate')} "
        f"coverage_status={data.get('coverage_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
