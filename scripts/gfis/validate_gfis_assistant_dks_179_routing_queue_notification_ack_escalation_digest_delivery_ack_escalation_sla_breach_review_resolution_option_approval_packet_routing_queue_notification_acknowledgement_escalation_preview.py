#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-179 acknowledgement escalation preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-dks-179-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-dks-179-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-179-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
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
    previews: list[dict[str, Any]] = fixture["escalationPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewType": policy["escalation_types"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewStatus": policy["escalation_statuses"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewDecision": policy["escalation_decisions"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewScope": policy["escalation_scopes"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewLevel": policy["escalation_levels"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewTrigger": policy["escalation_triggers"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewReason": policy["escalation_reasons"],
        "GfisAssistantDks179RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    escalation_reasons = set(policy["escalation_reasons"])
    escalation_levels = set(policy["escalation_levels"])
    escalation_triggers = set(policy["escalation_triggers"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "totalEscalationLevelCount": 0,
        "totalCandidateEscalationRecipientCount": 0,
        "totalRequiredEvidenceCount": 0,
        "totalEscalationReasonCount": 0,
        "totalBlockedEscalationCount": 0,
        "createsEscalations": 0, "createsTimeoutEvents": 0,
        "createsKweWorkItems": 0, "createsNotifications": 0,
        "createsAcknowledgements": 0, "createsReceipts": 0,
        "createsReadReceipts": 0, "updatesDeliveryStatus": 0,
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
        "createsEscalation": "createsEscalations",
        "createsTimeoutEvent": "createsTimeoutEvents",
        "createsKweWorkItem": "createsKweWorkItems",
        "createsNotification": "createsNotifications",
        "createsAcknowledgement": "createsAcknowledgements",
        "createsReceipt": "createsReceipts",
        "createsReadReceipt": "createsReadReceipts",
        "updatesDeliveryStatus": "updatesDeliveryStatus",
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
        preview_id = preview["escalationPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if not set(preview["acknowledgementPreviewRefs"]) <= set(preview["sourceAcknowledgementPreviewRefs"]):
            failures.append(f"{preview_id}: acknowledgementPreviewRefs must be included in sourceAcknowledgementPreviewRefs")
        if not preview["notificationPreviewRefs"] or not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: notificationPreviewRefs, routingQueuePreviewRefs, and approvalPacketPreviewRefs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateEscalationRecipientRefs"] or not preview["escalationReasonRefs"]:
            failures.append(f"{preview_id}: candidateEscalationRecipientRefs and escalationReasonRefs are required")
        if preview["blockedEscalationCount"] < 0 or preview["blockedEscalationCount"] > len(preview["candidateEscalationRecipientRefs"]):
            failures.append(f"{preview_id}: blockedEscalationCount must be between 0 and candidateEscalationRecipientRefs length")
        if not set(preview["escalationReasonRefs"]) <= escalation_reasons:
            failures.append(f"{preview_id}: escalationReasonRefs must be declared")
        if preview["escalationLevel"] not in escalation_levels:
            failures.append(f"{preview_id}: escalationLevel must be declared")
        if preview["escalationTrigger"] not in escalation_triggers:
            failures.append(f"{preview_id}: escalationTrigger must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["escalationSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, escalationSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalEscalationLevelCount"] += int(bool(preview["escalationLevel"]))
        counts["totalCandidateEscalationRecipientCount"] += len(preview["candidateEscalationRecipientRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalEscalationReasonCount"] += len(preview["escalationReasonRefs"])
        counts["totalBlockedEscalationCount"] += preview["blockedEscalationCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"escalationPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_179_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_dks_179_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_preview=pass "
        f"escalations={actual['escalationPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_escalation_levels={actual['totalEscalationLevelCount']} "
        f"total_escalation_recipients={actual['totalCandidateEscalationRecipientCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_escalation_reasons={actual['totalEscalationReasonCount']} total_blocked_escalations={actual['totalBlockedEscalationCount']} "
        f"creates_escalations={actual['createsEscalations']} creates_timeout_events={actual['createsTimeoutEvents']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_notifications={actual['createsNotifications']} "
        f"creates_acknowledgements={actual['createsAcknowledgements']} creates_receipts={actual['createsReceipts']} "
        f"creates_read_receipts={actual['createsReadReceipts']} updates_delivery_status={actual['updatesDeliveryStatus']} "
        f"sends_external_notifications={actual['sendsExternalNotifications']} creates_approval_assignments={actual['createsApprovalAssignments']} "
        f"locks_approvers={actual['locksApprovers']} creates_approval_packets={actual['createsApprovalPackets']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_committee_decisions={actual['createsCommitteeDecisions']} creates_freeze_actions={actual['createsFreezeActions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_escalation=0 writes_timeout_event=0 "
        "writes_kwe_work_item=0 writes_notification=0 writes_acknowledgement=0 writes_receipt=0 "
        "writes_read_receipt=0 writes_delivery_status=0 writes_approval_assignment=0 writes_approval_lock=0 "
        "writes_approval_packet=0 writes_approval_request=0 writes_approval_decision=0 writes_committee_decision=0 "
        "writes_freeze_action=0 writes_waes_gate_result=0 writes_harness_evidence=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
