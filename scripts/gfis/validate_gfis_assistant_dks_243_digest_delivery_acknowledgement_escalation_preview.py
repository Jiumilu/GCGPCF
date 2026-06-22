#!/usr/bin/env python3
"""Validate GFIS Assistant DKS-243 digest delivery acknowledgement escalation preview no-write boundary."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[2]
SLUG = "gfis-assistant-dks-243-digest-delivery-acknowledgement-escalation-preview"
POLICY = ROOT / "okf" / f"{SLUG}-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / f"{SLUG}.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / f"{SLUG}-dry-run.json"
UPSTREAM = ROOT / "fixtures" / "gfis" / "gfis-assistant-dks-242-digest-delivery-acknowledgement-preview-dry-run.json"
TYPE_PREFIX = "GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreview"
NO_WRITE_KEYS = ('writesGfis', 'writesGpc', 'writesErp', 'writesMes', 'writesEscalation', 'writesEscalationTask', 'writesDeliveryAcknowledgement', 'writesDigestDelivery', 'writesDelivery', 'writesDigest', 'writesKweWorkItem', 'writesNotification', 'writesAcknowledgement', 'writesReceipt', 'writesReadReceipt', 'writesDeliveryStatus', 'writesApprovalAssignment', 'writesApprovalLock', 'writesApprovalPacket', 'writesApprovalRequest', 'writesApprovalDecision', 'writesCommitteeDecision', 'writesFreezeAction', 'writesWaesGateResult', 'writesHarnessEvidence', 'writesKdsLifecycle', 'writesKdsFact', 'writesKdsAcceptedFact', 'writesExternalApi')

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
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))["deliveryAcknowledgementPreviews"]
    upstream_ids = {item["deliveryAcknowledgementPreviewId"] for item in upstream}
    previews: list[dict[str, Any]] = fixture["escalationPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []
    unions = {
        f"{TYPE_PREFIX}Type": policy["escalation_types"],
        f"{TYPE_PREFIX}Status": policy["escalation_statuses"],
        f"{TYPE_PREFIX}Decision": policy["escalation_decisions"],
        f"{TYPE_PREFIX}Scope": policy["escalation_scopes"],
        f"{TYPE_PREFIX}Priority": policy["escalation_priorities"],
        f"{TYPE_PREFIX}Reason": policy["escalation_reasons"],
        f"{TYPE_PREFIX}BlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")
    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    reasons = set(policy["escalation_reasons"])
    priorities = set(policy["escalation_priorities"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "totalEscalationOwnerCount": 0,
        "totalRequiredEvidenceCount": 0,
        "totalEscalationReasonCount": 0,
        "totalBlockedEscalationCount": 0,
        "createsEscalations": 0,
        "createsEscalationTasks": 0,
        "createsDeliveryAcknowledgements": 0,
        "createsDigestDeliveries": 0,
        "createsDeliveries": 0,
        "createsDigests": 0,
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
    false_flags = ('createsEscalation', 'createsEscalationTask', 'createsDeliveryAcknowledgement', 'createsDigestDelivery', 'createsDelivery', 'createsDigest', 'createsKweWorkItem', 'createsNotification', 'createsAcknowledgement', 'createsReceipt', 'createsReadReceipt', 'updatesDeliveryStatus', 'sendsExternalNotification', 'createsApprovalAssignment', 'locksApprover', 'createsApprovalPacket', 'createsApprovalRequest', 'createsApprovalDecision', 'createsCommitteeDecision', 'createsFreezeAction', 'createsHarnessEvidence', 'createsWaesGateResult', 'persistsEvidence', 'approvesBusinessWrite', 'promotesLifecycle', 'completesCommitteeDecision')
    flag_count_keys = {
        "createsEscalation": "createsEscalations",
        "createsEscalationTask": "createsEscalationTasks",
        "createsDeliveryAcknowledgement": "createsDeliveryAcknowledgements",
        "createsDigestDelivery": "createsDigestDeliveries",
        "createsDelivery": "createsDeliveries",
        "createsDigest": "createsDigests",
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
        preview_id = preview["escalationPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["deliveryAcknowledgementPreviewRefs"] != preview["sourceDeliveryAcknowledgementPreviewRefs"]:
            failures.append(f"{preview_id}: deliveryAcknowledgementPreviewRefs must equal sourceDeliveryAcknowledgementPreviewRefs")
        if not set(preview["deliveryAcknowledgementPreviewRefs"]) <= upstream_ids:
            failures.append(f"{preview_id}: deliveryAcknowledgementPreviewRefs must come from DKS-242 upstream")
        if not preview["deliveryPreviewRefs"] or not preview["digestPreviewRefs"] or not preview["acknowledgementPreviewRefs"] or not preview["notificationPreviewRefs"]:
            failures.append(f"{preview_id}: delivery, digest, acknowledgement, and notification refs are required")
        if not preview["routingQueuePreviewRefs"] or not preview["approvalPacketPreviewRefs"]:
            failures.append(f"{preview_id}: routing queue and approval packet refs are required")
        if not preview["resolutionOptionPreviewRefs"] or not preview["breachReviewPreviewRefs"]:
            failures.append(f"{preview_id}: resolutionOptionPreviewRefs and breachReviewPreviewRefs are required")
        if not preview["candidateEscalationOwnerRefs"] or not preview["escalationReasonRefs"]:
            failures.append(f"{preview_id}: candidate escalation owners and reasons are required")
        if preview["blockedEscalationCount"] < 0 or preview["blockedEscalationCount"] > len(preview["candidateEscalationOwnerRefs"]):
            failures.append(f"{preview_id}: blockedEscalationCount must be between 0 and candidateEscalationOwnerRefs length")
        if not set(preview["escalationReasonRefs"]) <= reasons:
            failures.append(f"{preview_id}: escalationReasonRefs must be declared")
        if preview["escalationPriority"] not in priorities:
            failures.append(f"{preview_id}: escalationPriority must be declared")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["boundaryRefs"] or not preview["escalationSummaryRef"] or not preview["nextStepCandidateRefs"]:
            failures.append(f"{preview_id}: boundaryRefs, escalationSummaryRef, and nextStepCandidateRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts["totalEscalationOwnerCount"] += len(preview["candidateEscalationOwnerRefs"])
        counts["totalRequiredEvidenceCount"] += len(preview["requiredEvidenceRefs"])
        counts["totalEscalationReasonCount"] += len(preview["escalationReasonRefs"])
        counts["totalBlockedEscalationCount"] += preview["blockedEscalationCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value
    actual = {"escalationPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_dks_243_digest_delivery_acknowledgement_escalation_preview=fail")
        for failure in failures:
            print(failure)
        return 1
    print(
        "gfis_assistant_dks_243_digest_delivery_acknowledgement_escalation_preview=pass "
        f"escalations={actual['escalationPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} total_escalation_owners={actual['totalEscalationOwnerCount']} "
        f"total_required_evidence={actual['totalRequiredEvidenceCount']} total_escalation_reasons={actual['totalEscalationReasonCount']} "
        f"total_blocked_escalations={actual['totalBlockedEscalationCount']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_escalation=0 writes_escalation_task=0 writes_delivery_acknowledgement=0 writes_digest_delivery=0 "
        "writes_delivery=0 writes_digest=0 writes_kwe_work_item=0 writes_external_api=0"
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
