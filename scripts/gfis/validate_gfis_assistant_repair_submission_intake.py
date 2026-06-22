#!/usr/bin/env python3
"""Validate GFIS Assistant repair submission intake dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-submission-intake-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-submission-intake.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-submission-intake-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
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
    intakes: list[dict[str, Any]] = fixture["intakes"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairSubmissionIntakeStatus": policy["intake_statuses"],
        "GfisAssistantRepairSubmissionRecommendedRoute": policy["recommended_routes"],
        "GfisAssistantRepairSubmissionDisplayAction": policy["allowed_display_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    intake_statuses = set(policy["intake_statuses"])
    recommended_routes = set(policy["recommended_routes"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "draft": 0,
        "readyForReview": 0,
        "repairRequired": 0,
        "blocked": 0,
        "humanReview": 0,
        "committeeReview": 0,
        "metadataBoundaryReview": 0,
        "freezeReview": 0,
        "blockedHold": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "intakesWithBlockedReasons": 0,
        "submitsEvidence": 0,
        "persistsEvidence": 0,
        "createsGapRecords": 0,
        "createsBountyRecords": 0,
        "createsKweWorkItems": 0,
        "createsWaesGateResults": 0,
        "routesToHumanQueue": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
        "intakesWithBlockedActions": 0,
    }

    for intake in intakes:
        intake_id = intake["intakeId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in intake})
        if missing:
            failures.append(f"{intake_id} missing required fields: {missing}")
        if intake["intakeStatus"] not in intake_statuses:
            failures.append(f"{intake_id}: invalid intakeStatus")
        if intake["recommendedRoute"] not in recommended_routes:
            failures.append(f"{intake_id}: invalid recommendedRoute")
        if not intake["submittedItemRefs"]:
            failures.append(f"{intake_id}: submittedItemRefs are required")
        missing_blocks = sorted(blocked_actions - set(intake["blockedActions"]))
        if missing_blocks:
            failures.append(f"{intake_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(intake["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{intake_id}: unknown allowedDisplayActions {unknown_display}")

        bundle = intake["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{intake_id}: metadataRefBundle objectRefs and sourceRefs are required")
        if bundle["metadataOnly"] is True and not intake["evidenceHintRefs"]:
            failures.append(f"{intake_id}: metadata-only intake requires evidenceHintRefs")

        status_key = {
            "draft": "draft",
            "ready_for_review": "readyForReview",
            "repair_required": "repairRequired",
            "blocked": "blocked",
        }[intake["intakeStatus"]]
        route_key = {
            "human_review": "humanReview",
            "committee_review": "committeeReview",
            "metadata_boundary_review": "metadataBoundaryReview",
            "freeze_review": "freezeReview",
            "blocked_hold": "blockedHold",
        }[intake["recommendedRoute"]]
        counts[status_key] += 1
        counts[route_key] += 1
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["intakesWithBlockedReasons"] += int(bool(intake["blockedReasonRefs"]))
        counts["submitsEvidence"] += int(intake["submitsEvidence"] is True)
        counts["persistsEvidence"] += int(intake["persistsEvidence"] is True)
        counts["createsGapRecords"] += int(intake["createsGapRecord"] is True)
        counts["createsBountyRecords"] += int(intake["createsBountyRecord"] is True)
        counts["createsKweWorkItems"] += int(intake["createsKweWorkItem"] is True)
        counts["createsWaesGateResults"] += int(intake["createsWaesGateResult"] is True)
        counts["routesToHumanQueue"] += int(intake["routesToHumanQueue"] is True)
        counts["approvesBusinessWrite"] += int(intake["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(intake["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(intake["completesCommitteeDecision"] is True)
        counts["intakesWithBlockedActions"] += int(bool(intake["blockedActions"]))

        false_flags = (
            "submitsEvidence",
            "persistsEvidence",
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
            if intake[flag] is not False:
                failures.append(f"{intake_id}: {flag} must be false")

        ref_text = " ".join(
            intake["submittedItemRefs"]
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + intake["evidenceHintRefs"]
            + intake["blockedReasonRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{intake_id}: intake must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = intake["noWrite"].get(key)
            if value != 0:
                failures.append(f"{intake_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "intakeCount": len(intakes),
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
        print("gfis_assistant_repair_submission_intake=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_submission_intake=pass "
        f"intakes={actual['intakeCount']} ready_for_review={actual['readyForReview']} "
        f"repair_required={actual['repairRequired']} blocked={actual['blocked']} "
        f"human_review={actual['humanReview']} committee_review={actual['committeeReview']} "
        f"metadata_boundary_review={actual['metadataBoundaryReview']} freeze_review={actual['freezeReview']} "
        f"metadata_only_bundles={actual['metadataOnlyBundles']} controlled_original_bundles={actual['controlledOriginalBundles']} "
        f"intakes_with_blocked_reasons={actual['intakesWithBlockedReasons']} submits_evidence={actual['submitsEvidence']} "
        f"persists_evidence={actual['persistsEvidence']} creates_gap_records={actual['createsGapRecords']} "
        f"creates_bounty_records={actual['createsBountyRecords']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} routes_to_human_queue={actual['routesToHumanQueue']} "
        f"approves_business_write={actual['approvesBusinessWrite']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
