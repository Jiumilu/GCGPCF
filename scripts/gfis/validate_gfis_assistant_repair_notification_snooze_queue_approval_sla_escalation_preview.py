#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval SLA escalation preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-sla-escalation-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesEscalationSchedule", "writesEscalationTask",
    "writesEscalationOwner", "writesReminder", "writesApprovalRoute",
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
    previews: list[dict[str, Any]] = fixture["escalationPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewType": policy["escalation_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewStatus": policy["escalation_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewDecision": policy["escalation_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewScope": policy["escalation_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "watchEscalation": 0, "urgentEscalation": 0, "governanceEscalation": 0,
        "externalBlockedEscalation": 0, "committeeEscalation": 0, "freezeEscalation": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "escalationPreviewOnly": 0, "escalationAtRiskPreview": 0,
        "escalationMetadataBoundary": 0, "escalationExternalBlocked": 0,
        "escalationCommitteeRequired": 0, "escalationFreezeRequired": 0,
        "createsEscalationSchedules": 0, "createsEscalationTasks": 0,
        "assignsEscalationOwners": 0, "createsReminders": 0,
        "createsApprovalRoutes": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "watch_escalation_preview": "watchEscalation",
        "urgent_escalation_preview": "urgentEscalation",
        "governance_escalation_preview": "governanceEscalation",
        "external_blocked_escalation_preview": "externalBlockedEscalation",
        "committee_escalation_preview": "committeeEscalation",
        "freeze_escalation_preview": "freezeEscalation",
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
        "escalation_preview_only": "escalationPreviewOnly",
        "escalation_at_risk_preview": "escalationAtRiskPreview",
        "escalation_metadata_boundary": "escalationMetadataBoundary",
        "escalation_external_blocked": "escalationExternalBlocked",
        "escalation_committee_required": "escalationCommitteeRequired",
        "escalation_freeze_required": "escalationFreezeRequired",
    }
    false_flags = (
        "createsEscalationSchedule", "createsEscalationTask",
        "assignsEscalationOwner", "createsReminder", "createsApprovalRoute",
        "createsApprovalRequest", "createsApprovalDecision",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsEscalationSchedule": "createsEscalationSchedules",
        "createsEscalationTask": "createsEscalationTasks",
        "assignsEscalationOwner": "assignsEscalationOwners",
        "createsReminder": "createsReminders",
        "createsApprovalRoute": "createsApprovalRoutes",
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
        preview_id = preview["escalationPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["slaPreviewRef"] not in preview["sourceSlaPreviewRefs"]:
            failures.append(f"{preview_id}: slaPreviewRef must be included in sourceSlaPreviewRefs")
        if preview["routePreviewRef"] not in preview["sourceRoutePreviewRefs"]:
            failures.append(f"{preview_id}: routePreviewRef must be included in sourceRoutePreviewRefs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["candidateOwnerRefs"] or not preview["responsibilityBoundaryRefs"]:
            failures.append(f"{preview_id}: candidateOwnerRefs and responsibilityBoundaryRefs are required")
        if not preview["escalationSummaryRef"] or not preview["reasonRefs"] or not preview["escalationNoteRefs"]:
            failures.append(f"{preview_id}: escalationSummaryRef, reasonRefs, and escalationNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["escalationType"]]] += 1
        counts[scope_keys[preview["escalationScope"]]] += 1
        counts[status_keys[preview["escalationStatus"]]] += 1
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_sla_escalation_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_sla_escalation_preview=pass "
        f"escalations={actual['escalationPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} creates_escalation_schedules={actual['createsEscalationSchedules']} "
        f"creates_escalation_tasks={actual['createsEscalationTasks']} assigns_escalation_owners={actual['assignsEscalationOwners']} "
        f"creates_reminders={actual['createsReminders']} creates_approval_routes={actual['createsApprovalRoutes']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_escalation_schedule=0 writes_escalation_task=0 writes_escalation_owner=0 writes_reminder=0 "
        "writes_approval_route=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
