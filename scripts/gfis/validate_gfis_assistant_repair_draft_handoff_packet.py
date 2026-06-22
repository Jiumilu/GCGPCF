#!/usr/bin/env python3
"""Validate GFIS Assistant repair draft handoff packet dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-draft-handoff-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-draft-handoff-packet.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-draft-handoff-packet-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesHandoffRecord",
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
    handoffs: list[dict[str, Any]] = fixture["handoffPackets"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairDraftHandoffPacketType": policy["handoff_types"],
        "GfisAssistantRepairDraftHandoffPacketStatus": policy["handoff_statuses"],
        "GfisAssistantRepairDraftHandoffTargetCandidate": policy["target_candidates"],
        "GfisAssistantRepairDraftHandoffPacketDisplayAction": policy["allowed_display_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    handoff_types = set(policy["handoff_types"])
    handoff_statuses = set(policy["handoff_statuses"])
    target_candidates = set(policy["target_candidates"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "draft": 0,
        "readyForHandoffReview": 0,
        "needsRepair": 0,
        "blocked": 0,
        "metadataOnly": 0,
        "humanReviewHandoff": 0,
        "metadataBoundaryHandoff": 0,
        "committeeAgendaHandoff": 0,
        "freezeReviewHandoff": 0,
        "blockedHoldHandoff": 0,
        "kweHumanReviewCandidate": 0,
        "metadataBoundaryReviewCandidate": 0,
        "committeeAgendaCandidate": 0,
        "freezeReviewCandidate": 0,
        "blockedHoldCandidate": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "handoffsWithRequiredRepairRefs": 0,
        "handoffsWithBlockedReasons": 0,
        "submitsEvidence": 0,
        "persistsEvidence": 0,
        "createsHandoffRecords": 0,
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
        "handoffsWithBlockedActions": 0,
    }

    for handoff in handoffs:
        handoff_id = handoff["handoffPacketId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in handoff})
        if missing:
            failures.append(f"{handoff_id} missing required fields: {missing}")
        if handoff["handoffType"] not in handoff_types:
            failures.append(f"{handoff_id}: invalid handoffType")
        if handoff["handoffStatus"] not in handoff_statuses:
            failures.append(f"{handoff_id}: invalid handoffStatus")
        if handoff["targetCandidate"] not in target_candidates:
            failures.append(f"{handoff_id}: invalid targetCandidate")
        if not handoff["handoffNoteRefs"]:
            failures.append(f"{handoff_id}: handoffNoteRefs are required")
        missing_blocks = sorted(blocked_actions - set(handoff["blockedActions"]))
        if missing_blocks:
            failures.append(f"{handoff_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(handoff["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{handoff_id}: unknown allowedDisplayActions {unknown_display}")

        bundle = handoff["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{handoff_id}: metadataRefBundle objectRefs and sourceRefs are required")
        if bundle["metadataOnly"] is True and not handoff["evidenceHintRefs"]:
            failures.append(f"{handoff_id}: metadata-only handoff requires evidenceHintRefs")

        status_key = {
            "draft": "draft",
            "ready_for_handoff_review": "readyForHandoffReview",
            "needs_repair": "needsRepair",
            "blocked": "blocked",
            "metadata_only": "metadataOnly",
        }[handoff["handoffStatus"]]
        type_key = {
            "human_review_handoff": "humanReviewHandoff",
            "metadata_boundary_handoff": "metadataBoundaryHandoff",
            "committee_agenda_handoff": "committeeAgendaHandoff",
            "freeze_review_handoff": "freezeReviewHandoff",
            "blocked_hold_handoff": "blockedHoldHandoff",
        }[handoff["handoffType"]]
        target_key = {
            "kwe_human_review_candidate": "kweHumanReviewCandidate",
            "metadata_boundary_review_candidate": "metadataBoundaryReviewCandidate",
            "committee_agenda_candidate": "committeeAgendaCandidate",
            "freeze_review_candidate": "freezeReviewCandidate",
            "blocked_hold_candidate": "blockedHoldCandidate",
        }[handoff["targetCandidate"]]
        counts[status_key] += 1
        counts[type_key] += 1
        counts[target_key] += 1
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["handoffsWithRequiredRepairRefs"] += int(bool(handoff["requiredRepairRefs"]))
        counts["handoffsWithBlockedReasons"] += int(bool(handoff["blockedReasonRefs"]))
        counts["submitsEvidence"] += int(handoff["submitsEvidence"] is True)
        counts["persistsEvidence"] += int(handoff["persistsEvidence"] is True)
        counts["createsHandoffRecords"] += int(handoff["createsHandoffRecord"] is True)
        counts["createsReviewQueueItems"] += int(handoff["createsReviewQueueItem"] is True)
        counts["createsConfirmationRecords"] += int(handoff["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(handoff["createsDecisionRecord"] is True)
        counts["createsGapRecords"] += int(handoff["createsGapRecord"] is True)
        counts["createsBountyRecords"] += int(handoff["createsBountyRecord"] is True)
        counts["createsKweWorkItems"] += int(handoff["createsKweWorkItem"] is True)
        counts["createsWaesGateResults"] += int(handoff["createsWaesGateResult"] is True)
        counts["routesToHumanQueue"] += int(handoff["routesToHumanQueue"] is True)
        counts["approvesBusinessWrite"] += int(handoff["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(handoff["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(handoff["completesCommitteeDecision"] is True)
        counts["handoffsWithBlockedActions"] += int(bool(handoff["blockedActions"]))

        false_flags = (
            "submitsEvidence",
            "persistsEvidence",
            "createsHandoffRecord",
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
            if handoff[flag] is not False:
                failures.append(f"{handoff_id}: {flag} must be false")

        ref_text = " ".join(
            handoff["handoffNoteRefs"]
            + handoff["requiredRepairRefs"]
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + handoff["evidenceHintRefs"]
            + handoff["blockedReasonRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{handoff_id}: handoff packet must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = handoff["noWrite"].get(key)
            if value != 0:
                failures.append(f"{handoff_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "handoffPacketCount": len(handoffs),
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
        print("gfis_assistant_repair_draft_handoff_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_draft_handoff_packet=pass "
        f"handoffs={actual['handoffPacketCount']} needs_repair={actual['needsRepair']} "
        f"metadata_only={actual['metadataOnly']} blocked={actual['blocked']} "
        f"human_review_handoff={actual['humanReviewHandoff']} metadata_boundary_handoff={actual['metadataBoundaryHandoff']} "
        f"committee_agenda_handoff={actual['committeeAgendaHandoff']} freeze_review_handoff={actual['freezeReviewHandoff']} "
        f"kwe_human_review_candidate={actual['kweHumanReviewCandidate']} "
        f"metadata_boundary_review_candidate={actual['metadataBoundaryReviewCandidate']} "
        f"committee_agenda_candidate={actual['committeeAgendaCandidate']} freeze_review_candidate={actual['freezeReviewCandidate']} "
        f"metadata_only_bundles={actual['metadataOnlyBundles']} controlled_original_bundles={actual['controlledOriginalBundles']} "
        f"handoffs_with_required_repair_refs={actual['handoffsWithRequiredRepairRefs']} "
        f"handoffs_with_blocked_reasons={actual['handoffsWithBlockedReasons']} submits_evidence={actual['submitsEvidence']} "
        f"persists_evidence={actual['persistsEvidence']} creates_handoff_records={actual['createsHandoffRecords']} "
        f"creates_review_queue_items={actual['createsReviewQueueItems']} creates_confirmation_records={actual['createsConfirmationRecords']} "
        f"creates_decision_records={actual['createsDecisionRecords']} creates_gap_records={actual['createsGapRecords']} "
        f"creates_bounty_records={actual['createsBountyRecords']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} routes_to_human_queue={actual['routesToHumanQueue']} "
        f"approves_business_write={actual['approvesBusinessWrite']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_handoff_record=0 writes_review_queue_item=0 "
        "writes_confirmation_record=0 writes_decision_record=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
