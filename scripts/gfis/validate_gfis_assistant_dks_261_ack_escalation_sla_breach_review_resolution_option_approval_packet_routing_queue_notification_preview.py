#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-261 routing queue notification preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-261-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks261AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesNotification', 'writesNotificationDelivery', 'writesMessage', 'writesInboxItem', 'writesRoutingQueue', 'writesQueueItem', 'writesApprovalAssignment', 'writesApprovalLock', 'writesApprovalPacket', 'writesApprovalRequest', 'writesApprovalDecision', 'writesCommitteeDecision', 'writesFreezeAction', 'writesWaesGateResult', 'writesKweWorkItem', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["routingQueuePreviews"]
    upstream_ids = {item["routingQueuePreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["notificationPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["notification_types"],
        f"{TYPE_PREFIX}Status": policy["notification_statuses"],
        f"{TYPE_PREFIX}Decision": policy["notification_decisions"],
        f"{TYPE_PREFIX}Scope": policy["notification_scopes"],
        f"{TYPE_PREFIX}Channel": policy["notification_channels"],
        f"{TYPE_PREFIX}Priority": policy["notification_priorities"],
        f"{TYPE_PREFIX}Reason": policy["notification_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    notification_reasons = set(policy["notification_reasons"])
    notification_channels = set(policy["notification_channels"])
    notification_priorities = set(policy["notification_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {"brainSurface":0,"pkcSurface":0,"gfisAssistantSurface":0,"totalChannelCount":0,"totalCandidateRecipientCount":0,"totalRequiredEvidenceCount":0,"totalNotificationReasonCount":0,"totalBlockedNotificationCount":0,"createsNotifications":0,"createsNotificationDeliveries":0,"createsMessages":0,"createsInboxItems":0,"sendsExternalNotifications":0,"createsRoutingQueues":0,"createsQueueItems":0,"createsApprovalAssignments":0,"locksApprovers":0,"createsApprovalPackets":0,"createsApprovalRequests":0,"createsApprovalDecisions":0,"createsCommitteeDecisions":0,"createsFreezeActions":0,"createsHarnessEvidence":0,"createsWaesGateResults":0,"createsKweWorkItems":0,"persistsEvidence":0,"approvesBusinessWrite":0,"promotesLifecycle":0,"completesCommitteeDecision":0}
    surface_keys = {"brain":"brainSurface","pkc":"pkcSurface","gfis_assistant":"gfisAssistantSurface"}
    false_flags = ("createsNotification","createsNotificationDelivery","createsMessage","createsInboxItem","sendsExternalNotification","createsRoutingQueue","createsQueueItem","createsApprovalAssignment","locksApprover","createsApprovalPacket","createsApprovalRequest","createsApprovalDecision","createsCommitteeDecision","createsFreezeAction","createsHarnessEvidence","createsWaesGateResult","createsKweWorkItem","persistsEvidence","approvesBusinessWrite","promotesLifecycle","completesCommitteeDecision")
    flag_count_keys = {"createsNotification":"createsNotifications","createsNotificationDelivery":"createsNotificationDeliveries","createsMessage":"createsMessages","createsInboxItem":"createsInboxItems","sendsExternalNotification":"sendsExternalNotifications","createsRoutingQueue":"createsRoutingQueues","createsQueueItem":"createsQueueItems","createsApprovalAssignment":"createsApprovalAssignments","locksApprover":"locksApprovers","createsApprovalPacket":"createsApprovalPackets","createsApprovalRequest":"createsApprovalRequests","createsApprovalDecision":"createsApprovalDecisions","createsCommitteeDecision":"createsCommitteeDecisions","createsFreezeAction":"createsFreezeActions","createsHarnessEvidence":"createsHarnessEvidence","createsWaesGateResult":"createsWaesGateResults","createsKweWorkItem":"createsKweWorkItems","persistsEvidence":"persistsEvidence","approvesBusinessWrite":"approvesBusinessWrite","promotesLifecycle":"promotesLifecycle","completesCommitteeDecision":"completesCommitteeDecision"}
    for preview in previews:
        preview_id = preview["notificationPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["routingQueuePreviewRefs"] != preview["sourceRoutingQueuePreviewRefs"]:
            failures.append(f"{preview_id}: routingQueuePreviewRefs must equal sourceRoutingQueuePreviewRefs")
        if not set(preview["routingQueuePreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: routingQueuePreviewRefs must come from DKS-260 upstream")
        if not preview["approvalPacketPreviewRefs"] or not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: approvalPacketPreviewRefs, resolutionOptionPreviewRefs, and breachReviewPreviewRefs are required")
        if not preview["candidateRecipientRefs"] or not preview["notificationReasonRefs"]:
            failures.append(f"{preview_id}: candidateRecipientRefs and notificationReasonRefs are required")
        if preview["blockedNotificationCount"] < 0 or preview["blockedNotificationCount"] > len(preview["candidateRecipientRefs"]):
            failures.append(f"{preview_id}: blockedNotificationCount must be between 0 and candidateRecipientRefs length")
        if not set(preview["notificationReasonRefs"]) <= notification_reasons:
            failures.append(f"{preview_id}: notificationReasonRefs must be declared")
        if preview["notificationChannel"] not in notification_channels:
            failures.append(f"{preview_id}: notificationChannel must be declared")
        if preview["notificationPriority"] not in notification_priorities:
            failures.append(f"{preview_id}: notificationPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["notificationSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, notificationSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalChannelCount"] += int(bool(preview["notificationChannel"]))
        counts["totalCandidateRecipientCount"] += len(preview["candidateRecipientRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalNotificationReasonCount"] += len(preview["notificationReasonRefs"])
        counts["totalBlockedNotificationCount"] += preview["blockedNotificationCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
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
        print("gfis_assistant_dks_261_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_261_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_preview=pass "
        f"notifications={actual['notificationPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_channels={actual['totalChannelCount']} "
        f"total_recipients={actual['totalCandidateRecipientCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_notification_reasons={actual['totalNotificationReasonCount']} total_blocked_notifications={actual['totalBlockedNotificationCount']} "
        "creates_notifications=0 creates_notification_deliveries=0 creates_messages=0 creates_inbox_items=0 "
        "sends_external_notifications=0 creates_routing_queues=0 creates_queue_items=0 creates_approval_assignments=0 "
        "locks_approvers=0 creates_approval_packets=0 creates_approval_requests=0 creates_approval_decisions=0 "
        "creates_committee_decisions=0 creates_freeze_actions=0 creates_harness_evidence=0 creates_waes_gate_results=0 "
        "creates_kwe_work_items=0 writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_notification=0 "
        "writes_notification_delivery=0 writes_message=0 writes_inbox_item=0 writes_routing_queue=0 writes_queue_item=0 "
        "writes_approval_assignment=0 writes_approval_lock=0 writes_approval_packet=0 writes_approval_request=0 "
        "writes_approval_decision=0 writes_committee_decision=0 writes_freeze_action=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
