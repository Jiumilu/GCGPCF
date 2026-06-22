#!/usr/bin/env python3
"""Validate GC-Knowledge Fabric governance ledger dry-run rules.

This script uses local fixtures only. It does not distribute revenue,
mutate quota balances, settle bounties, or write KDS/GFIS/GPC records.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "governance" / "ledger-dry-run.json"


def has_evidence(record: dict[str, Any]) -> bool:
    refs = record.get("evidenceRefs")
    return isinstance(refs, list) and len(refs) > 0


def contribution_confirmed(record: dict[str, Any]) -> bool:
    return record.get("confirmationStatus") in {"human_confirmed", "committee_confirmed"}


def revenue_distribution_eligible(record: dict[str, Any]) -> bool:
    return (
        record.get("revenueType") == "formal_revenue"
        and record.get("basis") == "cash_received"
        and has_evidence(record)
        and record.get("distributionStatus") == "confirmed"
    )


def quota_valid(record: dict[str, Any]) -> bool:
    if record.get("usedAmount", 0) > record.get("amount", 0):
        return False
    if record.get("quotaType") == "self_purchased_quota" and record.get("revenuePoolEligible") is True:
        return False
    return True


def bounty_settlement_eligible(record: dict[str, Any]) -> bool:
    return bool(record.get("gapRef")) and record.get("status") in {"accepted", "partially_accepted"} and has_evidence(record)


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []

    confirmed_contributions = sum(1 for item in data["contributions"] if contribution_confirmed(item))
    formal_distribution_eligible = sum(1 for item in data["revenues"] if revenue_distribution_eligible(item))
    valid_quotas = sum(1 for item in data["quotas"] if quota_valid(item))
    invalid_quotas = len(data["quotas"]) - valid_quotas
    settlement_eligible_bounties = sum(1 for item in data["bounties"] if bounty_settlement_eligible(item))

    expected = data["expected"]
    actual = {
        "formalDistributionEligible": formal_distribution_eligible,
        "confirmedContributions": confirmed_contributions,
        "validQuotas": valid_quotas,
        "invalidQuotas": invalid_quotas,
        "settlementEligibleBounties": settlement_eligible_bounties,
        "realRevenueDistributions": 0,
        "realQuotaMutations": 0,
        "realBountySettlements": 0,
    }

    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    for item in data["contributions"]:
        if contribution_confirmed(item) != item["expectedConfirmed"]:
            failures.append(f"{item['id']} contribution confirmation mismatch")
    for item in data["revenues"]:
        if revenue_distribution_eligible(item) != item["expectedDistributionEligible"]:
            failures.append(f"{item['id']} revenue eligibility mismatch")
    for item in data["quotas"]:
        if quota_valid(item) != item["expectedValid"]:
            failures.append(f"{item['id']} quota validity mismatch")
    for item in data["bounties"]:
        if bounty_settlement_eligible(item) != item["expectedSettlementEligible"]:
            failures.append(f"{item['id']} bounty settlement mismatch")

    if failures:
        print("governance_ledger_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "governance_ledger_dry_run=pass "
        f"contributions={len(data['contributions'])} "
        f"revenues={len(data['revenues'])} "
        f"quotas={len(data['quotas'])} "
        f"bounties={len(data['bounties'])} "
        f"formal_distribution_eligible={formal_distribution_eligible} "
        f"confirmed_contributions={confirmed_contributions} "
        f"valid_quotas={valid_quotas} invalid_quotas={invalid_quotas} "
        f"settlement_eligible_bounties={settlement_eligible_bounties} "
        "real_revenue_distributions=0 real_quota_mutations=0 real_bounty_settlements=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
