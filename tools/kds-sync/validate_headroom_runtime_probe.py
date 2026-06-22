#!/usr/bin/env python3
"""Validate Headroom runtime probe evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-PROBE-001.md"
PROBE_SCRIPT = ROOT / "tools/kds-sync/probe_headroom_runtime.py"

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
    probe_script = read(PROBE_SCRIPT)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("HEADROOM_TELEMETRY" in probe_script, "probe script must enforce telemetry gate")

    require(evidence.get("evidence_id") == "HEADROOM-RUNTIME-PROBE-20260621", "invalid evidence id")
    require(evidence.get("status") == "runtime_probe_completed_no_project_group_compression", "invalid status")
    require(evidence.get("headroom_runtime_imported") is True, "runtime must import in probe evidence")
    require(evidence.get("headroom_runtime_used") is True, "runtime must be executed in probe evidence")
    require(evidence.get("headroom_version") == "0.26.0", "unexpected headroom version")
    require(evidence.get("python_version") == "3.12.13", "unexpected probe python version")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects_covered") == PROJECTS, "project coverage mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurements")

    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("tokens_before") == aggregate.get("tokens_after"), "runtime probe should currently prove no savings")
    require(aggregate.get("tokens_saved") == 0, "runtime tokens saved must currently be zero")
    require(aggregate.get("runtime_saving_rate") == 0.0, "runtime saving rate must currently be zero")
    require(aggregate.get("all_marker_gates_pass") is True, "marker gates must pass")
    require(aggregate.get("all_runtime_compressions_positive") is False, "runtime compression must not be claimed positive")
    require(aggregate.get("all_transforms_noop") is True, "all transforms should be noop in current evidence")
    require(evidence.get("decision", {}).get("runtime_admission_gate") is False, "runtime admission gate must be false")

    measurements = evidence.get("measurements", [])
    require(len(measurements) == 15, "measurement count mismatch")
    for item in measurements:
        require(item.get("project") in PROJECTS, f"unexpected project: {item.get('project')}")
        require(item.get("tokens_saved") == 0, f"unexpected runtime savings for {item.get('project')}")
        require(item.get("transforms_applied") == ["router:noop"], f"unexpected transform for {item.get('project')}")
        require(item.get("marker_gate") is True, f"marker gate failed for {item.get('project')}")
        require(item.get("raw_text_stored") is False, f"raw text stored for {item.get('project')}")

    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")

    for phrase in [
        "HEADROOM-RUNTIME-PROBE-20260621",
        "runtime_admission_gate | false",
        "router:noop",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("probe_headroom_runtime.py" in loop_round, "loop round missing probe script")

    print(
        "headroom_runtime_probe=pass "
        "runtime_imported=true version=0.26.0 "
        "project_count=15 runtime_saving_rate=0.0 "
        "runtime_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
