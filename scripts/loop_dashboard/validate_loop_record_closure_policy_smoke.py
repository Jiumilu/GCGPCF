#!/usr/bin/env python3
"""Validate LOOP record schema and next-action closure gate.

This validator reads local OKF, shared type and fixture files only. It does not
write LOOP state, Harness evidence, KDS, WAES, KWE, business systems, ledgers,
committee records, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "loop-record-closure-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "loop-record-closure.ts"
FIXTURE = ROOT / "fixtures" / "loop-dashboard" / "loop-record-closure-policy-smoke.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def camel_from_snake(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]
    record = fixture["loopRecord"]
    closure_gate = record["closureGate"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("LoopNextActionStatus") != policy["next_action_statuses"]:
        failures.append("LoopNextActionStatus union does not match policy")
    if union_literals("LoopClosureGateStatus") != policy["closure_gate_statuses"]:
        failures.append("LoopClosureGateStatus union does not match policy")

    for field in policy["minimum_loop_record_fields"]:
        if camel_from_snake(field) not in record:
            failures.append(f"sample loop record missing field: {field}")
    for field in policy["minimum_next_action_fields"]:
        if camel_from_snake(field) not in record["nextActions"][0]:
            failures.append(f"sample next action missing field: {field}")

    for rule in policy["closure_rules"]:
        if rule["required"] is not True:
            failures.append(f"closure rule must be required: {rule['id']}")

    checks = {
        "minimumLoopRecordFieldCount": len(policy["minimum_loop_record_fields"]),
        "minimumNextActionFieldCount": len(policy["minimum_next_action_fields"]),
        "nextActionStatusCount": len(policy["next_action_statuses"]),
        "closureGateStatusCount": len(policy["closure_gate_statuses"]),
        "closureRuleCount": len(policy["closure_rules"]),
        "closedForRoundIsBusinessCompletion": hard["closed_for_round_is_business_completion"],
        "loopCanMarkAccepted": hard["loop_can_mark_accepted"],
        "loopCanMarkIntegrated": hard["loop_can_mark_integrated"],
        "loopCanMarkProductionReadiness": hard["loop_can_mark_production_readiness"],
        "loopCanWriteBusinessSystem": hard["loop_can_write_business_system"],
        "loopCanConfirmRevenueOrScore": hard["loop_can_confirm_revenue_or_score"],
        "loopCanTransferQuota": hard["loop_can_transfer_quota"],
        "loopCanSettleBounty": hard["loop_can_settle_bounty"],
        "loopCanCompleteCommitteeDecision": hard["loop_can_complete_committee_decision"],
        "loopCanWriteExternalApi": hard["loop_can_write_external_api"],
        "writesAccepted": no_write["writes_accepted"],
        "writesIntegrated": no_write["writes_integrated"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueOrScoreConfirmation": no_write["writes_revenue_or_score_confirmation"],
        "writesQuotaTransfer": no_write["writes_quota_transfer"],
        "writesBountySettlement": no_write["writes_bounty_settlement"],
        "writesCommitteeDecisionCompletion": no_write["writes_committee_decision_completion"],
        "writesExternalApi": no_write["writes_external_api"],
        "sampleCloseableForRound": closure_gate["closeableForRound"],
        "sampleOpenP0P1ActionCount": closure_gate["openP0P1ActionCount"],
        "sampleMissingEvidenceCount": closure_gate["missingEvidenceCount"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("loop_record_closure_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "loop_record_closure_policy_smoke=pass "
        f"loop_fields={checks['minimumLoopRecordFieldCount']} "
        f"next_action_fields={checks['minimumNextActionFieldCount']} "
        f"next_action_statuses={checks['nextActionStatusCount']} "
        f"closure_statuses={checks['closureGateStatusCount']} "
        f"closure_rules={checks['closureRuleCount']} "
        "closed_for_round_business_completion=false "
        "writes_accepted=0 writes_integrated=0 writes_business_system=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_committee_decision_completion=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
