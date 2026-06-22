#!/usr/bin/env python3
"""Validate GFIS runtime SOP E2E mapping to the WAS semantic profile."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT.parent
WAS_ROOT = BASE / "WAS世界资产体系"
GFIS_ROOT = BASE / "GlobalCloud GFIS"

EVIDENCE_JSON = ROOT / "docs/harness/evidence/gfis-was-profile-runtime-gate-mapping-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gfis-was-profile-runtime-gate-mapping-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GFIS-WAS-PROFILE-MAPPING-001.md"
WAS_PROFILE = WAS_ROOT / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
GFIS_12_STAGE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-12-stage.json"
GFIS_SCENARIO = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-scenario-coverage-evidence.json"
GFIS_REPLAY = GFIS_ROOT / "docs/harness/sop-e2e/test-data/replay/gfis-runtime-sop-e2e.test-replay-input.json"
GFIS_OBJECT_CONTRACT = GFIS_ROOT / "docs/harness/sop-e2e/test-data/replay/gfis-runtime-sop-e2e.test-runtime-object-contract.json"

DIMENSIONS = {
    "physical_asset",
    "rule_asset",
    "intelligence_asset",
    "data_asset",
    "economic_asset",
    "energy_asset",
    "organization_asset",
    "spacetime_asset",
}
FLOWS = {
    "material_flow",
    "information_flow",
    "capital_flow",
    "spacetime_flow",
    "energy_flow",
    "commerce_flow",
    "knowledge_flow",
    "rule_flow",
}
ZERO_COUNT_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
    "accepted_integrated",
    "production_ready",
    "production_writes",
    "real_external_api_writes",
]


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


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(read(path))
    require(isinstance(value, dict), f"{path} must contain a YAML mapping")
    return value


def run(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout}\n{completed.stderr}",
    )
    return (completed.stdout + completed.stderr).strip()


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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    profile = load_yaml(WAS_PROFILE)
    gfis_12 = load_json(GFIS_12_STAGE)
    gfis_scenario = load_json(GFIS_SCENARIO)
    gfis_replay = load_json(GFIS_REPLAY)
    gfis_objects = load_json(GFIS_OBJECT_CONTRACT)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "GFIS-WAS-PROFILE-RUNTIME-GATE-MAPPING-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_was_profile_runtime_gate_mapping_pass", "invalid evidence status")
    require(evidence.get("scope", {}).get("mapping_type") == "read_only_semantic_gate_mapping", "mapping type mismatch")

    require(profile.get("profileId") == "gfis-runtime-sop-e2e-was-profile", "WAS profile id mismatch")
    require(profile.get("stageCount") == 12, "WAS profile must have 12 stages")
    stages = profile.get("stages")
    require(isinstance(stages, list) and len(stages) == 12, "WAS profile stages mismatch")
    require({stage["assetDimension"] for stage in stages} == DIMENSIONS, "WAS stage dimensions must cover 8 dimensions")
    require({stage["flowType"] for stage in stages} == FLOWS, "WAS stage flows must cover 8 flows")

    replay_sequence = gfis_replay.get("replay_sequence")
    require(isinstance(replay_sequence, list) and len(replay_sequence) == 12, "GFIS replay must have 12 stages")
    object_contracts = gfis_objects.get("object_contracts")
    require(isinstance(object_contracts, list) and len(object_contracts) == 15, "GFIS object contract must have 15 objects")
    object_types = {obj["runtime_object_id"]: obj["object_type"] for obj in object_contracts}
    replay_objects = {step["stage_id"]: step["runtime_object_id"] for step in replay_sequence}

    coverage = evidence.get("coverage", {})
    require(coverage.get("was_stage_count") == 12, "coverage.was_stage_count mismatch")
    require(coverage.get("gfis_replay_stage_count") == 12, "coverage.gfis_replay_stage_count mismatch")
    require(coverage.get("gfis_runtime_object_count") == 15, "coverage.gfis_runtime_object_count mismatch")
    require(coverage.get("all_was_dimensions_covered") is True, "WAS dimensions not covered")
    require(coverage.get("all_was_flows_covered") is True, "WAS flows not covered")
    require(coverage.get("test_data_lane") == "pass", "test_data_lane must pass")
    require(coverage.get("real_business_lane") == "repair_required", "real_business_lane must remain repair_required")
    require(coverage.get("runtime_sop_e2e") == "repair_required", "runtime_sop_e2e must remain repair_required")

    mapping = evidence.get("mapping")
    require(isinstance(mapping, list) and len(mapping) == 12, "mapping must have 12 entries")
    require([entry["was_stage_id"] for entry in mapping] == [stage["stageId"] for stage in stages], "mapping must follow WAS stage order")
    require([entry["gfis_stage_id"] for entry in mapping] == [step["stage_id"] for step in replay_sequence], "mapping must follow GFIS replay order")
    for entry, stage in zip(mapping, stages):
        gfis_stage_id = entry["gfis_stage_id"]
        gfis_object_id = entry["gfis_runtime_object_id"]
        require(gfis_stage_id in replay_objects, f"unknown GFIS stage: {gfis_stage_id}")
        require(replay_objects[gfis_stage_id] == gfis_object_id, f"{gfis_stage_id} runtime object mismatch")
        require(object_types.get(gfis_object_id) == entry["gfis_runtime_object_type"], f"{gfis_object_id} object type mismatch")
        require(entry["asset_dimension"] == stage["assetDimension"], f"{stage['stageId']} asset dimension mismatch")
        require(entry["flow_type"] == stage["flowType"], f"{stage['stageId']} flow type mismatch")

    for source_name, source_path in evidence.get("sources", {}).items():
        require(Path(source_path).exists(), f"source missing for {source_name}: {source_path}")

    require(gfis_12.get("test_stage_count") == 12, "GFIS 12 stage count mismatch")
    require(gfis_12.get("test_data_lane") == "pass", "GFIS test lane must pass")
    require(gfis_12.get("real_business_lane") == "repair_required", "GFIS real lane must remain repair_required")
    require(gfis_scenario.get("covered_stage_count") == 12, "GFIS scenario coverage count mismatch")
    require(gfis_scenario.get("test_data_scenario_coverage") == "pass", "GFIS scenario coverage must pass")
    require(gfis_scenario.get("runtime_sop_e2e") == "repair_required", "GFIS runtime SOP E2E must remain repair_required")

    blocked_counts = evidence.get("blocked_real_business_counts", {})
    for key in ZERO_COUNT_KEYS:
        require(blocked_counts.get(key) == 0, f"blocked_real_business_counts.{key} must be 0")
        require(gfis_scenario.get(key) == 0, f"GFIS scenario {key} must be 0")

    for claim in ["accepted", "integrated", "production_ready"]:
        require(claim not in evidence.get("status", ""), f"status must not claim {claim}")
    for phrase in ["real_business_lane | repair_required", "不证明 GFIS 真实业务 SOP E2E 完成", "不升级 accepted"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GFIS runtime SOP E2E 已具备 WAS 语义 profile 的只读映射基线" in loop_round, "loop round missing feedback")

    was_output = run(["python3", "okf/validators/validate_all.py"], WAS_ROOT)
    require("PASS validate_gfis_runtime_sop_e2e_profile" in was_output, "WAS profile validator must pass")

    print(
        "gfis_was_profile_runtime_gate_mapping=pass "
        "was_stages=12 gfis_stages=12 dimensions=8 flows=8 "
        "test_data_lane=pass real_business_lane=repair_required "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
