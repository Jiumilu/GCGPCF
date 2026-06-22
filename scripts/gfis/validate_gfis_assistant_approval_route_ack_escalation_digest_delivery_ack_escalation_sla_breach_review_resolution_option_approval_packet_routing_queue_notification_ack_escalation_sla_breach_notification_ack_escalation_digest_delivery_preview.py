#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-169 routing queue notification acknowledgement escalation digest delivery preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-sla-breach-notification-ack-escalation-digest-delivery-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-sla-breach-notification-ack-escalation-digest-delivery-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-sla-breach-notification-ack-escalation-digest-delivery-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesDigestDelivery", "writesDelivery", "writesDigest",
    "writesEscalation", "writesTimeoutEvent", "writesKweWorkItem",
    "writesNotification", "writesAcknowledgement", "writesReceipt",
    "writesReadReceipt", "writesDeliveryStatus", "writesApprovalAssignment",
    "writesApprovalLock", "writesApprovalPacket", "writesApprovalRequest",
    "writesApprovalDecision", "writesCommitteeDecision", "writesFreezeAction",
    "writesWaesGateResult", "writesHarnessEvidence", "writesKdsLifecycle",
    "writesKdsFact", "writesKdsAcceptedFact", "writesExternalApi",
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
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewType": policy["delivery_types"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewStatus": policy["delivery_statuses"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewDecision": policy["delivery_decisions"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewScope": policy["delivery_scopes"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewChannel": policy["delivery_channels"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationSlaBreachNotificationAckEscalationDigestDeliveryPreviewBlockedAction": policy["blocked_actions"],
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
        "totalRecipientCount": 0, "totalChannelCount": 0,
        "totalBlockedDeliveryCount": 0, "createsDigestDeliveries": 0,
        "createsDeliveries": 0, "createsDigests": 0,
        "createsEscalations": 0, "createsTimeoutEvents": 0,
        "createsKweWorkItems": 0, "createsNotifications": 0,
        "createsAcknowledgements": 0, "createsReceipts": 0,
        "createsReadReceipts": 0, "updatesDeliveryStatuses": 0,
        "sendsExternalNotifications": 0, "createsApprovalAssignments": 0,
        "locksApprovers": 0, "createsApprovalPackets": 0,
        "createsApprovalRequests": 0, "createsApprovalDecisions": 0,
        "createsCommitteeDecisions": 0, "createsFreezeActions": 0,
        "createsHarnessEvidence": 0, "createsWaesGateResults": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    false_flags = (
        "createsDigestDelivery", "createsDelivery", "createsDigest",
        "createsEscalation", "createsTimeoutEvent", "createsKweWorkItem",
        "createsNotification", "createsAcknowledgement", "createsReceipt",
        "createsReadReceipt", "updatesDeliveryStatus", "sendsExternalNotification",
        "createsApprovalAssignment", "locksApprover", "createsApprovalPacket",
        "createsApprovalRequest", "createsApprovalDecision", "createsCommitteeDecision",
        "createsFreezeAction", "createsHarnessEvidence", "createsWaesGateResult",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsDigestDelivery": "createsDigestDeliveries",
        "createsDelivery": "createsDeliveries",
        "createsDigest": "createsDigests",
        "createsEscalation": "createsEscalations",
        "createsTimeoutEvent": "createsTimeoutEvents",
        "createsKweWorkItem": "createsKweWorkItems",
        "createsNotification": "createsNotifications",
        "createsAcknowledgement": "createsAcknowledgements",
        "createsReceipt": "createsReceipts",
        "createsReadReceipt": "createsReadReceipts",
        "updatesDeliveryStatus": "updatesDeliveryStatuses",
        "sendsExternalNotification": "sendsExternalNotifications",
        "createsApprovalAssignment": "createsApprovalAssignments",
        "locksApprover": "locksApprovers",
        "createsApprovalPacket": "createsApprovalPackets",
        "createsApprovalRequest": "createsApprovalRequests",
        "createsApprovalDecision": "createsApprovalDecisions",
        "createsCommitteeDecision": "createsCommitteeDecisions",
        "createsFreezeAction": "createsFreezeActions",
        "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults",
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
        if (
            not preview["escalationPreviewRefs"]
            or not preview["acknowledgementPreviewRefs"]
            or not preview["notificationPreviewRefs"]
            or not preview["routingQueuePreviewRefs"]
            or not preview["approvalPacketPreviewRefs"]
        ):
            failures.append(f"{preview_id}: upstream lineage refs are required")
        if not preview["candidateRecipientRefs"] or not preview["candidateChannelRefs"]:
            failures.append(f"{preview_id}: candidateRecipientRefs and candidateChannelRefs are required")
        if not set(preview["candidateChannelRefs"]) <= delivery_channels:
            failures.append(f"{preview_id}: candidateChannelRefs must be declared delivery channels")
        if preview["blockedDeliveryCount"] < 0 or preview["blockedDeliveryCount"] > len(preview["candidateRecipientRefs"]):
            failures.append(f"{preview_id}: blockedDeliveryCount must be between 0 and candidateRecipientRefs length")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["deliverySummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, deliverySummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
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
        print("gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_sla_breach_notification_ack_escalation_digest_delivery_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_sla_breach_notification_ack_escalation_digest_delivery_preview=pass "
        f"deliveries={actual['deliveryPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_recipients={actual['totalRecipientCount']} "
        f"total_channels={actual['totalChannelCount']} total_blocked_delivery={actual['totalBlockedDeliveryCount']} "
        f"creates_digest_deliveries={actual['createsDigestDeliveries']} creates_deliveries={actual['createsDeliveries']} "
        f"creates_digests={actual['createsDigests']} creates_escalations={actual['createsEscalations']} "
        f"creates_timeout_events={actual['createsTimeoutEvents']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"creates_notifications={actual['createsNotifications']} creates_acknowledgements={actual['createsAcknowledgements']} "
        f"creates_receipts={actual['createsReceipts']} creates_read_receipts={actual['createsReadReceipts']} "
        f"updates_delivery_statuses={actual['updatesDeliveryStatuses']} sends_external_notifications={actual['sendsExternalNotifications']} "
        f"creates_approval_assignments={actual['createsApprovalAssignments']} locks_approvers={actual['locksApprovers']} "
        f"creates_approval_packets={actual['createsApprovalPackets']} creates_approval_requests={actual['createsApprovalRequests']} "
        f"creates_approval_decisions={actual['createsApprovalDecisions']} creates_committee_decisions={actual['createsCommitteeDecisions']} "
        f"creates_freeze_actions={actual['createsFreezeActions']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_digest_delivery=0 writes_delivery=0 "
        "writes_digest=0 writes_escalation=0 writes_timeout_event=0 writes_kwe_work_item=0 writes_notification=0 "
        "writes_acknowledgement=0 writes_receipt=0 writes_read_receipt=0 writes_delivery_status=0 "
        "writes_approval_assignment=0 writes_approval_lock=0 writes_approval_packet=0 writes_approval_request=0 "
        "writes_approval_decision=0 writes_committee_decision=0 writes_freeze_action=0 writes_waes_gate_result=0 "
        "writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
