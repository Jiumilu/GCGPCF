#!/usr/bin/env python3
"""Validate the Headroom LCX readiness and L3.5 pilot authorization package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_readiness_pilot_authorization_package.py"

PROJECTS = {
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
}


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
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    builder = read(BUILDER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("EVIDENCE_CHAIN" in builder, "builder must define evidence chain")
    require("L3.5_controlled_sanitized_pilot" in builder, "builder must declare L3.5 recommendation")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-20260622", "invalid evidence id")
    require(evidence.get("status") == "l3_5_controlled_sanitized_pilot_recommended_not_production", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(set(evidence.get("projects", [])) == PROJECTS, "project coverage mismatch")
    require(evidence.get("evidence_chain_count", 0) >= 20, "evidence chain too short")
    require(evidence.get("failures") == [], "failures must be empty")

    readiness = evidence.get("readiness_summary", {})
    require(readiness.get("route_project_count") == 15, "route project count mismatch")
    require(readiness.get("fixture_project_count") == 15, "fixture project count mismatch")
    require(readiness.get("fixture_entry_count") == 45, "fixture entry count mismatch")
    require(readiness.get("replay_round_count") == 3, "replay round count mismatch")
    require(readiness.get("replay_entry_count") == 45, "replay entry count mismatch")
    require(readiness.get("stable_hash_count") == 1, "stable hash count mismatch")
    require(readiness.get("coverage_ok") is True, "coverage must be true")
    require(readiness.get("stability_ok") is True, "stability must be true")
    for key in [
        "real_production_measurement",
        "runtime_compression_effectiveness_proven",
        "business_answer_equivalence_proven",
    ]:
        require(readiness.get(key) is False, f"readiness field must be false: {key}")

    recommendation = evidence.get("recommendation", {})
    require(recommendation.get("recommended_next_authorization") == "L3.5_controlled_sanitized_pilot", "wrong recommendation")
    require(recommendation.get("recommendation_gate") is True, "recommendation gate must be true")
    for key in ["l4_candidate", "l5_candidate", "production_candidate"]:
        require(recommendation.get(key) is False, f"recommendation field must be false: {key}")

    permissions = evidence.get("requested_permissions", {})
    for key in [
        "allow_local_headroom_dry_run",
        "allow_sanitized_fixture_replay",
        "allow_harness_evidence_generation",
        "allow_waes_gate_check",
    ]:
        require(permissions.get(key) is True, f"permission must be true: {key}")
    for key in [
        "allow_raw_prompt_or_completion",
        "allow_unredacted_sensitive_material",
        "allow_production_proxy",
        "allow_external_api_write",
        "allow_kds_api_write",
        "allow_database_migration",
        "allow_permission_change",
        "allow_headroom_learn_apply",
        "allow_status_promotion_to_accepted_integrated_or_production_ready",
    ]:
        require(permissions.get(key) is False, f"permission must be false: {key}")

    gates = evidence.get("gates", {})
    for key in [
        "readiness_package_generated",
        "evidence_chain_present",
        "prior_evidence_has_no_status_promotion",
        "project_group_coverage_gate",
        "project_group_replay_stability_gate",
        "l3_5_controlled_sanitized_pilot_recommended",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "l4_candidate",
        "l5_candidate",
        "real_production_measurement",
        "runtime_compression_effectiveness_proven",
        "business_answer_equivalence_proven",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "headroom_learn_apply_executed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-20260622",
        "recommended_next_authorization | L3.5_controlled_sanitized_pilot",
        "l3_5_controlled_sanitized_pilot_recommended | true",
        "l4_candidate | false",
        "real_production_measurement | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    require("run:" in loop_round, "loop round must include run")
    require("stop:" in loop_round, "loop round must include stop")
    require("verify:" in loop_round, "loop round must include verify")
    require("recover:" in loop_round, "loop round must include recover")
    require("debug:" in loop_round, "loop round must include debug")
    require("validate_headroom_lcx_readiness_pilot_authorization_package.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_readiness_pilot_authorization_package=pass_check_only "
        "recommended_next_authorization=L3.5_controlled_sanitized_pilot "
        "project_count=15 evidence_chain_count="
        f"{evidence.get('evidence_chain_count')} "
        "l4_candidate=false production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
