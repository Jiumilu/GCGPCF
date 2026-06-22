#!/usr/bin/env python3
"""Validate the GC-Knowledge Fabric lifecycle state machine policy.

This validator reads local OKF, schema, shared type and fixture files only. It
does not write KDS facts, business systems, governance ledgers, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "status-machine-policy.yaml"
ONTOLOGY = ROOT / "okf" / "ontology.yaml"
SCHEMA = ROOT / "okf" / "knowledge-object.schema.json"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "object.ts"
FIXTURE = ROOT / "fixtures" / "status-machine" / "status-machine-policy-smoke.json"


def string_literals(block: str) -> list[str]:
    return re.findall(r'"([^"]+)"', block)


def knowledge_lifecycle_union() -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(r"export type KnowledgeLifecycle =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError("KnowledgeLifecycle union not found")
    return string_literals(match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    ontology: dict[str, Any] = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]

    policy_states = [item["code"] for item in policy["lifecycle_states"]]
    schema_states = schema["properties"]["lifecycle"]["enum"]
    type_states = knowledge_lifecycle_union()
    ontology_states = ontology["lifecycle"]
    terminal_states = [item["code"] for item in policy["lifecycle_states"] if item["terminal"]]
    promotion_rules = policy["promotion_rules"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    for label, states in {
        "schema": schema_states,
        "type": type_states,
        "ontology": ontology_states,
    }.items():
        if states != policy_states:
            failures.append(f"{label} lifecycle mismatch expected={policy_states} actual={states}")

    checks = {
        "stateCount": len(policy_states),
        "promotionRuleCount": len(promotion_rules),
        "terminalStates": terminal_states,
        "aiAllowedTargetStates": hard["ai_allowed_target_states"],
        "loopAllowedTargetStates": hard["loop_allowed_target_states"],
        "aiCannotPromoteTo": hard["ai_cannot_promote_to"],
        "loopCannotPromoteTo": hard["loop_cannot_promote_to"],
        "formalWritebackRequiresAccepted": hard["formal_writeback_requires_accepted"],
        "revenueConfirmationRequiresAccepted": hard["revenue_confirmation_requires_accepted"],
        "templateIsNotFact": hard["template_is_not_fact"],
        "writesKdsFact": no_write["writes_kds_fact"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    accepted = next(item for item in policy["lifecycle_states"] if item["code"] == "accepted")
    verified = next(item for item in policy["lifecycle_states"] if item["code"] == "verified")
    frozen = next(item for item in policy["lifecycle_states"] if item["code"] == "frozen")
    if not accepted["formal_writeback"] or not accepted["revenue_confirmation"]:
        failures.append("accepted must allow gated formal writeback and revenue confirmation")
    if verified["formal_writeback"] or verified["revenue_confirmation"]:
        failures.append("verified must not allow formal writeback or revenue confirmation")
    if frozen["rag_strong_reference"] or frozen["formal_writeback"] or frozen["revenue_confirmation"]:
        failures.append("frozen must block strong RAG, formal writeback and revenue confirmation")

    if failures:
        print("status_machine_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "status_machine_policy_smoke=pass "
        f"states={checks['stateCount']} "
        f"promotion_rules={checks['promotionRuleCount']} "
        "terminal_states=superseded,archived "
        "ai_boundary=covered loop_boundary=covered "
        "formal_writeback_requires_accepted=true "
        "revenue_confirmation_requires_accepted=true "
        "template_is_not_fact=true "
        "writes_kds_fact=0 writes_business_system=0 "
        "writes_revenue_distribution=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
