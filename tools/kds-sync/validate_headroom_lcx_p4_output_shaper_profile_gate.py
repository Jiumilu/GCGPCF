#!/usr/bin/env python3
"""Validate Headroom LCX P4 output-shaper profile gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p4_output_shaper_profile_gate.py"

PROJECTS = [
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
]

FORBIDDEN_CONTEXTS = {
    "official_acceptance",
    "compliance_review",
    "legal_contract",
    "finance_decision",
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
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("FORBIDDEN_CONTEXTS" in runner, "runner must define forbidden contexts")
    require("output_shaper" in runner, "runner must inspect output_shaper")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    profile_gate = evidence.get("profile_gate", {})
    require(profile_gate.get("output_shaper_profile_gate") is True, "P4 profile gate must pass")
    require(profile_gate.get("forbidden_context_pass_count") == 4, "all forbidden contexts must pass")
    require(profile_gate.get("allowed_context_pass_count") == 5, "all allowed shaper contexts must pass")
    require(profile_gate.get("schema_forbidden_context_gate") is True, "schema forbidden context gate must pass")
    require(profile_gate.get("waes_disable_output_shaper_gate") is True, "WAES output shaper gate must pass")
    scenarios = evidence.get("scenario_results", [])
    forbidden_seen = set()
    for item in scenarios:
        if item.get("context") in FORBIDDEN_CONTEXTS:
            forbidden_seen.add(item["context"])
            require(item.get("output_shaper") is False, f"forbidden context must disable output_shaper: {item['context']}")
            require(item.get("gate") is True, f"forbidden context gate must pass: {item['context']}")
    require(forbidden_seen == FORBIDDEN_CONTEXTS, "forbidden contexts mismatch")
    gates = evidence.get("gates", {})
    for key in [
        "p4_output_shaper_profile_gate",
        "official_acceptance_output_shaper_disabled",
        "compliance_review_output_shaper_disabled",
        "legal_contract_output_shaper_disabled",
        "finance_decision_output_shaper_disabled",
        "development_output_shaper_allowed",
        "log_debug_output_shaper_allowed",
        "telemetry_default_off",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-20260621",
        "p4_output_shaper_profile_gate | true",
        "official_acceptance_output_shaper_disabled | true",
        "compliance_review_output_shaper_disabled | true",
        "legal_contract_output_shaper_disabled | true",
        "finance_decision_output_shaper_disabled | true",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p4_output_shaper_profile_gate.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p4_output_shaper_profile_gate.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p4_output_shaper_profile_gate=pass "
        "project_count=15 forbidden_context_pass_count=4 allowed_context_pass_count=5 "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
