#!/usr/bin/env python3
"""Validate GFIS Assistant repair read-model action guard dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-read-model-action-guard-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-read-model-action-guard.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-read-model-action-guard-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
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
    guards: list[dict[str, Any]] = fixture["actionGuards"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairReadModelActionGuardKind": policy["action_kinds"],
        "GfisAssistantRepairReadModelActionGuardStatus": policy["guard_statuses"],
        "GfisAssistantRepairReadModelActionGuardDecision": policy["guard_decisions"],
        "GfisAssistantRepairReadModelDisplayAction": policy["allowed_display_actions"],
        "GfisAssistantRepairReadModelActionGuardBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    action_kinds = set(policy["action_kinds"])
    guard_statuses = set(policy["guard_statuses"])
    guard_decisions = set(policy["guard_decisions"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "displayOnly": 0,
        "repairPrompt": 0,
        "metadataBoundaryPrompt": 0,
        "committeeNotePrompt": 0,
        "freezeNotePrompt": 0,
        "blockedWriteAction": 0,
        "allowedDisplayOnly": 0,
        "repairPromptOnly": 0,
        "metadataPromptOnly": 0,
        "committeePromptOnly": 0,
        "freezePromptOnly": 0,
        "blockedNoWrite": 0,
        "showOnly": 0,
        "showRepairPrompt": 0,
        "showMetadataBoundaryPrompt": 0,
        "showCommitteeNotePrompt": 0,
        "showFreezeNotePrompt": 0,
        "blockWriteAction": 0,
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
    kind_keys = {
        "display_only": "displayOnly",
        "repair_prompt": "repairPrompt",
        "metadata_boundary_prompt": "metadataBoundaryPrompt",
        "committee_note_prompt": "committeeNotePrompt",
        "freeze_note_prompt": "freezeNotePrompt",
        "blocked_write_action": "blockedWriteAction",
    }
    status_keys = {
        "allowed_display_only": "allowedDisplayOnly",
        "repair_prompt_only": "repairPromptOnly",
        "metadata_prompt_only": "metadataPromptOnly",
        "committee_prompt_only": "committeePromptOnly",
        "freeze_prompt_only": "freezePromptOnly",
        "blocked_no_write": "blockedNoWrite",
    }
    decision_keys = {
        "show_only": "showOnly",
        "show_repair_prompt": "showRepairPrompt",
        "show_metadata_boundary_prompt": "showMetadataBoundaryPrompt",
        "show_committee_note_prompt": "showCommitteeNotePrompt",
        "show_freeze_note_prompt": "showFreezeNotePrompt",
        "block_write_action": "blockWriteAction",
    }

    for guard in guards:
        guard_id = guard["actionGuardId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in guard})
        if missing:
            failures.append(f"{guard_id} missing required fields: {missing}")
        if guard["actionKind"] not in action_kinds:
            failures.append(f"{guard_id}: invalid actionKind")
        if guard["guardStatus"] not in guard_statuses:
            failures.append(f"{guard_id}: invalid guardStatus")
        if guard["guardDecision"] not in guard_decisions:
            failures.append(f"{guard_id}: invalid guardDecision")
        if guard["actionKind"] == "blocked_write_action" and guard["actionId"] not in blocked_actions:
            failures.append(f"{guard_id}: blocked write actionId must be a blocked action")
        if guard["actionKind"] != "blocked_write_action" and guard["actionId"] not in display_actions:
            failures.append(f"{guard_id}: display actionId must be an allowed display action")
        missing_blocks = sorted(blocked_actions - set(guard["blockedActions"]))
        if missing_blocks:
            failures.append(f"{guard_id}: missing blockedActions {missing_blocks}")
        if not guard["reasonRefs"] or not guard["displayLabelRef"]:
            failures.append(f"{guard_id}: reasonRefs and displayLabelRef are required")

        counts[surface_keys[guard["surface"]]] += 1
        counts[kind_keys[guard["actionKind"]]] += 1
        counts[status_keys[guard["guardStatus"]]] += 1
        counts[decision_keys[guard["guardDecision"]]] += 1
        false_flags = (
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
            if guard[flag] is not False:
                failures.append(f"{guard_id}: {flag} must be false")
        counts["createsActionReceipts"] += int(guard["createsActionReceipt"] is True)
        counts["createsReadReceipts"] += int(guard["createsReadReceipt"] is True)
        counts["createsAdmissionRecords"] += int(guard["createsAdmissionRecord"] is True)
        counts["createsReviewQueueItems"] += int(guard["createsReviewQueueItem"] is True)
        counts["createsKweWorkItems"] += int(guard["createsKweWorkItem"] is True)
        counts["createsConfirmationRecords"] += int(guard["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(guard["createsDecisionRecord"] is True)
        counts["createsWaesGateResults"] += int(guard["createsWaesGateResult"] is True)
        counts["persistsEvidence"] += int(guard["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(guard["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(guard["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(guard["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            [guard["actionId"], guard["displayLabelRef"]]
            + guard["reasonRefs"]
            + guard["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{guard_id}: action guard must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = guard["noWrite"].get(key)
            if value != 0:
                failures.append(f"{guard_id}: {key} must be 0")
            totals[key] += value

    actual = {"actionGuardCount": len(guards), **counts, **totals}

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
        print("gfis_assistant_repair_read_model_action_guard=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_read_model_action_guard=pass "
        f"guards={actual['actionGuardCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} display_only={actual['displayOnly']} "
        f"repair_prompt={actual['repairPrompt']} metadata_boundary_prompt={actual['metadataBoundaryPrompt']} "
        f"committee_note_prompt={actual['committeeNotePrompt']} freeze_note_prompt={actual['freezeNotePrompt']} "
        f"blocked_write_action={actual['blockedWriteAction']} blocked_no_write={actual['blockedNoWrite']} "
        f"creates_action_receipts={actual['createsActionReceipts']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_admission_records={actual['createsAdmissionRecords']} creates_review_queue_items={actual['createsReviewQueueItems']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_confirmation_records={actual['createsConfirmationRecords']} "
        f"creates_decision_records={actual['createsDecisionRecords']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_action_receipt=0 writes_read_receipt=0 "
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
