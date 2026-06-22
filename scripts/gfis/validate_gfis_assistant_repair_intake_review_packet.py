#!/usr/bin/env python3
"""Validate GFIS Assistant repair intake review packet dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-intake-review-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-intake-review-packet.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-intake-review-packet-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesReviewQueueItem",
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
    packets: list[dict[str, Any]] = fixture["reviewPackets"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairIntakeReviewPacketType": policy["review_types"],
        "GfisAssistantRepairIntakeReviewPacketStatus": policy["review_statuses"],
        "GfisAssistantRepairIntakeReviewPacketDisplayAction": policy["allowed_display_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    review_types = set(policy["review_types"])
    review_statuses = set(policy["review_statuses"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "queuedPreview": 0,
        "needsRepair": 0,
        "blocked": 0,
        "metadataOnly": 0,
        "humanReviewPacket": 0,
        "metadataBoundaryPacket": 0,
        "committeeReviewPacket": 0,
        "freezeReviewPacket": 0,
        "blockedHoldPacket": 0,
        "metadataOnlyBundles": 0,
        "controlledOriginalBundles": 0,
        "packetsWithBlockedReasons": 0,
        "submitsEvidence": 0,
        "persistsEvidence": 0,
        "createsReviewQueueItems": 0,
        "createsGapRecords": 0,
        "createsBountyRecords": 0,
        "createsKweWorkItems": 0,
        "createsWaesGateResults": 0,
        "routesToHumanQueue": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
        "packetsWithBlockedActions": 0,
    }

    for packet in packets:
        packet_id = packet["reviewPacketId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in packet})
        if missing:
            failures.append(f"{packet_id} missing required fields: {missing}")
        if packet["reviewType"] not in review_types:
            failures.append(f"{packet_id}: invalid reviewType")
        if packet["reviewStatus"] not in review_statuses:
            failures.append(f"{packet_id}: invalid reviewStatus")
        if not packet["reviewerFocus"] or not packet["intakeItemRefs"]:
            failures.append(f"{packet_id}: reviewerFocus and intakeItemRefs are required")
        missing_blocks = sorted(blocked_actions - set(packet["blockedActions"]))
        if missing_blocks:
            failures.append(f"{packet_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(packet["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{packet_id}: unknown allowedDisplayActions {unknown_display}")

        bundle = packet["metadataRefBundle"]
        if not bundle["objectRefs"] or not bundle["sourceRefs"]:
            failures.append(f"{packet_id}: metadataRefBundle objectRefs and sourceRefs are required")
        if bundle["metadataOnly"] is True and not packet["evidenceHintRefs"]:
            failures.append(f"{packet_id}: metadata-only packet requires evidenceHintRefs")

        status_key = {
            "queued_preview": "queuedPreview",
            "needs_repair": "needsRepair",
            "blocked": "blocked",
            "metadata_only": "metadataOnly",
        }[packet["reviewStatus"]]
        type_key = {
            "human_review_packet": "humanReviewPacket",
            "metadata_boundary_packet": "metadataBoundaryPacket",
            "committee_review_packet": "committeeReviewPacket",
            "freeze_review_packet": "freezeReviewPacket",
            "blocked_hold_packet": "blockedHoldPacket",
        }[packet["reviewType"]]
        counts[status_key] += 1
        counts[type_key] += 1
        counts["metadataOnlyBundles"] += int(bundle["metadataOnly"] is True)
        counts["controlledOriginalBundles"] += int(bool(bundle["controlledOriginalRefs"]))
        counts["packetsWithBlockedReasons"] += int(bool(packet["blockedReasonRefs"]))
        counts["submitsEvidence"] += int(packet["submitsEvidence"] is True)
        counts["persistsEvidence"] += int(packet["persistsEvidence"] is True)
        counts["createsReviewQueueItems"] += int(packet["createsReviewQueueItem"] is True)
        counts["createsGapRecords"] += int(packet["createsGapRecord"] is True)
        counts["createsBountyRecords"] += int(packet["createsBountyRecord"] is True)
        counts["createsKweWorkItems"] += int(packet["createsKweWorkItem"] is True)
        counts["createsWaesGateResults"] += int(packet["createsWaesGateResult"] is True)
        counts["routesToHumanQueue"] += int(packet["routesToHumanQueue"] is True)
        counts["approvesBusinessWrite"] += int(packet["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(packet["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(packet["completesCommitteeDecision"] is True)
        counts["packetsWithBlockedActions"] += int(bool(packet["blockedActions"]))

        false_flags = (
            "submitsEvidence",
            "persistsEvidence",
            "createsReviewQueueItem",
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
            if packet[flag] is not False:
                failures.append(f"{packet_id}: {flag} must be false")

        ref_text = " ".join(
            packet["reviewerFocus"]
            + packet["intakeItemRefs"]
            + bundle["objectRefs"]
            + bundle["sourceRefs"]
            + bundle["controlledOriginalRefs"]
            + packet["evidenceHintRefs"]
            + packet["blockedReasonRefs"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{packet_id}: review packet must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = packet["noWrite"].get(key)
            if value != 0:
                failures.append(f"{packet_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "reviewPacketCount": len(packets),
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
        print("gfis_assistant_repair_intake_review_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_intake_review_packet=pass "
        f"packets={actual['reviewPacketCount']} needs_repair={actual['needsRepair']} "
        f"metadata_only={actual['metadataOnly']} blocked={actual['blocked']} "
        f"human_review_packet={actual['humanReviewPacket']} metadata_boundary_packet={actual['metadataBoundaryPacket']} "
        f"committee_review_packet={actual['committeeReviewPacket']} freeze_review_packet={actual['freezeReviewPacket']} "
        f"metadata_only_bundles={actual['metadataOnlyBundles']} controlled_original_bundles={actual['controlledOriginalBundles']} "
        f"packets_with_blocked_reasons={actual['packetsWithBlockedReasons']} submits_evidence={actual['submitsEvidence']} "
        f"persists_evidence={actual['persistsEvidence']} creates_review_queue_items={actual['createsReviewQueueItems']} "
        f"creates_gap_records={actual['createsGapRecords']} creates_bounty_records={actual['createsBountyRecords']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"routes_to_human_queue={actual['routesToHumanQueue']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_review_queue_item=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
