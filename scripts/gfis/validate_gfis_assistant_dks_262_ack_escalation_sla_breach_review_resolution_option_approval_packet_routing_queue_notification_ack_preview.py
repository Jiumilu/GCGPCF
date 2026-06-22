#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-262 routing queue notification acknowledgement no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-262-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks262AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckPreview"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesAcknowledgement", "writesReceipt", "writesReadReceipt",
    "writesDeliveryStatus", "writesNotification", "writesMessage",
    "writesInboxItem", "writesRoutingQueue", "writesQueueItem",
    "writesApprovalAssignment", "writesApprovalLock", "writesApprovalPacket",
    "writesApprovalRequest", "writesApprovalDecision", "writesCommitteeDecision",
    "writesFreezeAction", "writesWaesGateResult", "writesKweWorkItem",
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
        f"{TYPE_PREFIX}Type": policy["acknowledgement_types"],
        f"{TYPE_PREFIX}Status": policy["acknowledgement_statuses"],
        f"{TYPE_PREFIX}Decision": policy["acknowledgement_decisions"],
        f"{TYPE_PREFIX}Scope": policy["acknowledgement_scopes"],
        f"{TYPE_PREFIX}Channel": policy["acknowledgement_channels"],
        f"{TYPE_PREFIX}Deadline": policy["acknowledgement_deadlines"],
        f"{TYPE_PREFIX}Reason": policy["acknowledgement_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    acknowledgement_reasons = set(policy["acknowledgement_reasons"])
    acknowledgement_channels = set(policy["acknowledgement_channels"])
    acknowledgement_deadlines = set(policy["acknowledgement_deadlines"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "totalAcknowledgementChannelCount": 0, "totalCandidateAcknowledgerCount": 0,
        "totalRequiredEvidenceCount": 0, "totalAcknowledgementReasonCount": 0,
        "totalBlockedAcknowledgementCount": 0, "createsAcknowledgements": 0,
        "createsReceipts": 0, "createsReadReceipts": 0, "updatesDeliveryStatus": 0,
        "createsNotifications": 0, "createsMessages": 0, "createsInboxItems": 0,
        "sendsExternalNotifications": 0, "createsRoutingQueues": 0,
        "createsQueueItems": 0, "createsApprovalAssignments": 0, "locksApprovers": 0,
        "createsApprovalPackets": 0, "createsApprovalRequests": 0, "createsApprovalDecisions": 0,
        "createsCommitteeDecisions": 0, "createsFreezeActions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0, "persistsEvidence": 0,
        "approvesBusinessWrite": 0, "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    false_flags = (
        "createsAcknowledgement", "createsReceipt", "createsReadReceipt", "updatesDeliveryStatus",
        "createsNotification", "createsMessage", "createsInboxItem", "sendsExternalNotification",
        "createsRoutingQueue", "createsQueueItem", "createsApprovalAssignment", "locksApprover",
        "createsApprovalPacket", "createsApprovalRequest", "createsApprovalDecision", "createsCommitteeDecision",
        "createsFreezeAction", "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle", "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsAcknowledgement": "createsAcknowledgements", "createsReceipt": "createsReceipts",
        "createsReadReceipt": "createsReadReceipts", "updatesDeliveryStatus": "updatesDeliveryStatus",
        "createsNotification": "createsNotifications", "createsMessage": "createsMessages",
        "createsInboxItem": "createsInboxItems", "sendsExternalNotification": "sendsExternalNotifications",
        "createsRoutingQueue": "createsRoutingQueues", "createsQueueItem": "createsQueueItems",
        "createsApprovalAssignment": "createsApprovalAssignments", "locksApprover": "locksApprovers",
        "createsApprovalPacket": "createsApprovalPackets", "createsApprovalRequest": "createsApprovalRequests",
        "createsApprovalDecision": "createsApprovalDecisions", "createsCommitteeDecision": "createsCommitteeDecisions",
        "createsFreezeAction": "createsFreezeActions", "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults", "createsKweWorkItem": "createsKweWorkItems",
        "persistsEvidence": "persistsEvidence", "approvesBusinessWrite": "approvesBusinessWrite",
        "promotesLifecycle": "promotesLifecycle", "completesCommitteeDecision": "completesCommitteeDecision",
    }

    for preview in previews:
        preview_id = preview["acknowledgementPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if not set(preview["notificationPreviewRefs"]) <= set(preview["sourceNotificationPreviewRefs"]):
            failures.append(f"{preview_id}: notificationPreviewRefs must be included in sourceNotificationPreviewRefs")
        if not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: routingQueuePreviewRefs and approvalPacketPreviewRefs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateAcknowledgerRefs"] or not preview["acknowledgementReasonRefs"]:
            failures.append(f"{preview_id}: candidateAcknowledgerRefs and acknowledgementReasonRefs are required")
        if preview["blockedAcknowledgementCount"] < 0 or preview["blockedAcknowledgementCount"] > len(preview["candidateAcknowledgerRefs"]):
            failures.append(f"{preview_id}: blockedAcknowledgementCount must be between 0 and candidateAcknowledgerRefs length")
        if not set(preview["acknowledgementReasonRefs"]) <= acknowledgement_reasons:
            failures.append(f"{preview_id}: acknowledgementReasonRefs must be declared")
        if preview["acknowledgementChannel"] not in acknowledgement_channels:
            failures.append(f"{preview_id}: acknowledgementChannel must be declared")
        if preview["acknowledgementDeadline"] not in acknowledgement_deadlines:
            failures.append(f"{preview_id}: acknowledgementDeadline must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["acknowledgementSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, acknowledgementSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalAcknowledgementChannelCount"] += int(bool(preview["acknowledgementChannel"]))
        counts["totalCandidateAcknowledgerCount"] += len(preview["candidateAcknowledgerRefs"])
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
        print("gfis_assistant_dks_262_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_dks_262_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_preview=pass "
        f"acknowledgements={actual['acknowledgementPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_ack_channels={actual['totalAcknowledgementChannelCount']} "
        f"total_acknowledgers={actual['totalCandidateAcknowledgerCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_ack_reasons={actual['totalAcknowledgementReasonCount']} total_blocked_acknowledgements={actual['totalBlockedAcknowledgementCount']} "
        f"creates_acknowledgements={actual['createsAcknowledgements']} creates_receipts={actual['createsReceipts']} "
        f"creates_read_receipts={actual['createsReadReceipts']} updates_delivery_status={actual['updatesDeliveryStatus']} "
        f"creates_notifications={actual['createsNotifications']} creates_messages={actual['createsMessages']} "
        f"creates_inbox_items={actual['createsInboxItems']} sends_external_notifications={actual['sendsExternalNotifications']} "
        f"creates_routing_queues={actual['createsRoutingQueues']} creates_queue_items={actual['createsQueueItems']} "
        f"creates_approval_assignments={actual['createsApprovalAssignments']} locks_approvers={actual['locksApprovers']} "
        f"creates_approval_packets={actual['createsApprovalPackets']} creates_approval_requests={actual['createsApprovalRequests']} "
        f"creates_approval_decisions={actual['createsApprovalDecisions']} creates_committee_decisions={actual['createsCommitteeDecisions']} "
        f"creates_freeze_actions={actual['createsFreezeActions']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_acknowledgement=0 writes_receipt=0 "
        "writes_read_receipt=0 writes_delivery_status=0 writes_notification=0 writes_message=0 writes_inbox_item=0 "
        "writes_routing_queue=0 writes_queue_item=0 writes_approval_assignment=0 writes_approval_lock=0 "
        "writes_approval_packet=0 writes_approval_request=0 writes_approval_decision=0 writes_committee_decision=0 "
        "writes_freeze_action=0 writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
