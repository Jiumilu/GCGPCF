#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "docs/harness/evidence/gfis-source-record-owner-request-package-20260617.json"


def fail(reason: str) -> None:
    raise SystemExit(f"gfis_source_record_owner_request_package=fail reason={reason}")


def main() -> None:
    if not PACKAGE.exists():
        fail("package_missing")
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    if package.get("task_key") != "customer_requirement_platform_order_source_of_record":
        fail("unexpected_task_key")
    if package.get("request_state") != "ready_to_request_owner_response_not_submitted":
        fail("request_state_must_not_claim_submission")
    required = package.get("required_fields", [])
    for field in [
        "source_kind",
        "customer_order_original_or_platform_order_receipt",
        "source_record_hash",
        "owner_confirmation",
        "runtime_site_context",
    ]:
        if field not in required:
            fail(f"required_field_missing:{field}")
    counts = package.get("current_counts", {})
    for gate in [
        "submitted_files_found",
        "valid_source_records",
        "structure_valid_records",
        "runtime_primary_key_ready",
        "review_queue",
        "runtime_intake",
        "waes_review",
        "verified",
    ]:
        if counts.get(gate) != 0:
            fail(f"{gate}_must_remain_0")
    non_claims = package.get("non_claims", {})
    for key, value in non_claims.items():
        if value is not False:
            fail(f"non_claim_must_be_false:{key}")
    print(
        "gfis_source_record_owner_request_package=pass "
        f"required_fields={len(required)} submitted_files_found={counts.get('submitted_files_found')} "
        f"valid_source_records={counts.get('valid_source_records')} runtime_intake={counts.get('runtime_intake')} "
        "runtime_sop_e2e=repair_required"
    )


if __name__ == "__main__":
    main()
