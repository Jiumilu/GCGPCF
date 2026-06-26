#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "scenario_matrix_id",
    "scenario_scope",
    "source_admission_package",
    "source_full_run_ledger",
    "source_object_coverage",
    "scenario_inventory_source",
    "total_scenario_count",
    "in_scope_scenario_count",
    "excluded_scenario_count",
    "passed_scenario_count",
    "failed_scenario_count",
    "untested_scenario_count",
    "pass_rate",
    "scenario_groups",
    "failure_records",
    "exclusion_records",
    "scenario_matrix_status",
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
        default="fixtures/cognee/cognee-full-scenario-matrix-template.json",
    )
    parser.add_argument(
        "--require-real-scenarios",
        action="store_true",
        help="Require real scenario inventory and non-zero scenario coverage.",
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
    groups_shape_ok = isinstance(data.get("scenario_groups"), list) and len(data.get("scenario_groups", [])) >= 1
    count_shape_ok = (
        isinstance(data.get("total_scenario_count"), int)
        and isinstance(data.get("in_scope_scenario_count"), int)
        and isinstance(data.get("passed_scenario_count"), int)
        and isinstance(data.get("failed_scenario_count"), int)
        and isinstance(data.get("untested_scenario_count"), int)
        and isinstance(data.get("pass_rate"), (int, float))
    )

    if args.require_real_scenarios:
        status_ok = data.get("scenario_matrix_status") == "real_scenario_matrix_recorded"
        scenario_ok = data.get("total_scenario_count", 0) > 0 and data.get("in_scope_scenario_count", 0) > 0
        result = (
            "pass_real"
            if not missing and bool_gate_ok and groups_shape_ok and count_shape_ok and status_ok and scenario_ok
            else "fail"
        )
    else:
        status_ok = data.get("scenario_matrix_status") in {"template_only", "real_scenario_matrix_recorded"}
        result = (
            "pass_template"
            if not missing and bool_gate_ok and groups_shape_ok and count_shape_ok and status_ok
            else "fail"
        )

    print(
        "cognee_full_scenario_matrix_template="
        f"{result} missing_required_field_count={len(missing)} "
        f"total_scenario_count={data.get('total_scenario_count')} "
        f"passed_scenario_count={data.get('passed_scenario_count')} "
        f"failed_scenario_count={data.get('failed_scenario_count')} "
        f"pass_rate={data.get('pass_rate')} "
        f"scenario_matrix_status={data.get('scenario_matrix_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
