#!/usr/bin/env python3
"""Validate GFIS Assistant WAES guidance packet dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-waes-guidance-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-waes-guidance-packet.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "waes-guidance-packet-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
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
    packets: list[dict[str, Any]] = fixture["packets"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantWaesGuidanceSurface": policy["assistant_surfaces"],
        "GfisAssistantWaesGuidanceMode": policy["guidance_modes"],
        "GfisAssistantWaesAllowedAction": policy["allowed_assistant_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    surfaces = set(policy["assistant_surfaces"])
    modes = set(policy["guidance_modes"])
    allowed_actions = set(policy["allowed_assistant_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "writebackBlocked": 0,
        "metadataOnlyGuidance": 0,
        "committeeGuidance": 0,
        "freezeGuidance": 0,
        "approvedForBusinessWrite": 0,
        "createsWaesGateResults": 0,
        "createsKweWorkItems": 0,
        "promotesLifecycle": 0,
        "packetsWithBlockedActions": 0,
    }

    for packet in packets:
        packet_id = packet["packetId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in packet})
        if missing:
            failures.append(f"{packet_id} missing required fields: {missing}")
        if packet["assistantSurface"] not in surfaces:
            failures.append(f"{packet_id}: invalid assistantSurface")
        if packet["guidanceMode"] not in modes:
            failures.append(f"{packet_id}: invalid guidanceMode")
        if not packet["writebackExplanation"]:
            failures.append(f"{packet_id}: writebackExplanation is required")
        if not packet["repairPrompts"]:
            failures.append(f"{packet_id}: repairPrompts are required")
        unknown_allowed = sorted(set(packet["allowedAssistantActions"]) - allowed_actions)
        if unknown_allowed:
            failures.append(f"{packet_id}: unknown allowedAssistantActions {unknown_allowed}")
        missing_blocks = sorted(blocked_actions - set(packet["blockedActions"]))
        if missing_blocks:
            failures.append(f"{packet_id}: missing blockedActions {missing_blocks}")

        counts["writebackBlocked"] += int(packet["guidanceMode"] == "writeback_blocked")
        counts["metadataOnlyGuidance"] += int(packet["guidanceMode"] == "metadata_only_guidance")
        counts["committeeGuidance"] += int(packet["guidanceMode"] == "committee_guidance")
        counts["freezeGuidance"] += int(packet["guidanceMode"] == "freeze_guidance")
        counts["approvedForBusinessWrite"] += int(packet["approvedForBusinessWrite"] is True)
        counts["createsWaesGateResults"] += int(packet["createsWaesGateResult"] is True)
        counts["createsKweWorkItems"] += int(packet["createsKweWorkItem"] is True)
        counts["promotesLifecycle"] += int(packet["promotesLifecycle"] is True)
        counts["packetsWithBlockedActions"] += int(bool(packet["blockedActions"]))

        if packet["approvedForBusinessWrite"] is not False:
            failures.append(f"{packet_id}: approvedForBusinessWrite must be false")
        if packet["createsWaesGateResult"] is not False:
            failures.append(f"{packet_id}: createsWaesGateResult must be false")
        if packet["createsKweWorkItem"] is not False:
            failures.append(f"{packet_id}: createsKweWorkItem must be false")
        if packet["promotesLifecycle"] is not False:
            failures.append(f"{packet_id}: promotesLifecycle must be false")
        if packet["guidanceMode"] == "metadata_only_guidance" and not packet["metadataOnlyHints"]:
            failures.append(f"{packet_id}: metadata_only_guidance requires metadataOnlyHints")
        if packet["guidanceMode"] == "committee_guidance" and not packet["committeeTriggers"]:
            failures.append(f"{packet_id}: committee_guidance requires committeeTriggers")
        if packet["guidanceMode"] == "freeze_guidance" and not packet["committeeTriggers"]:
            failures.append(f"{packet_id}: freeze_guidance requires risk or committee triggers")

        raw_tokens = " ".join(packet["metadataOnlyHints"] + packet["repairPrompts"])
        if "raw" in raw_tokens or "原文" in raw_tokens:
            failures.append(f"{packet_id}: guidance must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = packet["noWrite"].get(key)
            if value != 0:
                failures.append(f"{packet_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "packetCount": len(packets),
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
        print("gfis_assistant_waes_guidance_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_waes_guidance_packet=pass "
        f"packets={actual['packetCount']} writeback_blocked={actual['writebackBlocked']} "
        f"metadata_only_guidance={actual['metadataOnlyGuidance']} committee_guidance={actual['committeeGuidance']} "
        f"freeze_guidance={actual['freezeGuidance']} approved_for_business_write={actual['approvedForBusinessWrite']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} packets_with_blocked_actions={actual['packetsWithBlockedActions']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_target_receipt=0 "
        "writes_committee_decision_completion=0 writes_revenue_or_score_confirmation=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
