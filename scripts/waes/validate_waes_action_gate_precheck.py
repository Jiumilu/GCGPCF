#!/usr/bin/env python3
"""Validate WAES action gate precheck dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "waes-action-gate-precheck-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "waes-action-gate-precheck.ts"
FIXTURE = ROOT / "fixtures" / "waes" / "action-gate-precheck-dry-run.json"

NO_WRITE_KEYS = (
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesBusinessSystem",
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
    prechecks: list[dict[str, Any]] = fixture["prechecks"]
    expected = fixture["expected"]
    failures: list[str] = []

    if union_literals("WaesActionGatePrecheckStatus") != policy["precheck_statuses"]:
        failures.append("WaesActionGatePrecheckStatus union does not match policy")

    required_fields = set(policy["required_fields"])
    requested_gate_types = set(policy["requested_gate_types"])
    reason_codes = set(policy["reason_codes"])
    reviewer_requirements = set(policy["reviewer_requirements"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "precheckPassed": 0,
        "repairRequired": 0,
        "committeeRequired": 0,
        "freezeRequired": 0,
        "blocked": 0,
        "createsWaesGateResults": 0,
        "createsKweWorkItems": 0,
        "promotesLifecycle": 0,
        "harnessEvidenceRequired": 0,
    }

    for precheck in prechecks:
        precheck_id = precheck["precheckId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in precheck})
        if missing:
            failures.append(f"{precheck_id} missing required fields: {missing}")
        if precheck["createsWaesGateResult"] is not False:
            failures.append(f"{precheck_id}: createsWaesGateResult must be false")
        if precheck["createsKweWorkItem"] is not False:
            failures.append(f"{precheck_id}: createsKweWorkItem must be false")
        if precheck["promotesLifecycle"] is not False:
            failures.append(f"{precheck_id}: promotesLifecycle must be false")
        counts["createsWaesGateResults"] += int(precheck["createsWaesGateResult"] is True)
        counts["createsKweWorkItems"] += int(precheck["createsKweWorkItem"] is True)
        counts["promotesLifecycle"] += int(precheck["promotesLifecycle"] is True)
        counts["harnessEvidenceRequired"] += int(precheck["harnessEvidenceRequired"] is True)

        unknown_gates = sorted(set(precheck["requestedGateTypes"]) - requested_gate_types)
        if unknown_gates:
            failures.append(f"{precheck_id}: unknown requested gate types {unknown_gates}")
        unknown_reasons = sorted(set(precheck["reasonCodes"]) - reason_codes)
        if unknown_reasons:
            failures.append(f"{precheck_id}: unknown reason codes {unknown_reasons}")
        if precheck["reviewerRequirement"] not in reviewer_requirements:
            failures.append(f"{precheck_id}: invalid reviewerRequirement")
        if not precheck["requiredActions"]:
            failures.append(f"{precheck_id}: requiredActions must not be empty")

        if precheck["precheckStatus"] == "precheck_passed":
            counts["precheckPassed"] += 1
        if precheck["precheckStatus"] == "repair_required":
            counts["repairRequired"] += 1
            if not precheck["reasonCodes"]:
                failures.append(f"{precheck_id}: repair_required requires reasonCodes")
        if precheck["precheckStatus"] == "committee_required":
            counts["committeeRequired"] += 1
            if "committee_gate" not in precheck["requestedGateTypes"]:
                failures.append(f"{precheck_id}: committee_required requires committee_gate")
        if precheck["precheckStatus"] == "freeze_required":
            counts["freezeRequired"] += 1
            if "freeze_gate" not in precheck["requestedGateTypes"]:
                failures.append(f"{precheck_id}: freeze_required requires freeze_gate")
        if precheck["precheckStatus"] == "blocked":
            counts["blocked"] += 1
            if not precheck["reasonCodes"]:
                failures.append(f"{precheck_id}: blocked requires reasonCodes")

        for key in NO_WRITE_KEYS:
            value = precheck["noWrite"].get(key)
            if value != 0:
                failures.append(f"{precheck_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "precheckCount": len(prechecks),
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
        print("waes_action_gate_precheck=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "waes_action_gate_precheck=pass "
        f"prechecks={actual['precheckCount']} precheck_passed={actual['precheckPassed']} "
        f"repair_required={actual['repairRequired']} committee_required={actual['committeeRequired']} "
        f"freeze_required={actual['freezeRequired']} blocked={actual['blocked']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"harness_evidence_required={actual['harnessEvidenceRequired']} "
        "writes_waes_gate_result=0 writes_kwe_work_item=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_business_system=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
