#!/usr/bin/env python3
"""Validate refreshed loop_was_context coverage for WAS/Ontology Loop rounds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-loop-context-coverage-refresh-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-loop-context-coverage-refresh-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-LOOP-CONTEXT-COVERAGE-REFRESH-001.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
CONTEXT_SHAPES = ["flat_v1", "nested_v2"]
ZERO_BOUNDARY_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]
FALSE_BOUNDARY_KEYS = ["accepted", "integrated", "production_ready"]


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


def extract_context(path: Path) -> tuple[str, dict[str, Any]]:
    text = read(path)
    marker = "## loop_was_context\n\n```yaml\n"
    start = text.find(marker)
    require(start >= 0, f"{path.relative_to(ROOT)} missing loop_was_context block")
    start += len(marker)
    end = text.find("\n```", start)
    require(end > start, f"{path.relative_to(ROOT)} has unterminated loop_was_context block")
    value = yaml.safe_load(text[start:end])
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} loop_was_context must be mapping")
    if "loop_was_context" in value:
        context = value["loop_was_context"]
        require(isinstance(context, dict), f"{path.relative_to(ROOT)} nested loop_was_context must be mapping")
        return "nested_v2", context
    return "flat_v1", value


def validate_flat_context(source: str, context: dict[str, Any]) -> None:
    for key in [
        "project_scope",
        "related_asset_dimensions",
        "related_flows",
        "related_objects",
        "source_refs",
        "evidence_refs",
        "waes_gate_refs",
        "kds_backlinks",
        "promotion_blockers",
        "next_action",
        "no_write_declaration",
    ]:
        require(key in context, f"{source} missing flat context key: {key}")
    require(context["project_scope"] == PROJECT_GROUP, f"{source} project_scope mismatch")
    require(context["no_write_declaration"] == "no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready", f"{source} no-write declaration mismatch")


def validate_nested_context(source: str, context: dict[str, Any]) -> None:
    for key in [
        "project_group_scope",
        "source_of_record",
        "ontology_role",
        "waes_gate",
        "loop_role",
        "llm_role",
        "rag_role",
        "runtime_writeback",
        "promotion_boundary",
    ]:
        require(key in context, f"{source} missing nested context key: {key}")
    require(context["project_group_scope"] == PROJECT_GROUP, f"{source} project_group_scope mismatch")
    require(context["source_of_record"] == "KDS", f"{source} source_of_record must be KDS")
    require(context["llm_role"] == "candidate_generation_only", f"{source} llm role mismatch")
    require(str(context["runtime_writeback"]).startswith("blocked_without"), f"{source} runtime writeback boundary mismatch")
    boundary = context["promotion_boundary"]
    require(isinstance(boundary, dict), f"{source} promotion_boundary must be mapping")
    for key in ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "waes_review"]:
        require(boundary.get(key) == 0, f"{source} promotion_boundary.{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{source} promotion_boundary.{key} must be false")


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if fixture.get("loop_round_count") != 112:
        failures.append("loop_round_count_mismatch")
    if fixture.get("project_group_scope") != PROJECT_GROUP:
        failures.append("project_group_scope_mismatch")
    if fixture.get("context_shapes_supported") != CONTEXT_SHAPES:
        failures.append("context_shapes_supported_mismatch")
    boundary = fixture.get("boundary", {})
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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)

    require(evidence.get("evidence_id") == "WAS-LOOP-CONTEXT-COVERAGE-REFRESH-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_loop_context_coverage_refresh_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-LOOP-CONTEXT-COVERAGE-REFRESH-001", "invalid round id")

    covered = evidence.get("covered_loop_rounds")
    require(isinstance(covered, list), "covered_loop_rounds must be a list")
    require(len(covered) == evidence.get("coverage_scope", {}).get("loop_round_count") == 112, "loop round count mismatch")
    require(evidence.get("coverage_scope", {}).get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("coverage_scope", {}).get("context_shapes_supported") == CONTEXT_SHAPES, "context shape list mismatch")

    shapes_seen: set[str] = set()
    for source in covered:
        shape, context = extract_context(ROOT / source)
        shapes_seen.add(shape)
        if shape == "flat_v1":
            validate_flat_context(source, context)
        elif shape == "nested_v2":
            validate_nested_context(source, context)
        else:
            raise SystemExit(f"FAIL: unsupported context shape: {shape}")
    require(shapes_seen == set(CONTEXT_SHAPES), "both flat_v1 and nested_v2 contexts must be covered")

    positive = load_json(FIXTURE_DIR / "loop-context-coverage-refresh-positive.json")
    require(not validate_fixture(positive), "positive fixture should pass")
    negative_paths = sorted(FIXTURE_DIR.glob("loop-context-coverage-refresh-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        require(validate_fixture(load_json(path)), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    boundary = evidence.get("boundary", {})
    for key in ZERO_BOUNDARY_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_BOUNDARY_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "loop_round_count | `112`",
        "project_scope_count | `14`",
        "context_shapes_supported | `flat_v1,nested_v2`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("覆盖统计已刷新到 112 个 round" in loop_text, "loop feedback missing")
    require("object_family: LoopWasContextCoverageRefresh" in loop_text, "loop_was_context missing refresh object family")

    print(
        "was_loop_context_coverage_refresh=pass "
        "loop_round_count=112 project_scope_count=14 context_shapes=flat_v1,nested_v2 "
        "positive_fixtures=1 negative_fixtures=3 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-STATUS-MATRIX-AND-CONTROL-BOARD-REFRESH-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
