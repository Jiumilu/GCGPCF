#!/usr/bin/env python3
"""Validate WAES CodeGraph high-risk gate policy."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "governance/codegraph/waes-codegraph-gates.yaml"
DOC = ROOT / "docs/codegraph/codegraph-waes-gate.md"
IMPACT_TEMPLATE = ROOT / "harness/templates/codegraph-impact-report.yaml"
EVIDENCE_TEMPLATE = ROOT / "harness/templates/codegraph-evidence-bundle.yaml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    policy = read(POLICY)
    doc = read(DOC)
    impact_template = read(IMPACT_TEMPLATE)
    evidence_template = read(EVIDENCE_TEMPLATE)

    required_for = [
        "auth_changes",
        "permission_changes",
        "tenant_boundary_changes",
        "financial_flow_changes",
        "settlement_changes",
        "waes_rule_changes",
        "kds_schema_changes",
        "ontology_changes",
        "okf_collection_changes",
        "harness_policy_changes",
        "loop_policy_changes",
        "api_contract_changes",
        "multi_agent_protocol_changes",
    ]
    for item in required_for:
        require(item in policy, f"WAES policy missing required_for item: {item}")

    for rule_id in ["CG-WAES-001", "CG-WAES-002", "CG-WAES-003", "CG-WAES-004", "CG-WAES-005"]:
        require(rule_id in policy, f"WAES policy missing rule: {rule_id}")

    for evidence in ["codegraph_impact_report", "impacted_tests", "reviewer_approval", "call_graph_trace"]:
        require(evidence in policy, f"WAES policy missing evidence: {evidence}")

    for field in ["changed_files:", "impacted_symbols:", "impacted_tests:", "risk:", "accepted: false"]:
        require(field in impact_template, f"impact template missing field: {field}")

    for field in ["codegraph_evidence_bundle:", "queries:", "kds_candidates:", "status: candidate", "production_write: false"]:
        require(field in evidence_template, f"evidence bundle missing field: {field}")

    for phrase in ["WAES 使用 CodeGraph", "不是把 CodeGraph 作为裁决者", "AI Agent 不能代替人员或委员会批准"]:
        require(phrase in doc, f"WAES doc missing phrase: {phrase}")

    print("codegraph_waes_gate_policy=pass rules=5 high_risk_required=true ai_approval=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
