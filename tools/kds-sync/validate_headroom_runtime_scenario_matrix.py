#!/usr/bin/env python3
"""Validate Headroom runtime scenario matrix evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-SCENARIO-MATRIX-001.md"
MATRIX_SCRIPT = ROOT / "tools/kds-sync/run_headroom_runtime_scenario_matrix.py"

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
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
    matrix_script = read(MATRIX_SCRIPT)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("HEADROOM_TELEMETRY" in matrix_script, "matrix script must enforce telemetry gate")
    require("CompressionUnit" in matrix_script, "matrix script must use Headroom CompressionUnit")
    require("ContentRouter" in matrix_script, "matrix script must use Headroom ContentRouter")

    require(evidence.get("evidence_id") == "HEADROOM-RUNTIME-SCENARIO-MATRIX-20260621", "invalid evidence id")
    require(evidence.get("status") == "runtime_scenario_matrix_measured_partial", "invalid status")
    require(evidence.get("headroom_runtime_imported") is True, "runtime must import")
    require(evidence.get("headroom_runtime_used") is True, "runtime must execute")
    require(evidence.get("headroom_version") == "0.26.0", "unexpected headroom version")
    require(evidence.get("python_version") == "3.12.13", "unexpected probe python version")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects_covered") == PROJECTS, "project coverage mismatch")
    require(evidence.get("scenario_count") == 4, "scenario count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurements")

    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("tokens_saved", 0) > 0, "matrix must show positive runtime compression")
    require(aggregate.get("saving_rate", 0) > 0, "aggregate saving rate must be positive")
    require(aggregate.get("scenario_gate_pass_count", 0) >= 1, "at least one scenario must pass")
    require(aggregate.get("scenario_gate_pass_count", 0) < evidence.get("scenario_count", 4), "matrix must remain partial")
    require(aggregate.get("all_marker_gates_pass") is False, "matrix must expose marker failures for unsafe scenarios")
    require(aggregate.get("all_scenario_gates_pass") is False, "all scenario gates must not pass yet")
    require(evidence.get("decision", {}).get("runtime_matrix_admission_gate") is False, "matrix admission must remain false")

    measurements = evidence.get("measurements", [])
    require(len(measurements) == 4, "measurement count mismatch")
    scenario_ids = {item.get("scenario_id") for item in measurements}
    require(
        scenario_ids
        == {
            "project_group_evidence_json",
            "headroom_metric_json_array",
            "loop_validation_log",
            "rg_marker_search_output",
        },
        "scenario id mismatch",
    )
    for item in measurements:
        require(item.get("tokens_before", 0) > 0, f"empty scenario: {item.get('scenario_id')}")
        require(item.get("raw_text_stored") is False, f"raw text stored: {item.get('scenario_id')}")
    require(
        any(item.get("scenario_gate") is True for item in measurements),
        "missing passing scenario",
    )
    require(
        any(item.get("scenario_gate") is False for item in measurements),
        "matrix must retain blocked scenarios",
    )
    require(
        any(item.get("marker_gate") is False for item in measurements),
        "matrix must retain marker-failed scenarios",
    )

    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")

    for phrase in [
        "HEADROOM-RUNTIME-SCENARIO-MATRIX-20260621",
        "runtime_matrix_admission_gate | false",
        "partial",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_runtime_scenario_matrix.py" in loop_round, "loop round missing matrix script")

    print(
        "headroom_runtime_scenario_matrix=pass "
        f"scenario_count={evidence['scenario_count']} "
        f"scenario_gate_pass_count={aggregate['scenario_gate_pass_count']} "
        f"saving_rate={aggregate['saving_rate']} "
        "runtime_matrix_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
