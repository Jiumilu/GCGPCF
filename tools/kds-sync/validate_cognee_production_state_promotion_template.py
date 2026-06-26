#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "promotion_evidence_id",
    "promotion_scope",
    "source_admission_package",
    "source_external_execution_receipt",
    "source_full_run_ledger",
    "source_object_coverage",
    "source_scenario_matrix",
    "promotion_request",
    "waes_decision",
    "harness_decision",
    "rollback_plan",
    "promotion_status",
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
        default="fixtures/cognee/cognee-production-state-promotion-evidence-template.json",
    )
    parser.add_argument(
        "--require-real-promotion",
        action="store_true",
        help="Require WAES and Harness decisions and a real promotion status.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]

    request = data.get("promotion_request", {})
    waes = data.get("waes_decision", {})
    harness = data.get("harness_decision", {})
    rollback = data.get("rollback_plan", {})

    shape_ok = (
        isinstance(request, dict)
        and isinstance(waes, dict)
        and isinstance(harness, dict)
        and isinstance(rollback, dict)
        and "requested_state_changes" in request
        and "rollback_entry" in rollback
    )
    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )

    if args.require_real_promotion:
        status_ok = data.get("promotion_status") == "real_promotion_recorded"
        decision_ok = waes.get("decision") in {"pass", "approved"} and harness.get("decision") in {
            "pass",
            "approved",
            "accepted",
        }
        result = (
            "pass_real"
            if not missing and shape_ok and bool_gate_ok and status_ok and decision_ok
            else "fail"
        )
    else:
        status_ok = data.get("promotion_status") in {"template_only", "real_promotion_recorded"}
        result = "pass_template" if not missing and shape_ok and bool_gate_ok and status_ok else "fail"

    print(
        "cognee_production_state_promotion_template="
        f"{result} missing_required_field_count={len(missing)} "
        f"promotion_status={data.get('promotion_status')} "
        f"waes_decision={waes.get('decision')} "
        f"harness_decision={harness.get('decision')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
