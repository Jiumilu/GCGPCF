#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-266 digest delivery acknowledgement preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-266-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-265-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks266AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAcknowledgementPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesDeliveryAcknowledgement', 'writesDigestDelivery', 'writesDelivery', 'writesDigest', 'writesEscalation', 'writesTimeoutEvent', 'writesKweWorkItem', 'writesNotification', 'writesAcknowledgement', 'writesReceipt', 'writesReadReceipt', 'writesDeliveryStatus', 'writesApprovalAssignment', 'writesApprovalLock', 'writesApprovalPacket', 'writesApprovalRequest', 'writesApprovalDecision', 'writesCommitteeDecision', 'writesFreezeAction', 'writesWaesGateResult', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["deliveryPreviews"]
    upstream_ids = {item["deliveryPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["deliveryAcknowledgementPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["acknowledgement_types"],
        f"{TYPE_PREFIX}Status": policy["acknowledgement_statuses"],
        f"{TYPE_PREFIX}Decision": policy["acknowledgement_decisions"],
        f"{TYPE_PREFIX}Scope": policy["acknowledgement_scopes"],
        f"{TYPE_PREFIX}Method": policy["acknowledgement_methods"],
        f"{TYPE_PREFIX}Priority": policy["acknowledgement_priorities"],
        f"{TYPE_PREFIX}Reason": policy["acknowledgement_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    methods = set(policy["acknowledgement_methods"])
    reasons = set(policy["acknowledgement_reasons"])
    priorities = set(policy["acknowledgement_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "totalAcknowledgerCount": 0,
        "totalAcknowledgementMethodCount": 0,
        "totalRequiredEvidenceCount": 0,
        "totalAcknowledgementReasonCount": 0,
        "totalBlockedAcknowledgementCount": 0,
        "createsDeliveryAcknowledgements": 0,
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
    false_flags = ('createsDeliveryAcknowledgement', 'createsDigestDelivery', 'createsDelivery', 'createsDigest', 'createsEscalation', 'createsTimeoutEvent', 'createsKweWorkItem', 'createsNotification', 'createsAcknowledgement', 'createsReceipt', 'createsReadReceipt', 'updatesDeliveryStatus', 'sendsExternalNotification', 'createsApprovalAssignment', 'locksApprover', 'createsApprovalPacket', 'createsApprovalRequest', 'createsApprovalDecision', 'createsCommitteeDecision', 'createsFreezeAction', 'createsHarnessEvidence', 'createsWaesGateResult', 'persistsEvidence', 'approvesBusinessWrite', 'promotesLifecycle', 'completesCommitteeDecision')
    flag_count_keys = {
        "createsDeliveryAcknowledgement": "createsDeliveryAcknowledgements",
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
        preview_id = preview["deliveryAcknowledgementPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["deliveryPreviewRefs"] != preview["sourceDeliveryPreviewRefs"]:
            failures.append(f"{preview_id}: deliveryPreviewRefs must equal sourceDeliveryPreviewRefs")
        if not set(preview["deliveryPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: deliveryPreviewRefs must come from DKS-265 upstream")
        if not preview["digestPreviewRefs"] or not preview["escalationPreviewRefs"] or not preview["acknowledgementPreviewRefs"] or not preview["notificationPreviewRefs"]:
            failures.append(f"{preview_id}: digest, escalation, acknowledgement, and notification refs are required")
        if not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: routing queue and approval packet refs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateAcknowledgerRefs"] or not preview["acknowledgementMethodRefs"] or not preview["acknowledgementReasonRefs"]:
            failures.append(f"{preview_id}: candidate acknowledgers, methods, and reasons are required")
        if preview["blockedAcknowledgementCount"] < 0 or preview["blockedAcknowledgementCount"] > len(preview["candidateAcknowledgerRefs"]):
            failures.append(f"{preview_id}: blockedAcknowledgementCount must be between 0 and candidateAcknowledgerRefs length")
        if not set(preview["acknowledgementMethodRefs"]) <= methods:
            failures.append(f"{preview_id}: acknowledgementMethodRefs must be declared")
        if not set(preview["acknowledgementReasonRefs"]) <= reasons:
            failures.append(f"{preview_id}: acknowledgementReasonRefs must be declared")
        if preview["acknowledgementPriority"] not in priorities:
            failures.append(f"{preview_id}: acknowledgementPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["acknowledgementSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, acknowledgementSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalAcknowledgerCount"] += len(preview["candidateAcknowledgerRefs"])
        counts["totalAcknowledgementMethodCount"] += len(preview["acknowledgementMethodRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalAcknowledgementReasonCount"] += len(preview["acknowledgementReasonRefs"])
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
    actual = {"deliveryAcknowledgementPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_266_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_266_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_preview=pass "
        f"delivery_acks={actual['deliveryAcknowledgementPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_acknowledgers={actual['totalAcknowledgerCount']} "
        f"total_methods={actual['totalAcknowledgementMethodCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_ack_reasons={actual['totalAcknowledgementReasonCount']} total_blocked_acknowledgements={actual['totalBlockedAcknowledgementCount']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_delivery_acknowledgement=0 "
        "writes_digest_delivery=0 writes_delivery=0 writes_digest=0 writes_escalation=0 writes_timeout_event=0 "
        "writes_kwe_work_item=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
