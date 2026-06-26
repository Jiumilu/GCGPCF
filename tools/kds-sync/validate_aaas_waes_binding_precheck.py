#!/usr/bin/env python3
"""Validate AaaS-WAES binding precheck evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
DOC = ROOT / "docs/harness/AaaS/evidence/aaas-waes-binding-precheck-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
DEPENDENCY = ROOT / "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

AAAS_PACKAGE = PROJECT_ROOT / "GlobalCloud AAAS/service-packages/examples/green-supply-chain/service-package.aaas.json"

REQUIRED_DIMENSIONS = [
    "Physical",
    "Rule",
    "Intellectual",
    "Data",
    "Economic",
    "Energy",
    "Organization",
    "SpaceTime",
]

REQUIRED_DOC_TOKENS = [
    "AAAS-WAES-BINDING-PRECHECK-001",
    "aaas_waes_binding_precheck = controlled",
    "integration_precheck_candidate",
    "service-packages/examples/green-supply-chain/service-package.aaas.json",
    "aaas.service.green-supply-chain.basic",
    "GlobalCloud 绿色供应链体系",
    "WAES status",
    "Draft",
    "candidate_only_not_published",
    "commercial status",
    "realCustomerSubscription",
    "false",
    "realBillingEnabled = false",
    "not_enforced_local_dev",
    "customerAcceptanceRequired = true",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "不声明 WAES 已发布",
    "不声明客户可订阅",
]

REQUIRED_REFERENCE_TOKENS = [
    "AAAS-WAES-BINDING-PRECHECK-001",
    "aaas-waes-binding-precheck-20260625.md",
    "validate_aaas_waes_binding_precheck.py",
    "integration_precheck_candidate",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "realCustomerSubscription = true",
    "realBillingEnabled = true",
    "WAES 已发布完成",
    "AaaS 已上架完成",
    "客户可订阅 = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def load_json(path: Path, failures: list[str]) -> dict:
    text = read(path, failures)
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        failures.append(f"invalid JSON: {path}: {exc}")
        return {}
    if not isinstance(data, dict):
        failures.append(f"JSON root must be object: {path}")
        return {}
    return data


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
    package = load_json(AAAS_PACKAGE, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in AaaS-WAES binding precheck evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    if package:
        if package.get("kind") != "AaaSServicePackage":
            failures.append("service package kind must be AaaSServicePackage")
        if package.get("packageId") != "aaas.service.green-supply-chain.basic":
            failures.append("unexpected service package id")
        if package.get("scenarioName") != "GlobalCloud 绿色供应链体系":
            failures.append("unexpected scenarioName")
        waes = package.get("waes") if isinstance(package.get("waes"), dict) else {}
        if waes.get("status") != "Draft":
            failures.append("WAES status must remain Draft for this precheck")
        if waes.get("decision") != "candidate_only_not_published":
            failures.append("WAES decision must remain candidate_only_not_published")
        commercial = package.get("commercial") if isinstance(package.get("commercial"), dict) else {}
        if commercial.get("status") != "draft":
            failures.append("commercial.status must remain draft")
        if commercial.get("realCustomerSubscription") is not False:
            failures.append("realCustomerSubscription must remain false")
        metering = package.get("metering") if isinstance(package.get("metering"), dict) else {}
        if metering.get("realBillingEnabled") is not False:
            failures.append("metering.realBillingEnabled must remain false")
        sla = package.get("sla") if isinstance(package.get("sla"), dict) else {}
        if sla.get("enforcementStatus") != "not_enforced_local_dev":
            failures.append("SLA enforcement must remain not_enforced_local_dev")
        evidence = package.get("evidenceRequirement") if isinstance(package.get("evidenceRequirement"), dict) else {}
        if evidence.get("customerAcceptanceRequired") is not True:
            failures.append("customerAcceptanceRequired must remain true")
        dimensions = package.get("wasDimensions")
        if not isinstance(dimensions, list) or set(dimensions) != set(REQUIRED_DIMENSIONS):
            failures.append("wasDimensions must cover 8/8 WAS dimensions")
        binding = package.get("xwailBinding") if isinstance(package.get("xwailBinding"), dict) else {}
        if not binding.get("modelId") or not binding.get("profile"):
            failures.append("xwailBinding must include modelId and profile")
        refs = binding.get("ontologyRefs")
        if not isinstance(refs, list) or len(refs) < 3:
            failures.append("xwailBinding.ontologyRefs must include at least 3 references")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "aaas_waes_binding_precheck",
        "status": "pass" if not failures else "fail",
        "candidate_status": "integration_precheck_candidate",
        "dimensions_checked": len(REQUIRED_DIMENSIONS),
        "failures": failures,
        "warnings": [
            "This validates AaaS-WAES binding precheck evidence only; it does not publish WAES, enable billing, create subscription, enforce SLA, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
