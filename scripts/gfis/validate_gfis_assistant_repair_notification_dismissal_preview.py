#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification dismissal preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-dismissal-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-dismissal-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-dismissal-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesDismissalRecord",
    "writesNotification",
    "modifiesNotification",
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
    previews: list[dict[str, Any]] = fixture["dismissalPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationDismissalPreviewType": policy["dismissal_types"],
        "GfisAssistantRepairNotificationDismissalPreviewStatus": policy["dismissal_statuses"],
        "GfisAssistantRepairNotificationDismissalPreviewDecision": policy["dismissal_decisions"],
        "GfisAssistantRepairNotificationDismissalPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    dismissal_types = set(policy["dismissal_types"])
    dismissal_statuses = set(policy["dismissal_statuses"])
    dismissal_decisions = set(policy["dismissal_decisions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "dismissDisplayNotificationPreview": 0,
        "deferRepairNotificationPreview": 0,
        "retainMetadataBoundaryNotificationPreview": 0,
        "retainCommitteeNotificationPreview": 0,
        "blockFreezeNotificationDismissalPreview": 0,
        "retainBlockedWriteNotificationPreview": 0,
        "dismissalPreviewOnly": 0,
        "deferredDismissalPreview": 0,
        "retainedNotificationPreview": 0,
        "blockedDismissalPreview": 0,
        "metadataBoundaryRetainedPreview": 0,
        "freezeDismissalBlockedPreview": 0,
        "showDismissalPreviewOnly": 0,
        "showDeferRepairPreview": 0,
        "showMetadataRetainedPreview": 0,
        "showCommitteeRetainedPreview": 0,
        "showFreezeDismissalBlockedPreview": 0,
        "showBlockedWriteRetainedPreview": 0,
        "createsDismissalRecords": 0,
        "createsNotifications": 0,
        "modifiesNotifications": 0,
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
        "dismiss_display_notification_preview": "dismissDisplayNotificationPreview",
        "defer_repair_notification_preview": "deferRepairNotificationPreview",
        "retain_metadata_boundary_notification_preview": "retainMetadataBoundaryNotificationPreview",
        "retain_committee_notification_preview": "retainCommitteeNotificationPreview",
        "block_freeze_notification_dismissal_preview": "blockFreezeNotificationDismissalPreview",
        "retain_blocked_write_notification_preview": "retainBlockedWriteNotificationPreview",
    }
    status_keys = {
        "dismissal_preview_only": "dismissalPreviewOnly",
        "deferred_dismissal_preview": "deferredDismissalPreview",
        "retained_notification_preview": "retainedNotificationPreview",
        "blocked_dismissal_preview": "blockedDismissalPreview",
        "metadata_boundary_retained_preview": "metadataBoundaryRetainedPreview",
        "freeze_dismissal_blocked_preview": "freezeDismissalBlockedPreview",
    }
    decision_keys = {
        "show_dismissal_preview_only": "showDismissalPreviewOnly",
        "show_defer_repair_preview": "showDeferRepairPreview",
        "show_metadata_retained_preview": "showMetadataRetainedPreview",
        "show_committee_retained_preview": "showCommitteeRetainedPreview",
        "show_freeze_dismissal_blocked_preview": "showFreezeDismissalBlockedPreview",
        "show_blocked_write_retained_preview": "showBlockedWriteRetainedPreview",
    }

    for preview in previews:
        preview_id = preview["dismissalPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["dismissalType"] not in dismissal_types:
            failures.append(f"{preview_id}: invalid dismissalType")
        if preview["dismissalStatus"] not in dismissal_statuses:
            failures.append(f"{preview_id}: invalid dismissalStatus")
        if preview["dismissalDecision"] not in dismissal_decisions:
            failures.append(f"{preview_id}: invalid dismissalDecision")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["dismissalSummaryRef"] or not preview["reasonRefs"] or not preview["dismissalNoteRefs"]:
            failures.append(f"{preview_id}: dismissalSummaryRef, reasonRefs, and dismissalNoteRefs are required")
        if not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: nextStepCandidateRefs are required")

        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["dismissalType"]]] += 1
        counts[status_keys[preview["dismissalStatus"]]] += 1
        counts[decision_keys[preview["dismissalDecision"]]] += 1
        false_flags = (
            "createsDismissalRecord",
            "createsNotification",
            "modifiesNotification",
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
        counts["createsDismissalRecords"] += int(preview["createsDismissalRecord"] is True)
        counts["createsNotifications"] += int(preview["createsNotification"] is True)
        counts["modifiesNotifications"] += int(preview["modifiesNotification"] is True)
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
            [preview["dismissalSummaryRef"]]
            + preview["lineageHintRefs"]
            + preview["reasonRefs"]
            + preview["dismissalNoteRefs"]
            + preview["nextStepCandidateRefs"]
            + preview["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{preview_id}: dismissal preview must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"dismissalPreviewCount": len(previews), **counts, **totals}

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
        print("gfis_assistant_repair_notification_dismissal_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_dismissal_preview=pass "
        f"previews={actual['dismissalPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} dismiss_display_notification_preview={actual['dismissDisplayNotificationPreview']} "
        f"defer_repair_notification_preview={actual['deferRepairNotificationPreview']} "
        f"retain_metadata_boundary_notification_preview={actual['retainMetadataBoundaryNotificationPreview']} "
        f"retain_committee_notification_preview={actual['retainCommitteeNotificationPreview']} "
        f"block_freeze_notification_dismissal_preview={actual['blockFreezeNotificationDismissalPreview']} "
        f"retain_blocked_write_notification_preview={actual['retainBlockedWriteNotificationPreview']} "
        f"creates_dismissal_records={actual['createsDismissalRecords']} creates_notifications={actual['createsNotifications']} "
        f"modifies_notifications={actual['modifiesNotifications']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_audit_trace_records={actual['createsAuditTraceRecords']} creates_event_records={actual['createsEventRecords']} "
        f"creates_action_receipts={actual['createsActionReceipts']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_dismissal_record=0 writes_notification=0 modifies_notification=0 "
        "writes_read_receipt=0 writes_audit_trace_record=0 writes_event_record=0 writes_action_receipt=0 "
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
