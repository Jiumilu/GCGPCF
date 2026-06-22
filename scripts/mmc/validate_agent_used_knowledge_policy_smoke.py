#!/usr/bin/env python3
"""Validate MMC AgentUsedKnowledge policy.

This validator reads local OKF, shared type and fixture files only. It does not
call model providers, read live KDS APIs, write Harness evidence, write business
systems, confirm facts, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "agent-used-knowledge-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "agent-used-knowledge.ts"
FIXTURE = ROOT / "fixtures" / "mmc" / "agent-used-knowledge-policy-smoke.json"


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
    if union_literals("AgentCapabilityType") != policy["capability_types"]:
        failures.append("AgentCapabilityType union does not match policy")
    if union_literals("AgentOverreadRiskSignal") != policy["overread_risk_signals"]:
        failures.append("AgentOverreadRiskSignal union does not match policy")
    if union_literals("AgentKnowledgeUseOutcome") != policy["allowed_outcomes"]:
        failures.append("AgentKnowledgeUseOutcome union does not match policy")

    for field in policy["minimum_invocation_fields"]:
        if field.startswith("writes_") and field not in no_write:
            failures.append(f"write assertion missing for field: {field}")

    checks = {
        "capabilityTypeCount": len(policy["capability_types"]),
        "minimumInvocationFieldCount": len(policy["minimum_invocation_fields"]),
        "overreadRiskSignalCount": len(policy["overread_risk_signals"]),
        "allowedOutcomeCount": len(policy["allowed_outcomes"]),
        "requiredGateCount": len(policy["required_gates"]),
        "agentCanWriteAccepted": hard["agent_can_write_accepted"],
        "agentCanWritePublic": hard["agent_can_write_public"],
        "agentCanModifyGovernanceEvidence": hard["agent_can_modify_governance_evidence"],
        "crossSupplierWithoutAclAllowed": hard["cross_supplier_without_acl_allowed"],
        "t5FinalFactAllowed": hard["t5_final_fact_allowed"],
        "promotionWithoutKweAllowed": hard["promotion_without_kwe_allowed"],
        "businessSystemWriteAllowed": hard["business_system_write_allowed"],
        "revenueOrScoreConfirmationAllowed": hard["revenue_or_score_confirmation_allowed"],
        "sensitiveRawContentAllowedInEvidence": hard["sensitive_raw_content_allowed_in_evidence"],
        "harnessEvidenceRequiredForHighRisk": hard["harness_evidence_required_for_high_risk"],
        "writesAccepted": no_write["writes_accepted"],
        "writesPublic": no_write["writes_public"],
        "writesGovernanceEvidence": no_write["writes_governance_evidence"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueOrScoreConfirmation": no_write["writes_revenue_or_score_confirmation"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("agent_used_knowledge_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "agent_used_knowledge_policy_smoke=pass "
        f"capability_types={checks['capabilityTypeCount']} "
        f"invocation_fields={checks['minimumInvocationFieldCount']} "
        f"overread_signals={checks['overreadRiskSignalCount']} "
        f"allowed_outcomes={checks['allowedOutcomeCount']} "
        f"required_gates={checks['requiredGateCount']} "
        "harness_evidence_required=true "
        "writes_accepted=0 writes_public=0 writes_governance_evidence=0 "
        "writes_business_system=0 writes_revenue_or_score_confirmation=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
