#!/usr/bin/env python3
"""Validate GFIS Assistant repair review decision draft dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-review-decision-draft-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-review-decision-draft.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-review-decision-draft-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
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
    drafts: list[dict[str, Any]] = fixture["decisionDrafts"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairReviewDecisionDraftType": policy["draft_types"],
        "GfisAssistantRepairReviewDecisionDraftStatus": policy["draft_statuses"],
        "GfisAssistantRepairReviewSuggestedDisposition": policy["suggested_dispositions"],
        "GfisAssistantRepairReviewDecisionDraftDisplayAction": policy["allowed_display_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    draft_types = set(policy["draft_types"])
    draft_statuses = set(policy["draft_statuses"])
    dispositions = set(policy["suggested_dispositions"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "draft": 0,
        "needsRepair": 0,
        "blocked": 0,
        "metadataOnly": 0,
        "humanActionDraft": 0,
        "metadataBoundaryNote": 0,
        "committeeAgendaNote": 0,
        "freezeNote": 0,
        "blockedHoldNote": 0,
        "requestMoreEvidence": 0,
        "keepMetadataOnly": 0,
        "prepareCommitteeAgenda": 0,
        "keepFrozen": 0,
        "holdBlocked": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "draftsWithRequiredRepairRefs": 0,
        "draftsWithBlockedReasons": 0,
        "submitsEvidence": 0,
        "persistsEvidence": 0,
        "createsReviewQueueItems": 0,
        "createsConfirmationRecords": 0,
        "createsDecisionRecords": 0,
        "createsGapRecords": 0,
        "createsBountyRecords": 0,
        "createsKweWorkItems": 0,
        "createsWaesGateResults": 0,
        "routesToHumanQueue": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
        "draftsWithBlockedActions": 0,
    }

    for draft in drafts:
        draft_id = draft["decisionDraftId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in draft})
        if missing:
            failures.append(f"{draft_id} missing required fields: {missing}")
        if draft["draftType"] not in draft_types:
            failures.append(f"{draft_id}: invalid draftType")
        if draft["draftStatus"] not in draft_statuses:
            failures.append(f"{draft_id}: invalid draftStatus")
        if draft["suggestedDisposition"] not in dispositions:
            failures.append(f"{draft_id}: invalid suggestedDisposition")
        if not draft["reviewerNoteRefs"]:
            failures.append(f"{draft_id}: reviewerNoteRefs are required")
        missing_blocks = sorted(blocked_actions - set(draft["blockedActions"]))
        if missing_blocks:
            failures.append(f"{draft_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(draft["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{draft_id}: unknown allowedDisplayActions {unknown_display}")

        bundle = draft["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{draft_id}: metadataRefBundle objectRefs and sourceRefs are required")
        if bundle["metadataOnly"] is True and not draft["evidenceHintRefs"]:
            failures.append(f"{draft_id}: metadata-only draft requires evidenceHintRefs")

        status_key = {
            "draft": "draft",
            "needs_repair": "needsRepair",
            "blocked": "blocked",
            "metadata_only": "metadataOnly",
        }[draft["draftStatus"]]
        type_key = {
            "human_action_draft": "humanActionDraft",
            "metadata_boundary_note": "metadataBoundaryNote",
            "committee_agenda_note": "committeeAgendaNote",
            "freeze_note": "freezeNote",
            "blocked_hold_note": "blockedHoldNote",
        }[draft["draftType"]]
        disposition_key = {
            "request_more_evidence": "requestMoreEvidence",
            "keep_metadata_only": "keepMetadataOnly",
            "prepare_committee_agenda": "prepareCommitteeAgenda",
            "keep_frozen": "keepFrozen",
            "hold_blocked": "holdBlocked",
        }[draft["suggestedDisposition"]]
        counts[status_key] += 1
        counts[type_key] += 1
        counts[disposition_key] += 1
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["draftsWithRequiredRepairRefs"] += int(bool(draft["requiredRepairRefs"]))
        counts["draftsWithBlockedReasons"] += int(bool(draft["blockedReasonRefs"]))
        counts["submitsEvidence"] += int(draft["submitsEvidence"] is True)
        counts["persistsEvidence"] += int(draft["persistsEvidence"] is True)
        counts["createsReviewQueueItems"] += int(draft["createsReviewQueueItem"] is True)
        counts["createsConfirmationRecords"] += int(draft["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(draft["createsDecisionRecord"] is True)
        counts["createsGapRecords"] += int(draft["createsGapRecord"] is True)
        counts["createsBountyRecords"] += int(draft["createsBountyRecord"] is True)
        counts["createsKweWorkItems"] += int(draft["createsKweWorkItem"] is True)
        counts["createsWaesGateResults"] += int(draft["createsWaesGateResult"] is True)
        counts["routesToHumanQueue"] += int(draft["routesToHumanQueue"] is True)
        counts["approvesBusinessWrite"] += int(draft["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(draft["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(draft["completesCommitteeDecision"] is True)
        counts["draftsWithBlockedActions"] += int(bool(draft["blockedActions"]))

        false_flags = (
            "submitsEvidence",
            "persistsEvidence",
            "createsReviewQueueItem",
            "createsConfirmationRecord",
            "createsDecisionRecord",
            "createsGapRecord",
            "createsBountyRecord",
            "createsKweWorkItem",
            "createsWaesGateResult",
            "routesToHumanQueue",
            "approvesBusinessWrite",
            "promotesLifecycle",
            "completesCommitteeDecision",
        )
        for flag in false_flags:
            if draft[flag] is not False:
                failures.append(f"{draft_id}: {flag} must be false")

        ref_text = " ".join(
            draft["reviewerNoteRefs"]
            + draft["requiredRepairRefs"]
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + draft["evidenceHintRefs"]
            + draft["blockedReasonRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{draft_id}: decision draft must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = draft["noWrite"].get(key)
            if value != 0:
                failures.append(f"{draft_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "decisionDraftCount": len(drafts),
        **counts,
        **totals,
    }

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
        print("gfis_assistant_repair_review_decision_draft=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_review_decision_draft=pass "
        f"drafts={actual['decisionDraftCount']} needs_repair={actual['needsRepair']} "
        f"metadata_only={actual['metadataOnly']} blocked={actual['blocked']} "
        f"human_action_draft={actual['humanActionDraft']} metadata_boundary_note={actual['metadataBoundaryNote']} "
        f"committee_agenda_note={actual['committeeAgendaNote']} freeze_note={actual['freezeNote']} "
        f"request_more_evidence={actual['requestMoreEvidence']} keep_metadata_only={actual['keepMetadataOnly']} "
        f"prepare_committee_agenda={actual['prepareCommitteeAgenda']} keep_frozen={actual['keepFrozen']} "
        f"metadata_only_bundles={actual['metadataOnlyBundles']} controlled_original_bundles={actual['controlledOriginalBundles']} "
        f"drafts_with_required_repair_refs={actual['draftsWithRequiredRepairRefs']} "
        f"drafts_with_blocked_reasons={actual['draftsWithBlockedReasons']} submits_evidence={actual['submitsEvidence']} "
        f"persists_evidence={actual['persistsEvidence']} creates_review_queue_items={actual['createsReviewQueueItems']} "
        f"creates_confirmation_records={actual['createsConfirmationRecords']} creates_decision_records={actual['createsDecisionRecords']} "
        f"creates_gap_records={actual['createsGapRecords']} creates_bounty_records={actual['createsBountyRecords']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"routes_to_human_queue={actual['routesToHumanQueue']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_review_queue_item=0 writes_confirmation_record=0 writes_decision_record=0 "
        "writes_gap_record=0 writes_bounty_record=0 writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
