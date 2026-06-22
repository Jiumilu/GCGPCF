#!/usr/bin/env python3
"""Validate Headroom marker-preserving adapter pilot evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_marker_preserving_adapter_pilot.py"


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
    require("marker_manifest" in runner, "runner must include marker_manifest adapter")
    require(evidence.get("evidence_id") == "HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-20260621", "invalid evidence id")
    require(evidence.get("status") == "marker_preserving_adapter_pilot_measured", "invalid status")
    require(evidence.get("headroom_runtime_used") is True, "runtime must be used")
    require(evidence.get("adapter_scope") == "log_and_search_outputs_only", "adapter scope mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    measurements = evidence.get("measurements", [])
    require(len(measurements) == 2, "measurement count mismatch")
    require({item.get("scenario_id") for item in measurements} == {"loop_validation_log", "rg_marker_search_output"}, "scenario ids mismatch")
    for item in measurements:
        require(item.get("marker_gate") is True, f"marker gate failed: {item.get('scenario_id')}")
        require(item.get("adapter_gate") is True, f"adapter gate failed: {item.get('scenario_id')}")
        require(item.get("saving_rate", 0) >= item.get("minimum_saving_rate", 1), f"saving rate below threshold: {item.get('scenario_id')}")
        require(item.get("raw_text_stored") is False, f"raw text must not be stored: {item.get('scenario_id')}")
    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("scenario_count") == 2, "scenario count mismatch")
    require(aggregate.get("adapter_gate_pass_count") == 2, "adapter pass count mismatch")
    require(aggregate.get("all_marker_gates_pass") is True, "all marker gates must pass")
    require(aggregate.get("all_adapter_gates_pass") is True, "all adapter gates must pass")
    require(evidence.get("decision", {}).get("marker_preserving_adapter_pilot_gate") is True, "adapter pilot gate must pass")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-20260621",
        "marker_preserving_adapter_pilot_gate | true",
        "production_admission_gate | false",
        "log_and_search_outputs_only",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_marker_preserving_adapter_pilot.py" in loop_round, "loop round missing runner")
    print(
        "headroom_marker_preserving_adapter_pilot=pass "
        f"scenario_count={aggregate['scenario_count']} "
        f"adapter_gate_pass_count={aggregate['adapter_gate_pass_count']} "
        f"saving_rate={aggregate['saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
