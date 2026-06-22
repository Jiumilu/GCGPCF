#!/usr/bin/env python3
"""Validate Committee DecisionRecord IO and dispute freeze policy.

This validator reads local OKF, shared type and fixture files only. It does not
write business systems, distribute revenue, confirm scores, transfer quota,
settle bounties, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "committee-decision-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "committee-decision.ts"
FIXTURE = ROOT / "fixtures" / "governance" / "committee-decision-policy-smoke.json"


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
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("CommitteeDecisionTrigger") != policy["decision_triggers"]:
        failures.append("CommitteeDecisionTrigger union does not match policy")
    if union_literals("CommitteeFreezeScope") != policy["freeze_scopes"]:
        failures.append("CommitteeFreezeScope union does not match policy")
    if union_literals("CommitteeDecisionReasonCode") != policy["reason_codes"]:
        failures.append("CommitteeDecisionReasonCode union does not match policy")
    if union_literals("CommitteeVotingMethod") != policy["voting_methods"]:
        failures.append("CommitteeVotingMethod union does not match policy")

    checks = {
        "decisionTriggerCount": len(policy["decision_triggers"]),
        "minimumInputFieldCount": len(policy["minimum_input_fields"]),
        "minimumOutputFieldCount": len(policy["minimum_output_fields"]),
        "freezeScopeCount": len(policy["freeze_scopes"]),
        "reasonCodeCount": len(policy["reason_codes"]),
        "votingMethodCount": len(policy["voting_methods"]),
        "decisionDomain": hard["decision_domain"],
        "committeeDoesNotReplaceWaesGate": hard["committee_does_not_replace_waes_gate"],
        "committeeCannotWriteBusinessSystem": hard["committee_cannot_write_business_system"],
        "committeeCannotDirectlyDistributeRevenue": hard["committee_cannot_directly_distribute_revenue"],
        "committeeCannotDirectlyConfirmScore": hard["committee_cannot_directly_confirm_score"],
        "harnessEvidenceRequired": hard["harness_evidence_required"],
        "externalAccountAuthorizedViewOnly": hard["external_account_authorized_view_only"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesScoreConfirmation": no_write["writes_score_confirmation"],
        "writesQuotaTransfer": no_write["writes_quota_transfer"],
        "writesBountySettlement": no_write["writes_bounty_settlement"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("committee_decision_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "committee_decision_policy_smoke=pass "
        f"triggers={checks['decisionTriggerCount']} "
        f"input_fields={checks['minimumInputFieldCount']} "
        f"output_fields={checks['minimumOutputFieldCount']} "
        f"freeze_scopes={checks['freezeScopeCount']} "
        "decision_domain=governance "
        "waes_not_replaced=covered "
        "harness_evidence_required=true "
        "writes_business_system=0 writes_revenue_distribution=0 "
        "writes_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
