#!/usr/bin/env python3
"""Validate WAES Gate IO and hard-stop policy.

This validator reads local OKF, shared type and fixture files only. It does not
persist WAES gate results, write business systems, distribute revenue, or call
external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "waes-gate-io-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "waes-gate-io.ts"
FIXTURE = ROOT / "fixtures" / "waes" / "gate-io-policy-smoke.json"


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
    hard_stop_gates = [item["gate_type"] for item in policy["hard_stop_rules"]]
    reason_codes = policy["reason_codes"]
    allowed_operations = policy["allowed_operations"]

    failures: list[str] = []
    if union_literals("WaesReasonCode") != reason_codes:
        failures.append("WaesReasonCode union does not match policy reason_codes")
    if union_literals("WaesAllowedOperation") != allowed_operations:
        failures.append("WaesAllowedOperation union does not match policy allowed_operations")

    for rule in policy["hard_stop_rules"]:
        if not rule["triggers"]:
            failures.append(f"hard-stop rule missing triggers: {rule}")
        if rule["default_result"] not in {
            "blocked",
            "repair_required",
            "human_required",
            "committee_required",
            "redaction_required",
            "freeze_required",
            "metadata_only",
        }:
            failures.append(f"invalid hard-stop default result: {rule}")

    checks = {
        "minimumInputFieldCount": len(policy["minimum_input_fields"]),
        "minimumOutputFieldCount": len(policy["minimum_output_fields"]),
        "reasonCodeCount": len(reason_codes),
        "hardStopRuleCount": len(policy["hard_stop_rules"]),
        "allowedOperationCount": len(allowed_operations),
        "hardStopGates": hard_stop_gates,
        "p0P1RequiresDryRun": hard["p0_p1_requires_dry_run"],
        "noDirectGateResultPersistence": hard["no_direct_gate_result_persistence"],
        "noBusinessWriteback": hard["no_business_writeback"],
        "noRevenueDistribution": hard["no_revenue_distribution"],
        "noExternalApiWrite": hard["no_external_api_write"],
        "humanOrCommitteeRequiredForFinality": hard["human_or_committee_required_for_finality"],
        "writesGateResult": no_write["writes_gate_result"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("waes_gate_io_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "waes_gate_io_policy_smoke=pass "
        f"input_fields={checks['minimumInputFieldCount']} "
        f"output_fields={checks['minimumOutputFieldCount']} "
        f"reason_codes={checks['reasonCodeCount']} "
        f"hard_stop_rules={checks['hardStopRuleCount']} "
        f"allowed_operations={checks['allowedOperationCount']} "
        "dry_run_required=true "
        "human_or_committee_finality=covered "
        "writes_gate_result=0 writes_business_system=0 "
        "writes_revenue_distribution=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
