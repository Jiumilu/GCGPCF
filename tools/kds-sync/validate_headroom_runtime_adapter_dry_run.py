#!/usr/bin/env python3
"""Validate Headroom runtime adapter dry-run evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-ADAPTER-DRY-RUN-001.md"
ADAPTER_SCRIPT = ROOT / "tools/kds-sync/run_headroom_runtime_adapter_dry_run.py"

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
    adapter_script = read(ADAPTER_SCRIPT)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("HEADROOM_TELEMETRY" in adapter_script, "adapter script must enforce telemetry gate")
    require("CompressionUnit" in adapter_script, "adapter script must use Headroom CompressionUnit")
    require("compress_unit_with_router" in adapter_script, "adapter script must use Headroom router unit path")

    require(evidence.get("evidence_id") == "HEADROOM-RUNTIME-ADAPTER-DRY-RUN-20260621", "invalid evidence id")
    require(evidence.get("status") == "runtime_adapter_dry_run_measured_below_l2_threshold", "invalid status")
    require(evidence.get("headroom_runtime_imported") is True, "runtime must import")
    require(evidence.get("headroom_runtime_used") is True, "runtime must execute")
    require(evidence.get("headroom_version") == "0.26.0", "unexpected headroom version")
    require(evidence.get("python_version") == "3.12.13", "unexpected probe python version")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects_covered") == PROJECTS, "project coverage mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurements")

    adapter = evidence.get("adapter", {})
    require(adapter.get("name") == "project_group_evidence_json", "adapter name mismatch")
    require(adapter.get("role") == "tool", "adapter role mismatch")
    require(adapter.get("raw_text_stored") is False, "adapter must not store raw text")
    require(isinstance(adapter.get("input_sha256"), str) and len(adapter["input_sha256"]) == 64, "missing input hash")

    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("tokens_before", 0) > aggregate.get("tokens_after", 0), "adapter must show positive runtime compression")
    require(aggregate.get("tokens_saved", 0) > 0, "adapter must save tokens")
    require(aggregate.get("runtime_adapter_saving_rate", 0) > 0, "saving rate must be positive")
    require(
        aggregate.get("runtime_adapter_saving_rate", 0) < aggregate.get("minimum_saving_rate", 0.2),
        "adapter evidence should remain below L2 threshold until remeasured",
    )
    require(aggregate.get("modified") is True, "runtime adapter should modify the payload")
    require(aggregate.get("all_marker_gates_pass") is True, "marker gates must pass")
    require(aggregate.get("missing_markers") == [], "missing marker list must be empty")
    require("mixed" in aggregate.get("transforms_applied", []), "expected mixed transform marker")
    require(evidence.get("decision", {}).get("runtime_adapter_admission_gate") is False, "adapter admission must remain false")

    records = evidence.get("records", [])
    require(len(records) == 15, "record count mismatch")
    for item in records:
        require(item.get("project") in PROJECTS, f"unexpected project: {item.get('project')}")
        require(item.get("evidence_line_count", 0) > 0, f"missing evidence lines for {item.get('project')}")
        require(item.get("raw_text_stored") is False, f"raw text stored for {item.get('project')}")

    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")

    for phrase in [
        "HEADROOM-RUNTIME-ADAPTER-DRY-RUN-20260621",
        "runtime_adapter_admission_gate | false",
        "below L2 threshold",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_runtime_adapter_dry_run.py" in loop_round, "loop round missing adapter script")

    print(
        "headroom_runtime_adapter_dry_run=pass "
        "runtime_imported=true version=0.26.0 "
        f"project_count=15 runtime_adapter_saving_rate={aggregate['runtime_adapter_saving_rate']} "
        "runtime_adapter_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
