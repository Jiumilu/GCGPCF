#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval escalation acknowledgement preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesAcknowledgement", "writesReadReceipt",
    "writesAcknowledgerAssignment", "writesReminder",
    "writesEscalationTask", "writesApprovalRequest",
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
    previews: list[dict[str, Any]] = fixture["acknowledgementPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewType": policy["ack_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewStatus": policy["ack_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewDecision": policy["ack_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewScope": policy["ack_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "watchAck": 0, "urgentAck": 0, "governanceAck": 0,
        "externalBlockedAck": 0, "committeeAck": 0, "freezeAck": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "ackPreviewOnly": 0, "ackAtRiskPreview": 0,
        "ackMetadataBoundary": 0, "ackExternalBlocked": 0,
        "ackCommitteeRequired": 0, "ackFreezeRequired": 0,
        "createsAcknowledgements": 0, "createsReadReceipts": 0,
        "assignsAcknowledgers": 0, "createsReminders": 0,
        "createsEscalationTasks": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "watch_ack_preview": "watchAck",
        "urgent_ack_preview": "urgentAck",
        "governance_ack_preview": "governanceAck",
        "external_blocked_ack_preview": "externalBlockedAck",
        "committee_ack_preview": "committeeAck",
        "freeze_ack_preview": "freezeAck",
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
        "ack_preview_only": "ackPreviewOnly",
        "ack_at_risk_preview": "ackAtRiskPreview",
        "ack_metadata_boundary": "ackMetadataBoundary",
        "ack_external_blocked": "ackExternalBlocked",
        "ack_committee_required": "ackCommitteeRequired",
        "ack_freeze_required": "ackFreezeRequired",
    }
    false_flags = (
        "createsAcknowledgement", "createsReadReceipt",
        "assignsAcknowledger", "createsReminder", "createsEscalationTask",
        "createsApprovalRequest", "createsApprovalDecision",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsAcknowledgement": "createsAcknowledgements",
        "createsReadReceipt": "createsReadReceipts",
        "assignsAcknowledger": "assignsAcknowledgers",
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
        preview_id = preview["acknowledgementPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["escalationPreviewRef"] not in preview["sourceEscalationPreviewRefs"]:
            failures.append(f"{preview_id}: escalationPreviewRef must be included in sourceEscalationPreviewRefs")
        if preview["slaPreviewRef"] not in preview["sourceSlaPreviewRefs"]:
            failures.append(f"{preview_id}: slaPreviewRef must be included in sourceSlaPreviewRefs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["candidateAcknowledgerRefs"] or not preview["ackBoundaryRefs"]:
            failures.append(f"{preview_id}: candidateAcknowledgerRefs and ackBoundaryRefs are required")
        if not preview["ackSummaryRef"] or not preview["reasonRefs"] or not preview["ackNoteRefs"]:
            failures.append(f"{preview_id}: ackSummaryRef, reasonRefs, and ackNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["ackType"]]] += 1
        counts[scope_keys[preview["ackScope"]]] += 1
        counts[status_keys[preview["ackStatus"]]] += 1
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_escalation_acknowledgement_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_escalation_acknowledgement_preview=pass "
        f"acknowledgements={actual['acknowledgementPreviewCount']} brain={actual['brainSurface']} "
        f"pkc={actual['pkcSurface']} gfis_assistant={actual['gfisAssistantSurface']} "
        f"creates_acknowledgements={actual['createsAcknowledgements']} "
        f"creates_read_receipts={actual['createsReadReceipts']} assigns_acknowledgers={actual['assignsAcknowledgers']} "
        f"creates_reminders={actual['createsReminders']} creates_escalation_tasks={actual['createsEscalationTasks']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_acknowledgement=0 writes_read_receipt=0 writes_acknowledger_assignment=0 writes_reminder=0 "
        "writes_escalation_task=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
