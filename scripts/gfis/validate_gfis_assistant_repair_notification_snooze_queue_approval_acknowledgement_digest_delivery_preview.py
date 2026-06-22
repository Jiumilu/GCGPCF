#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval acknowledgement digest delivery preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesDelivery", "writesNotification", "writesDigest",
    "writesAcknowledgement", "writesReadReceipt", "writesReminder",
    "writesEscalationTask", "writesApprovalRequest", "writesApprovalDecision",
    "writesWaesGateResult", "writesKweWorkItem", "writesHarnessEvidence",
    "writesKdsLifecycle", "writesKdsFact", "writesKdsAcceptedFact",
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
    previews: list[dict[str, Any]] = fixture["deliveryPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewType": policy["delivery_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewStatus": policy["delivery_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewDecision": policy["delivery_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewScope": policy["delivery_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewChannel": policy["delivery_channels"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    delivery_channels = set(policy["delivery_channels"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "teamDelivery": 0, "projectDelivery": 0, "governanceDelivery": 0,
        "externalBlockedDelivery": 0, "committeeDelivery": 0, "freezeDelivery": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "deliveryPreviewOnly": 0, "deliveryAtRiskPreview": 0,
        "deliveryMetadataBoundary": 0, "deliveryExternalBlocked": 0,
        "deliveryCommitteeRequired": 0, "deliveryFreezeRequired": 0,
        "totalRecipientCount": 0, "totalChannelCount": 0,
        "totalBlockedDeliveryCount": 0,
        "createsDeliveries": 0, "createsNotifications": 0,
        "createsDigests": 0, "createsAcknowledgements": 0,
        "createsReadReceipts": 0, "createsReminders": 0,
        "createsEscalationTasks": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "team_digest_delivery_preview": "teamDelivery",
        "project_digest_delivery_preview": "projectDelivery",
        "governance_digest_delivery_preview": "governanceDelivery",
        "external_blocked_digest_delivery_preview": "externalBlockedDelivery",
        "committee_digest_delivery_preview": "committeeDelivery",
        "freeze_digest_delivery_preview": "freezeDelivery",
    }
    scope_keys = {
        "team_internal": "teamInternalScope",
        "project_internal": "projectInternalScope",
        "governance_review": "governanceReviewScope",
        "external_blocked": "externalBlockedScope",
        "committee_review": "committeeReviewScope",
        "freeze_review": "freezeReviewScope",
    }
    status_keys = {
        "delivery_preview_only": "deliveryPreviewOnly",
        "delivery_at_risk_preview": "deliveryAtRiskPreview",
        "delivery_metadata_boundary": "deliveryMetadataBoundary",
        "delivery_external_blocked": "deliveryExternalBlocked",
        "delivery_committee_required": "deliveryCommitteeRequired",
        "delivery_freeze_required": "deliveryFreezeRequired",
    }
    false_flags = (
        "createsDelivery", "createsNotification", "createsDigest",
        "createsAcknowledgement", "createsReadReceipt", "createsReminder",
        "createsEscalationTask", "createsApprovalRequest",
        "createsApprovalDecision", "createsHarnessEvidence",
        "createsWaesGateResult", "createsKweWorkItem", "persistsEvidence",
        "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsDelivery": "createsDeliveries",
        "createsNotification": "createsNotifications",
        "createsDigest": "createsDigests",
        "createsAcknowledgement": "createsAcknowledgements",
        "createsReadReceipt": "createsReadReceipts",
        "createsReminder": "createsReminders",
        "createsEscalationTask": "createsEscalationTasks",
        "createsApprovalRequest": "createsApprovalRequests",
        "createsApprovalDecision": "createsApprovalDecisions",
        "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults",
        "createsKweWorkItem": "createsKweWorkItems",
        "persistsEvidence": "persistsEvidence",
        "approvesBusinessWrite": "approvesBusinessWrite",
        "promotesLifecycle": "promotesLifecycle",
        "completesCommitteeDecision": "completesCommitteeDecision",
    }

    for preview in previews:
        preview_id = preview["deliveryPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        digest_refs = set(preview["digestPreviewRefs"])
        source_digest_refs = set(preview["sourceDigestPreviewRefs"])
        if not digest_refs or not digest_refs <= source_digest_refs:
            failures.append(f"{preview_id}: digestPreviewRefs must be included in sourceDigestPreviewRefs")
        if not preview["candidateRecipientRefs"] or not preview["candidateChannelRefs"]:
            failures.append(f"{preview_id}: candidateRecipientRefs and candidateChannelRefs are required")
        if not set(preview["candidateChannelRefs"]) <= delivery_channels:
            failures.append(f"{preview_id}: candidateChannelRefs must be declared delivery channels")
        if preview["blockedDeliveryCount"] < 0 or preview["blockedDeliveryCount"] > len(preview["candidateRecipientRefs"]):
            failures.append(f"{preview_id}: blockedDeliveryCount must be between 0 and candidateRecipientRefs length")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"]:
            failures.append(f"{preview_id}: boundaryRefs are required")
        if not preview["deliverySummaryRef"] or not preview["reasonRefs"] or not preview["deliveryNoteRefs"]:
            failures.append(f"{preview_id}: deliverySummaryRef, reasonRefs, and deliveryNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["deliveryType"]]] += 1
        counts[scope_keys[preview["deliveryScope"]]] += 1
        counts[status_keys[preview["deliveryStatus"]]] += 1
        counts["totalRecipientCount"] += len(preview["candidateRecipientRefs"])
        counts["totalChannelCount"] += len(preview["candidateChannelRefs"])
        counts["totalBlockedDeliveryCount"] += preview["blockedDeliveryCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"deliveryPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_preview=pass "
        f"deliveries={actual['deliveryPreviewCount']} brain={actual['brainSurface']} "
        f"pkc={actual['pkcSurface']} gfis_assistant={actual['gfisAssistantSurface']} "
        f"total_recipients={actual['totalRecipientCount']} total_channels={actual['totalChannelCount']} "
        f"total_blocked_delivery={actual['totalBlockedDeliveryCount']} creates_deliveries={actual['createsDeliveries']} "
        f"creates_notifications={actual['createsNotifications']} creates_digests={actual['createsDigests']} "
        f"creates_acknowledgements={actual['createsAcknowledgements']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_reminders={actual['createsReminders']} creates_escalation_tasks={actual['createsEscalationTasks']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_delivery=0 writes_notification=0 writes_digest=0 writes_acknowledgement=0 writes_read_receipt=0 "
        "writes_reminder=0 writes_escalation_task=0 writes_approval_request=0 writes_approval_decision=0 "
        "writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
