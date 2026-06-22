#!/usr/bin/env python3
"""Validate Headroom controlled metric-output pilot evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-CONTROLLED-METRIC-PILOT-001.md"
PILOT = ROOT / "tools/kds-sync/run_headroom_controlled_metric_pilot.py"


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
    pilot = read(PILOT)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("all_rejected_applications_blocked" in pilot, "pilot must verify rejected applications")
    require(evidence.get("evidence_id") == "HEADROOM-CONTROLLED-METRIC-PILOT-20260621", "invalid evidence id")
    require(evidence.get("status") == "controlled_metric_output_pilot_applied", "invalid status")
    require(evidence.get("pilot_scope") == "structured_metric_and_marker_preserving_adapter_outputs", "pilot scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("allowed_application_count") == 2, "allowed application count mismatch")
    require(evidence.get("rejected_application_count") == 3, "rejected application count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurement")
    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("saving_rate") == 0.636619, "saving rate mismatch")
    require(aggregate.get("tokens_saved") == 1589, "tokens saved mismatch")
    require(aggregate.get("all_allowed_applications_applied") is True, "allowed application was not applied")
    require(aggregate.get("all_rejected_applications_blocked") is True, "rejected application was applied")
    require(aggregate.get("all_marker_gates_pass") is True, "marker gate failed")
    applications = evidence.get("applications", [])
    require(len(applications) == 2, "application count mismatch")
    applied = {item["scenario_id"]: item for item in applications}
    for scenario in ["headroom_cost_measurement_output", "marker_preserving_log_search_adapter_output"]:
        require(scenario in applied, f"missing applied scenario: {scenario}")
        require(applied[scenario].get("applied") is True, f"allowed scenario must be applied: {scenario}")
    rejections = {item["scenario_id"]: item for item in evidence.get("rejections", [])}
    for scenario in ["project_group_evidence_json", "loop_validation_log", "rg_marker_search_output"]:
        require(scenario in rejections, f"missing rejection: {scenario}")
        require(rejections[scenario].get("applied") is False, f"rejected scenario applied: {scenario}")
    require(evidence.get("decision", {}).get("controlled_metric_pilot_gate") is True, "pilot gate must pass")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-CONTROLLED-METRIC-PILOT-20260621",
        "controlled_metric_pilot_gate | true",
        "production_admission_gate | false",
        "structured_metric_and_marker_preserving_adapter_outputs",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_controlled_metric_pilot.py" in loop_round, "loop round missing pilot")
    print(
        "headroom_controlled_metric_pilot=pass "
        "allowed_applied=2 rejected_blocked=3 saving_rate=0.636619 "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
