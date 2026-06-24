#!/usr/bin/env python3
"""Validate the Headroom LCX production runtime graph evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_production_runtime_graph.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
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
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    graph = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    runner = read(RUNNER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_headroom_lcx_production_runtime_graph" in runner, "runner must build runtime graph")

    require(graph.get("runtime_graph_id") == "HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623", "invalid runtime graph id")
    require(graph.get("status") == "production_runtime_graph_defined_controlled_only", "invalid runtime graph status")
    require(graph.get("scope", {}).get("project_count") == 15, "project count mismatch")

    node_ids = {node.get("node_id") for node in graph.get("nodes", [])}
    for node_id in [
        "current_controlled_graph",
        "runtime_route_layer",
        "runtime_cost_layer",
        "runtime_rollback_layer",
        "runtime_execution_contract",
        "measurement_authorization_boundary",
        "real_business_equivalence_boundary",
        "production_branch",
    ]:
        require(node_id in node_ids, f"missing node: {node_id}")

    edges = graph.get("edges", [])
    require(len(edges) >= 8, "edge count too short")
    require(any(edge.get("relation") == "execution_contract_does_not_open_production_branch" for edge in edges), "missing execution block edge")
    require(any(edge.get("relation") == "synthetic_equivalence_does_not_open_production_branch" for edge in edges), "missing equivalence block edge")
    require(any(edge.get("relation") == "rollback_layer_guards_no_production_write" for edge in edges), "missing rollback block edge")

    controls = graph.get("runtime_controls", {})
    require(controls.get("execution_allowed_now") is False, "execution must remain blocked")
    require(controls.get("production_proxy_started") is False, "production proxy must remain false")
    require(controls.get("production_sdk_enabled") is False, "production sdk must remain false")
    require(controls.get("production_external_api_write") is False, "production external api write must remain false")
    require(controls.get("real_kds_api_write") is False, "real kds api write must remain false")

    for phrase in [
        "HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623",
        "production_runtime_graph_defined_controlled_only",
        "production_branch_blocked: `true`",
        "production_ready: `false`",
    ]:
        require(phrase in md, f"md missing phrase: {phrase}")

    for phrase in [
        "production runtime graph",
        "build_headroom_lcx_production_runtime_graph.py",
        "validate_headroom_lcx_production_runtime_graph.py",
    ]:
        require(phrase in loop, f"loop missing phrase: {phrase}")

    print(
        "headroom_lcx_production_runtime_graph=pass "
        "project_count=15 production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
