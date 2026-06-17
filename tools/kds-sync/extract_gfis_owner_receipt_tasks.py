#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
OUTPUT_JSON = ROOT / "docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.md"


def load_json(relative_path: str) -> dict[str, Any]:
    path = GFIS_ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8"))


def targeted_candidate_for(search: dict[str, Any], proof_key: str) -> dict[str, Any]:
    for item in search.get("items", []):
        if item.get("proof_key") == proof_key:
            top = item.get("top_candidate") or {}
            return {
                "proof_key": proof_key,
                "candidate_count": item.get("candidate_count", 0),
                "top_kds_path": top.get("kds_path"),
                "top_source_record_uri": top.get("source_record_uri"),
                "top_source_record_hash": top.get("source_record_hash"),
                "artifact_status": top.get("artifact_status"),
                "rejection_reason": top.get("rejection_reason"),
            }
    return {"proof_key": proof_key, "candidate_count": 0}


def directory_entry_for(receipt_structure: dict[str, Any], category: str) -> dict[str, Any]:
    for item in receipt_structure.get("directory_entries", []):
        if item.get("category") == category:
            return item
    raise SystemExit(f"missing directory entry: {category}")


def customer_requirement_readiness(primary_key_gate: dict[str, Any]) -> dict[str, Any]:
    for item in primary_key_gate.get("object_readiness", []):
        if item.get("object_family") == "CustomerRequirementOrPlatformOrder":
            return item
    raise SystemExit("missing CustomerRequirementOrPlatformOrder readiness")


