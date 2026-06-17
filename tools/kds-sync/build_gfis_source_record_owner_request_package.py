#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
OUTPUT_JSON = ROOT / "docs/harness/evidence/gfis-source-record-owner-request-package-20260617.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_package() -> dict[str, Any]:
    ledger = load_json(ROOT / "docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.json")
    readiness = load_json(
        GFIS_ROOT
        / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-structure-readiness.json"
    )
    source_scan = load_json(
        GFIS_ROOT
        / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-scan.json"
    )

    task = next(
        item for item in ledger["tasks"] if item["task_key"] == "customer_requirement_platform_order_source_of_record"
    )
    expected = readiness["expected_submission"]
    counts = source_scan["counts"]

    package = {
        "package_id": "GPCF-GFIS-SOURCE-RECORD-OWNER-REQUEST-20260617",
        "round_id": "GPCF-L4-GFIS-REPAIR-214",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": "CustomerRequirementOrPlatformOrder source-of-record owner request",
        "task_id": task["task_id"],
        "task_key": task["task_key"],
        "request_owner": task["owner"],
        "runtime_site_current": "modern_jinggong_oem_current",
        "runtime_site_future": "gehu_owned_factory_after_commissioning",
        "object_family": "CustomerRequirementOrPlatformOrder",
        "sop_stage": "01_customer_requirement_platform_order",
        "request_state": "ready_to_request_owner_response_not_submitted",
        "expected_submission_path": task["expected_submission_path"],
        "allowed_source_kinds": expected["allowed_source_kinds"],
        "forbidden_source_kinds": expected["forbidden_source_kinds"],
        "required_fields": expected["required_fields"],
        "owner_request_payload": {
            "business_question": "Please provide the real customer order original or platform order receipt for Liaoning Yuanhang.",
            "must_include": expected["required_fields"],
            "must_not_use_as_substitute": expected["forbidden_source_kinds"],
            "kds_backlink_requirement": expected["kds_backlink_must_start_with"],
            "source_record_hash_format": expected["source_record_hash_format"],
            "owner_confirmation_required": expected["owner_confirmation_required"],
        },
        "current_counts": {
            "submitted_files_found": counts.get("submitted_files_found", 0),
            "valid_source_records": counts.get("valid_source_records", 0),
            "structure_valid_records": counts.get("structure_valid_records", 0),
            "runtime_primary_key_ready": counts.get("runtime_primary_key_ready", 0),
            "runtime_primary_key_missing": counts.get("runtime_primary_key_missing", 1),
            "review_queue": counts.get("review_queue", 0),
            "runtime_intake": counts.get("runtime_intake", 0),
            "waes_review": counts.get("waes_review", 0),
            "verified": counts.get("verified", 0),
        },
        "source_evidence": [
            "GPCF:docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.json",
            "GFIS:docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-scan.json",
            "GFIS:docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-structure-readiness.json",
        ],
        "non_claims": {
            "request_package_is_source_record": False,
            "owner_response_received": False,
            "source_of_record_received": False,
            "structure_valid_source_record": False,
            "runtime_primary_key_created": False,
            "review_queue_created": False,
            "runtime_intake_created": False,
            "waes_review_created": False,
            "verified_artifact_created": False,
            "production_write": False,
            "real_external_api_write": False,
            "real_kds_write": False,
            "real_waes_write": False,
            "bench_migrate": False,
            "schema_sync": False,
            "permission_change": False,
            "accepted_integrated": False,
        },
        "next": "obtain_real_customer_order_original_or_platform_order_receipt_json_from_owner",
    }
    return package


def render_markdown(package: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-GFIS-SOURCE-RECORD-OWNER-REQUEST-20260617",
        "title: GFIS Source Record Owner Request Package",
        "project: GPCF",
        "related_projects: [GFIS, GPC, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md",
        "source_path: docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-17",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GFIS Source Record Owner Request Package",
        "",
        f"- package_id: `{package['package_id']}`",
        f"- round_id: `{package['round_id']}`",
        f"- request_owner: `{package['request_owner']}`",
        f"- request_state: `{package['request_state']}`",
        f"- expected_submission_path: `{package['expected_submission_path']}`",
        "",
        "## Required Fields",
        "",
    ]
    for field in package["required_fields"]:
        lines.append(f"- `{field}`")
    lines.extend(["", "## Forbidden Substitutes", ""])
    for source_kind in package["forbidden_source_kinds"]:
        lines.append(f"- `{source_kind}`")
    lines.extend(
        [
            "",
            "## Current Counts",
            "",
            "| metric | value |",
            "|---|---:|",
        ]
    )
    for key, value in package["current_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Non-claims", ""])
    for key, value in package["non_claims"].items():
        lines.append(f"- `{key}`: `{str(value).lower()}`")
    lines.extend(["", "## Next", "", f"`{package['next']}`", ""])
    return "\n".join(lines)


def main() -> None:
    package = build_package()
    OUTPUT_JSON.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(package), encoding="utf-8")
    counts = package["current_counts"]
    print(
        "gfis_source_record_owner_request_package=pass "
        f"submitted_files_found={counts['submitted_files_found']} "
        f"valid_source_records={counts['valid_source_records']} "
        f"runtime_primary_key_ready={counts['runtime_primary_key_ready']} "
        f"runtime_sop_e2e=repair_required"
    )


if __name__ == "__main__":
    main()
