#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue approval route preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-approval-route-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-approval-route-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-approval-route-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes",
    "writesApprovalRoute", "writesRouteStep", "writesApproverAssignment",
    "writesApprovalRequest", "writesApprovalDecision", "writesShareLink",
    "writesAclGrant", "writesExternalSharePermission",
    "writesPublicationApproval", "writesWaesGateResult", "writesKweWorkItem",
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
    previews: list[dict[str, Any]] = fixture["routePreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewType": policy["route_types"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewStatus": policy["route_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewDecision": policy["route_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewScope": policy["route_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "teamRoute": 0, "projectRoute": 0, "governanceRoute": 0,
        "externalBlockedRoute": 0, "committeeRoute": 0, "freezeRoute": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "governanceReviewScope": 0, "committeeReviewScope": 0,
        "externalBlockedScope": 0, "freezeReviewScope": 0,
        "routePreviewOnly": 0, "routeContainsBlockedItems": 0,
        "routeMetadataBoundary": 0, "routeCommitteeRequired": 0,
        "routeExternalBlocked": 0, "routeFreezeRequired": 0,
        "createsApprovalRoutes": 0, "createsRouteSteps": 0,
        "assignsApprovers": 0, "createsApprovalRequests": 0,
        "createsApprovalDecisions": 0, "createsShareLinks": 0,
        "createsAclGrants": 0, "createsExternalSharePermissions": 0,
        "createsPublicationApprovals": 0, "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0, "createsKweWorkItems": 0,
        "persistsEvidence": 0, "approvesBusinessWrite": 0,
        "promotesLifecycle": 0, "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "team_route_preview": "teamRoute",
        "project_route_preview": "projectRoute",
        "governance_route_preview": "governanceRoute",
        "external_blocked_route_preview": "externalBlockedRoute",
        "committee_route_preview": "committeeRoute",
        "freeze_route_preview": "freezeRoute",
    }
    scope_keys = {
        "team_internal": "teamInternalScope",
        "project_internal": "projectInternalScope",
        "governance_review": "governanceReviewScope",
        "committee_review": "committeeReviewScope",
        "external_blocked": "externalBlockedScope",
        "freeze_review": "freezeReviewScope",
    }
    status_keys = {
        "route_preview_only": "routePreviewOnly",
        "route_contains_blocked_items": "routeContainsBlockedItems",
        "route_metadata_boundary": "routeMetadataBoundary",
        "route_committee_required": "routeCommitteeRequired",
        "route_external_blocked": "routeExternalBlocked",
        "route_freeze_required": "routeFreezeRequired",
    }
    false_flags = (
        "createsApprovalRoute", "createsRouteStep", "assignsApprover",
        "createsApprovalRequest", "createsApprovalDecision", "createsShareLink",
        "createsAclGrant", "createsExternalSharePermission",
        "createsPublicationApproval", "createsHarnessEvidence",
        "createsWaesGateResult", "createsKweWorkItem", "persistsEvidence",
        "approvesBusinessWrite", "promotesLifecycle", "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsApprovalRoute": "createsApprovalRoutes",
        "createsRouteStep": "createsRouteSteps",
        "assignsApprover": "assignsApprovers",
        "createsApprovalRequest": "createsApprovalRequests",
        "createsApprovalDecision": "createsApprovalDecisions",
        "createsShareLink": "createsShareLinks",
        "createsAclGrant": "createsAclGrants",
        "createsExternalSharePermission": "createsExternalSharePermissions",
        "createsPublicationApproval": "createsPublicationApprovals",
        "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults",
        "createsKweWorkItem": "createsKweWorkItems",
        "persistsEvidence": "persistsEvidence",
        "approvesBusinessWrite": "approvesBusinessWrite",
        "promotesLifecycle": "promotesLifecycle",
        "completesCommitteeDecision": "completesCommitteeDecision",
    }

    for preview in previews:
        preview_id = preview["routePreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["approvalPreviewRef"] not in preview["sourceApprovalPreviewRefs"]:
            failures.append(f"{preview_id}: approvalPreviewRef must be included in sourceApprovalPreviewRefs")
        if preview["sharePreviewRef"] not in preview["sourceSharePreviewRefs"]:
            failures.append(f"{preview_id}: sharePreviewRef must be included in sourceSharePreviewRefs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["routeStepRefs"] or not preview["routeSummaryRef"]:
            failures.append(f"{preview_id}: routeStepRefs and routeSummaryRef are required")
        if not preview["reasonRefs"] or not preview["routeNoteRefs"]:
            failures.append(f"{preview_id}: reasonRefs and routeNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["routeType"]]] += 1
        counts[scope_keys[preview["routeScope"]]] += 1
        counts[status_keys[preview["routeStatus"]]] += 1
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"routePreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_repair_notification_snooze_queue_approval_route_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_approval_route_preview=pass "
        f"routes={actual['routePreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} creates_approval_routes={actual['createsApprovalRoutes']} "
        f"creates_route_steps={actual['createsRouteSteps']} assigns_approvers={actual['assignsApprovers']} "
        f"creates_approval_requests={actual['createsApprovalRequests']} creates_approval_decisions={actual['createsApprovalDecisions']} "
        f"creates_share_links={actual['createsShareLinks']} creates_acl_grants={actual['createsAclGrants']} "
        f"creates_external_share_permissions={actual['createsExternalSharePermissions']} "
        f"creates_publication_approvals={actual['createsPublicationApprovals']} "
        f"creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_approval_route=0 writes_route_step=0 "
        "writes_approver_assignment=0 writes_approval_request=0 writes_approval_decision=0 writes_share_link=0 "
        "writes_acl_grant=0 writes_external_share_permission=0 writes_publication_approval=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
