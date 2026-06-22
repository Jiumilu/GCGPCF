#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-247 resolution option approval packet preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-247-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-246-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks247DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesApprovalPacket', 'writesApprovalRequest', 'writesApprovalDecision', 'writesCommitteeDecision', 'writesFreezeAction', 'writesWaesGateResult', 'writesKweWorkItem', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["resolutionOptionPreviews"]
    upstream_ids = {item["resolutionOptionPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["approvalPacketPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["approval_packet_types"],
        f"{TYPE_PREFIX}Status": policy["approval_packet_statuses"],
        f"{TYPE_PREFIX}Decision": policy["approval_packet_decisions"],
        f"{TYPE_PREFIX}Scope": policy["approval_packet_scopes"],
        f"{TYPE_PREFIX}Route": policy["approval_routes"],
        f"{TYPE_PREFIX}Reason": policy["approval_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    reasons = set(policy["approval_reasons"])
    routes = set(policy["approval_routes"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {"brainSurface":0,"pkcSurface":0,"gfisAssistantSurface":0,"totalApproverCount":0,"totalRequiredEvidenceCount":0,"totalApprovalReasonCount":0,"totalBlockedApprovalCount":0,"createsApprovalPackets":0,"createsApprovalRequests":0,"createsApprovalDecisions":0,"createsCommitteeDecisions":0,"createsFreezeActions":0,"createsHarnessEvidence":0,"createsWaesGateResults":0,"createsKweWorkItems":0,"persistsEvidence":0,"approvesBusinessWrite":0,"promotesLifecycle":0,"completesCommitteeDecision":0}
    surface_keys = {"brain":"brainSurface","pkc":"pkcSurface","gfis_assistant":"gfisAssistantSurface"}
    false_flags = ("createsApprovalPacket","createsApprovalRequest","createsApprovalDecision","createsCommitteeDecision","createsFreezeAction","createsHarnessEvidence","createsWaesGateResult","createsKweWorkItem","persistsEvidence","approvesBusinessWrite","promotesLifecycle","completesCommitteeDecision")
    flag_count_keys = {"createsApprovalPacket":"createsApprovalPackets","createsApprovalRequest":"createsApprovalRequests","createsApprovalDecision":"createsApprovalDecisions","createsCommitteeDecision":"createsCommitteeDecisions","createsFreezeAction":"createsFreezeActions","createsHarnessEvidence":"createsHarnessEvidence","createsWaesGateResult":"createsWaesGateResults","createsKweWorkItem":"createsKweWorkItems","persistsEvidence":"persistsEvidence","approvesBusinessWrite":"approvesBusinessWrite","promotesLifecycle":"promotesLifecycle","completesCommitteeDecision":"completesCommitteeDecision"}
    for preview in previews:
        preview_id = preview["approvalPacketPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["resolutionOptionPreviewRefs"] != preview["sourceResolutionOptionPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs must equal sourceResolutionOptionPreviewRefs")
        if not set(preview["resolutionOptionPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs must come from DKS-246 upstream")
        if not preview["breachReviewPreviewRefs"] or not preview["slaPreviewRefs"]:
            failures.append(f"{preview_id}: breachReviewPreviewRefs and slaPreviewRefs are required")
        if not preview["candidateApproverRefs"] or not preview["approvalReasonRefs"]:
            failures.append(f"{preview_id}: candidateApproverRefs and approvalReasonRefs are required")
        if preview["blockedApprovalCount"] < 0 or preview["blockedApprovalCount"] > len(preview["candidateApproverRefs"]):
            failures.append(f"{preview_id}: blockedApprovalCount must be between 0 and approver refs length")
        if not set(preview["approvalReasonRefs"]) <= reasons:
            failures.append(f"{preview_id}: approvalReasonRefs must be declared")
        if preview["approvalRoute"] not in routes:
            failures.append(f"{preview_id}: approvalRoute must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["approvalSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, approvalSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalApproverCount"] += len(preview["candidateApproverRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalApprovalReasonCount"] += len(preview["approvalReasonRefs"])
        counts["totalBlockedApprovalCount"] += preview["blockedApprovalCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value
    actual = {"approvalPacketPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_247_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_247_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_preview=pass "
        f"approval_packets={actual['approvalPacketPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_approvers={actual['totalApproverCount']} "
        f"total_required_evidence={actual['totalRequiredEvidenceCount']} total_approval_reasons={actual['totalApprovalReasonCount']} "
        f"total_blocked_approval={actual['totalBlockedApprovalCount']} creates_approval_packets=0 creates_approval_requests=0 "
        "creates_approval_decisions=0 creates_committee_decisions=0 creates_freeze_actions=0 creates_harness_evidence=0 "
        "creates_waes_gate_results=0 creates_kwe_work_items=0 writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_approval_packet=0 writes_approval_request=0 writes_approval_decision=0 writes_committee_decision=0 "
        "writes_freeze_action=0 writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
