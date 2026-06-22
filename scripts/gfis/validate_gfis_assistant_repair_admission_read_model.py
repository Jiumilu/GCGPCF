#!/usr/bin/env python3
"""Validate GFIS Assistant repair admission read model dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-admission-read-model-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-admission-read-model.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-admission-read-model-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
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
    models: list[dict[str, Any]] = fixture["readModels"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairAdmissionReadModelSurface": policy["surfaces"],
        "GfisAssistantRepairAdmissionReadModelViewType": policy["view_types"],
        "GfisAssistantRepairAdmissionReadModelVisibilityMode": policy["visibility_modes"],
        "GfisAssistantRepairAdmissionReadModelDisplaySection": policy["display_sections"],
        "GfisAssistantRepairAdmissionReadModelBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    surfaces = set(policy["surfaces"])
    view_types = set(policy["view_types"])
    visibility_modes = set(policy["visibility_modes"])
    display_sections = set(policy["display_sections"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "brainGovernanceRead": 0,
        "pkcOwnerRead": 0,
        "gfisAssistantRead": 0,
        "committeeCandidateRead": 0,
        "freezeCandidateRead": 0,
        "ownProjectOnly": 0,
        "metadataOnly": 0,
        "governanceSummary": 0,
        "committeeAuthorized": 0,
        "freezeAuthorized": 0,
        "repairRequired": 0,
        "metadataOnlyAdmitted": 0,
        "committeeAgendaBlocked": 0,
        "freezeReviewBlocked": 0,
        "requireRepair": 0,
        "metadataOnlyReviewCandidate": 0,
        "prepareCommitteeAgendaCandidate": 0,
        "prepareFreezeReviewCandidate": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "modelsWithMaskedFields": 0,
        "modelsWithMissingRequirements": 0,
        "modelsWithBlockedReasons": 0,
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

    for model in models:
        model_id = model["readModelId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in model})
        if missing:
            failures.append(f"{model_id} missing required fields: {missing}")
        if model["surface"] not in surfaces:
            failures.append(f"{model_id}: invalid surface")
        if model["viewType"] not in view_types:
            failures.append(f"{model_id}: invalid viewType")
        if model["visibilityMode"] not in visibility_modes:
            failures.append(f"{model_id}: invalid visibilityMode")
        unknown_sections = sorted(set(model["displaySections"]) - display_sections)
        if unknown_sections:
            failures.append(f"{model_id}: unknown displaySections {unknown_sections}")
        missing_blocks = sorted(blocked_actions - set(model["blockedActions"]))
        if missing_blocks:
            failures.append(f"{model_id}: missing blockedActions {missing_blocks}")
        if "no_write_notice" not in model["displaySections"]:
            failures.append(f"{model_id}: no_write_notice display section is required")
        if not model["maskedFields"]:
            failures.append(f"{model_id}: maskedFields are required")

        bundle = model["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{model_id}: metadataRefBundle objectRefs and sourceRefs are required")

        counts[{"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}[model["surface"]]] += 1
        counts[
            {
                "brain_governance_read": "brainGovernanceRead",
                "pkc_owner_read": "pkcOwnerRead",
                "gfis_assistant_read": "gfisAssistantRead",
                "committee_candidate_read": "committeeCandidateRead",
                "freeze_candidate_read": "freezeCandidateRead",
            }[model["viewType"]]
        ] += 1
        counts[
            {
                "own_project_only": "ownProjectOnly",
                "metadata_only": "metadataOnly",
                "governance_summary": "governanceSummary",
                "committee_authorized": "committeeAuthorized",
                "freeze_authorized": "freezeAuthorized",
            }[model["visibilityMode"]]
        ] += 1
        counts[
            {
                "repair_required": "repairRequired",
                "metadata_only_admitted": "metadataOnlyAdmitted",
                "committee_agenda_blocked": "committeeAgendaBlocked",
                "freeze_review_blocked": "freezeReviewBlocked",
                "admitted_candidate": "admittedCandidate",
                "blocked_hold": "blockedHold",
            }.get(model["admissionStatus"], "blockedHold")
        ] = counts.get(
            {
                "repair_required": "repairRequired",
                "metadata_only_admitted": "metadataOnlyAdmitted",
                "committee_agenda_blocked": "committeeAgendaBlocked",
                "freeze_review_blocked": "freezeReviewBlocked",
                "admitted_candidate": "admittedCandidate",
                "blocked_hold": "blockedHold",
            }.get(model["admissionStatus"], "blockedHold"),
            0,
        ) + 1
        counts[
            {
                "require_repair": "requireRepair",
                "metadata_only_review_candidate": "metadataOnlyReviewCandidate",
                "prepare_committee_agenda_candidate": "prepareCommitteeAgendaCandidate",
                "prepare_freeze_review_candidate": "prepareFreezeReviewCandidate",
                "allow_review_candidate": "allowReviewCandidate",
                "hold_blocked": "holdBlocked",
            }.get(model["admissionDecision"], "holdBlocked")
        ] = counts.get(
            {
                "require_repair": "requireRepair",
                "metadata_only_review_candidate": "metadataOnlyReviewCandidate",
                "prepare_committee_agenda_candidate": "prepareCommitteeAgendaCandidate",
                "prepare_freeze_review_candidate": "prepareFreezeReviewCandidate",
                "allow_review_candidate": "allowReviewCandidate",
                "hold_blocked": "holdBlocked",
            }.get(model["admissionDecision"], "holdBlocked"),
            0,
        ) + 1
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["modelsWithMaskedFields"] += int(bool(model["maskedFields"]))
        counts["modelsWithMissingRequirements"] += int(bool(model["missingRequirementRefs"]))
        counts["modelsWithBlockedReasons"] += int(bool(model["blockedReasonRefs"]))

        false_flags = (
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
            if model[flag] is not False:
                failures.append(f"{model_id}: {flag} must be false")
        counts["createsReadReceipts"] += int(model["createsReadReceipt"] is True)
        counts["createsAdmissionRecords"] += int(model["createsAdmissionRecord"] is True)
        counts["createsReviewQueueItems"] += int(model["createsReviewQueueItem"] is True)
        counts["createsKweWorkItems"] += int(model["createsKweWorkItem"] is True)
        counts["createsConfirmationRecords"] += int(model["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(model["createsDecisionRecord"] is True)
        counts["createsWaesGateResults"] += int(model["createsWaesGateResult"] is True)
        counts["persistsEvidence"] += int(model["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(model["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(model["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(model["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            model["admissionPacketRef"].split()
            + model["handoffPacketRef"].split()
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + model["missingRequirementRefs"]
            + model["blockedReasonRefs"]
            + model["nextStepCandidateRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{model_id}: read model must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = model["noWrite"].get(key)
            if value != 0:
                failures.append(f"{model_id}: {key} must be 0")
            totals[key] += value

    actual = {"readModelCount": len(models), **counts, **totals}

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
        print("gfis_assistant_repair_admission_read_model=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_admission_read_model=pass "
        f"models={actual['readModelCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} repair_required={actual['repairRequired']} "
        f"metadata_only_admitted={actual['metadataOnlyAdmitted']} committee_agenda_blocked={actual['committeeAgendaBlocked']} "
        f"freeze_review_blocked={actual['freezeReviewBlocked']} metadata_only_bundles={actual['metadataOnlyBundles']} "
        f"controlled_original_bundles={actual['controlledOriginalBundles']} models_with_masked_fields={actual['modelsWithMaskedFields']} "
        f"models_with_missing_requirements={actual['modelsWithMissingRequirements']} "
        f"models_with_blocked_reasons={actual['modelsWithBlockedReasons']} creates_read_receipts={actual['createsReadReceipts']} "
        f"creates_admission_records={actual['createsAdmissionRecords']} creates_review_queue_items={actual['createsReviewQueueItems']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_confirmation_records={actual['createsConfirmationRecords']} "
        f"creates_decision_records={actual['createsDecisionRecords']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_read_receipt=0 writes_admission_record=0 "
        "writes_review_queue_item=0 writes_confirmation_record=0 writes_decision_record=0 "
        "writes_gap_record=0 writes_bounty_record=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_evidence_record=0 writes_target_receipt=0 "
        "writes_committee_decision_completion=0 writes_revenue_or_score_confirmation=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
