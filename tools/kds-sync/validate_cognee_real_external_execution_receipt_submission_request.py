#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "submission_request_id",
    "request_scope",
    "request_to",
    "request_from",
    "source_responsibility_assignment",
    "source_receipt_intake",
    "requested_artifacts",
    "forbidden_artifacts",
    "submission_status",
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
        default="fixtures/cognee/cognee-real-external-execution-receipt-submission-request.json",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    artifacts = data.get("requested_artifacts", [])
    artifact_ids = {artifact.get("artifact_id") for artifact in artifacts if isinstance(artifact, dict)}

    bool_gate_ok = (
        data.get("gap_001_ready") is False
        and data.get("production_write") is False
        and data.get("accepted") is False
        and data.get("integrated") is False
        and data.get("production_ready") is False
        and data.get("full_run_claim") is False
    )
    artifacts_ok = artifact_ids == REQUIRED_ARTIFACTS and all(
        artifact.get("required") is True for artifact in artifacts if isinstance(artifact, dict)
    )
    forbidden_ok = "fixtures/cognee/cognee-external-execution-receipt.completed.example.json" in data.get(
        "forbidden_artifacts", []
    )
    status_ok = data.get("submission_status") == "requested_pending_real_receipt"

    result = (
        "pass_requested"
        if not missing and bool_gate_ok and artifacts_ok and forbidden_ok and status_ok
        else "fail"
    )

    print(
        "cognee_real_external_execution_receipt_submission_request="
        f"{result} missing_required_field_count={len(missing)} "
        f"requested_artifact_count={len(artifacts)} "
        f"forbidden_artifact_count={len(data.get('forbidden_artifacts', []))} "
        f"submission_status={data.get('submission_status')} "
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
