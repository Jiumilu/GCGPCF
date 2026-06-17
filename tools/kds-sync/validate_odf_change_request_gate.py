#!/usr/bin/env python3
"""Validate ODF change/admission request governance.

This gate checks that future ODF sample expansion is request-driven and bounded.
It is read-only and does not authorize rollout, KDS writes, or business status
upgrades by itself.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUEST_LEDGER = ROOT / "docs/harness/evidence/odf-phase5-change-request-ledger-20260617.json"
MAX_SMALL_BATCH_SAMPLES = 5
REQUIRED_REQUEST_FIELDS = {
    "request_id",
    "request_type",
    "status",
    "requested_by",
    "manual_confirmation",
    "sample_scope",
    "source_paths",
    "odf_paths",
    "kds_sync_paths",
    "rollback_hints",
    "boundary",
}
ALLOWED_REQUEST_STATUSES = {"approved_for_small_batch_audit", "closed_after_audit"}
FORBIDDEN_MARKERS = {"full_rollout", "accepted", "integrated"}
REQUIRED_BOUNDARY_FALSE = {
    "full_rollout",
    "accepted",
    "integrated",
    "business_completion_claim",
    "production_write",
    "external_api_write",
}


def fail(reason: str) -> None:
    raise SystemExit(f"odf_change_request_gate=fail reason={reason}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing_request_ledger:{path.relative_to(ROOT).as_posix()}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid_request_ledger_json:{exc}")


def require_list(value: object, field: str, request_id: str) -> list:
    if not isinstance(value, list) or not value:
        fail(f"{request_id}:{field}_must_be_non_empty_list")
    return value


def main() -> int:
    ledger = load_json(REQUEST_LEDGER)
    if ledger.get("status") != "phase5_change_request_closed":
        fail(f"invalid_ledger_status:{ledger.get('status')}")
    if ledger.get("max_small_batch_samples") != MAX_SMALL_BATCH_SAMPLES:
        fail("max_small_batch_samples_mismatch")

    requests = ledger.get("requests", [])
    if not isinstance(requests, list) or not requests:
        fail("requests_empty")

    seen_request_ids: set[str] = set()
    total_samples = 0
    closed = 0
    approved = 0

    for request in requests:
        missing = sorted(REQUIRED_REQUEST_FIELDS - request.keys())
        request_id = request.get("request_id", "<missing>")
        if missing:
            fail(f"{request_id}:missing_fields:{','.join(missing)}")
        if request_id in seen_request_ids:
            fail(f"duplicate_request_id:{request_id}")
        seen_request_ids.add(request_id)

        status = request.get("status")
        if status not in ALLOWED_REQUEST_STATUSES:
            fail(f"{request_id}:invalid_status:{status}")
        if status in FORBIDDEN_MARKERS:
            fail(f"{request_id}:forbidden_status:{status}")
        if status == "closed_after_audit":
            closed += 1
        if status == "approved_for_small_batch_audit":
            approved += 1

        if request.get("request_type") != "odf_small_batch_admission":
            fail(f"{request_id}:invalid_request_type")
        if request.get("manual_confirmation") is not True:
            fail(f"{request_id}:manual_confirmation_required")

        sample_scope = request.get("sample_scope", {})
        sample_count = sample_scope.get("sample_count")
        if not isinstance(sample_count, int) or sample_count < 1:
            fail(f"{request_id}:invalid_sample_count")
        if sample_count > MAX_SMALL_BATCH_SAMPLES:
            fail(f"{request_id}:sample_count_exceeds_limit")
        total_samples += sample_count

        source_paths = require_list(request.get("source_paths"), "source_paths", request_id)
        odf_paths = require_list(request.get("odf_paths"), "odf_paths", request_id)
        kds_sync_paths = require_list(request.get("kds_sync_paths"), "kds_sync_paths", request_id)
        rollback_hints = require_list(request.get("rollback_hints"), "rollback_hints", request_id)
        if len(source_paths) != sample_count:
            fail(f"{request_id}:source_path_count_mismatch")
        if len(odf_paths) != sample_count:
            fail(f"{request_id}:odf_path_count_mismatch")
        if len(rollback_hints) != sample_count:
            fail(f"{request_id}:rollback_hint_count_mismatch")
        for path in source_paths + odf_paths + kds_sync_paths:
            if not isinstance(path, str) or not path:
                fail(f"{request_id}:empty_path")
            if "TOKEN" in path or "token" in path:
                fail(f"{request_id}:path_must_not_reference_token")

        boundary = request.get("boundary", {})
        for key in REQUIRED_BOUNDARY_FALSE:
            if boundary.get(key) is not False:
                fail(f"{request_id}:boundary_must_be_false:{key}")

    print(
        "odf_change_request_gate=pass "
        f"requests={len(requests)} "
        f"closed={closed} "
        f"approved_open={approved} "
        f"total_samples={total_samples} "
        f"max_small_batch_samples={MAX_SMALL_BATCH_SAMPLES} "
        "manual_confirmation=pass rollback_hints=pass kds_sync_paths=pass "
        "forbidden_rollout=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
