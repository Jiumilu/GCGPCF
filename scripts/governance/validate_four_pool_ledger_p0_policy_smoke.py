#!/usr/bin/env python3
"""Validate four-pool P0 ledger boundary.

This validator reads local OKF, shared type and fixture files only. It does not
confirm scores, distribute revenue, transfer quota, settle bounties, or call
external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "four-pool-ledger-p0-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "four-pool-ledger-p0.ts"
FIXTURE = ROOT / "fixtures" / "governance" / "four-pool-ledger-p0-policy-smoke.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]
    pools = policy["pools"]
    pool_names = list(pools.keys())
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("FourPoolLedger") != pool_names:
        failures.append("FourPoolLedger union does not match policy pools")
    for pool, config in pools.items():
        if not config["allowed_actions"]:
            failures.append(f"{pool} missing allowed actions")
        if not config["blocked_actions"]:
            failures.append(f"{pool} missing blocked actions")

    checks = {
        "poolCount": len(pool_names),
        "requiredPools": pool_names,
        "formalRevenueRequiresCashReceived": hard["formal_revenue_requires_cash_received"],
        "invoicedRevenueIsFinancialStatisticsOnly": hard["invoiced_revenue_is_financial_statistics_only"],
        "potentialRevenueMustNotAutoPromote": hard["potential_revenue_must_not_auto_promote"],
        "contributionConfirmedScoreRequiresHumanOrCommittee": hard[
            "contribution_confirmed_score_requires_human_or_committee"
        ],
        "selfPurchasedQuotaExcludedFromUnifiedRevenuePool": hard[
            "self_purchased_quota_excluded_from_unified_revenue_pool"
        ],
        "bountySettlementRequiresWaesHumanAcceptanceAndDisputeWindowClosed": hard[
            "bounty_settlement_requires_waes_human_acceptance_and_dispute_window_closed"
        ],
        "majorDisputeCanFreezeAllFourPools": hard["major_dispute_can_freeze_all_four_pools"],
        "writesScoreConfirmation": no_write["writes_score_confirmation"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesQuotaTransfer": no_write["writes_quota_transfer"],
        "writesBountySettlement": no_write["writes_bounty_settlement"],
        "writesExternalApi": no_write["writes_external_api"],
    }
    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("four_pool_ledger_p0_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "four_pool_ledger_p0_policy_smoke=pass "
        f"pools={checks['poolCount']} "
        "formal_revenue_requires_cash=true "
        "potential_no_auto_promote=covered "
        "self_purchased_quota_excluded=covered "
        "bounty_dispute_window_required=covered "
        "writes_score_confirmation=0 writes_revenue_distribution=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
