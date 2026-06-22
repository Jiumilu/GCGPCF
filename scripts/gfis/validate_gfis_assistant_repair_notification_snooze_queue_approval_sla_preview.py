#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval SLA preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-sla-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-sla-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-sla-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesSlaTimer", "writesReminder", "writesEscalationSchedule",
    "writesEscalationOwner", "writesApprovalRoute", "writesApprovalRequest",
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
    previews: list[dict[str, Any]] = fixture["slaPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewType": policy["sla_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewStatus": policy["sla_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewDecision": policy["sla_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewScope": policy["sla_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "standardSla": 0, "urgentSla": 0, "governanceSla": 0,
        "externalBlockedSla": 0, "committeeSla": 0, "freezeSla": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "externalBlockedScope": 0,
        "committeeReviewScope": 0, "freezeReviewScope": 0,
        "slaPreviewOnly": 0, "slaAtRiskPreview": 0,
        "slaMetadataBoundary": 0, "slaExternalBlocked": 0,
        "slaCommitteeRequired": 0, "slaFreezeRequired": 0,
        "createsSlaTimers": 0, "createsReminders": 0,
        "schedulesEscalations": 0, "assignsEscalationOwners": 0,
        "createsApprovalRoutes": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "standard_sla_preview": "standardSla",
        "urgent_sla_preview": "urgentSla",
        "governance_sla_preview": "governanceSla",
        "external_blocked_sla_preview": "externalBlockedSla",
        "committee_sla_preview": "committeeSla",
        "freeze_sla_preview": "freezeSla",
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
        "sla_preview_only": "slaPreviewOnly",
        "sla_at_risk_preview": "slaAtRiskPreview",
        "sla_metadata_boundary": "slaMetadataBoundary",
        "sla_external_blocked": "slaExternalBlocked",
        "sla_committee_required": "slaCommitteeRequired",
        "sla_freeze_required": "slaFreezeRequired",
    }
    false_flags = (
        "createsSlaTimer", "createsReminder", "schedulesEscalation",
        "assignsEscalationOwner", "createsApprovalRoute",
        "createsApprovalRequest", "createsApprovalDecision",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsSlaTimer": "createsSlaTimers",
        "createsReminder": "createsReminders",
        "schedulesEscalation": "schedulesEscalations",
        "assignsEscalationOwner": "assignsEscalationOwners",
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
        preview_id = preview["slaPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["routePreviewRef"] not in preview["sourceRoutePreviewRefs"]:
            failures.append(f"{preview_id}: routePreviewRef must be included in sourceRoutePreviewRefs")
        if preview["approvalPreviewRef"] not in preview["sourceApprovalPreviewRefs"]:
            failures.append(f"{preview_id}: approvalPreviewRef must be included in sourceApprovalPreviewRefs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        due_window = preview["dueWindowMinutes"]
        elapsed = preview["elapsedMinutes"]
        remaining = preview["remainingMinutes"]
        if min(due_window, elapsed, remaining) < 0:
            failures.append(f"{preview_id}: SLA time fields must be non-negative")
        if remaining != max(due_window - elapsed, 0):
            failures.append(f"{preview_id}: remainingMinutes must equal max(dueWindowMinutes - elapsedMinutes, 0)")
        if not preview["slaSummaryRef"] or not preview["reasonRefs"] or not preview["slaNoteRefs"]:
            failures.append(f"{preview_id}: slaSummaryRef, reasonRefs, and slaNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["slaType"]]] += 1
        counts[scope_keys[preview["slaScope"]]] += 1
        counts[status_keys[preview["slaStatus"]]] += 1
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_sla_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_sla_preview=pass "
        f"slas={actual['slaPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} creates_sla_timers={actual['createsSlaTimers']} "
        f"creates_reminders={actual['createsReminders']} schedules_escalations={actual['schedulesEscalations']} "
        f"assigns_escalation_owners={actual['assignsEscalationOwners']} "
        f"creates_approval_routes={actual['createsApprovalRoutes']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_sla_timer=0 writes_reminder=0 writes_escalation_schedule=0 writes_escalation_owner=0 "
        "writes_approval_route=0 writes_approval_request=0 writes_approval_decision=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
