#!/usr/bin/env python3
"""Validate WAS scenario profile matrix coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-scenario-profile-matrix-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-scenario-profile-matrix-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-SCENARIO-PROFILE-MATRIX-001.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
DIMENSIONS = ["physical_asset", "rule_asset", "intelligence_asset", "data_asset", "economic_asset", "energy_asset", "organization_asset", "spacetime_asset"]
FLOWS = ["material_flow", "information_flow", "capital_flow", "spacetime_flow", "energy_flow", "commerce_flow", "knowledge_flow", "rule_flow"]
CHAIN_LINKS = ["customer_order", "supplier_procurement", "production_work_order", "quality_inspection", "logistics_delivery", "energy_consumption", "carbon_footprint", "settlement_profit", "knowledge_reference", "recycling_circular"]
PROFILE_REQUIRED_KEYS = ["profile_id", "projects", "business_chain_links", "required_asset_dimensions", "required_flows", "source_of_record", "waes_gate", "kds_backlink_policy", "rag_reference_policy", "writeback_policy", "pool_link_policy", "blockers", "closure_policy"]


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


def validate_matrix(matrix: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if set(matrix.get("project_group_scope", [])) != set(PROJECT_GROUP):
        failures.append("project_group_scope_not_complete")
    if set(matrix.get("required_green_supply_chain_links", [])) != set(CHAIN_LINKS):
        failures.append("green_supply_chain_links_not_complete")
    if matrix.get("boundary", {}).get("accepted") is not False:
        failures.append("accepted_must_be_false")
    if matrix.get("boundary", {}).get("integrated") is not False:
        failures.append("integrated_must_be_false")
    if matrix.get("boundary", {}).get("production_ready") is not False:
        failures.append("production_ready_must_be_false")

    profiles = matrix.get("profiles", [])
    if not isinstance(profiles, list) or not profiles:
        failures.append("profiles_missing")
        return failures

    covered_projects: set[str] = set(matrix.get("project_group_scope", []))
    covered_dimensions: set[str] = set(matrix.get("required_asset_dimensions", []))
    covered_flows: set[str] = set(matrix.get("required_flows", []))
    covered_links: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, dict):
            failures.append("profile_not_object")
            continue
        for key in PROFILE_REQUIRED_KEYS:
            if key not in profile:
                failures.append(f"profile_missing_{key}")
        covered_projects.update(profile.get("projects", []))
        covered_dimensions.update(profile.get("required_asset_dimensions", []))
        covered_flows.update(profile.get("required_flows", []))
        covered_links.update(profile.get("business_chain_links", []))
        if profile.get("source_of_record") != "KDS":
            failures.append(f"{profile.get('profile_id')}:source_of_record_not_kds")
        if not str(profile.get("waes_gate", "")).startswith("waes://gate/"):
            failures.append(f"{profile.get('profile_id')}:waes_gate_missing")
        if "does_not_equal" not in str(profile.get("closure_policy", "")) and "no_business_acceptance" not in str(profile.get("closure_policy", "")) and "not production integration" not in str(profile.get("closure_policy", "")):
            failures.append(f"{profile.get('profile_id')}:closure_policy_must_block_status_overclaim")

    if set(PROJECT_GROUP) - covered_projects:
        failures.append("profiles_do_not_cover_all_projects")
    if set(DIMENSIONS) - covered_dimensions:
        failures.append("profiles_do_not_cover_all_dimensions")
    if set(FLOWS) - covered_flows:
        failures.append("profiles_do_not_cover_all_flows")
    if set(CHAIN_LINKS) - covered_links:
        failures.append("profiles_do_not_cover_all_chain_links")
    return failures


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "WAS-SCENARIO-PROFILE-MATRIX-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_scenario_profile_matrix_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-SCENARIO-PROFILE-MATRIX-001", "invalid round id")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group order mismatch")
    require(evidence.get("required_asset_dimensions") == DIMENSIONS, "dimension list mismatch")
    require(evidence.get("required_flows") == FLOWS, "flow list mismatch")
    require(evidence.get("required_green_supply_chain_links") == CHAIN_LINKS, "chain list mismatch")
    require(len(evidence.get("profiles", [])) == 10, "profile count must be 10")

    failures = validate_matrix(evidence)
    require(not failures, f"matrix should pass: {failures}")

    positive = load_json(FIXTURE_DIR / "scenario-profile-matrix-positive.json")
    positive_failures = validate_matrix(positive)
    require(not positive_failures, f"positive fixture should pass: {positive_failures}")

    negative_paths = sorted(FIXTURE_DIR.glob("scenario-profile-matrix-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        fixture = load_json(path)
        require(validate_matrix(fixture), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    boundary = evidence.get("boundary", {})
    for key in ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "project_group_scope | `14/14`",
        "scenario_profiles | `10`",
        "asset_dimensions | `8/8`",
        "green_supply_chain_links | `10/10`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("WAS scenario profile matrix 已建立" in loop_round, "loop feedback missing")

    print(
        "was_scenario_profile_matrix=pass "
        "project_group_scope=14/14 scenario_profiles=10 asset_dimensions=8/8 flows=8/8 "
        "green_supply_chain_links=10/10 positive_fixtures=1 negative_fixtures=3 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-WAES-KDS-RAG-WRITEBACK-GATE-PACK-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
