#!/usr/bin/env python3
"""Validate GFIS Assistant repair handoff review admission dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-handoff-review-admission-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-handoff-review-admission.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-handoff-review-admission-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
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
    packets: list[dict[str, Any]] = fixture["admissionPackets"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairHandoffReviewAdmissionStatus": policy["admission_statuses"],
        "GfisAssistantRepairHandoffReviewAdmissionDecision": policy["admission_decisions"],
        "GfisAssistantRepairHandoffReviewAdmissionDisplayAction": policy["allowed_display_actions"],
        "GfisAssistantRepairHandoffReviewAdmissionBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    statuses = set(policy["admission_statuses"])
    decisions = set(policy["admission_decisions"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "admittedCandidate": 0,
        "repairRequired": 0,
        "metadataOnlyAdmitted": 0,
        "committeeAgendaBlocked": 0,
        "freezeReviewBlocked": 0,
        "blockedHold": 0,
        "allowReviewCandidate": 0,
        "requireRepair": 0,
        "metadataOnlyReviewCandidate": 0,
        "prepareCommitteeAgendaCandidate": 0,
        "prepareFreezeReviewCandidate": 0,
        "holdBlocked": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "packetsWithMissingRequirements": 0,
        "packetsWithBlockedReasons": 0,
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

    for packet in packets:
        packet_id = packet["admissionPacketId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in packet})
        if missing:
            failures.append(f"{packet_id} missing required fields: {missing}")
        if packet["admissionStatus"] not in statuses:
            failures.append(f"{packet_id}: invalid admissionStatus")
        if packet["admissionDecision"] not in decisions:
            failures.append(f"{packet_id}: invalid admissionDecision")
        if not packet["handoffPacketRef"] or not packet["admissionCheckRefs"]:
            failures.append(f"{packet_id}: handoffPacketRef and admissionCheckRefs are required")
        missing_blocks = sorted(blocked_actions - set(packet["blockedActions"]))
        if missing_blocks:
            failures.append(f"{packet_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(packet["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{packet_id}: unknown allowedDisplayActions {unknown_display}")

        status_key = {
            "admitted_candidate": "admittedCandidate",
            "repair_required": "repairRequired",
            "metadata_only_admitted": "metadataOnlyAdmitted",
            "committee_agenda_blocked": "committeeAgendaBlocked",
            "freeze_review_blocked": "freezeReviewBlocked",
            "blocked_hold": "blockedHold",
        }[packet["admissionStatus"]]
        decision_key = {
            "allow_review_candidate": "allowReviewCandidate",
            "require_repair": "requireRepair",
            "metadata_only_review_candidate": "metadataOnlyReviewCandidate",
            "prepare_committee_agenda_candidate": "prepareCommitteeAgendaCandidate",
            "prepare_freeze_review_candidate": "prepareFreezeReviewCandidate",
            "hold_blocked": "holdBlocked",
        }[packet["admissionDecision"]]
        counts[status_key] += 1
        counts[decision_key] += 1

        bundle = packet["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{packet_id}: metadataRefBundle objectRefs and sourceRefs are required")
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["packetsWithMissingRequirements"] += int(bool(packet["missingRequirementRefs"]))
        counts["packetsWithBlockedReasons"] += int(bool(packet["blockedReasonRefs"]))

        false_flags = (
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
            counts[f"{flag}s" if flag != "persistsEvidence" else "persistsEvidence"] = counts.get(
                f"{flag}s" if flag != "persistsEvidence" else "persistsEvidence", 0
            )
            if packet[flag] is not False:
                failures.append(f"{packet_id}: {flag} must be false")

        counts["createsAdmissionRecords"] += int(packet["createsAdmissionRecord"] is True)
        counts["createsReviewQueueItems"] += int(packet["createsReviewQueueItem"] is True)
        counts["createsKweWorkItems"] += int(packet["createsKweWorkItem"] is True)
        counts["createsConfirmationRecords"] += int(packet["createsConfirmationRecord"] is True)
        counts["createsDecisionRecords"] += int(packet["createsDecisionRecord"] is True)
        counts["createsWaesGateResults"] += int(packet["createsWaesGateResult"] is True)
        counts["persistsEvidence"] += int(packet["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(packet["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(packet["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(packet["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            packet["admissionCheckRefs"]
            + packet["missingRequirementRefs"]
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + packet["blockedReasonRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{packet_id}: admission packet must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = packet["noWrite"].get(key)
            if value != 0:
                failures.append(f"{packet_id}: {key} must be 0")
            totals[key] += value

    actual = {"admissionPacketCount": len(packets), **counts, **totals}

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
        print("gfis_assistant_repair_handoff_review_admission=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_handoff_review_admission=pass "
        f"packets={actual['admissionPacketCount']} repair_required={actual['repairRequired']} "
        f"metadata_only_admitted={actual['metadataOnlyAdmitted']} committee_agenda_blocked={actual['committeeAgendaBlocked']} "
        f"freeze_review_blocked={actual['freezeReviewBlocked']} require_repair={actual['requireRepair']} "
        f"metadata_only_review_candidate={actual['metadataOnlyReviewCandidate']} "
        f"prepare_committee_agenda_candidate={actual['prepareCommitteeAgendaCandidate']} "
        f"prepare_freeze_review_candidate={actual['prepareFreezeReviewCandidate']} "
        f"metadata_only_bundles={actual['metadataOnlyBundles']} controlled_original_bundles={actual['controlledOriginalBundles']} "
        f"packets_with_missing_requirements={actual['packetsWithMissingRequirements']} "
        f"packets_with_blocked_reasons={actual['packetsWithBlockedReasons']} creates_admission_records={actual['createsAdmissionRecords']} "
        f"creates_review_queue_items={actual['createsReviewQueueItems']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"creates_confirmation_records={actual['createsConfirmationRecords']} creates_decision_records={actual['createsDecisionRecords']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} persists_evidence={actual['persistsEvidence']} "
        f"approves_business_write={actual['approvesBusinessWrite']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_admission_record=0 writes_review_queue_item=0 "
        "writes_confirmation_record=0 writes_decision_record=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
