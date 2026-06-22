#!/usr/bin/env python3
"""Validate RAG citation strength L0-L5 policy.

This validator reads local OKF, shared type and fixture files only. It does not
write KDS facts, WAES gate results, business systems, revenue ledgers, or
external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "rag-citation-strength-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "rag-citation-strength.ts"
FIXTURE = ROOT / "fixtures" / "rag" / "citation-strength-policy-smoke.json"


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

    levels = [item["code"] for item in policy["levels"]]
    mapping = policy["rag_admission_mapping"]
    l5 = policy["l5_conditions"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("RagCitationStrength") != levels:
        failures.append("RagCitationStrength union does not match policy levels")
    if any(item["can_business_assist"] for item in policy["levels"] if item["code"] != "L5"):
        failures.append("Only L5 may allow business assist")
    if not next(item for item in policy["levels"] if item["code"] == "L0")["can_retrieve"] is False:
        failures.append("L0 must not retrieve")

    checks = {
        "levelCount": len(levels),
        "mappingCount": len(mapping),
        "blocked": mapping["blocked"],
        "sensitiveMetadataOnly": mapping["sensitive_metadata_only"],
        "repairRequired": mapping["repair_required"],
        "limited": mapping["limited"],
        "safe": mapping["safe"],
        "l5TrustLevels": l5["trust_levels"],
        "l5ConfirmationStatus": l5["confirmation_status"],
        "l5DoesNotAutoWriteback": hard["l5_does_not_auto_writeback"],
        "l5DoesNotAutoConfirmRevenue": hard["l5_does_not_auto_confirm_revenue"],
        "l5DoesNotReplaceCommitteeDecision": hard["l5_does_not_replace_committee_decision"],
        "sensitiveRequiresMetadataOrRedaction": hard["sensitive_requires_metadata_or_redaction"],
        "limitedRequiresBoundaryNotice": hard["limited_requires_boundary_notice"],
        "repairRequiredMustNotBeConclusion": hard["repair_required_must_not_be_conclusion"],
        "writesKdsFact": no_write["writes_kds_fact"],
        "writesWaesGateResult": no_write["writes_waes_gate_result"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("rag_citation_strength_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "rag_citation_strength_policy_smoke=pass "
        f"levels={checks['levelCount']} "
        f"mappings={checks['mappingCount']} "
        "blocked=L0 limited=L3 safe=L4 "
        "l5_conditions=T0,T1+confirmed+evidence "
        "l5_no_auto_writeback=covered "
        "sensitive_metadata_boundary=covered "
        "writes_kds_fact=0 writes_waes_gate_result=0 "
        "writes_business_system=0 writes_revenue_distribution=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
