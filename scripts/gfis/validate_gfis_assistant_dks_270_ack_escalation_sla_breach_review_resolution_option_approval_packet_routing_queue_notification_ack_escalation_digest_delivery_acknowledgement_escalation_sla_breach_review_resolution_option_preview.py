#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-270 breach review resolution option preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-270-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks270AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesResolution', 'writesDisputeUpdate', 'writesCommitteeDecision', 'writesFreezeAction', 'writesApprovalRequest', 'writesApprovalDecision', 'writesWaesGateResult', 'writesKweWorkItem', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["breachReviewPreviews"]
    upstream_ids = {item["breachReviewPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["resolutionOptionPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["resolution_option_types"],
        f"{TYPE_PREFIX}Status": policy["resolution_option_statuses"],
        f"{TYPE_PREFIX}Decision": policy["resolution_option_decisions"],
        f"{TYPE_PREFIX}Scope": policy["resolution_option_scopes"],
        f"{TYPE_PREFIX}Priority": policy["resolution_priorities"],
        f"{TYPE_PREFIX}Reason": policy["resolution_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    resolution_reasons = set(policy["resolution_reasons"])
    priorities = set(policy["resolution_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {"brainSurface":0,"pkcSurface":0,"gfisAssistantSurface":0,"totalAssigneeCount":0,"totalRequiredEvidenceCount":0,"totalResolutionReasonCount":0,"totalBlockedResolutionCount":0,"createsResolutions":0,"createsDisputeUpdates":0,"createsCommitteeDecisions":0,"createsFreezeActions":0,"createsApprovalRequests":0,"createsApprovalDecisions":0,"createsHarnessEvidence":0,"createsWaesGateResults":0,"createsKweWorkItems":0,"persistsEvidence":0,"approvesBusinessWrite":0,"promotesLifecycle":0,"completesCommitteeDecision":0}
    surface_keys = {"brain":"brainSurface","pkc":"pkcSurface","gfis_assistant":"gfisAssistantSurface"}
    false_flags = ("createsResolution","createsDisputeUpdate","createsCommitteeDecision","createsFreezeAction","createsApprovalRequest","createsApprovalDecision","createsHarnessEvidence","createsWaesGateResult","createsKweWorkItem","persistsEvidence","approvesBusinessWrite","promotesLifecycle","completesCommitteeDecision")
    flag_count_keys = {"createsResolution":"createsResolutions","createsDisputeUpdate":"createsDisputeUpdates","createsCommitteeDecision":"createsCommitteeDecisions","createsFreezeAction":"createsFreezeActions","createsApprovalRequest":"createsApprovalRequests","createsApprovalDecision":"createsApprovalDecisions","createsHarnessEvidence":"createsHarnessEvidence","createsWaesGateResult":"createsWaesGateResults","createsKweWorkItem":"createsKweWorkItems","persistsEvidence":"persistsEvidence","approvesBusinessWrite":"approvesBusinessWrite","promotesLifecycle":"promotesLifecycle","completesCommitteeDecision":"completesCommitteeDecision"}
    for preview in previews:
        preview_id = preview["resolutionOptionPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["breachReviewPreviewRefs"] != preview["sourceBreachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: breachReviewPreviewRefs must equal sourceBreachReviewPreviewRefs")
        if not set(preview["breachReviewPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: breachReviewPreviewRefs must come from DKS-269 upstream")
        if not preview["slaPreviewRefs"] or not preview["escalationPreviewRefs"]:
            failures.append(f"{preview_id}: upstream SLA and escalation refs are required")
        if not preview["candidateAssigneeRefs"] or not preview["requiredEvidenceRefs"]:
            failures.append(f"{preview_id}: candidateAssigneeRefs and requiredEvidenceRefs are required")
        if preview["blockedResolutionCount"] < 0 or preview["blockedResolutionCount"] > len(preview["candidateAssigneeRefs"]):
            failures.append(f"{preview_id}: blockedResolutionCount must be between 0 and candidateAssigneeRefs length")
        if not set(preview["resolutionReasonRefs"]) <= resolution_reasons:
            failures.append(f"{preview_id}: resolutionReasonRefs must be declared resolution reasons")
        if preview["resolutionPriority"] not in priorities:
            failures.append(f"{preview_id}: resolutionPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["resolutionSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, resolutionSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalAssigneeCount"] += len(preview["candidateAssigneeRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalResolutionReasonCount"] += len(preview["resolutionReasonRefs"])
        counts["totalBlockedResolutionCount"] += preview["blockedResolutionCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value
    actual = {"resolutionOptionPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_270_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_270_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_preview=pass "
        f"resolution_options={actual['resolutionOptionPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_assignees={actual['totalAssigneeCount']} "
        f"total_required_evidence={actual['totalRequiredEvidenceCount']} total_reasons={actual['totalResolutionReasonCount']} "
        f"total_blocked_resolutions={actual['totalBlockedResolutionCount']} creates_resolutions=0 creates_dispute_updates=0 "
        "creates_committee_decisions=0 creates_freeze_actions=0 creates_approval_requests=0 creates_approval_decisions=0 "
        "creates_harness_evidence=0 creates_waes_gate_results=0 creates_kwe_work_items=0 writes_gfis=0 writes_gpc=0 "
        "writes_erp=0 writes_mes=0 writes_resolution=0 writes_dispute_update=0 writes_committee_decision=0 "
        "writes_freeze_action=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
