#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue view share preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-view-share-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-view-share-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-view-share-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes", "writesShareLink",
    "writesAclGrant", "writesExternalSharePermission", "writesPublicationApproval",
    "writesSavedView", "writesViewPreference", "writesFilterState",
    "writesNotification", "modifiesNotification", "writesWaesGateResult",
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
    previews: list[dict[str, Any]] = fixture["sharePreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewType": policy["share_types"],
        "GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewStatus": policy["share_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewDecision": policy["share_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewScope": policy["share_scopes"],
        "GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "personalToTeamShare": 0, "teamToProjectShare": 0,
        "surfaceDefaultShare": 0, "governanceReviewShare": 0,
        "externalShareBlocked": 0, "committeeShare": 0,
        "teamInternalScope": 0, "projectInternalScope": 0,
        "surfaceDefaultScope": 0, "governanceReviewScope": 0,
        "externalBlockedScope": 0, "sharePreviewOnly": 0,
        "shareContainsBlockedItems": 0, "shareContainsRetainedItems": 0,
        "shareMetadataBoundary": 0, "shareCommitteeItems": 0,
        "shareExternalBlocked": 0, "createsShareLinks": 0,
        "createsAclGrants": 0, "createsExternalSharePermissions": 0,
        "createsPublicationApprovals": 0, "createsSavedViews": 0,
        "createsViewPreferences": 0, "createsFilterStates": 0,
        "createsNotifications": 0, "modifiesNotifications": 0,
        "createsHarnessEvidence": 0, "createsWaesGateResults": 0,
        "createsKweWorkItems": 0, "persistsEvidence": 0,
        "approvesBusinessWrite": 0, "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "personal_to_team_share_preview": "personalToTeamShare",
        "team_to_project_share_preview": "teamToProjectShare",
        "surface_default_share_preview": "surfaceDefaultShare",
        "governance_review_share_preview": "governanceReviewShare",
        "external_share_blocked_preview": "externalShareBlocked",
        "committee_share_preview": "committeeShare",
    }
    scope_keys = {
        "team_internal": "teamInternalScope",
        "project_internal": "projectInternalScope",
        "surface_default": "surfaceDefaultScope",
        "governance_review": "governanceReviewScope",
        "external_blocked": "externalBlockedScope",
    }
    status_keys = {
        "share_preview_only": "sharePreviewOnly",
        "share_contains_blocked_items": "shareContainsBlockedItems",
        "share_contains_retained_items": "shareContainsRetainedItems",
        "share_metadata_boundary": "shareMetadataBoundary",
        "share_committee_items": "shareCommitteeItems",
        "share_external_blocked": "shareExternalBlocked",
    }
    false_flags = (
        "createsShareLink", "createsAclGrant", "createsExternalSharePermission",
        "createsPublicationApproval", "createsSavedView", "createsViewPreference",
        "createsFilterState", "createsNotification", "modifiesNotification",
        "createsHarnessEvidence", "createsWaesGateResult", "createsKweWorkItem",
        "persistsEvidence", "approvesBusinessWrite", "promotesLifecycle",
        "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsShareLink": "createsShareLinks",
        "createsAclGrant": "createsAclGrants",
        "createsExternalSharePermission": "createsExternalSharePermissions",
        "createsPublicationApproval": "createsPublicationApprovals",
        "createsSavedView": "createsSavedViews",
        "createsViewPreference": "createsViewPreferences",
        "createsFilterState": "createsFilterStates",
        "createsNotification": "createsNotifications",
        "modifiesNotification": "modifiesNotifications",
        "createsHarnessEvidence": "createsHarnessEvidence",
        "createsWaesGateResult": "createsWaesGateResults",
        "createsKweWorkItem": "createsKweWorkItems",
        "persistsEvidence": "persistsEvidence",
        "approvesBusinessWrite": "approvesBusinessWrite",
        "promotesLifecycle": "promotesLifecycle",
        "completesCommitteeDecision": "completesCommitteeDecision",
    }

    for preview in previews:
        preview_id = preview["sharePreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["savedViewPreviewRef"] not in preview["sourceSavedViewPreviewRefs"]:
            failures.append(f"{preview_id}: savedViewPreviewRef must be included in sourceSavedViewPreviewRefs")
        if preview["filterPreviewRef"] not in preview["sourceFilterPreviewRefs"]:
            failures.append(f"{preview_id}: filterPreviewRef must be included in sourceFilterPreviewRefs")
        if preview["queuePreviewRef"] not in preview["sourceQueuePreviewRefs"]:
            failures.append(f"{preview_id}: queuePreviewRef must be included in sourceQueuePreviewRefs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["shareSummaryRef"] or not preview["reasonRefs"] or not preview["shareNoteRefs"]:
            failures.append(f"{preview_id}: shareSummaryRef, reasonRefs, and shareNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["shareType"]]] += 1
        counts[scope_keys[preview["shareScope"]]] += 1
        counts[status_keys[preview["shareStatus"]]] += 1
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"sharePreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_repair_notification_snooze_queue_view_share_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_view_share_preview=pass "
        f"shares={actual['sharePreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} creates_share_links={actual['createsShareLinks']} "
        f"creates_acl_grants={actual['createsAclGrants']} "
        f"creates_external_share_permissions={actual['createsExternalSharePermissions']} "
        f"creates_publication_approvals={actual['createsPublicationApprovals']} "
        f"creates_saved_views={actual['createsSavedViews']} creates_view_preferences={actual['createsViewPreferences']} "
        f"creates_filter_states={actual['createsFilterStates']} creates_notifications={actual['createsNotifications']} "
        f"modifies_notifications={actual['modifiesNotifications']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_share_link=0 writes_acl_grant=0 "
        "writes_external_share_permission=0 writes_publication_approval=0 writes_saved_view=0 "
        "writes_view_preference=0 writes_filter_state=0 writes_notification=0 modifies_notification=0 "
        "writes_waes_gate_result=0 writes_kwe_work_item=0 writes_harness_evidence=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
