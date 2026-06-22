#!/usr/bin/env python3
"""Validate GFIS Assistant repair action guard event preview dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-action-guard-event-preview-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-action-guard-event-preview.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-action-guard-event-preview-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesEventRecord",
    "writesActionReceipt",
    "writesReadReceipt",
    "writesAdmissionRecord",
    "writesReviewQueueItem",
    "writesConfirmationRecord",
    "writesDecisionRecord",
    "writesGapRecord",
    "writesBountyRecord",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesEvidenceRecord",
    "writesTargetReceipt",
    "writesCommitteeDecisionCompletion",
    "writesRevenueOrScoreConfirmation",
    "writesQuotaTransfer",
    "writesBountySettlement",
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
    previews: list[dict[str, Any]] = fixture["eventPreviews"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairActionGuardEventPreviewType": policy["preview_types"],
        "GfisAssistantRepairActionGuardEventPreviewStatus": policy["preview_statuses"],
        "GfisAssistantRepairActionGuardEventPreviewDecision": policy["preview_decisions"],
        "GfisAssistantRepairActionGuardEventPreviewBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    preview_types = set(policy["preview_types"])
    preview_statuses = set(policy["preview_statuses"])
    preview_decisions = set(policy["preview_decisions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "displayEventPreview": 0,
        "repairPromptEventPreview": 0,
        "metadataBoundaryEventPreview": 0,
        "committeeNoteEventPreview": 0,
        "freezeNoteEventPreview": 0,
        "blockedWriteEventPreview": 0,
        "previewOnly": 0,
        "blockedPreview": 0,
        "metadataOnlyPreview": 0,
        "repairRequiredPreview": 0,
        "committeePreview": 0,
        "freezePreview": 0,
        "showPreviewOnly": 0,
        "showRepairPreview": 0,
        "showMetadataBoundaryPreview": 0,
        "showCommitteePreview": 0,
        "showFreezePreview": 0,
        "showBlockedWritePreview": 0,
        "createsEventRecords": 0,
        "createsActionReceipts": 0,
        "createsReadReceipts": 0,
        "createsAdmissionRecords": 0,
        "createsReviewQueueItems": 0,
        "createsKweWorkItems": 0,
        "createsConfirmationRecords": 0,
        "createsDecisionRecords": 0,
        "createsWaesGateResults": 0,
        "persistsEvidence": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "display_event_preview": "displayEventPreview",
        "repair_prompt_event_preview": "repairPromptEventPreview",
        "metadata_boundary_event_preview": "metadataBoundaryEventPreview",
        "committee_note_event_preview": "committeeNoteEventPreview",
        "freeze_note_event_preview": "freezeNoteEventPreview",
        "blocked_write_event_preview": "blockedWriteEventPreview",
    }
    status_keys = {
        "preview_only": "previewOnly",
        "blocked_preview": "blockedPreview",
        "metadata_only_preview": "metadataOnlyPreview",
        "repair_required_preview": "repairRequiredPreview",
        "committee_preview": "committeePreview",
        "freeze_preview": "freezePreview",
    }
    decision_keys = {
        "show_preview_only": "showPreviewOnly",
        "show_repair_preview": "showRepairPreview",
        "show_metadata_boundary_preview": "showMetadataBoundaryPreview",
        "show_committee_preview": "showCommitteePreview",
        "show_freeze_preview": "showFreezePreview",
        "show_blocked_write_preview": "showBlockedWritePreview",
    }

    for preview in previews:
        preview_id = preview["eventPreviewId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in preview})
        if missing:
            failures.append(f"{preview_id} missing required fields: {missing}")
        if preview["previewType"] not in preview_types:
            failures.append(f"{preview_id}: invalid previewType")
        if preview["previewStatus"] not in preview_statuses:
            failures.append(f"{preview_id}: invalid previewStatus")
        if preview["previewDecision"] not in preview_decisions:
            failures.append(f"{preview_id}: invalid previewDecision")
        missing_blocks = sorted(blocked_actions - set(preview["blockedActions"]))
        if missing_blocks:
            failures.append(f"{preview_id}: missing blockedActions {missing_blocks}")
        if not preview["previewSummaryRef"] or not preview["reasonRefs"]:
            failures.append(f"{preview_id}: previewSummaryRef and reasonRefs are required")

        counts[surface_keys[preview["surface"]]] += 1
        counts[type_keys[preview["previewType"]]] += 1
        counts[status_keys[preview["previewStatus"]]] += 1
        counts[decision_keys[preview["previewDecision"]]] += 1
        false_flags = (
            "createsEventRecord",
            "createsActionReceipt",
            "createsReadReceipt",
            "createsAdmissionRecord",
            "createsReviewQueueItem",
            "createsKweWorkItem",
            "createsConfirmationRecord",
            "createsDecisionRecord",
            "createsWaesGateResult",
            "persistsEvidence",
            "approvesBusinessWrite",
            "promotesLifecycle",
            "completesCommitteeDecision",
        )
        for flag in false_flags:
            if preview[flag] is not False:
                failures.append(f"{preview_id}: {flag} must be false")
        counts["createsEventRecords"] += int(preview["createsEventRecord"] is True)
        counts["createsActionReceipts"] += int(preview["createsActionReceipt"] is True)
        counts["createsReadReceipts"] += int(preview["createsReadReceipt"] is True)
        counts["createsAdmissionRecords"] += int(preview["createsAdmissionRecord"] is True)
        counts["createsReviewQueueItems"] += int(preview["createsReviewQueueItem"] is True)
        counts["createsKweWorkItems"] += int(preview["createsKweWorkItem"] is True)
        counts["createsConfirmationRecords"] += int(preview["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(preview["createsDecisionRecord"] is True)
        counts["createsWaesGateResults"] += int(preview["createsWaesGateResult"] is True)
        counts["persistsEvidence"] += int(preview["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(preview["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(preview["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(preview["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            [preview["previewSummaryRef"]]
            + preview["reasonRefs"]
            + preview["nextStepCandidateRefs"]
            + preview["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{preview_id}: event preview must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = preview["noWrite"].get(key)
            if value != 0:
                failures.append(f"{preview_id}: {key} must be 0")
            totals[key] += value

    actual = {"eventPreviewCount": len(previews), **counts, **totals}

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
        print("gfis_assistant_repair_action_guard_event_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_action_guard_event_preview=pass "
        f"previews={actual['eventPreviewCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} display_event_preview={actual['displayEventPreview']} "
        f"repair_prompt_event_preview={actual['repairPromptEventPreview']} metadata_boundary_event_preview={actual['metadataBoundaryEventPreview']} "
        f"committee_note_event_preview={actual['committeeNoteEventPreview']} freeze_note_event_preview={actual['freezeNoteEventPreview']} "
        f"blocked_write_event_preview={actual['blockedWriteEventPreview']} creates_event_records={actual['createsEventRecords']} "
        f"creates_action_receipts={actual['createsActionReceipts']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_admission_records={actual['createsAdmissionRecords']} creates_review_queue_items={actual['createsReviewQueueItems']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_confirmation_records={actual['createsConfirmationRecords']} "
        f"creates_decision_records={actual['createsDecisionRecords']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_event_record=0 writes_action_receipt=0 writes_read_receipt=0 "
        "writes_admission_record=0 writes_review_queue_item=0 writes_confirmation_record=0 "
        "writes_decision_record=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
