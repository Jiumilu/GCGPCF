#!/usr/bin/env python3
"""Validate KDS/OKF CodeGraph candidate-only mapping."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "governance/codegraph/kds-codegraph-mapping.yaml"
DOC = ROOT / "docs/codegraph/codegraph-kds-okf-mapping.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    mapping = read(MAPPING)
    doc = read(DOC)

    for candidate in [
        "code_fact_candidate",
        "api_fact_candidate",
        "dependency_fact_candidate",
        "architecture_fact_candidate",
        "test_mapping_candidate",
    ]:
        require(candidate in mapping, f"mapping missing candidate type: {candidate}")
        require(candidate in doc, f"mapping doc missing candidate type: {candidate}")

    for phrase in [
        "default_status: candidate",
        "accepted_direct_write_allowed: false",
        "production_evidence_allowed: false",
        "codegraph_may_promote_to_accepted: false",
        "initial: candidate",
    ]:
        require(phrase in mapping, f"mapping missing guard: {phrase}")

    for required in ["harness_evidence", "waes_gate", "human_review", "lineage_backlink"]:
        require(required in mapping, f"mapping missing promotion requirement: {required}")

    for rejection in [
        "demo_not_runtime_evidence",
        "mock_not_production_evidence",
        "generated_doc_not_accepted_fact",
        "ai_agent_not_final_approver",
    ]:
        require(rejection in mapping, f"mapping missing rejection rule: {rejection}")

    for phrase in ["只能是候选事实", "禁止", "升格条件"]:
        require(phrase in doc, f"mapping doc missing phrase: {phrase}")

    print("codegraph_kds_candidate_policy=pass candidate_types=5 accepted_direct_write=false production_evidence=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
