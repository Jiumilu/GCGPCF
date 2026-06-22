#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-265 digest delivery preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-265-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-264-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks265AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesDigestDelivery', 'writesDelivery', 'writesDigest', 'writesEscalation', 'writesTimeoutEvent', 'writesKweWorkItem', 'writesNotification', 'writesAcknowledgement', 'writesReceipt', 'writesReadReceipt', 'writesDeliveryStatus', 'writesApprovalAssignment', 'writesApprovalLock', 'writesApprovalPacket', 'writesApprovalRequest', 'writesApprovalDecision', 'writesCommitteeDecision', 'writesFreezeAction', 'writesWaesGateResult', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["digestPreviews"]
    upstream_ids = {item["digestPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["deliveryPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["delivery_types"],
        f"{TYPE_PREFIX}Status": policy["delivery_statuses"],
        f"{TYPE_PREFIX}Decision": policy["delivery_decisions"],
        f"{TYPE_PREFIX}Scope": policy["delivery_scopes"],
        f"{TYPE_PREFIX}Channel": policy["delivery_channels"],
        f"{TYPE_PREFIX}Priority": policy["delivery_priorities"],
        f"{TYPE_PREFIX}Reason": policy["delivery_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    delivery_reasons = set(policy["delivery_reasons"])
    delivery_channels = set(policy["delivery_channels"])
    delivery_priorities = set(policy["delivery_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "totalCandidateRecipientCount": 0,
        "totalCandidateChannelCount": 0,
        "totalRequiredEvidenceCount": 0,
        "totalDeliveryReasonCount": 0,
        "totalBlockedDeliveryCount": 0,
        "createsDigestDeliveries": 0,
        "createsDeliveries": 0,
        "createsDigests": 0,
        "createsEscalations": 0,
        "createsTimeoutEvents": 0,
        "createsKweWorkItems": 0,
        "createsNotifications": 0,
        "createsAcknowledgements": 0,
        "createsReceipts": 0,
        "createsReadReceipts": 0,
        "updatesDeliveryStatus": 0,
        "sendsExternalNotifications": 0,
        "createsApprovalAssignments": 0,
        "locksApprovers": 0,
        "createsApprovalPackets": 0,
        "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0,
        "createsCommitteeDecisions": 0,
        "createsFreezeActions": 0,
        "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0,
        "persistsEvidence": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    false_flags = ('createsDigestDelivery', 'createsDelivery', 'createsDigest', 'createsEscalation', 'createsTimeoutEvent', 'createsKweWorkItem', 'createsNotification', 'createsAcknowledgement', 'createsReceipt', 'createsReadReceipt', 'updatesDeliveryStatus', 'sendsExternalNotification', 'createsApprovalAssignment', 'locksApprover', 'createsApprovalPacket', 'createsApprovalRequest', 'createsApprovalDecision', 'createsCommitteeDecision', 'createsFreezeAction', 'createsHarnessEvidence', 'createsWaesGateResult', 'persistsEvidence', 'approvesBusinessWrite', 'promotesLifecycle', 'completesCommitteeDecision')
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
        preview_id = preview["deliveryPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["digestPreviewRefs"] != preview["sourceDigestPreviewRefs"]:
            failures.append(f"{preview_id}: digestPreviewRefs must equal sourceDigestPreviewRefs")
        if not set(preview["digestPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: digestPreviewRefs must come from DKS-264 upstream")
        if not preview["escalationPreviewRefs"] or not preview["acknowledgementPreviewRefs"] or not preview["notificationPreviewRefs"]:
            failures.append(f"{preview_id}: escalation, acknowledgement, and notification refs are required")
        if not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: routing queue and approval packet refs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateRecipientRefs"] or not preview["candidateChannelRefs"] or not preview["deliveryReasonRefs"]:
            failures.append(f"{preview_id}: candidateRecipientRefs, candidateChannelRefs, and deliveryReasonRefs are required")
        if preview["blockedDeliveryCount"] < 0 or preview["blockedDeliveryCount"] > len(preview["candidateRecipientRefs"]):
            failures.append(f"{preview_id}: blockedDeliveryCount must be between 0 and candidateRecipientRefs length")
        if not set(preview["deliveryReasonRefs"]) <= delivery_reasons:
            failures.append(f"{preview_id}: deliveryReasonRefs must be declared")
        if not set(preview["candidateChannelRefs"]) <= delivery_channels:
            failures.append(f"{preview_id}: candidateChannelRefs must be declared")
        if preview["deliveryPriority"] not in delivery_priorities:
            failures.append(f"{preview_id}: deliveryPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["deliverySummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, deliverySummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalCandidateRecipientCount"] += len(preview["candidateRecipientRefs"])
        counts["totalCandidateChannelCount"] += len(preview["candidateChannelRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalDeliveryReasonCount"] += len(preview["deliveryReasonRefs"])
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
        print("gfis_assistant_dks_265_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_265_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_preview=pass "
        f"deliveries={actual['deliveryPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_delivery_channels={actual['totalCandidateChannelCount']} "
        f"total_delivery_recipients={actual['totalCandidateRecipientCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_delivery_reasons={actual['totalDeliveryReasonCount']} total_blocked_deliveries={actual['totalBlockedDeliveryCount']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_digest_delivery=0 writes_delivery=0 "
        "writes_digest=0 writes_escalation=0 writes_timeout_event=0 writes_kwe_work_item=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
