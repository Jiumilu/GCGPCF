#!/usr/bin/env python3
"""Validate the 15-project Headroom LCX sanitized metadata fixture."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_project_group_sanitized_fixture.py"

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
SCENARIOS = {"loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"}


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
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("--check-only is required" in runner, "runner must require --check-only")

    require(fixture.get("fixture_id") == "HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622", "invalid fixture id")
    require(fixture.get("project_count") == 15 and fixture.get("projects") == PROJECTS, "project coverage mismatch")
    require(fixture.get("scenario_count") == 3 and set(fixture.get("scenarios", [])) == SCENARIOS, "scenario coverage mismatch")
    require(fixture.get("entry_count") == 45, "entry count mismatch")
    entries = fixture.get("entries", [])
    require(isinstance(entries, list) and len(entries) == 45, "entries mismatch")
    require({entry.get("project") for entry in entries} == set(PROJECTS), "entry project coverage mismatch")
    require({entry.get("scenario") for entry in entries} == SCENARIOS, "entry scenario coverage mismatch")
    for key in [
        "sensitive_raw_text_stored",
        "contains_provider_secret",
        "contains_authorization_header",
        "contains_raw_prompt",
        "contains_raw_completion",
        "contains_customer_contract_text",
        "measured_production_tokens",
        "production_token_measurement_allowed",
    ]:
        require(fixture.get(key) is False, f"fixture boundary must be false: {key}")
    for entry in entries:
        require(entry.get("source_kind") == "project_group_sanitized_fixture_metadata_only", "source kind mismatch")
        require(entry.get("input_tokens_before", 0) > entry.get("input_tokens_after", 0), "input token fixture must decrease")
        require(entry.get("answer_equivalence") == "not_measured", "answer equivalence must be not_measured")
        require(entry.get("sensitive_redaction_gate") == "pass", "redaction gate must pass")
        require(entry.get("project_marker_gate") == "fixture_marker_preserved", "marker gate mismatch")
        require(entry.get("retrieval_miss_count") in {0, 1}, "retrieval miss threshold mismatch")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622", "invalid evidence id")
    require(evidence.get("status") == "project_group_sanitized_fixture_pass_no_measurement", "invalid status")
    require(evidence.get("project_count") == 15, "evidence project count mismatch")
    require(evidence.get("scenario_count") == 3, "evidence scenario count mismatch")
    require(evidence.get("entry_count") == 45, "evidence entry count mismatch")
    require(evidence.get("coverage_failures") == [], "coverage failures must be empty")
    gates = evidence.get("gates", {})
    for key in ["project_group_fixture_gate", "project_coverage_gate", "scenario_coverage_gate", "entry_count_gate", "metadata_only", "check_only"]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "raw_text_stored",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622",
        "project_group_fixture_gate | true",
        "project_coverage_gate | true",
        "metadata_only | true",
        "saving_rate | not_calculated",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_project_group_sanitized_fixture.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_project_group_sanitized_fixture.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_project_group_sanitized_fixture=pass_check_only "
        "project_count=15 scenario_count=3 entry_count=45 metadata_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
