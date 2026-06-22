#!/usr/bin/env python3
"""Validate the HeadroomCostMeasurement output evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-COST-MEASUREMENT-OUTPUT-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_cost_measurement_output.py"

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
    builder = read(BUILDER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("HEADROOM_TELEMETRY" in builder, "builder must enforce telemetry gate")
    require("HeadroomCostMeasurement" in builder, "builder must define output type")
    require(evidence.get("evidence_id") == "HEADROOM-COST-MEASUREMENT-OUTPUT-20260621", "invalid evidence id")
    require(evidence.get("status") == "cost_measurement_output_class_measured", "invalid status")
    require(evidence.get("headroom_runtime_used") is True, "runtime must execute")
    require(evidence.get("headroom_version") == "0.26.0", "unexpected headroom version")
    require(evidence.get("python_version") == "3.12.13", "unexpected python version")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects_covered") == PROJECTS, "project coverage mismatch")
    require(evidence.get("record_count") == 15, "record count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurements")
    schema = evidence.get("schema", {})
    require(schema.get("name") == "HeadroomCostMeasurement", "schema name mismatch")
    require(schema.get("allowed_application") == "structured_metric_tool_output_only", "application boundary mismatch")
    for field in ["project", "source_path", "structured_surrogate_saving_rate", "marker_gate", "raw_text_stored"]:
        require(field in schema.get("required_fields", []), f"schema missing field: {field}")
    require(schema.get("full_cost_detail_source") == "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json", "full cost source mismatch")
    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("tokens_saved", 0) > 0, "must save tokens")
    require(aggregate.get("saving_rate", 0) >= aggregate.get("minimum_saving_rate", 0.2), "saving gate failed")
    require(aggregate.get("marker_gate") is True, "marker gate failed")
    require(aggregate.get("output_gate") is True, "output gate must pass")
    require("smart_crusher" in aggregate.get("transforms_applied", []), "expected smart_crusher transform")
    require(evidence.get("decision", {}).get("headroom_cost_measurement_output_gate") is True, "decision gate must pass")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-COST-MEASUREMENT-OUTPUT-20260621",
        "HeadroomCostMeasurement",
        "output_gate | true",
        "structured_metric_tool_output_only",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_cost_measurement_output.py" in loop_round, "loop round missing builder")
    print(
        "headroom_cost_measurement_output=pass "
        f"record_count={evidence['record_count']} saving_rate={aggregate['saving_rate']} "
        "output_gate=true measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
