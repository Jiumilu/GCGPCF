#!/usr/bin/env python3
"""Validate GFIS Assistant repair notification snooze queue filter preview no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-notification-snooze-queue-filter-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-notification-snooze-queue-filter-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-notification-snooze-queue-filter-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis", "writesGpc", "writesErp", "writesMes", "writesFilterState",
    "writesQueueItem", "writesSnoozeRecord", "writesScheduledReminder",
    "writesDismissalRecord", "writesNotification", "modifiesNotification",
    "writesWaesGateResult", "writesKweWorkItem", "writesHarnessEvidence",
    "writesKdsLifecycle", "writesKdsFact", "writesKdsAcceptedFact",
    "writesExternalApi",
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
    previews: list[dict[str, Any]] = fixture["filterPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairNotificationSnoozeQueueFilterPreviewType": policy["filter_types"],
        "GfisAssistantRepairNotificationSnoozeQueueFilterPreviewStatus": policy["filter_statuses"],
        "GfisAssistantRepairNotificationSnoozeQueueFilterPreviewDecision": policy["filter_decisions"],
        "GfisAssistantRepairNotificationSnoozeQueueFilterPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0, "pkcSurface": 0, "gfisAssistantSurface": 0,
        "surfaceFilter": 0, "blockedItemsFilter": 0, "retainedItemsFilter": 0,
        "metadataBoundaryFilter": 0, "committeeFilter": 0, "freezeFilter": 0,
        "filterPreviewOnly": 0, "filterContainsBlockedItems": 0,
        "filterContainsRetainedItems": 0, "filterMetadataBoundary": 0,
        "filterCommitteeItems": 0, "filterFreezeItems": 0,
        "createsFilterStates": 0, "createsQueueItems": 0, "createsSnoozeRecords": 0,
        "createsScheduledReminders": 0, "createsDismissalRecords": 0,
        "createsNotifications": 0, "modifiesNotifications": 0,
        "createsHarnessEvidence": 0, "createsWaesGateResults": 0,
        "createsKweWorkItems": 0, "persistsEvidence": 0,
        "approvesBusinessWrite": 0, "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "surface_filter_preview": "surfaceFilter",
        "blocked_items_filter_preview": "blockedItemsFilter",
        "retained_items_filter_preview": "retainedItemsFilter",
        "metadata_boundary_filter_preview": "metadataBoundaryFilter",
        "committee_filter_preview": "committeeFilter",
        "freeze_filter_preview": "freezeFilter",
    }
    status_keys = {
        "filter_preview_only": "filterPreviewOnly",
        "filter_contains_blocked_items": "filterContainsBlockedItems",
        "filter_contains_retained_items": "filterContainsRetainedItems",
        "filter_metadata_boundary": "filterMetadataBoundary",
        "filter_committee_items": "filterCommitteeItems",
        "filter_freeze_items": "filterFreezeItems",
    }
    false_flags = (
        "createsFilterState", "createsQueueItem", "createsSnoozeRecord",
        "createsScheduledReminder", "createsDismissalRecord", "createsNotification",
        "modifiesNotification", "createsHarnessEvidence", "createsWaesGateResult",
        "createsKweWorkItem", "persistsEvidence", "approvesBusinessWrite",
        "promotesLifecycle", "completesCommitteeDecision",
    )
    flag_count_keys = {
        "createsFilterState": "createsFilterStates",
        "createsQueueItem": "createsQueueItems",
        "createsSnoozeRecord": "createsSnoozeRecords",
        "createsScheduledReminder": "createsScheduledReminders",
        "createsDismissalRecord": "createsDismissalRecords",
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
        preview_id = preview["filterPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["queuePreviewRef"] not in preview["sourceQueuePreviewRefs"]:
            failures.append(f"{preview_id}: queuePreviewRef must be included in sourceQueuePreviewRefs")
        if not set(preview["filteredSnoozePreviewRefs"]).issubset(set(preview["sourceSnoozePreviewRefs"])):
            failures.append(f"{preview_id}: filtered refs must be a subset of source snooze refs")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["filterSummaryRef"] or not preview["reasonRefs"] or not preview["filterNoteRefs"]:
            failures.append(f"{preview_id}: filterSummaryRef, reasonRefs, and filterNoteRefs are required")
        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["filterType"]]] += 1
        counts[status_keys[preview["filterStatus"]]] += 1
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
            counts[flag_count_keys[flag]] += int(preview[flag] is True)
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"filterPreviewCount": len(previews), **counts, **totals}
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
        print("gfis_assistant_repair_notification_snooze_queue_filter_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_notification_snooze_queue_filter_preview=pass "
        f"filters={actual['filterPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} creates_filter_states={actual['createsFilterStates']} "
        f"creates_queue_items={actual['createsQueueItems']} creates_snooze_records={actual['createsSnoozeRecords']} "
        f"creates_scheduled_reminders={actual['createsScheduledReminders']} creates_notifications={actual['createsNotifications']} "
        f"modifies_notifications={actual['modifiesNotifications']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_filter_state=0 writes_queue_item=0 "
        "writes_snooze_record=0 writes_scheduled_reminder=0 writes_dismissal_record=0 "
        "writes_notification=0 modifies_notification=0 writes_waes_gate_result=0 writes_kwe_work_item=0 "
        "writes_harness_evidence=0 writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
