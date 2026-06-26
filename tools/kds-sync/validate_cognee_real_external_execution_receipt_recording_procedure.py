#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "procedure_id",
    "procedure_scope",
    "source_receipt_intake",
    "source_readiness_rollup",
    "steps",
    "forbidden_inputs",
    "required_commands",
    "procedure_status",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

REQUIRED_STEPS = {
    "receive_real_external_execution_receipt",
    "reject_completed_example_or_template_receipt",
    "fill_receipt_intake_fields",
    "run_receipt_intake_validator_require_real_receipt",
    "update_readiness_rollup_gap_001_only",
    "rerun_readiness_rollup_validator",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-real-external-execution-receipt-recording-procedure.json",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    steps = data.get("steps", [])
    step_actions = {step.get("action") for step in steps if isinstance(step, dict)}

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    steps_ok = step_actions == REQUIRED_STEPS
    forbidden_ok = "fixtures/cognee/cognee-external-execution-receipt.completed.example.json" in data.get("forbidden_inputs", [])
    commands = data.get("required_commands", [])
    commands_ok = (
        "python3 tools/kds-sync/validate_cognee_real_external_execution_receipt_intake.py --require-real-receipt" in commands
        and "python3 tools/kds-sync/validate_cognee_full_run_readiness_rollup.py" in commands
    )
    status_ok = data.get("procedure_status") == "defined_pending_real_receipt"

    result = (
        "pass_defined"
        if not missing and bool_gate_ok and steps_ok and forbidden_ok and commands_ok and status_ok
        else "fail"
    )

    print(
        "cognee_real_external_execution_receipt_recording_procedure="
        f"{result} missing_required_field_count={len(missing)} "
        f"step_count={len(steps)} forbidden_input_count={len(data.get('forbidden_inputs', []))} "
        f"procedure_status={data.get('procedure_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