def build_tasks() -> dict[str, Any]:
    source_scan = load_json(
        "docs/harness/sop-e2e/evidence/"
        "gfis-customer-requirement-platform-order-source-record-scan.json"
    )
    source_readiness = load_json(
        "docs/harness/sop-e2e/evidence/"
        "gfis-customer-requirement-platform-order-source-record-structure-readiness.json"
    )
    dispatch_scan = load_json(
        "docs/harness/sop-e2e/evidence/"
        "gfis-customer-requirement-platform-order-review-authorization-envelope-owner-manual-request-dispatch-confirmation-receiving-file-scan.json"
    )
    receipt_structure = load_json(
        "docs/harness/sop-e2e/evidence/"
        "liaoning-yuanhang-contract-chain-real-receipt-receiving-directory-structure.json"
    )
    primary_key_gate = load_json(
        "docs/harness/sop-e2e/evidence/gfis-kds-to-runtime-primary-key-readiness-gate.json"
    )
    kds_search = load_json(
        "docs/harness/sop-e2e/evidence/liaoning-yuanhang-targeted-kds-search-result.json"
    )

    customer_readiness = customer_requirement_readiness(primary_key_gate)
    kds_entry = directory_entry_for(receipt_structure, "kds_write_receipt")
    waes_entry = directory_entry_for(receipt_structure, "waes_confirmation")

    source_required = source_readiness.get("expected_submission", {}).get("required_fields", [])
    source_receiving_dir = source_scan.get("sources", {}).get("receiving_directory")
    source_expected_suffix = source_scan.get("expected_submission", {}).get("expected_suffix")

    tasks = [
        {
            "task_id": "GFIS-OWNER-RECEIPT-TASK-001",
            "task_key": "customer_requirement_platform_order_source_of_record",
            "priority": 1,
            "object_family": "CustomerRequirementOrPlatformOrder",
            "owner": "GPC_or_Liaoning_Yuanhang_order_owner",
            "required_receipt": "structure_valid_customer_order_original_or_platform_order_receipt",
            "expected_submission_path": f"{source_receiving_dir}/*{source_expected_suffix}",
            "required_fields": source_required,
            "kds_candidate": targeted_candidate_for(kds_search, "liaoning_yuanhang_project_quotation"),
            "source_evidence": [
                "GFIS:docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-scan.json",
                "GFIS:docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-structure-readiness.json",
            ],
            "current_counts": source_scan.get("counts", {}),
            "state": "open_missing_real_source_of_record",
            "blocks": [
                "runtime_primary_key",
                "review_queue",
                "runtime_intake",
                "waes_review",
                "verified_artifact",
            ],
        },
        {
            "task_id": "GFIS-OWNER-RECEIPT-TASK-002",
            "task_key": "customer_requirement_platform_order_dispatch_confirmation",
            "priority": 2,
            "object_family": "CustomerRequirementOrPlatformOrder",
            "owner": "GFIS_GPC_manual_dispatch_owner_and_receiving_owner",
            "required_receipt": "real_dispatch_confirmation_file",
            "expected_submission_path": dispatch_scan.get("expected_confirmation_path"),
            "required_fields": dispatch_scan.get("required_schema_fields", []),
            "kds_candidate": {
                "candidate_status": "not_a_substitute_for_dispatch_confirmation",
                "reason": "KDS candidates can guide owner lookup but cannot confirm manual dispatch.",
            },
            "source_evidence": [
                "GFIS:docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-review-authorization-envelope-owner-manual-request-dispatch-confirmation-receiving-file-scan.json",
            ],
            "current_counts": dispatch_scan.get("counts", {}),
            "state": "open_missing_real_dispatch_confirmation",
            "blocks": [
                "acknowledgement",
                "owner_response",
                "submission_package",
                "review_queue",
                "runtime_intake",
            ],
        },
        {
            "task_id": "GFIS-OWNER-RECEIPT-TASK-003",
            "task_key": "waes_confirmation",
            "priority": 3,
            "object_family": "CustomerRequirementOrPlatformOrder",
            "owner": waes_entry.get("handoff_owner"),
            "required_receipt": waes_entry.get("required_file"),
            "expected_submission_path": waes_entry.get("collection_path"),
            "required_fields": waes_entry.get("required_fields", []),
            "kds_candidate": {
                "candidate_status": "controlled_reference_only",
                "reason": "WAES confirmation must come from WAES decision/evidence owner, not from KDS mirror text.",
            },
            "source_evidence": [
                "GFIS:docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-receiving-directory-structure.json",
            ],
            "current_counts": {
                "submitted_file_count": waes_entry.get("submitted_file_count", 0),
                "owner_response_count": waes_entry.get("owner_response_count", 0),
                "structure_valid": waes_entry.get("structure_valid", 0),
            },
            "state": "open_missing_waes_confirmation",
            "blocks": ["waes_review", "verified_artifact", "runtime_intake"],
        },
        {
            "task_id": "GFIS-OWNER-RECEIPT-TASK-004",
            "task_key": "kds_write_receipt",
            "priority": 4,
            "object_family": "CustomerRequirementOrPlatformOrder",
            "owner": kds_entry.get("handoff_owner"),
            "required_receipt": kds_entry.get("required_file"),
            "expected_submission_path": kds_entry.get("collection_path"),
            "required_fields": kds_entry.get("required_fields", []),
            "kds_candidate": {
                "candidate_status": "local_mirror_or_candidate_not_receipt",
                "reason": "A KDS candidate path is not a write receipt; ledger/write receipt id and content hash are required.",
            },
            "source_evidence": [
                "GFIS:docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-receiving-directory-structure.json",
            ],
            "current_counts": {
                "submitted_file_count": kds_entry.get("submitted_file_count", 0),
                "owner_response_count": kds_entry.get("owner_response_count", 0),
                "structure_valid": kds_entry.get("structure_valid", 0),
            },
            "state": "open_missing_kds_write_receipt",
            "blocks": ["kds_backlink", "runtime_primary_key", "verified_artifact"],
        },
        {
            "task_id": "GFIS-OWNER-RECEIPT-TASK-005",
            "task_key": "runtime_primary_key",
            "priority": 5,
            "object_family": "CustomerRequirementOrPlatformOrder",
            "owner": "GFIS_runtime_owner_after_source_dispatch_waes_kds_receipts",
            "required_receipt": customer_readiness.get("required_runtime_primary_key"),
            "expected_submission_path": "GFIS runtime read-only primary key evidence after authorized intake",
            "required_fields": [
                "object_family",
                "sop_stage",
                "runtime_primary_key_value",
                "source_of_record_task_id",
                "dispatch_confirmation_task_id",
                "waes_confirmation_task_id",
                "kds_write_receipt_task_id",
            ],
            "kds_candidate": {
                "candidate_status": "blocked_until_upstream_receipts_valid",
                "reason": "Primary key evidence cannot exist until source-of-record, dispatch, WAES and KDS receipts pass.",
            },
            "source_evidence": [
                "GFIS:docs/harness/sop-e2e/evidence/gfis-kds-to-runtime-primary-key-readiness-gate.json",
            ],
            "current_counts": {
                "runtime_primary_key_present": int(bool(customer_readiness.get("runtime_primary_key_present"))),
                "runtime_primary_key_ready": customer_readiness.get("runtime_primary_key_ready", 0),
                "review_queue": customer_readiness.get("review_queue", 0),
                "runtime_intake": customer_readiness.get("runtime_intake", 0),
                "waes_review": customer_readiness.get("waes_review", 0),
                "verified": customer_readiness.get("verified", 0),
            },
            "state": "blocked_missing_upstream_receipts",
            "blocks": ["runtime_sop_e2e_acceptance"],
        },
    ]

    return {
        "ledger_id": "GPCF-GFIS-OWNER-RECEIPT-TASK-LEDGER-20260617",
        "round_id": "GPCF-L4-GFIS-REPAIR-213",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": "GFIS runtime owner receipt tasks from KDS candidates",
        "policy": "extract_tasks_only_no_business_completion_no_production_write",
        "current_runtime_site": "modern_jinggong_oem_current",
        "future_runtime_site": "gehu_owned_factory_after_commissioning",
        "task_count": len(tasks),
        "open_task_count": len([task for task in tasks if task["state"].startswith("open")]),
        "blocked_task_count": len([task for task in tasks if task["state"].startswith("blocked")]),
        "completed_task_count": 0,
        "review_queue": 0,
        "runtime_intake": 0,
        "waes_review": 0,
        "verified": 0,
        "runtime_sop_e2e": "repair_required",
        "tasks": tasks,
        "non_claims": {
            "kds_candidate_is_live_proof": False,
            "task_ledger_is_owner_receipt": False,
            "source_of_record_received": False,
            "dispatch_confirmation_received": False,
            "waes_confirmation_received": False,
            "kds_write_receipt_received": False,
            "runtime_primary_key_created": False,
            "production_write": False,
            "real_external_api_write": False,
            "real_kds_write": False,
            "real_waes_write": False,
            "bench_migrate": False,
            "schema_sync": False,
            "permission_change": False,
            "accepted_integrated": False,
        },
        "next": "collect_task_001_source_of_record_then_task_002_dispatch_confirmation",
    }


