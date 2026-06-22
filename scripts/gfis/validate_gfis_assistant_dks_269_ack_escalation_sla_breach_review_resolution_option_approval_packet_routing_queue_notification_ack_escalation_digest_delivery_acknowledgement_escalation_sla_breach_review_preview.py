#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-269 SLA breach review preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-268-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks269AckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesBreachRecord', 'writesDispute', 'writesCommitteeCase', 'writesFreezeRequest', 'writesReminder', 'writesApprovalRequest', 'writesApprovalDecision', 'writesWaesGateResult', 'writesKweWorkItem', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["slaPreviews"]
    upstream_ids = {item["slaPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["breachReviewPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["breach_review_types"],
        f"{TYPE_PREFIX}Status": policy["breach_review_statuses"],
        f"{TYPE_PREFIX}Decision": policy["breach_review_decisions"],
        f"{TYPE_PREFIX}Scope": policy["breach_review_scopes"],
        f"{TYPE_PREFIX}Severity": policy["breach_severities"],
        f"{TYPE_PREFIX}Reason": policy["breach_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    breach_reasons = set(policy["breach_reasons"])
    severities = set(policy["breach_severities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {"brainSurface":0,"pkcSurface":0,"gfisAssistantSurface":0,"totalReviewerCount":0,"totalEvidenceGapCount":0,"totalBreachReasonCount":0,"totalBlockedReviewCount":0,"totalOverdueMinutes":0,"createsBreachRecords":0,"createsDisputes":0,"createsCommitteeCases":0,"createsFreezeRequests":0,"createsReminders":0,"createsApprovalRequests":0,"createsApprovalDecisions":0,"createsHarnessEvidence":0,"createsWaesGateResults":0,"createsKweWorkItems":0,"persistsEvidence":0,"approvesBusinessWrite":0,"promotesLifecycle":0,"completesCommitteeDecision":0}
    surface_keys = {"brain":"brainSurface","pkc":"pkcSurface","gfis_assistant":"gfisAssistantSurface"}
    false_flags = ("createsBreachRecord","createsDispute","createsCommitteeCase","createsFreezeRequest","createsReminder","createsApprovalRequest","createsApprovalDecision","createsHarnessEvidence","createsWaesGateResult","createsKweWorkItem","persistsEvidence","approvesBusinessWrite","promotesLifecycle","completesCommitteeDecision")
    flag_count_keys = {"createsBreachRecord":"createsBreachRecords","createsDispute":"createsDisputes","createsCommitteeCase":"createsCommitteeCases","createsFreezeRequest":"createsFreezeRequests","createsReminder":"createsReminders","createsApprovalRequest":"createsApprovalRequests","createsApprovalDecision":"createsApprovalDecisions","createsHarnessEvidence":"createsHarnessEvidence","createsWaesGateResult":"createsWaesGateResults","createsKweWorkItem":"createsKweWorkItems","persistsEvidence":"persistsEvidence","approvesBusinessWrite":"approvesBusinessWrite","promotesLifecycle":"promotesLifecycle","completesCommitteeDecision":"completesCommitteeDecision"}
    for preview in previews:
        preview_id = preview["breachReviewPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["slaPreviewRefs"] != preview["sourceSlaPreviewRefs"]:
            failures.append(f"{preview_id}: slaPreviewRefs must equal sourceSlaPreviewRefs")
        if not set(preview["slaPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: slaPreviewRefs must come from DKS-268 upstream")
        if not preview["escalationPreviewRefs"] or not preview["deliveryAcknowledgementPreviewRefs"] or not preview["deliveryPreviewRefs"] or not preview["digestPreviewRefs"]:
            failures.append(f"{preview_id}: upstream preview refs are required")
        if not preview["candidateReviewerRefs"] or not preview["breachReasonRefs"]:
            failures.append(f"{preview_id}: candidateReviewerRefs and breachReasonRefs are required")
        if preview["blockedReviewCount"] < 0 or preview["blockedReviewCount"] > len(preview["candidateReviewerRefs"]):
            failures.append(f"{preview_id}: blockedReviewCount must be between 0 and candidateReviewerRefs length")
        if preview["overdueMinutes"] < 0:
            failures.append(f"{preview_id}: overdueMinutes must be non-negative")
        if not set(preview["breachReasonRefs"]) <= breach_reasons:
            failures.append(f"{preview_id}: breachReasonRefs must be declared breach reasons")
        if preview["breachSeverity"] not in severities:
            failures.append(f"{preview_id}: breachSeverity must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["breachSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, breachSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalReviewerCount"] += len(preview["candidateReviewerRefs"])
        counts["totalEvidenceGapCount"] += len(preview["evidenceGapRefs"])
        counts["totalBreachReasonCount"] += len(preview["breachReasonRefs"])
        counts["totalBlockedReviewCount"] += preview["blockedReviewCount"]
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
    actual = {"breachReviewPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_269_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_escalation_sla_breach_review_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_269_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_escalation_sla_breach_review_preview=pass "
        f"breach_reviews={actual['breachReviewPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_reviewers={actual['totalReviewerCount']} "
        f"total_evidence_gaps={actual['totalEvidenceGapCount']} total_breach_reasons={actual['totalBreachReasonCount']} "
        f"total_blocked_reviews={actual['totalBlockedReviewCount']} total_overdue_minutes={actual['totalOverdueMinutes']} "
        "creates_breach_records=0 creates_disputes=0 creates_committee_cases=0 creates_freeze_requests=0 "
        "creates_reminders=0 creates_approval_requests=0 creates_approval_decisions=0 creates_harness_evidence=0 "
        "creates_waes_gate_results=0 creates_kwe_work_items=0 writes_gfis=0 writes_gpc=0 writes_erp=0 "
        "writes_mes=0 writes_breach_record=0 writes_dispute=0 writes_committee_case=0 writes_freeze_request=0 "
        "writes_reminder=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
