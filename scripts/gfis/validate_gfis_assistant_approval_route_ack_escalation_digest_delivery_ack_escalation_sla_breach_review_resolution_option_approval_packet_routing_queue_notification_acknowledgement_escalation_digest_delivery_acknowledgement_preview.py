#!/usr/bin/env python3
"""Validate GFIS Assistant approval route acknowledgement escalation digest delivery acknowledgement preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesDeliveryAcknowledgement", "writesDelivery", "writesNotification",
    "writesDigest", "writesAcknowledgement", "writesReadReceipt",
    "writesReminder", "writesEscalationTask", "writesApprovalRequest",
    "writesApprovalDecision", "writesWaesGateResult", "writesKweWorkItem",
    "writesHarnessEvidence", "writesKdsLifecycle", "writesKdsFact",
    "writesKdsAcceptedFact", "writesExternalApi",
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
    previews: list[dict[str, Any]] = fixture["acknowledgementPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewType": policy["acknowledgement_types"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewStatus": policy["acknowledgement_statuses"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewDecision": policy["acknowledgement_decisions"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewScope": policy["acknowledgement_scopes"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewMethod": policy["acknowledgement_methods"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    acknowledgement_methods = set(policy["acknowledgement_methods"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "teamAck": 0, "projectAck": 0, "governanceAck": 0,
        "externalBlockedAck": 0, "committeeAck": 0, "freezeAck": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "acknowledgementPreviewOnly": 0, "acknowledgementAtRiskPreview": 0,
        "acknowledgementMetadataBoundary": 0, "acknowledgementExternalBlocked": 0,
        "acknowledgementCommitteeRequired": 0, "acknowledgementFreezeRequired": 0,
        "totalAcknowledgerCount": 0, "totalMethodCount": 0,
        "totalBlockedAcknowledgementCount": 0,
        "createsDeliveryAcknowledgements": 0, "createsDeliveries": 0,
        "createsNotifications": 0, "createsDigests": 0,
        "createsAcknowledgements": 0, "createsReadReceipts": 0,
        "createsReminders": 0, "createsEscalationTasks": 0,
        "createsApprovalRequests": 0, "createsApprovalDecisions": 0,
        "createsHarnessEvidence": 0, "createsWaesGateResults": 0,
        "createsKweWorkItems": 0, "persistsEvidence": 0,
        "approvesBusinessWrite": 0, "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "team_delivery_ack_preview": "teamAck",
        "project_delivery_ack_preview": "projectAck",
        "governance_delivery_ack_preview": "governanceAck",
        "external_blocked_delivery_ack_preview": "externalBlockedAck",
        "committee_delivery_ack_preview": "committeeAck",
        "freeze_delivery_ack_preview": "freezeAck",
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
        "acknowledgement_preview_only": "acknowledgementPreviewOnly",
        "acknowledgement_at_risk_preview": "acknowledgementAtRiskPreview",
        "acknowledgement_metadata_boundary": "acknowledgementMetadataBoundary",
        "acknowledgement_external_blocked": "acknowledgementExternalBlocked",
        "acknowledgement_committee_required": "acknowledgementCommitteeRequired",
        "acknowledgement_freeze_required": "acknowledgementFreezeRequired",
    }
    false_flags = (
        "createsDeliveryAcknowledgement", "createsDelivery",
        "createsNotification", "createsDigest", "createsAcknowledgement",
        "createsReadReceipt", "createsReminder", "createsEscalationTask",
        "createsApprovalRequest", "createsApprovalDecision",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsDeliveryAcknowledgement": "createsDeliveryAcknowledgements",
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
        preview_id = preview["deliveryAcknowledgementPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        delivery_refs = set(preview["deliveryPreviewRefs"])
        source_delivery_refs = set(preview["sourceDeliveryPreviewRefs"])
        if not delivery_refs or not delivery_refs <= source_delivery_refs:
            failures.append(f"{preview_id}: deliveryPreviewRefs must be included in sourceDeliveryPreviewRefs")
        if not preview["candidateAcknowledgerRefs"] or not preview["acknowledgementMethodRefs"]:
            failures.append(f"{preview_id}: candidateAcknowledgerRefs and acknowledgementMethodRefs are required")
        if not set(preview["acknowledgementMethodRefs"]) <= acknowledgement_methods:
            failures.append(f"{preview_id}: acknowledgementMethodRefs must be declared acknowledgement methods")
        if preview["blockedAcknowledgementCount"] < 0 or preview["blockedAcknowledgementCount"] > len(preview["candidateAcknowledgerRefs"]):
            failures.append(f"{preview_id}: blockedAcknowledgementCount must be between 0 and candidateAcknowledgerRefs length")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"]:
            failures.append(f"{preview_id}: boundaryRefs are required")
        if not preview["acknowledgementSummaryRef"] or not preview["reasonRefs"] or not preview["acknowledgementNoteRefs"]:
            failures.append(f"{preview_id}: acknowledgementSummaryRef, reasonRefs, and acknowledgementNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["acknowledgementType"]]] += 1
        counts[scope_keys[preview["acknowledgementScope"]]] += 1
        counts[status_keys[preview["acknowledgementStatus"]]] += 1
        counts["totalAcknowledgerCount"] += len(preview["candidateAcknowledgerRefs"])
        counts["totalMethodCount"] += len(preview["acknowledgementMethodRefs"])
        counts["totalBlockedAcknowledgementCount"] += preview["blockedAcknowledgementCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"acknowledgementPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_digest_delivery_acknowledgement_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_digest_delivery_acknowledgement_preview=pass "
        f"acknowledgements={actual['acknowledgementPreviewCount']} brain={actual['brainSurface']} "
        f"pkc={actual['pkcSurface']} gfis_assistant={actual['gfisAssistantSurface']} "
        f"total_acknowledgers={actual['totalAcknowledgerCount']} total_methods={actual['totalMethodCount']} "
        f"total_blocked_acknowledgement={actual['totalBlockedAcknowledgementCount']} "
        f"creates_delivery_acknowledgements={actual['createsDeliveryAcknowledgements']} "
        f"creates_deliveries={actual['createsDeliveries']} creates_notifications={actual['createsNotifications']} "
        f"creates_digests={actual['createsDigests']} creates_acknowledgements={actual['createsAcknowledgements']} "
        f"creates_read_receipts={actual['createsReadReceipts']} creates_reminders={actual['createsReminders']} "
        f"creates_escalation_tasks={actual['createsEscalationTasks']} creates_approval_requests={actual['createsApprovalRequests']} "
        f"creates_approval_decisions={actual['createsApprovalDecisions']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_delivery_acknowledgement=0 writes_delivery=0 "
        "writes_notification=0 writes_digest=0 writes_acknowledgement=0 writes_read_receipt=0 writes_reminder=0 "
        "writes_escalation_task=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
