#!/usr/bin/env python3
"""Validate three-window Headroom LOOP cost observation series evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LOOP-COST-OBSERVATION-SERIES-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_loop_cost_observation_series.py"


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
    require("saving_rate_stability_gate" in runner, "runner must check saving-rate stability")
    require(evidence.get("evidence_id") == "HEADROOM-LOOP-COST-OBSERVATION-SERIES-20260621", "invalid evidence id")
    require(evidence.get("status") == "three_window_loop_cost_observation_series_ready", "invalid status")
    require(evidence.get("window_count") == 3, "window count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    windows = evidence.get("windows", [])
    require(len(windows) == 3, "windows length mismatch")
    require(windows[0].get("window_id") == "HEADROOM-LOOP-COST-WINDOW-20260621-001", "window 1 id mismatch")
    require(windows[1].get("window_id") == "HEADROOM-LOOP-COST-WINDOW-20260621-002", "window 2 id mismatch")
    require(windows[2].get("window_id") == "HEADROOM-LOOP-COST-WINDOW-20260621-003", "window 3 id mismatch")
    for window in windows:
        require(window.get("loop_cost_observation_gate") is True, f"window gate failed: {window.get('window_id')}")
        require(window.get("all_blocked_scenarios_excluded") is True, f"blocked scenario included: {window.get('window_id')}")
        require(window.get("runtime_tokens_saved", 0) > 0, f"window has no runtime savings: {window.get('window_id')}")
        require(window.get("production_admission_gate") is False, f"window production gate must stay false: {window.get('window_id')}")
    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("all_window_gates_pass") is True, "all window gates must pass")
    require(aggregate.get("all_blocked_scenarios_excluded") is True, "all blocked scenarios must be excluded")
    require(aggregate.get("window_scope_normalized") is True, "window scope must be normalized")
    require(aggregate.get("saving_rate_stability_gate") is True, "three-window saving rate stability gate must pass after scope normalization")
    require(aggregate.get("max_runtime_saving_rate_drift", 1) <= aggregate.get("drift_gate_threshold", 0), "saving rate drift too high")
    require(aggregate.get("production_admission_gate") is False, "series production gate must remain false")
    require(evidence.get("decision", {}).get("loop_cost_observation_series_gate") is True, "series gate must pass after scope normalization")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-LOOP-COST-OBSERVATION-SERIES-20260621",
        "loop_cost_observation_series_gate | true",
        "production_admission_gate | false",
        "three_window",
        "saving_rate_stability_gate | true",
        "window_scope_normalized | true",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_loop_cost_observation_series.py" in loop_round, "loop round missing runner")
    print(
        "headroom_loop_cost_observation_series=pass "
        f"window_count={evidence['window_count']} "
        f"max_drift={aggregate['max_runtime_saving_rate_drift']} "
        "stability_gate=true "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
