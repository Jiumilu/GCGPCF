#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-217 digest delivery preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-217-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks217RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryPreview"
NO_WRITE_KEYS = ("writesGfis", "writesGpc", "writesErp", "writesMes", "writesDigestDelivery", "writesDelivery", "writesDigest", "writesEscalation", "writesTimeoutEvent", "writesKweWorkItem", "writesNotification", "writesAcknowledgement", "writesReceipt", "writesReadReceipt", "writesDeliveryStatus", "writesApprovalAssignment", "writesApprovalLock", "writesApprovalPacket", "writesApprovalRequest", "writesApprovalDecision", "writesCommitteeDecision", "writesFreezeAction", "writesWaesGateResult", "writesHarnessEvidence", "writesKdsLifecycle", "writesKdsFact", "writesKdsAcceptedFact", "writesExternalApi")

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
    unions = {f"{TYPE_PREFIX}Type": policy["delivery_types"], f"{TYPE_PREFIX}Status": policy["delivery_statuses"], f"{TYPE_PREFIX}Decision": policy["delivery_decisions"], f"{TYPE_PREFIX}Scope": policy["delivery_scopes"], f"{TYPE_PREFIX}Channel": policy["delivery_channels"], f"{TYPE_PREFIX}Priority": policy["delivery_priorities"], f"{TYPE_PREFIX}Reason": policy["delivery_reasons"], f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"]}
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    channels = set(policy["delivery_channels"])
    reasons = set(policy["delivery_reasons"])
    priorities = set(policy["delivery_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {"brainSurface":0,"pkcSurface":0,"gfisAssistantSurface":0,"totalCandidateRecipientCount":0,"totalCandidateChannelCount":0,"totalRequiredEvidenceCount":0,"totalDeliveryReasonCount":0,"totalBlockedDeliveryCount":0,"createsDigestDeliveries":0,"createsDeliveries":0,"createsDigests":0,"createsEscalations":0,"createsTimeoutEvents":0,"createsKweWorkItems":0,"createsNotifications":0,"createsAcknowledgements":0,"createsReceipts":0,"createsReadReceipts":0,"updatesDeliveryStatus":0,"sendsExternalNotifications":0,"createsApprovalAssignments":0,"locksApprovers":0,"createsApprovalPackets":0,"createsApprovalRequests":0,"createsApprovalDecisions":0,"createsCommitteeDecisions":0,"createsFreezeActions":0,"createsHarnessEvidence":0,"createsWaesGateResults":0,"persistsEvidence":0,"approvesBusinessWrite":0,"promotesLifecycle":0,"completesCommitteeDecision":0}
    surface_keys = {"brain":"brainSurface","pkc":"pkcSurface","gfis_assistant":"gfisAssistantSurface"}
    false_flags = ("createsDigestDelivery","createsDelivery","createsDigest","createsEscalation","createsTimeoutEvent","createsKweWorkItem","createsNotification","createsAcknowledgement","createsReceipt","createsReadReceipt","updatesDeliveryStatus","sendsExternalNotification","createsApprovalAssignment","locksApprover","createsApprovalPacket","createsApprovalRequest","createsApprovalDecision","createsCommitteeDecision","createsFreezeAction","createsHarnessEvidence","createsWaesGateResult","persistsEvidence","approvesBusinessWrite","promotesLifecycle","completesCommitteeDecision")
    flag_count_keys = {"createsDigestDelivery":"createsDigestDeliveries","createsDelivery":"createsDeliveries","createsDigest":"createsDigests","createsEscalation":"createsEscalations","createsTimeoutEvent":"createsTimeoutEvents","createsKweWorkItem":"createsKweWorkItems","createsNotification":"createsNotifications","createsAcknowledgement":"createsAcknowledgements","createsReceipt":"createsReceipts","createsReadReceipt":"createsReadReceipts","updatesDeliveryStatus":"updatesDeliveryStatus","sendsExternalNotification":"sendsExternalNotifications","createsApprovalAssignment":"createsApprovalAssignments","locksApprover":"locksApprovers","createsApprovalPacket":"createsApprovalPackets","createsApprovalRequest":"createsApprovalRequests","createsApprovalDecision":"createsApprovalDecisions","createsCommitteeDecision":"createsCommitteeDecisions","createsFreezeAction":"createsFreezeActions","createsHarnessEvidence":"createsHarnessEvidence","createsWaesGateResult":"createsWaesGateResults","persistsEvidence":"persistsEvidence","approvesBusinessWrite":"approvesBusinessWrite","promotesLifecycle":"promotesLifecycle","completesCommitteeDecision":"completesCommitteeDecision"}
    for preview in previews:
        preview_id = preview["deliveryPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if not set(preview["digestPreviewRefs"]) <= set(preview["sourceDigestPreviewRefs"]):
            failures.append(f"{preview_id}: digestPreviewRefs must be included in sourceDigestPreviewRefs")
        if not preview["escalationPreviewRefs"] or not preview["acknowledgementPreviewRefs"] or not preview["notificationPreviewRefs"] or not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: upstream preview refs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateRecipientRefs"] or not preview["candidateChannelRefs"] or not preview["deliveryReasonRefs"]:
            failures.append(f"{preview_id}: candidate recipients, channels, and reasons are required")
        if preview["blockedDeliveryCount"] < 0 or preview["blockedDeliveryCount"] > len(preview["candidateRecipientRefs"]):
            failures.append(f"{preview_id}: blockedDeliveryCount must be between 0 and candidateRecipientRefs length")
        if not set(preview["candidateChannelRefs"]) <= channels:
            failures.append(f"{preview_id}: candidateChannelRefs must be declared")
        if not set(preview["deliveryReasonRefs"]) <= reasons:
            failures.append(f"{preview_id}: deliveryReasonRefs must be declared")
        if preview["deliveryPriority"] not in priorities:
            failures.append(f"{preview_id}: deliveryPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
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
        print("gfis_assistant_dks_217_routing_queue_notification_ack_escalation_digest_delivery_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print("gfis_assistant_dks_217_routing_queue_notification_ack_escalation_digest_delivery_preview=pass " f"deliveries={actual['deliveryPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} gfis_assistant={actual['gfisAssistantSurface']} total_recipients={actual['totalCandidateRecipientCount']} total_channels={actual['totalCandidateChannelCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} total_delivery_reasons={actual['totalDeliveryReasonCount']} total_blocked_deliveries={actual['totalBlockedDeliveryCount']} creates_digest_deliveries={actual['createsDigestDeliveries']} creates_deliveries={actual['createsDeliveries']} creates_digests={actual['createsDigests']} creates_escalations={actual['createsEscalations']} creates_timeout_events={actual['createsTimeoutEvents']} creates_kwe_work_items={actual['createsKweWorkItems']} creates_notifications={actual['createsNotifications']} creates_acknowledgements={actual['createsAcknowledgements']} creates_receipts={actual['createsReceipts']} creates_read_receipts={actual['createsReadReceipts']} updates_delivery_status={actual['updatesDeliveryStatus']} sends_external_notifications={actual['sendsExternalNotifications']} creates_approval_assignments={actual['createsApprovalAssignments']} locks_approvers={actual['locksApprovers']} creates_approval_packets={actual['createsApprovalPackets']} creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} creates_committee_decisions={actual['createsCommitteeDecisions']} creates_freeze_actions={actual['createsFreezeActions']} creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_digest_delivery=0 writes_delivery=0 writes_digest=0 writes_escalation=0 writes_timeout_event=0 writes_kwe_work_item=0 writes_notification=0 writes_acknowledgement=0 writes_receipt=0 writes_read_receipt=0 writes_delivery_status=0 writes_approval_assignment=0 writes_approval_lock=0 writes_approval_packet=0 writes_approval_request=0 writes_approval_decision=0 writes_committee_decision=0 writes_freeze_action=0 writes_waes_gate_result=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
