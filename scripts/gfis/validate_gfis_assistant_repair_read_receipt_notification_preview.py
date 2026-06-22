#!/usr/bin/env python3
"""Validate GFIS Assistant repair read receipt notification preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-read-receipt-notification-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-read-receipt-notification-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-read-receipt-notification-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesNotification",
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
    previews: list[dict[str, Any]] = fixture["notificationPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairReadReceiptNotificationPreviewType": policy["notification_types"],
        "GfisAssistantRepairReadReceiptNotificationPreviewStatus": policy["notification_statuses"],
        "GfisAssistantRepairReadReceiptNotificationPreviewDecision": policy["notification_decisions"],
        "GfisAssistantRepairReadReceiptNotificationPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    notification_types = set(policy["notification_types"])
    notification_statuses = set(policy["notification_statuses"])
    notification_decisions = set(policy["notification_decisions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "displayNotificationPreview": 0,
        "repairNotificationPreview": 0,
        "metadataBoundaryNotificationPreview": 0,
        "committeeNotificationPreview": 0,
        "freezeNotificationPreview": 0,
        "blockedWriteNotificationPreview": 0,
        "notificationPreviewOnly": 0,
        "blockedNotificationPreview": 0,
        "metadataNotificationPreview": 0,
        "repairNotificationPreviewStatus": 0,
        "committeeNotificationPreviewStatus": 0,
        "freezeNotificationPreviewStatus": 0,
        "showNotificationPreviewOnly": 0,
        "showRepairNotificationPreview": 0,
        "showMetadataBoundaryNotificationPreview": 0,
        "showCommitteeNotificationPreview": 0,
        "showFreezeNotificationPreview": 0,
        "showBlockedWriteNotificationPreview": 0,
        "createsNotifications": 0,
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
        "display_notification_preview": "displayNotificationPreview",
        "repair_notification_preview": "repairNotificationPreview",
        "metadata_boundary_notification_preview": "metadataBoundaryNotificationPreview",
        "committee_notification_preview": "committeeNotificationPreview",
        "freeze_notification_preview": "freezeNotificationPreview",
        "blocked_write_notification_preview": "blockedWriteNotificationPreview",
    }
    status_keys = {
        "notification_preview_only": "notificationPreviewOnly",
        "blocked_notification_preview": "blockedNotificationPreview",
        "metadata_notification_preview": "metadataNotificationPreview",
        "repair_notification_preview_status": "repairNotificationPreviewStatus",
        "committee_notification_preview_status": "committeeNotificationPreviewStatus",
        "freeze_notification_preview_status": "freezeNotificationPreviewStatus",
    }
    decision_keys = {
        "show_notification_preview_only": "showNotificationPreviewOnly",
        "show_repair_notification_preview": "showRepairNotificationPreview",
        "show_metadata_boundary_notification_preview": "showMetadataBoundaryNotificationPreview",
        "show_committee_notification_preview": "showCommitteeNotificationPreview",
        "show_freeze_notification_preview": "showFreezeNotificationPreview",
        "show_blocked_write_notification_preview": "showBlockedWriteNotificationPreview",
    }

    for preview in previews:
        preview_id = preview["notificationPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["notificationType"] not in notification_types:
            failures.append(f"{preview_id}: invalid notificationType")
        if preview["notificationStatus"] not in notification_statuses:
            failures.append(f"{preview_id}: invalid notificationStatus")
        if preview["notificationDecision"] not in notification_decisions:
            failures.append(f"{preview_id}: invalid notificationDecision")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["notificationSummaryRef"] or not preview["reasonRefs"] or not preview["notificationNoteRefs"]:
            failures.append(f"{preview_id}: notificationSummaryRef, reasonRefs, and notificationNoteRefs are required")
        if not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: nextStepCandidateRefs are required")

        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["notificationType"]]] += 1
        counts[status_keys[preview["notificationStatus"]]] += 1
        counts[decision_keys[preview["notificationDecision"]]] += 1
        false_flags = (
            "createsNotification",
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
        counts["createsNotifications"] += int(preview["createsNotification"] is True)
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
            [preview["notificationSummaryRef"]]
            + preview["lineageHintRefs"]
            + preview["reasonRefs"]
            + preview["notificationNoteRefs"]
            + preview["nextStepCandidateRefs"]
            + preview["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{preview_id}: notification preview must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"notificationPreviewCount": len(previews), **counts, **totals}

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
        print("gfis_assistant_repair_read_receipt_notification_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_read_receipt_notification_preview=pass "
        f"previews={actual['notificationPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} display_notification_preview={actual['displayNotificationPreview']} "
        f"repair_notification_preview={actual['repairNotificationPreview']} "
        f"metadata_boundary_notification_preview={actual['metadataBoundaryNotificationPreview']} "
        f"committee_notification_preview={actual['committeeNotificationPreview']} "
        f"freeze_notification_preview={actual['freezeNotificationPreview']} "
        f"blocked_write_notification_preview={actual['blockedWriteNotificationPreview']} "
        f"creates_notifications={actual['createsNotifications']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_audit_trace_records={actual['createsAuditTraceRecords']} creates_event_records={actual['createsEventRecords']} "
        f"creates_action_receipts={actual['createsActionReceipts']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_notification=0 writes_read_receipt=0 "
        "writes_audit_trace_record=0 writes_event_record=0 writes_action_receipt=0 "
        "writes_harness_evidence=0 writes_admission_record=0 writes_review_queue_item=0 "
        "writes_confirmation_record=0 writes_decision_record=0 writes_gap_record=0 "
        "writes_bounty_record=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_evidence_record=0 writes_target_receipt=0 "
        "writes_committee_decision_completion=0 writes_revenue_or_score_confirmation=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
