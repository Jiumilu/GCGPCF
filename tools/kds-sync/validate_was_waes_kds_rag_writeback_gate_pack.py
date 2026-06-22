#!/usr/bin/env python3
"""Validate WAS WAES/KDS/RAG/writeback phased gate pack."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-waes-kds-rag-writeback-gate-pack-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-waes-kds-rag-writeback-gate-pack-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-WAES-KDS-RAG-WRITEBACK-GATE-PACK-001.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
REQUIRED_STAGE_IDS = [
    "S1-WAES-GATE-INPUT",
    "S2-KDS-BINDING",
    "S3-RAG-REFERENCE",
    "S4-GFIS-KWE-WRITEBACK",
    "S5-ELEVEN-POOLS-LINK",
]
STAGE_REQUIRED_KEYS = ["stage_id", "owner", "required_contract", "required_before", "blocks"]
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


def validate_pack(pack: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if pack.get("project_group_scope") != PROJECT_GROUP:
        failures.append("project_group_scope_not_complete_or_ordered")

    stages = pack.get("gate_stages", [])
    if not isinstance(stages, list):
        failures.append("gate_stages_not_list")
        stages = []
    stage_ids = [stage.get("stage_id") for stage in stages if isinstance(stage, dict)]
    if stage_ids != REQUIRED_STAGE_IDS:
        failures.append("gate_stage_order_or_count_invalid")

    stage_by_id = {stage.get("stage_id"): stage for stage in stages if isinstance(stage, dict)}
    for stage in stages:
        if not isinstance(stage, dict):
            failures.append("stage_not_object")
            continue
        for key in STAGE_REQUIRED_KEYS:
            if key not in stage:
                failures.append(f"{stage.get('stage_id', 'unknown')}:missing_{key}")
        if not stage.get("required_before"):
            failures.append(f"{stage.get('stage_id', 'unknown')}:required_before_empty")
        if not stage.get("blocks"):
            failures.append(f"{stage.get('stage_id', 'unknown')}:blocks_empty")

    waes = stage_by_id.get("S1-WAES-GATE-INPUT", {})
    kds = stage_by_id.get("S2-KDS-BINDING", {})
    rag = stage_by_id.get("S3-RAG-REFERENCE", {})
    writeback = stage_by_id.get("S4-GFIS-KWE-WRITEBACK", {})
    pools = stage_by_id.get("S5-ELEVEN-POOLS-LINK", {})
    if waes.get("decision_state") != "not_submitted":
        failures.append("waes_decision_must_remain_not_submitted")
    if kds.get("binding_state") != "candidate_only":
        failures.append("kds_binding_must_remain_candidate_only")
    if kds.get("source_hash_state") not in {"not_applicable_without_real_source_record", "consistent_candidate"}:
        failures.append("kds_source_hash_state_invalid")
    if rag.get("reference_state") != "controlled_reference_only":
        failures.append("rag_must_remain_controlled_reference_only")
    if writeback.get("writeback_state") != "blocked_without_waes_kds_owner_confirmation":
        failures.append("writeback_must_remain_blocked")
    if pools.get("pool_link_state") != "schema_gate_only":
        failures.append("pool_link_must_remain_schema_gate_only")

    boundary = pack.get("boundary", {})
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
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "WAS-WAES-KDS-RAG-WRITEBACK-GATE-PACK-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_waes_kds_rag_writeback_gate_pack_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-WAES-KDS-RAG-WRITEBACK-GATE-PACK-001", "invalid round id")
    require(evidence.get("source_matrix") == "docs/harness/evidence/was-scenario-profile-matrix-20260621.json", "source matrix mismatch")

    failures = validate_pack(evidence)
    require(not failures, f"evidence should pass: {failures}")

    positive = load_json(FIXTURE_DIR / "waes-kds-rag-writeback-gate-pack-positive.json")
    positive_failures = validate_pack(positive)
    require(not positive_failures, f"positive fixture should pass: {positive_failures}")

    negative_paths = sorted(FIXTURE_DIR.glob("waes-kds-rag-writeback-gate-pack-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        fixture = load_json(path)
        require(validate_pack(fixture), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    for phrase in [
        "project_group_scope | `14/14`",
        "gate_stages | `5`",
        "runtime_primary_key_ready | `0`",
        "waes_review | `0`",
        "production_ready | `false`",
        "runtime_write | `false`",
        "kds_api_write | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("分阶段门禁包已建立" in loop_round, "loop feedback missing")
    require("real_source_records: 0" in loop_round, "loop_was_context missing real_source_records")
    require("production_ready: false" in loop_round, "loop_was_context missing production boundary")

    print(
        "was_waes_kds_rag_writeback_gate_pack=pass "
        "project_group_scope=14/14 gate_stages=5 positive_fixtures=1 negative_fixtures=3 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false runtime_write=false kds_api_write=false "
        "next_round=GPCF-ONTOLOGY-WAS-PROJECT-GROUP-ONTOLOGY-REGISTRY-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
