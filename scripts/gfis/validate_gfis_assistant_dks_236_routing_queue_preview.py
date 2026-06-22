#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-236 approval packet routing queue no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-dks-236-routing-queue-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-dks-236-routing-queue-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-236-routing-queue-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesRoutingQueue", "writesQueueItem", "writesApprovalAssignment",
    "writesApprovalLock", "writesApprovalPacket", "writesApprovalRequest",
    "writesApprovalDecision", "writesCommitteeDecision", "writesFreezeAction",
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
    previews: list[dict[str, Any]] = fixture["routingQueuePreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantDks236RoutingQueuePreviewType": policy["routing_queue_types"],
        "GfisAssistantDks236RoutingQueuePreviewStatus": policy["routing_queue_statuses"],
        "GfisAssistantDks236RoutingQueuePreviewDecision": policy["routing_queue_decisions"],
        "GfisAssistantDks236RoutingQueuePreviewScope": policy["routing_queue_scopes"],
        "GfisAssistantDks236RoutingQueuePreviewSlot": policy["routing_queue_slots"],
        "GfisAssistantDks236RoutingQueuePreviewPriority": policy["routing_queue_priorities"],
        "GfisAssistantDks236RoutingQueuePreviewReason": policy["queue_reasons"],
        "GfisAssistantDks236RoutingQueuePreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    queue_reasons = set(policy["queue_reasons"])
    queue_slots = set(policy["routing_queue_slots"])
    queue_priorities = set(policy["routing_queue_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "totalQueueSlotCount": 0, "totalCandidateAssigneeCount": 0,
        "totalRequiredEvidenceCount": 0, "totalQueueReasonCount": 0,
        "totalBlockedRouteCount": 0, "createsRoutingQueues": 0,
        "createsQueueItems": 0, "createsApprovalAssignments": 0,
        "locksApprovers": 0, "createsApprovalPackets": 0,
        "createsApprovalRequests": 0, "createsApprovalDecisions": 0,
        "createsCommitteeDecisions": 0, "createsFreezeActions": 0,
        "createsHarnessEvidence": 0, "createsWaesGateResults": 0,
        "createsKweWorkItems": 0, "persistsEvidence": 0,
        "approvesBusinessWrite": 0, "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    false_flags = (
        "createsRoutingQueue", "createsQueueItem", "createsApprovalAssignment",
        "locksApprover", "createsApprovalPacket", "createsApprovalRequest",
        "createsApprovalDecision", "createsCommitteeDecision", "createsFreezeAction",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsRoutingQueue": "createsRoutingQueues",
        "createsQueueItem": "createsQueueItems",
        "createsApprovalAssignment": "createsApprovalAssignments",
        "locksApprover": "locksApprovers",
        "createsApprovalPacket": "createsApprovalPackets",
        "createsApprovalRequest": "createsApprovalRequests",
        "createsApprovalDecision": "createsApprovalDecisions",
        "createsCommitteeDecision": "createsCommitteeDecisions",
        "createsFreezeAction": "createsFreezeActions",
        "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults",
        "createsKweWorkItem": "createsKweWorkItems",
        "persistsEvidence": "persistsEvidence",
        "approvesBusinessWrite": "approvesBusinessWrite",
        "promotesLifecycle": "promotesLifecycle",
        "completesCommitteeDecision": "completesCommitteeDecision",
    }

    for preview in previews:
        preview_id = preview["routingQueuePreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if not set(preview["approvalPacketPreviewRefs"]) <= set(preview["sourceApprovalPacketPreviewRefs"]):
            failures.append(f"{preview_id}: approvalPacketPreviewRefs must be included in source refs")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateAssigneeRefs"] or not preview["queueReasonRefs"]:
            failures.append(f"{preview_id}: candidateAssigneeRefs and queueReasonRefs are required")
        if preview["blockedRouteCount"] < 0 or preview["blockedRouteCount"] > len(preview["candidateAssigneeRefs"]):
            failures.append(f"{preview_id}: blockedRouteCount must be between 0 and candidateAssigneeRefs length")
        if not set(preview["queueReasonRefs"]) <= queue_reasons:
            failures.append(f"{preview_id}: queueReasonRefs must be declared")
        if preview["routingQueueSlot"] not in queue_slots:
            failures.append(f"{preview_id}: routingQueueSlot must be declared")
        if preview["routingQueuePriority"] not in queue_priorities:
            failures.append(f"{preview_id}: routingQueuePriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["routingSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, routingSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalQueueSlotCount"] += int(bool(preview["routingQueueSlot"]))
        counts["totalCandidateAssigneeCount"] += len(preview["candidateAssigneeRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalQueueReasonCount"] += len(preview["queueReasonRefs"])
        counts["totalBlockedRouteCount"] += preview["blockedRouteCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"routingQueuePreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_236_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_dks_236_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_preview=pass "
        f"routing_queues={actual['routingQueuePreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_queue_slots={actual['totalQueueSlotCount']} "
        f"total_assignees={actual['totalCandidateAssigneeCount']} total_required_evidence={actual['totalRequiredEvidenceCount']} "
        f"total_queue_reasons={actual['totalQueueReasonCount']} total_blocked_routes={actual['totalBlockedRouteCount']} "
        f"creates_routing_queues={actual['createsRoutingQueues']} creates_queue_items={actual['createsQueueItems']} "
        f"creates_approval_assignments={actual['createsApprovalAssignments']} locks_approvers={actual['locksApprovers']} "
        f"creates_approval_packets={actual['createsApprovalPackets']} creates_approval_requests={actual['createsApprovalRequests']} "
        f"creates_approval_decisions={actual['createsApprovalDecisions']} creates_committee_decisions={actual['createsCommitteeDecisions']} "
        f"creates_freeze_actions={actual['createsFreezeActions']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_routing_queue=0 writes_queue_item=0 "
        "writes_approval_assignment=0 writes_approval_lock=0 writes_approval_packet=0 writes_approval_request=0 "
        "writes_approval_decision=0 writes_committee_decision=0 writes_freeze_action=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
