#!/usr/bin/env python3
"""Validate loop_was_context coverage for WAS/Ontology Loop rounds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-loop-context-coverage-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-loop-context-coverage-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-LOOP-CONTEXT-COVERAGE-001.md"

PROJECT_GROUP = [
    "GFIS",
    "GPC",
    "PVAOS",
    "WAES",
    "KDS",
    "Brain",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "GPCF",
    "Studio",
    "WAS",
]
REQUIRED_CONTEXT_KEYS = [
    "project_scope",
    "related_asset_dimensions",
    "related_flows",
    "related_objects",
    "related_events",
    "source_refs",
    "evidence_refs",
    "waes_gate_refs",
    "kds_backlinks",
    "promotion_blockers",
    "next_action",
    "no_write_declaration",
]
REQUIRED_WAES_GATE = "waes://gate/customer-order-source-record-review"
REQUIRED_NO_WRITE_PHRASE = "no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready"


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


def extract_context(path: Path) -> dict[str, Any]:
    text = read(path)
    marker = "## loop_was_context\n\n```yaml\n"
    start = text.find(marker)
    require(start >= 0, f"{path.relative_to(ROOT)} missing loop_was_context block")
    start += len(marker)
    end = text.find("\n```", start)
    require(end > start, f"{path.relative_to(ROOT)} has unterminated loop_was_context block")
    value = yaml.safe_load(text[start:end])
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} loop_was_context must be mapping")
    return value


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)
    require(evidence.get("evidence_id") == "WAS-LOOP-CONTEXT-COVERAGE-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_loop_context_coverage_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-LOOP-CONTEXT-COVERAGE-001", "invalid round id")

    covered = evidence.get("covered_loop_rounds")
    require(isinstance(covered, list), "covered_loop_rounds must be a list")
    require(len(covered) == evidence.get("coverage_scope", {}).get("loop_round_count") == 13, "loop round count mismatch")
    require(evidence.get("coverage_scope", {}).get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("coverage_scope", {}).get("required_context_keys") == REQUIRED_CONTEXT_KEYS, "required key list mismatch")

    for source in covered:
        path = ROOT / source
        context = extract_context(path)
        for key in REQUIRED_CONTEXT_KEYS:
            require(key in context, f"{source} missing context key: {key}")
        require(context["project_scope"] == PROJECT_GROUP, f"{source} project_scope mismatch")
        require("data_asset" in context["related_asset_dimensions"], f"{source} missing data_asset")
        require("commerce_flow" in context["related_flows"], f"{source} missing commerce_flow")
        require("CustomerRequirementOrPlatformOrder" in context["related_objects"], f"{source} missing object family")
        require(REQUIRED_WAES_GATE in context["waes_gate_refs"], f"{source} missing WAES gate ref")
        require("pending_real_source_record" in context["kds_backlinks"], f"{source} missing pending KDS backlink")
        require("valid_source_record_missing" in context["promotion_blockers"], f"{source} missing valid source blocker")
        require("customer_confirmation_missing" in context["promotion_blockers"], f"{source} missing customer confirmation blocker")
        require(context["no_write_declaration"] == REQUIRED_NO_WRITE_PHRASE, f"{source} no-write declaration mismatch")

    boundary = evidence.get("boundary", {})
    for key in ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "waes_review"]:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "13 个 WAS/Ontology 相关 Loop round",
        "loop_round_count | `13`",
        "project_scope_count | `14`",
        "real_source_records | `0`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("WAS/Ontology 相关 Loop round 已具备结构化 `loop_was_context` 覆盖" in loop_text, "loop feedback missing")

    print(
        "was_loop_context_coverage=pass "
        "loop_round_count=13 project_scope_count=14 required_context_keys=12 "
        "asset_dimension=data_asset flow_type=commerce_flow object_family=CustomerRequirementOrPlatformOrder "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-SCENARIO-PROFILE-MATRIX-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
