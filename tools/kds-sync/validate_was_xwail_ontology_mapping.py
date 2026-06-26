#!/usr/bin/env python3
"""Validate WAS-XWAIL-Ontology mapping evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
DOC = ROOT / "docs/harness/evidence/was-xwail-ontology-mapping-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
DEPENDENCY = ROOT / "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

WAS_ONTOLOGY = PROJECT_ROOT / "WAS世界资产体系/okf/ontology.yaml"
WAS_DIMENSIONS = PROJECT_ROOT / "WAS世界资产体系/okf/was/was-dimensions.yaml"
WAS_FLOWS = PROJECT_ROOT / "WAS世界资产体系/okf/was/was-flows.yaml"
XWAIL_MODEL = PROJECT_ROOT / "GlobalCloud XWAIL/models/examples/warehouse-basic.xwail.json"
XWAIL_SCHEMA = PROJECT_ROOT / "GlobalCloud XWAIL/schemas-json/xwail-core.schema.json"

DIMENSIONS = [
    "physical_asset",
    "rule_asset",
    "intelligence_asset",
    "data_asset",
    "economic_asset",
    "energy_asset",
    "organization_asset",
    "spacetime_asset",
]

XWAIL_DIMENSIONS = [
    "Dimensions.Physical",
    "Dimensions.Rule",
    "Dimensions.Intellectual",
    "Dimensions.Data",
    "Dimensions.Economic",
    "Dimensions.Energy",
    "Dimensions.Organization",
    "Dimensions.SpaceTime",
]

FLOWS = [
    "material_flow",
    "information_flow",
    "capital_flow",
    "spacetime_flow",
    "energy_flow",
    "commerce_flow",
    "knowledge_flow",
    "rule_flow",
]

REQUIRED_DOC_TOKENS = [
    "WAS-XWAIL-ONTOLOGY-MAPPING-001",
    "was_xwail_ontology_mapping = controlled",
    "xwail_mapping_candidate",
    "Ontology 基线",
    "XWAIL 基线",
    "ontologyRef",
    "wasBaseline",
    "ontologyVersion",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "不声明 WAES 已发布",
    "不声明 AaaS 已绑定或可订阅",
]

REQUIRED_REFERENCE_TOKENS = [
    "WAS-XWAIL-ONTOLOGY-MAPPING-001",
    "was-xwail-ontology-mapping-20260625.md",
    "validate_was_xwail_ontology_mapping.py",
    "xwail_mapping_candidate",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "WAES 已发布完成",
    "AaaS 已绑定完成",
    "客户验收通过 = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join(
        [
            read(BOARD, failures),
            read(REGISTER, failures),
            read(DEPENDENCY, failures),
            read(STATUS, failures),
        ]
    )
    ontology_text = read(WAS_ONTOLOGY, failures)
    dimensions_text = read(WAS_DIMENSIONS, failures)
    flows_text = read(WAS_FLOWS, failures)
    model_text = read(XWAIL_MODEL, failures)
    schema_text = read(XWAIL_SCHEMA, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in mapping evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    for dimension in DIMENSIONS:
        if dimension not in dimensions_text:
            failures.append(f"missing WAS dimension source: {dimension}")
        if dimension not in doc_text:
            failures.append(f"missing dimension mapping in evidence: {dimension}")

    for dimension in XWAIL_DIMENSIONS:
        if dimension not in doc_text:
            failures.append(f"missing XWAIL dimension mapping in evidence: {dimension}")

    for flow in FLOWS:
        if flow not in flows_text:
            failures.append(f"missing WAS flow source: {flow}")
        if flow not in doc_text:
            failures.append(f"missing flow mapping in evidence: {flow}")

    for token in ["version: 0.1.0", "knowledgeObject", "relationship", "event", "waesGateInput"]:
        if token not in ontology_text:
            failures.append(f"missing ontology source token: {token}")

    for token in ["ontologyRef", "wasBaseline", "ontologyVersion", "profile", "flowRelations"]:
        if token not in model_text:
            failures.append(f"missing XWAIL model token: {token}")

    for token in ["wasBaseline", "ontologyVersion", "assets", "lifecycle"]:
        if token not in schema_text:
            failures.append(f"missing XWAIL schema token: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "was_xwail_ontology_mapping",
        "status": "pass" if not failures else "fail",
        "candidate_status": "xwail_mapping_candidate",
        "dimensions_checked": len(DIMENSIONS),
        "flows_checked": len(FLOWS),
        "failures": failures,
        "warnings": [
            "This validates semantic mapping evidence only; it does not modify WAS terms, publish WAES, bind AaaS, write KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
