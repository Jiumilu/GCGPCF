#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "patch_plan_id",
    "patch_plan_scope",
    "source_submission_request",
    "source_receipt_intake",
    "source_readiness_rollup",
    "patch_targets",
    "required_commands_after_patch",
    "forbidden_updates",
    "patch_plan_status",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

REQUIRED_TARGETS = {
    "fixtures/cognee/cognee-real-external-execution-receipt-intake.pending.json",
    "fixtures/cognee/cognee-full-run-readiness-rollup.json",
}

REQUIRED_COMMANDS = {
    "python3 tools/kds-sync/validate_cognee_real_external_execution_receipt_intake.py --require-real-receipt",
    "python3 tools/kds-sync/validate_cognee_full_run_readiness_rollup.py",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-real-external-execution-receipt-update-patch-plan.json",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    targets = data.get("patch_targets", [])
    target_ids = {target.get("target") for target in targets if isinstance(target, dict)}
    commands = set(data.get("required_commands_after_patch", []))

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    targets_ok = target_ids == REQUIRED_TARGETS and all(
        isinstance(target.get("fields_to_update"), list) and target.get("required_result")
        for target in targets
        if isinstance(target, dict)
    )
    commands_ok = REQUIRED_COMMANDS.issubset(commands)
    forbidden_ok = set(data.get("forbidden_updates", [])) == {
        "production_write=true",
        "accepted=true",
        "integrated=true",
        "production_ready=true",
        "full_run_claim=true",
    }
    status_ok = data.get("patch_plan_status") == "prepared_pending_real_receipt"

    result = (
        "pass_prepared"
        if not missing and bool_gate_ok and targets_ok and commands_ok and forbidden_ok and status_ok
        else "fail"
    )

    print(
        "cognee_real_external_execution_receipt_update_patch_plan="
        f"{result} missing_required_field_count={len(missing)} "
        f"patch_target_count={len(targets)} command_count={len(commands)} "
        f"patch_plan_status={data.get('patch_plan_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
