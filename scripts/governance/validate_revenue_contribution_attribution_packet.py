#!/usr/bin/env python3
"""Validate revenue/contribution attribution packet dry-run boundaries.

This validator reads local OKF, fixture, and shared type files only. It does
not confirm scores, distribute revenue, transfer quota, settle bounties, write
business systems, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "revenue-contribution-attribution-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "revenue-contribution-attribution-packet.ts"
FIXTURE = ROOT / "fixtures" / "governance" / "revenue-contribution-attribution-packet-dry-run.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def has_confirmed_contribution(packet: dict[str, Any]) -> bool:
    return any(
        ref.get("confirmationStatus") in {"human_confirmed", "committee_confirmed"}
        for ref in packet["contributionRefs"]
    )


def no_write_total(packet: dict[str, Any], *keys: str) -> int:
    no_write = packet["noWrite"]
    return sum(int(no_write[key]) for key in keys)


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    packets: list[dict[str, Any]] = fixture["packets"]
    expected = fixture["expected"]

    failures: list[str] = []
    required_fields = set(policy["required_fields"])
    hard = policy["hard_boundaries"]
    no_write_policy = policy["no_write_assertions"]

    if union_literals("RevenueContributionAttributionBasis") != policy["attribution_basis"]:
        failures.append("RevenueContributionAttributionBasis union does not match policy")
    if union_literals("RevenueContributionAttributionStatus") != policy["attribution_status"]:
        failures.append("RevenueContributionAttributionStatus union does not match policy")

    for packet in packets:
        normalized_keys = {re.sub(r"(?<!^)([A-Z])", r"_\1", key).lower() for key in packet}
        missing = sorted(required_fields - normalized_keys)
        if missing:
            failures.append(f"{packet['id']} missing required fields: {missing}")
        if no_write_total(
            packet,
            "writesScoreConfirmation",
            "writesRevenueDistribution",
            "writesQuotaTransfer",
            "writesBountySettlement",
            "writesKdsFact",
            "writesBusinessSystem",
            "writesExternalApi",
        ):
            failures.append(f"{packet['id']} has non-zero noWrite counters")

        is_distribution_candidate = packet["attributionStatus"] == "distribution_candidate"
        if is_distribution_candidate:
            if packet["revenueType"] != "formal_revenue" or packet["revenueBasis"] != "cash_received":
                failures.append(f"{packet['id']} distribution candidate without formal cash received")
            if not packet["evidenceRefs"] or not packet["waesGateRefs"]:
                failures.append(f"{packet['id']} distribution candidate missing evidence or WAES gate")
            if not has_confirmed_contribution(packet):
                failures.append(f"{packet['id']} distribution candidate without confirmed contribution")
            if packet["freezeRecommended"]:
                failures.append(f"{packet['id']} frozen record marked as distribution candidate")

        if packet["revenueType"] == "invoiced_revenue" and is_distribution_candidate:
            failures.append(f"{packet['id']} treats invoice as distribution candidate")
        if packet["revenueType"] == "potential_revenue" and is_distribution_candidate:
            failures.append(f"{packet['id']} auto-promotes potential revenue")
        if packet["revenueType"] == "channel_opportunity" and is_distribution_candidate:
            failures.append(f"{packet['id']} treats channel opportunity as distribution candidate")

    checks = {
        "packetCount": len(packets),
        "formalDistributionCandidates": sum(
            1 for packet in packets if packet["attributionStatus"] == "distribution_candidate"
        ),
        "invoicedStatisticalOnly": sum(
            1
            for packet in packets
            if packet["revenueType"] == "invoiced_revenue"
            and packet["attributionBasis"] == "invoice_statistical"
            and packet["attributionStatus"] != "distribution_candidate"
        ),
        "potentialNotPromoted": sum(
            1
            for packet in packets
            if packet["revenueType"] == "potential_revenue"
            and packet["attributionStatus"] != "distribution_candidate"
            and packet["committeeRequired"]
        ),
        "channelReferenceOnly": sum(
            1
            for packet in packets
            if packet["revenueType"] == "channel_opportunity"
            and packet["attributionBasis"] == "channel_reference"
            and packet["attributionStatus"] != "distribution_candidate"
        ),
        "committeeRequired": sum(1 for packet in packets if packet["committeeRequired"]),
        "freezeRecommended": sum(1 for packet in packets if packet["freezeRecommended"]),
        "scoreConfirmations": sum(packet["noWrite"]["writesScoreConfirmation"] for packet in packets),
        "revenueDistributions": sum(packet["noWrite"]["writesRevenueDistribution"] for packet in packets),
        "quotaTransfers": sum(packet["noWrite"]["writesQuotaTransfer"] for packet in packets),
        "bountySettlements": sum(packet["noWrite"]["writesBountySettlement"] for packet in packets),
        "businessWrites": sum(packet["noWrite"]["writesBusinessSystem"] for packet in packets),
        "externalApiWrites": sum(packet["noWrite"]["writesExternalApi"] for packet in packets),
    }

    if not hard["formal_distribution_requires_cash_received"]:
        failures.append("policy does not require cash received for formal distribution")
    if not hard["invoiced_is_statistics_only"]:
        failures.append("policy does not keep invoiced revenue as statistics only")
    if not hard["potential_must_not_auto_promote"]:
        failures.append("policy allows potential revenue auto-promotion")
    for key, value in no_write_policy.items():
        if value != 0:
            failures.append(f"policy no_write_assertions.{key} is non-zero")

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("revenue_contribution_attribution_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "revenue_contribution_attribution_packet=pass "
        f"packets={checks['packetCount']} "
        f"formal_distribution_candidates={checks['formalDistributionCandidates']} "
        f"invoiced_statistical_only={checks['invoicedStatisticalOnly']} "
        f"potential_not_promoted={checks['potentialNotPromoted']} "
        f"channel_reference_only={checks['channelReferenceOnly']} "
        f"committee_required={checks['committeeRequired']} "
        f"freeze_recommended={checks['freezeRecommended']} "
        "score_confirmations=0 revenue_distributions=0 quota_transfers=0 "
        "bounty_settlements=0 business_writes=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
