#!/usr/bin/env python3
"""Validate project-group WAS-Ontology registry coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-project-group-ontology-registry-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-project-group-ontology-registry-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-PROJECT-GROUP-ONTOLOGY-REGISTRY-001.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
REQUIRED_CATEGORIES = ["object", "relationship", "event", "evidence", "state", "interface"]
MIN_ENTRY_COUNTS = {
    "object": 10,
    "relationship": 6,
    "event": 7,
    "evidence": 7,
    "state": 7,
    "interface": 6,
}
ZERO_BOUNDARY_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]
FALSE_BOUNDARY_KEYS = ["accepted", "integrated", "production_ready", "runtime_write", "kds_api_write"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def validate_registry(registry: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if registry.get("project_group_scope") != PROJECT_GROUP:
        failures.append("project_group_scope_not_complete_or_ordered")

    categories = registry.get("registry_categories", [])
    if not isinstance(categories, list):
        failures.append("registry_categories_not_list")
        categories = []
    by_category = {item.get("category"): item for item in categories if isinstance(item, dict)}
    if list(by_category) != REQUIRED_CATEGORIES:
        failures.append("required_categories_missing_or_unordered")
    for category in REQUIRED_CATEGORIES:
        item = by_category.get(category)
        if not item:
            failures.append(f"missing_category_{category}")
            continue
        entries = item.get("entries", [])
        if not isinstance(entries, list):
            failures.append(f"{category}_entries_not_list")
            continue
        if len(entries) < MIN_ENTRY_COUNTS[category]:
            failures.append(f"{category}_entry_count_too_low")
        if len(set(entries)) != len(entries):
            failures.append(f"{category}_entries_not_unique")

    contracts = registry.get("category_contracts", {})
    if not isinstance(contracts, dict):
        failures.append("category_contracts_not_object")
    else:
        for category in REQUIRED_CATEGORIES:
            if category not in contracts:
                failures.append(f"missing_contract_{category}")

    promotion = registry.get("promotion_policy", {})
    required_promotion = {
        "kds_source_of_record": "required",
        "waes_decision": "required_before_promotion",
        "loop_evidence": "required",
        "llm_candidate": "never_official_fact",
        "runtime_writeback": "blocked_without_waes_kds_owner_confirmation",
    }
    for key, expected in required_promotion.items():
        if promotion.get(key) != expected:
            failures.append(f"promotion_policy_{key}_invalid")

    future_policy = registry.get("future_project_policy", {})
    if future_policy.get("admission_required") is not True:
        failures.append("future_project_admission_required_missing")
    if future_policy.get("must_bind_project_group_scope") is not True:
        failures.append("future_project_scope_binding_missing")
    if future_policy.get("must_map_to_registry_categories") != REQUIRED_CATEGORIES:
        failures.append("future_project_category_mapping_missing")
    if future_policy.get("must_not_bypass_kds_waes_loop") is not True:
        failures.append("future_project_boundary_missing")

    boundary = registry.get("boundary", {})
    if not isinstance(boundary, dict):
        failures.append("boundary_not_object")
        boundary = {}
    for key in ZERO_BOUNDARY_KEYS:
        if boundary.get(key) != 0:
            failures.append(f"boundary_{key}_must_be_zero")
    for key in FALSE_BOUNDARY_KEYS:
        if boundary.get(key) is not False:
            failures.append(f"boundary_{key}_must_be_false")

    return failures


def total_entries(registry: dict[str, Any]) -> int:
    total = 0
    for item in registry.get("registry_categories", []):
        if isinstance(item, dict) and isinstance(item.get("entries"), list):
            total += len(item["entries"])
    return total


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "WAS-PROJECT-GROUP-ONTOLOGY-REGISTRY-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_project_group_ontology_registry_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-PROJECT-GROUP-ONTOLOGY-REGISTRY-001", "invalid round id")
    require(evidence.get("source_gate_pack") == "docs/harness/evidence/was-waes-kds-rag-writeback-gate-pack-20260621.json", "source gate pack mismatch")
    require(evidence.get("source_scenario_matrix") == "docs/harness/evidence/was-scenario-profile-matrix-20260621.json", "source scenario matrix mismatch")

    failures = validate_registry(evidence)
    require(not failures, f"evidence should pass: {failures}")

    positive = load_json(FIXTURE_DIR / "project-group-ontology-registry-positive.json")
    positive_failures = validate_registry(positive)
    require(not positive_failures, f"positive fixture should pass: {positive_failures}")

    negative_paths = sorted(FIXTURE_DIR.glob("project-group-ontology-registry-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        fixture = load_json(path)
        require(validate_registry(fixture), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    for phrase in [
        "project_group_scope | `14/14`",
        "registry_categories | `6/6`",
        "runtime_primary_key_ready | `0`",
        "waes_review | `0`",
        "production_ready | `false`",
        "runtime_write | `false`",
        "kds_api_write | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("项目群 Registry 已建立" in loop_round, "loop feedback missing")
    require("object_family: ProjectGroupOntologyRegistry" in loop_round, "loop_was_context missing object family")
    require("production_ready: false" in loop_round, "loop_was_context missing production boundary")

    print(
        "was_project_group_ontology_registry=pass "
        "project_group_scope=14/14 registry_categories=6/6 "
        f"entries={total_entries(evidence)} positive_fixtures=1 negative_fixtures=3 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false runtime_write=false kds_api_write=false "
        "next_round=GPCF-ONTOLOGY-WAS-LOOP-CONTEXT-COVERAGE-REFRESH-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
