#!/usr/bin/env python3
"""Validate Headroom continuous LOOP cost observation evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LOOP-COST-OBSERVATION-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_loop_cost_observation.py"


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("all_blocked_scenarios_excluded" in runner, "runner must enforce blocked exclusion")
    require(evidence.get("evidence_id") == "HEADROOM-LOOP-COST-OBSERVATION-20260621", "invalid evidence id")
    require(evidence.get("status") == "continuous_loop_cost_observation_enabled_for_metric_output", "invalid status")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    window = evidence.get("observation_window", {})
    require(window.get("source_count") == 5, "source count mismatch")
    require(window.get("runtime_included_count") == 3, "runtime included count mismatch")
    require(window.get("blocked_scenario_count") == 3, "blocked scenario count mismatch")
    require("headroom_cost_measurement_output" in evidence.get("allowed_scenarios", []), "cost output must be allowed")
    blocked_ids = {item["scenario_id"] for item in evidence.get("blocked_scenarios", [])}
    require(blocked_ids == {"project_group_evidence_json", "loop_validation_log", "rg_marker_search_output"}, "blocked scenario mismatch")
    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("runtime_tokens_saved", 0) > 0, "must show runtime savings")
    require(aggregate.get("runtime_saving_rate", 0) > 0, "runtime saving rate must be positive")
    require(aggregate.get("all_included_gates_pass") is True, "included gates must pass")
    require(aggregate.get("all_blocked_scenarios_excluded") is True, "blocked scenarios must be excluded")
    require(aggregate.get("production_admission_gate") is False, "production gate must remain false")
    observations = evidence.get("observations", [])
    require(len(observations) == 5, "observation count mismatch")
    require(any(item["observation_type"] == "controlled_metric_pilot" for item in observations), "missing controlled pilot observation")
    require(evidence.get("decision", {}).get("loop_cost_observation_gate") is True, "observation gate must pass")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-LOOP-COST-OBSERVATION-20260621",
        "loop_cost_observation_gate | true",
        "production_admission_gate | false",
        "metric_and_adapter_output_and_cost_evidence_only",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_loop_cost_observation.py" in loop_round, "loop round missing runner")
    print(
        "headroom_loop_cost_observation=pass "
        f"runtime_included={window['runtime_included_count']} "
        f"runtime_saving_rate={aggregate['runtime_saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
