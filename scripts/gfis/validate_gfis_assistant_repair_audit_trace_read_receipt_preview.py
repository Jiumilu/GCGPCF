#!/usr/bin/env python3
"""Validate GFIS Assistant repair audit trace read receipt preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-audit-trace-read-receipt-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-audit-trace-read-receipt-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-audit-trace-read-receipt-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesReadReceipt",
    "writesAuditTraceRecord",
    "writesEventRecord",
    "writesActionReceipt",
    "writesHarnessEvidence",
    "writesAdmissionRecord",
    "writesReviewQueueItem",
    "writesConfirmationRecord",
    "writesDecisionRecord",
    "writesGapRecord",
    "writesBountyRecord",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesEvidenceRecord",
    "writesTargetReceipt",
    "writesCommitteeDecisionCompletion",
    "writesRevenueOrScoreConfirmation",
    "writesQuotaTransfer",
    "writesBountySettlement",
    "writesExternalApi",
)


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    previews: list[dict[str, Any]] = fixture["readReceiptPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairAuditTraceReadReceiptPreviewType": policy["receipt_types"],
        "GfisAssistantRepairAuditTraceReadReceiptPreviewStatus": policy["receipt_statuses"],
        "GfisAssistantRepairAuditTraceReadReceiptPreviewDecision": policy["receipt_decisions"],
        "GfisAssistantRepairAuditTraceReadReceiptPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    receipt_types = set(policy["receipt_types"])
    receipt_statuses = set(policy["receipt_statuses"])
    receipt_decisions = set(policy["receipt_decisions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "displayReadReceiptPreview": 0,
        "repairReadReceiptPreview": 0,
        "metadataBoundaryReadReceiptPreview": 0,
        "committeeReadReceiptPreview": 0,
        "freezeReadReceiptPreview": 0,
        "blockedWriteReadReceiptPreview": 0,
        "receiptPreviewOnly": 0,
        "blockedReceiptPreview": 0,
        "metadataReceiptPreview": 0,
        "repairReceiptPreview": 0,
        "committeeReceiptPreview": 0,
        "freezeReceiptPreview": 0,
        "showReceiptPreviewOnly": 0,
        "showRepairReceiptPreview": 0,
        "showMetadataBoundaryReceiptPreview": 0,
        "showCommitteeReceiptPreview": 0,
        "showFreezeReceiptPreview": 0,
        "showBlockedWriteReceiptPreview": 0,
        "createsReadReceipts": 0,
        "createsAuditTraceRecords": 0,
        "createsEventRecords": 0,
        "createsActionReceipts": 0,
        "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0,
        "createsKweWorkItems": 0,
        "persistsEvidence": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "display_read_receipt_preview": "displayReadReceiptPreview",
        "repair_read_receipt_preview": "repairReadReceiptPreview",
        "metadata_boundary_read_receipt_preview": "metadataBoundaryReadReceiptPreview",
        "committee_read_receipt_preview": "committeeReadReceiptPreview",
        "freeze_read_receipt_preview": "freezeReadReceiptPreview",
        "blocked_write_read_receipt_preview": "blockedWriteReadReceiptPreview",
    }
    status_keys = {
        "receipt_preview_only": "receiptPreviewOnly",
        "blocked_receipt_preview": "blockedReceiptPreview",
        "metadata_receipt_preview": "metadataReceiptPreview",
        "repair_receipt_preview": "repairReceiptPreview",
        "committee_receipt_preview": "committeeReceiptPreview",
        "freeze_receipt_preview": "freezeReceiptPreview",
    }
    decision_keys = {
        "show_receipt_preview_only": "showReceiptPreviewOnly",
        "show_repair_receipt_preview": "showRepairReceiptPreview",
        "show_metadata_boundary_receipt_preview": "showMetadataBoundaryReceiptPreview",
        "show_committee_receipt_preview": "showCommitteeReceiptPreview",
        "show_freeze_receipt_preview": "showFreezeReceiptPreview",
        "show_blocked_write_receipt_preview": "showBlockedWriteReceiptPreview",
    }

    for preview in previews:
        preview_id = preview["readReceiptPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["receiptType"] not in receipt_types:
            failures.append(f"{preview_id}: invalid receiptType")
        if preview["receiptStatus"] not in receipt_statuses:
            failures.append(f"{preview_id}: invalid receiptStatus")
        if preview["receiptDecision"] not in receipt_decisions:
            failures.append(f"{preview_id}: invalid receiptDecision")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["receiptSummaryRef"] or not preview["reasonRefs"] or not preview["receiptNoteRefs"]:
            failures.append(f"{preview_id}: receiptSummaryRef, reasonRefs, and receiptNoteRefs are required")

        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["receiptType"]]] += 1
        counts[status_keys[preview["receiptStatus"]]] += 1
        counts[decision_keys[preview["receiptDecision"]]] += 1
        false_flags = (
            "createsReadReceipt",
            "createsAuditTraceRecord",
            "createsEventRecord",
            "createsActionReceipt",
            "createsHarnessEvidence",
            "createsWaesGateResult",
            "createsKweWorkItem",
            "persistsEvidence",
            "approvesBusinessWrite",
            "promotesLifecycle",
            "completesCommitteeDecision",
        )
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
        counts["createsReadReceipts"] += int(preview["createsReadReceipt"] is True)
        counts["createsAuditTraceRecords"] += int(preview["createsAuditTraceRecord"] is True)
        counts["createsEventRecords"] += int(preview["createsEventRecord"] is True)
        counts["createsActionReceipts"] += int(preview["createsActionReceipt"] is True)
        counts["createsHarnessEvidence"] += int(preview["createsHarnessEvidence"] is True)
        counts["createsWaesGateResults"] += int(preview["createsWaesGateResult"] is True)
        counts["createsKweWorkItems"] += int(preview["createsKweWorkItem"] is True)
        counts["persistsEvidence"] += int(preview["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(preview["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(preview["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(preview["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            [preview["receiptSummaryRef"]]
            + preview["lineageHintRefs"]
            + preview["reasonRefs"]
            + preview["receiptNoteRefs"]
            + preview["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{preview_id}: read receipt preview must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"readReceiptPreviewCount": len(previews), **counts, **totals}

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            failures.append(f"policy hard_boundaries.{key} is not true")
    for key, value in policy["no_write_guards"].items():
        if value != 0:
            failures.append(f"policy no_write_guards.{key} is non-zero")
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("gfis_assistant_repair_audit_trace_read_receipt_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_audit_trace_read_receipt_preview=pass "
        f"previews={actual['readReceiptPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} display_read_receipt_preview={actual['displayReadReceiptPreview']} "
        f"repair_read_receipt_preview={actual['repairReadReceiptPreview']} "
        f"metadata_boundary_read_receipt_preview={actual['metadataBoundaryReadReceiptPreview']} "
        f"committee_read_receipt_preview={actual['committeeReadReceiptPreview']} "
        f"freeze_read_receipt_preview={actual['freezeReadReceiptPreview']} "
        f"blocked_write_read_receipt_preview={actual['blockedWriteReadReceiptPreview']} "
        f"creates_read_receipts={actual['createsReadReceipts']} creates_audit_trace_records={actual['createsAuditTraceRecords']} "
        f"creates_event_records={actual['createsEventRecords']} creates_action_receipts={actual['createsActionReceipts']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} persists_evidence={actual['persistsEvidence']} "
        f"approves_business_write={actual['approvesBusinessWrite']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"completes_committee_decision={actual['completesCommitteeDecision']} writes_gfis=0 writes_gpc=0 "
        "writes_erp=0 writes_mes=0 writes_waes_gate_result=0 writes_kwe_work_item=0 "
        "writes_read_receipt=0 writes_audit_trace_record=0 writes_event_record=0 "
        "writes_action_receipt=0 writes_harness_evidence=0 writes_admission_record=0 "
        "writes_review_queue_item=0 writes_confirmation_record=0 writes_decision_record=0 "
        "writes_gap_record=0 writes_bounty_record=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_evidence_record=0 writes_target_receipt=0 "
        "writes_committee_decision_completion=0 writes_revenue_or_score_confirmation=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
