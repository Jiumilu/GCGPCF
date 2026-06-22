#!/usr/bin/env python3
"""Validate GFIS Assistant delivery acknowledgement escalation SLA preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-escalation-sla-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-escalation-sla-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-escalation-sla-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesSlaTimer", "writesEscalation", "writesReminder",
    "writesEscalationTask", "writesDeliveryAcknowledgement",
    "writesApprovalRequest", "writesApprovalDecision", "writesWaesGateResult",
    "writesKweWorkItem", "writesHarnessEvidence", "writesKdsLifecycle",
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
    previews: list[dict[str, Any]] = fixture["slaPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewType": policy["sla_types"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewStatus": policy["sla_statuses"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewDecision": policy["sla_decisions"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewScope": policy["sla_scopes"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewRisk": policy["sla_risks"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewReason": policy["sla_reasons"],
        "GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementEscalationSlaPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    sla_reasons = set(policy["sla_reasons"])
    sla_risks = set(policy["sla_risks"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "totalEscalationOwnerCount": 0, "totalSlaReasonCount": 0,
        "totalBlockedSlaEscalationCount": 0, "totalOverdueMinutes": 0,
        "createsSlaTimers": 0, "createsEscalations": 0,
        "createsReminders": 0, "createsEscalationTasks": 0,
        "createsDeliveryAcknowledgements": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    false_flags = (
        "createsSlaTimer", "createsEscalation", "createsReminder",
        "createsEscalationTask", "createsDeliveryAcknowledgement",
        "createsApprovalRequest", "createsApprovalDecision",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsSlaTimer": "createsSlaTimers",
        "createsEscalation": "createsEscalations",
        "createsReminder": "createsReminders",
        "createsEscalationTask": "createsEscalationTasks",
        "createsDeliveryAcknowledgement": "createsDeliveryAcknowledgements",
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
        preview_id = preview["slaPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if not set(preview["escalationPreviewRefs"]) <= set(preview["sourceEscalationPreviewRefs"]):
            failures.append(f"{preview_id}: escalationPreviewRefs must be included in sourceEscalationPreviewRefs")
        if not preview["deliveryAcknowledgementPreviewRefs"]:
            failures.append(f"{preview_id}: deliveryAcknowledgementPreviewRefs are required")
        if not preview["candidateEscalationOwnerRefs"] or not preview["slaReasonRefs"]:
            failures.append(f"{preview_id}: candidateEscalationOwnerRefs and slaReasonRefs are required")
        if not set(preview["slaReasonRefs"]) <= sla_reasons:
            failures.append(f"{preview_id}: slaReasonRefs must be declared SLA reasons")
        if preview["slaRisk"] not in sla_risks:
            failures.append(f"{preview_id}: slaRisk must be declared")
        if preview["remainingMinutes"] != max(preview["slaWindowMinutes"] - preview["elapsedMinutes"], 0):
            failures.append(f"{preview_id}: remainingMinutes must equal max(slaWindowMinutes - elapsedMinutes, 0)")
        if preview["overdueMinutes"] != max(preview["elapsedMinutes"] - preview["slaWindowMinutes"], 0):
            failures.append(f"{preview_id}: overdueMinutes must equal max(elapsedMinutes - slaWindowMinutes, 0)")
        if preview["blockedSlaEscalationCount"] < 0 or preview["blockedSlaEscalationCount"] > len(preview["candidateEscalationOwnerRefs"]):
            failures.append(f"{preview_id}: blockedSlaEscalationCount must be between 0 and candidateEscalationOwnerRefs length")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["slaSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, slaSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalEscalationOwnerCount"] += len(preview["candidateEscalationOwnerRefs"])
        counts["totalSlaReasonCount"] += len(preview["slaReasonRefs"])
        counts["totalBlockedSlaEscalationCount"] += preview["blockedSlaEscalationCount"]
        counts["totalOverdueMinutes"] += preview["overdueMinutes"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"slaPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_digest_delivery_acknowledgement_escalation_sla_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_digest_delivery_acknowledgement_escalation_sla_preview=pass "
        f"slas={actual['slaPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_escalation_owners={actual['totalEscalationOwnerCount']} "
        f"total_sla_reasons={actual['totalSlaReasonCount']} total_blocked_sla_escalation={actual['totalBlockedSlaEscalationCount']} "
        f"total_overdue_minutes={actual['totalOverdueMinutes']} creates_sla_timers={actual['createsSlaTimers']} "
        f"creates_escalations={actual['createsEscalations']} creates_reminders={actual['createsReminders']} "
        f"creates_escalation_tasks={actual['createsEscalationTasks']} creates_delivery_acknowledgements={actual['createsDeliveryAcknowledgements']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_sla_timer=0 writes_escalation=0 writes_reminder=0 writes_escalation_task=0 "
        "writes_delivery_acknowledgement=0 writes_approval_request=0 writes_approval_decision=0 "
        "writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
