#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "assignment_id",
    "assignment_scope",
    "source_receipt_intake",
    "source_recording_procedure",
    "roles",
    "escalation_rule",
    "assignment_status",
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
    "full_run_claim",
]

REQUIRED_ROLES = {
    "receipt_provider",
    "technical_recorder",
    "waes_reviewer",
    "readiness_owner",
    "rollback_owner",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-real-external-execution-receipt-responsibility-assignment.json",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    roles = data.get("roles", [])
    role_ids = {role.get("role_id") for role in roles if isinstance(role, dict)}

    bool_gate_ok = (
        data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    roles_ok = role_ids == REQUIRED_ROLES
    role_shape_ok = all(
        isinstance(role, dict)
        and role.get("owner")
        and role.get("responsibility")
        and role.get("required_output")
        and role.get("status") == "assigned_pending_real_receipt"
        for role in roles
    )
    status_ok = data.get("assignment_status") == "assigned_pending_real_receipt"

    result = (
        "pass_assigned"
        if not missing and bool_gate_ok and roles_ok and role_shape_ok and status_ok
        else "fail"
    )

    print(
        "cognee_real_external_execution_receipt_responsibility_assignment="
        f"{result} missing_required_field_count={len(missing)} "
        f"role_count={len(roles)} assignment_status={data.get('assignment_status')} "
        f"production_write={str(data.get('production_write')).lower()} "
        f"accepted={str(data.get('accepted')).lower()} "
        f"integrated={str(data.get('integrated')).lower()} "
        f"production_ready={str(data.get('production_ready')).lower()} "
        f"full_run_claim={str(data.get('full_run_claim')).lower()}"
    )
    return 0 if result.startswith("pass_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