def render_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-DE35E75C5A",
        "title: GFIS owner receipt task ledger",
        "project: KDS",
        "related_projects: [GFIS, GPC, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.md",
        "source_path: docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-12",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GFIS owner receipt task ledger",
        "",
        f"- ledger_id: `{ledger['ledger_id']}`",
        f"- round_id: `{ledger['round_id']}`",
        f"- generated_at: `{ledger['generated_at']}`",
        f"- current_runtime_site: `{ledger['current_runtime_site']}`",
        f"- future_runtime_site: `{ledger['future_runtime_site']}`",
        f"- runtime_sop_e2e: `{ledger['runtime_sop_e2e']}`",
        "- policy: extract tasks only; no business completion claim",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| task_count | {ledger['task_count']} |",
        f"| open_task_count | {ledger['open_task_count']} |",
        f"| blocked_task_count | {ledger['blocked_task_count']} |",
        f"| completed_task_count | {ledger['completed_task_count']} |",
        f"| review_queue | {ledger['review_queue']} |",
        f"| runtime_intake | {ledger['runtime_intake']} |",
        f"| waes_review | {ledger['waes_review']} |",
        f"| verified | {ledger['verified']} |",
        "",
        "## Tasks",
        "",
        "| priority | task_id | task_key | owner | state | expected_submission_path |",
        "|---:|---|---|---|---|---|",
    ]
    for task in ledger["tasks"]:
        lines.append(
            "| {priority} | `{task_id}` | `{task_key}` | {owner} | `{state}` | `{path}` |".format(
                priority=task["priority"],
                task_id=task["task_id"],
                task_key=task["task_key"],
                owner=task["owner"],
                state=task["state"],
                path=task["expected_submission_path"],
            )
        )
    lines.extend(
        [
            "",
            "## Non-claims",
            "",
        ]
    )
    for key, value in ledger["non_claims"].items():
        lines.append(f"- `{key}`: `{str(value).lower()}`")
    lines.extend(
        [
            "",
            "## Next",
            "",
            f"`{ledger['next']}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    ledger = build_tasks()
    OUTPUT_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(ledger) + "\n", encoding="utf-8")
    print(
        "gfis_owner_receipt_tasks=pass "
        f"tasks={ledger['task_count']} open={ledger['open_task_count']} "
        f"blocked={ledger['blocked_task_count']} completed={ledger['completed_task_count']} "
        f"runtime_sop_e2e={ledger['runtime_sop_e2e']}"
    )


if __name__ == "__main__":
    main()
