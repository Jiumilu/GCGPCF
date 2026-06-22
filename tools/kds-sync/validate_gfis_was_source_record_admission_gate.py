#!/usr/bin/env python3
"""Validate the GFIS real source-record admission gate against the WAS profile."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT.parent
WAS_ROOT = BASE / "WAS世界资产体系"
GFIS_ROOT = BASE / "GlobalCloud GFIS"

EVIDENCE_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-admission-gate-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gfis-was-source-record-admission-gate-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-GATE-001.md"
WAS_PROFILE = WAS_ROOT / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
GFIS_REAL_GATE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-real-source-record-intake-gate.json"
GFIS_STRUCTURE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-structure-readiness.json"
GFIS_ELIGIBILITY = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-valid-source-record-eligibility-gate.json"

REQUIRED_WAS_FIELDS = {
    "objectFamily",
    "sourceRecordId",
    "assetDimension",
    "flowType",
    "lifecycle",
    "trustLevel",
    "sourceRefs",
    "evidenceRefs",
    "waesGateRefs",
    "promotionBlockers",
    "nextAction",
    "kdsBacklink",
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
    gfis_real_gate = load_json(GFIS_REAL_GATE)
    gfis_structure = load_json(GFIS_STRUCTURE)
    gfis_eligibility = load_json(GFIS_ELIGIBILITY)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "GFIS-WAS-SOURCE-RECORD-ADMISSION-GATE-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_was_source_record_admission_gate_pass", "invalid evidence status")
    require(evidence.get("scope", {}).get("gate_type") == "read_only_source_record_admission_gate", "gate type mismatch")

    stages = profile.get("stages")
    require(isinstance(stages, list), "WAS stages must be a list")
    s01 = next((stage for stage in stages if stage.get("stageId") == "S01-customer-requirement-or-platform-order"), None)
    require(isinstance(s01, dict), "missing WAS S01 stage")

    target = evidence.get("target_stage", {})
    require(target.get("was_stage_id") == s01.get("stageId"), "target WAS stage mismatch")
    require(target.get("gfis_object_family") == "CustomerRequirementOrPlatformOrder", "target object family mismatch")
    require(target.get("asset_dimension") == s01.get("assetDimension") == "data_asset", "asset dimension mismatch")
    require(target.get("flow_type") == s01.get("flowType") == "commerce_flow", "flow type mismatch")
    require(target.get("lifecycle") == s01.get("lifecycle") == "pending_business_verification", "lifecycle mismatch")
    require(target.get("trust_level") == s01.get("trustLevel") == "T4", "trust level mismatch")
    require(target.get("source_refs") == s01.get("sourceRefs"), "source refs mismatch")
    require(target.get("evidence_refs") == s01.get("evidenceRefs"), "evidence refs mismatch")
    require(target.get("waes_gate_refs") == s01.get("waesGateRefs"), "WAES gate refs mismatch")
    require(target.get("promotion_blockers") == s01.get("promotionBlockers"), "promotion blockers mismatch")
    require(target.get("next_action") == s01.get("nextAction"), "next action mismatch")

    required_fields = set(evidence.get("required_was_fields_for_future_real_source_record", []))
    require(required_fields == REQUIRED_WAS_FIELDS, "required WAS field set mismatch")

    policy = evidence.get("admission_policy", {})
    require(policy.get("must_match_was_stage") == s01.get("stageId"), "policy stage mismatch")
    require(policy.get("must_keep_candidate_state_before_manual_verification") == "pending_business_verification", "manual verification state mismatch")
    for key in [
        "must_reject_without_customer_or_platform_source",
        "must_reject_without_kds_backlink",
        "must_reject_without_waes_gate_ref",
    ]:
        require(policy.get(key) is True, f"{key} must be true")
    for key in [
        "auto_promote_to_valid_source_record",
        "may_create_runtime_primary_key_before_valid_source_record",
        "may_open_review_queue_before_runtime_primary_key",
        "may_open_runtime_intake_before_review_queue",
        "may_create_verified_artifact_before_waes_review",
    ]:
        require(policy.get(key) is False, f"{key} must be false")

    for source_name, source_path in evidence.get("sources", {}).items():
        require(Path(source_path).exists(), f"source missing for {source_name}: {source_path}")

    require(gfis_real_gate.get("object_family") == "CustomerRequirementOrPlatformOrder", "GFIS real gate object family mismatch")
    require(gfis_real_gate.get("state") == "blocked_missing_real_source_record", "GFIS real gate state mismatch")
    require(gfis_real_gate.get("real_business_lane") == "repair_required", "GFIS real lane must remain repair_required")
    require(gfis_real_gate.get("runtime_sop_e2e") == "repair_required", "GFIS runtime SOP must remain repair_required")
    require(gfis_structure.get("counts", {}).get("required_fields") == 12, "GFIS structure readiness must keep 12 required fields")
    require(gfis_structure.get("counts", {}).get("structure_valid_records") == 0, "GFIS structure-valid records must remain 0")
    require(gfis_eligibility.get("counts", {}).get("pending_business_verification_candidates") == 1, "GFIS eligibility pending candidate mismatch")
    require(gfis_eligibility.get("counts", {}).get("valid_source_records") == 0, "GFIS eligibility valid source records must remain 0")

    blocked_counts = evidence.get("gfis_current_blocking_counts", {})
    gfis_real_counts = gfis_real_gate.get("counts", {})
    for key in ZERO_COUNT_KEYS:
        require(blocked_counts.get(key) == 0, f"gfis_current_blocking_counts.{key} must be 0")
    for key in ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(gfis_real_counts.get(key) == 0, f"GFIS real gate count {key} must be 0")

    for phrase in [
        "GFIS 真实 `CustomerRequirementOrPlatformOrder` source-of-record 入场前的 WAS/Ontology 字段门禁",
        "不得自动提升为 `valid_source_record`",
        "本 evidence 不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GFIS 真实 source-of-record 入场已具备 WAS 字段门禁基线" in loop_round, "loop round missing feedback")

    print(
        "gfis_was_source_record_admission_gate=pass "
        "required_was_fields=12 object_family=CustomerRequirementOrPlatformOrder "
        "asset_dimension=data_asset flow_type=commerce_flow lifecycle=pending_business_verification "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
