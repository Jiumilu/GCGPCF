#!/usr/bin/env python3
"""Validate the GreenChainGraphBusinessDomain domain-slice registry entry package."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/business-domain-slice-registry-greenchain-graph-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/business-domain-slice-registry-greenchain-graph-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-001.md"
BASE_REGISTRY = ROOT / "docs/harness/evidence/was-project-group-ontology-registry-20260621.json"
REQUEST_JSON = ROOT / "docs/harness/evidence/industrial-green-chain-graph-domain-registration-request-20261011.json"
CATEGORIES = ["object", "relationship", "event", "evidence", "state", "interface"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-10-11",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "GPCF-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-20261011",
            "invalid evidence id")
    require(evidence.get("status") == "business_domain_slice_registered_candidate", "invalid status")
    require(evidence.get("round_id") == "GPCF-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-001", "invalid round id")

    base = evidence.get("registry_base", {})
    require(base.get("source_registry", "").endswith("was-project-group-ontology-registry-20260621.json"),
            "source registry ref missing")
    require(base.get("existing_entries_untouched") == 43, "existing entries untouched must be 43")
    require(base.get("request_decision") == "accepted", "source request must be accepted")

    slice_info = evidence.get("domain_slice", {})
    require(slice_info.get("name") == "GreenChainGraphBusinessDomain", "domain name mismatch")
    require("工业绿链" in str(slice_info.get("scope_binding", "")), "scope binding missing IGL")
    require("F-016" in str(slice_info.get("scope_binding", "")), "scope binding missing KDS(F-016)")

    mapping = evidence.get("six_category_mapping", {})
    for category in CATEGORIES:
        require(bool(mapping.get(category)), f"six-category mapping missing: {category}")

    boundary = evidence.get("boundary", {})
    for key in ["real_source_records", "runtime_primary_key_ready", "waes_review"]:
        require(boundary.get(key) == 0, f"boundary {key} must be 0")
    for key in ["accepted", "integrated", "production_ready", "runtime_write", "kds_api_write"]:
        require(boundary.get(key) is False, f"boundary {key} must be false")

    # 基础 registry 未被改动（43 条在位）
    base_reg = load_json(BASE_REGISTRY)
    total = sum(len(item.get("entries", [])) for item in base_reg.get("registry_categories", []))
    require(total == 43, f"base registry entries changed: {total} != 43")

    # 上游 request 已登记引用本件
    request = load_json(REQUEST_JSON)
    require(request.get("gates", {}).get("registry_entry_added") is True, "request registry_entry_added must be true")
    require("business-domain-slice-registry-greenchain-graph-20261011" in str(request.get("registry_entry_ref", "")),
            "request registry_entry_ref must point to this entry")

    for phrase in [
        "GPCF-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-20261011",
        "business_domain_slice_registered_candidate",
        "GreenChainGraphBusinessDomain",
        "既有 43 条一字未动",
        "accepted | false",
        "production_ready | false",
        "零写回",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_business_domain_slice_registry_greenchain_graph.py" in loop_round,
            "loop round missing validator")
    print(
        "business_domain_slice_registry_greenchain_graph=pass "
        "domain=GreenChainGraphBusinessDomain status=business_domain_slice_registered_candidate "
        "base_entries_untouched=43 request=accepted accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
