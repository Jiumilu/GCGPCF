#!/usr/bin/env python3
"""Validate the GC-Knowledge Fabric core object relationship policy.

This validator reads local OKF, shared type and fixture files only. It does not
write KDS facts, business systems, governance ledgers, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "object-relationship-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "object-relationship.ts"
FIXTURE = ROOT / "fixtures" / "object-relationship" / "object-relationship-policy-smoke.json"


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

    chain = policy["relation_chain"]
    relation_types = [item["relation_type"] for item in chain]
    type_relation_types = union_literals("KnowledgeRelationType")
    endpoint_types = union_literals("KnowledgeRelationEndpointType")
    minimum_fields = policy["minimum_relation_fields"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if relation_types != expected["requiredRelationTypes"]:
        failures.append(f"relation chain mismatch expected={expected['requiredRelationTypes']} actual={relation_types}")
    if type_relation_types != expected["requiredRelationTypes"]:
        failures.append(f"type relation mismatch expected={expected['requiredRelationTypes']} actual={type_relation_types}")

    for item in chain:
        if item["from_type"] not in endpoint_types:
            failures.append(f"unknown from_type: {item}")
        if item["to_type"] not in endpoint_types:
            failures.append(f"unknown to_type: {item}")
        if not item["required_refs"]:
            failures.append(f"missing required_refs: {item['relation_type']}")

    checks = {
        "relationCount": len(chain),
        "minimumFieldCount": len(minimum_fields),
        "sourceRequiredForFormalFact": hard["source_required_for_formal_fact"],
        "evidenceRequiredForEvidenceReady": hard["evidence_required_for_evidence_ready"],
        "waesGateRequiredForCandidates": hard["waes_gate_required_for_candidates"],
        "confirmationRequiredForWritebackCandidate": hard["confirmation_required_for_writeback_candidate"],
        "aiCannotCreateFormalWritebackRelation": hard["ai_cannot_create_formal_writeback_relation"],
        "loopCannotPromoteBusinessStatus": hard["loop_cannot_promote_business_status"],
        "harnessStoresGovernanceEvidenceOnly": hard["harness_stores_governance_evidence_only"],
        "revenueBasisRequiredForDistribution": hard["revenue_basis_required_for_distribution"],
        "writesKdsFact": no_write["writes_kds_fact"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesExternalApi": no_write["writes_external_api"],
    }
    for key, expected_value in expected.items():
        if key == "requiredRelationTypes":
            continue
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("object_relationship_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "object_relationship_policy_smoke=pass "
        f"relations={checks['relationCount']} "
        f"minimum_fields={checks['minimumFieldCount']} "
        "source_evidence_chain=covered "
        "candidate_gate_workflow_chain=covered "
        "decision_contribution_revenue_chain=covered "
        "harness_loop_chain=covered "
        "writes_kds_fact=0 writes_business_system=0 "
        "writes_revenue_distribution=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
