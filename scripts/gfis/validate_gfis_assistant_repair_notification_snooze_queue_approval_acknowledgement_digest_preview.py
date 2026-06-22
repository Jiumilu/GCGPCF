#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval acknowledgement digest preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-acknowledgement-digest-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesDigest", "writesAcknowledgement", "writesReadReceipt",
    "writesReminder", "writesEscalationTask", "writesApprovalRequest",
    "writesApprovalDecision", "writesWaesGateResult", "writesKweWorkItem",
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
    previews: list[dict[str, Any]] = fixture["digestPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewType": policy["digest_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewStatus": policy["digest_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewDecision": policy["digest_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewScope": policy["digest_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "teamDigest": 0, "projectDigest": 0, "governanceDigest": 0,
        "externalBlockedDigest": 0, "committeeDigest": 0, "freezeDigest": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "digestPreviewOnly": 0, "digestAtRiskPreview": 0,
        "digestMetadataBoundary": 0, "digestExternalBlocked": 0,
        "digestCommitteeRequired": 0, "digestFreezeRequired": 0,
        "totalCoverageCount": 0, "totalBlockedAckCount": 0,
        "createsDigests": 0, "createsAcknowledgements": 0,
        "createsReadReceipts": 0, "createsReminders": 0,
        "createsEscalationTasks": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "team_ack_digest_preview": "teamDigest",
        "project_ack_digest_preview": "projectDigest",
        "governance_ack_digest_preview": "governanceDigest",
        "external_blocked_ack_digest_preview": "externalBlockedDigest",
        "committee_ack_digest_preview": "committeeDigest",
        "freeze_ack_digest_preview": "freezeDigest",
    }
    scope_keys = {
        "team_internal": "teamInternalScope",
        "project_internal": "projectInternalScope",
        "governance_review": "governanceReviewScope",
        "external_blocked": "externalBlockedScope",
        "committee_review": "committeeReviewScope",
        "freeze_review": "freezeReviewScope",
    }
    status_keys = {
        "digest_preview_only": "digestPreviewOnly",
        "digest_at_risk_preview": "digestAtRiskPreview",
        "digest_metadata_boundary": "digestMetadataBoundary",
        "digest_external_blocked": "digestExternalBlocked",
        "digest_committee_required": "digestCommitteeRequired",
        "digest_freeze_required": "digestFreezeRequired",
    }
    false_flags = (
        "createsDigest", "createsAcknowledgement", "createsReadReceipt",
        "createsReminder", "createsEscalationTask", "createsApprovalRequest",
        "createsApprovalDecision", "createsHarnessEvidence",
        "createsWaesGateResult", "createsKweWorkItem", "persistsEvidence",
        "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsDigest": "createsDigests",
        "createsAcknowledgement": "createsAcknowledgements",
        "createsReadReceipt": "createsReadReceipts",
        "createsReminder": "createsReminders",
        "createsEscalationTask": "createsEscalationTasks",
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
        preview_id = preview["digestPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        ack_refs = set(preview["acknowledgementPreviewRefs"])
        source_ack_refs = set(preview["sourceAcknowledgementPreviewRefs"])
        if not ack_refs or not ack_refs <= source_ack_refs:
            failures.append(f"{preview_id}: acknowledgementPreviewRefs must be included in sourceAcknowledgementPreviewRefs")
        if preview["coverageCount"] != len(preview["acknowledgementPreviewRefs"]):
            failures.append(f"{preview_id}: coverageCount must equal acknowledgementPreviewRefs length")
        if preview["blockedAckCount"] < 0 or preview["blockedAckCount"] > preview["coverageCount"]:
            failures.append(f"{preview_id}: blockedAckCount must be between 0 and coverageCount")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["candidateAcknowledgerRefs"] or not preview["boundaryRefs"]:
            failures.append(f"{preview_id}: candidateAcknowledgerRefs and boundaryRefs are required")
        if not preview["digestSummaryRef"] or not preview["reasonRefs"] or not preview["digestNoteRefs"]:
            failures.append(f"{preview_id}: digestSummaryRef, reasonRefs, and digestNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["digestType"]]] += 1
        counts[scope_keys[preview["digestScope"]]] += 1
        counts[status_keys[preview["digestStatus"]]] += 1
        counts["totalCoverageCount"] += preview["coverageCount"]
        counts["totalBlockedAckCount"] += preview["blockedAckCount"]
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"digestPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_preview=pass "
        f"digests={actual['digestPreviewCount']} brain={actual['brainSurface']} "
        f"pkc={actual['pkcSurface']} gfis_assistant={actual['gfisAssistantSurface']} "
        f"total_coverage={actual['totalCoverageCount']} total_blocked_ack={actual['totalBlockedAckCount']} "
        f"creates_digests={actual['createsDigests']} creates_acknowledgements={actual['createsAcknowledgements']} "
        f"creates_read_receipts={actual['createsReadReceipts']} creates_reminders={actual['createsReminders']} "
        f"creates_escalation_tasks={actual['createsEscalationTasks']} creates_approval_requests={actual['createsApprovalRequests']} "
        f"creates_approval_decisions={actual['createsApprovalDecisions']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_digest=0 writes_acknowledgement=0 "
        "writes_read_receipt=0 writes_reminder=0 writes_escalation_task=0 writes_approval_request=0 "
        "writes_approval_decision=0 writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
