#!/usr/bin/env python3
"""Validate the Headroom LCX real-measurement transition graph evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_transition_graph.py"
GAP_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
ROLLBACK_MD = ROOT / "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md"
WINDOW_GRANT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json"


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
    graph = load_json(EVIDENCE_JSON)
    gap = load_json(GAP_JSON)
    window_grant = load_json(WINDOW_GRANT_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    rollback = read(ROLLBACK_MD)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("real_measurement_transition_graph" in runner, "runner must build transition graph")
    require("Headroom LCX Rollback Plan 20260622-001" in rollback, "rollback plan must be written")

    require(graph.get("transition_graph_id") == "HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623", "invalid transition graph id")
    require(graph.get("status") == "transition_graph_defined_blocked_real_measurement", "invalid transition graph status")
    require(graph.get("scope", {}).get("project_count") == 15, "project count mismatch")
    require("production_branch_blocked" in graph.get("current_state", {}), "current state must expose production_branch_blocked")
    require(graph.get("current_state", {}).get("production_branch_blocked") is True, "production branch must remain blocked")
    require(graph.get("current_state", {}).get("production_token_measurement_allowed") is False, "production token measurement must remain false")
    require(graph.get("current_state", {}).get("measured_production_tokens") is False, "measured production tokens must remain false")
    require(graph.get("current_state", {}).get("production_admission_gate") is False, "production admission gate must remain false")

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    require(len(nodes) >= 10, "node count too short")
    require(len(edges) >= 10, "edge count too short")
    node_ids = {node.get("node_id") for node in nodes}
    for node_id in [
        "current_controlled_graph",
        "real_measurement_gap_matrix",
        "real_measurement_authorization_request_package",
        "real_measurement_authorization_window_request_package",
        "rollback_runbook",
        "sanitized_precheck",
        "real_measurement_authorization_window",
        "waes_harness_decision",
        "sanitized_token_ledger",
        "production_proxy_enablement",
        "real_business_equivalence_measurement",
        "production_branch",
    ]:
        require(node_id in node_ids, f"missing node: {node_id}")
    require(any(node.get("node_id") == "real_measurement_authorization_window" and node.get("status") == "granted_precheck_only" for node in nodes), "authorization window node must be granted_precheck_only")
    require(
        any(node.get("node_id") == "real_measurement_authorization_window" and node.get("evidence") == window_grant.get("evidence_id") for node in nodes),
        "authorization window evidence mismatch",
    )

    blocked_edges = [edge for edge in edges if edge.get("allowed") is False]
    require(len(blocked_edges) >= 4, "blocked edge count too short")
    require(any(edge.get("relation") == "requires_waes_harness_admission" for edge in blocked_edges), "missing waes decision block")
    require(any(edge.get("relation") == "production_proxy_remains_blocked_until_future_authorization" for edge in blocked_edges), "missing proxy block")
    require(any(edge.get("relation") == "real_measurement_requires_non_synthetic_equivalence" for edge in blocked_edges), "missing equivalence block")
    require(any(edge.get("relation") == "production_branch_requires_real_business_equivalence_and_authorized_measurement" for edge in blocked_edges), "missing production branch block")

    require(any(edge.get("relation") == "gap_matrix_creates_precheck_only_request_package" for edge in edges), "missing request package edge")
    require(any(edge.get("relation") == "request_package_records_window_request_only" for edge in edges), "missing window request record edge")
    require(any(edge.get("relation") == "window_request_remains_sanitized_only" for edge in edges), "missing sanitized window request edge")
    require(any(edge.get("relation") == "requires_authorized_window" and edge.get("allowed") is True for edge in edges), "authorized window grant edge must be allowed")

    reqs = graph.get("transition_requirements", [])
    require(len(reqs) >= 9, "transition requirement count too short")
    require(any(req.get("requirement_id") == "requested_window_id" for req in reqs), "missing requested_window_id mapping")
    require(any(req.get("requirement_id") == "requested_by" for req in reqs), "missing requested_by mapping")
    require(any(req.get("requirement_id") == "requested_at" for req in reqs), "missing requested_at mapping")
    require(any(req.get("requirement_id") == "authorized_window_id" and req.get("current_value") != "missing" for req in reqs), "missing authorized_window_id mapping")
    require(any(req.get("requirement_id") == "authorized_by" and req.get("current_value") != "missing" for req in reqs), "missing authorized_by mapping")
    require(any(req.get("requirement_id") == "authorized_at" and req.get("current_value") != "missing" for req in reqs), "missing authorized_at mapping")
    require(any(req.get("requirement_id") == "sanitized_production_token_ledger" for req in reqs), "missing ledger mapping")
    require(any(req.get("requirement_id") == "rollback_plan_id" for req in reqs), "missing rollback plan mapping")
    require(any(req.get("requirement_id") == "waes_harness_admission_decision" for req in reqs), "missing waes decision mapping")
    require(any(req.get("requirement_id") == "real_business_equivalence_measurement" for req in reqs), "missing real equivalence mapping")

    require(graph.get("rollback_anchor", {}).get("rollback_plan_present") is True, "rollback anchor must be present")
    require(graph.get("rollback_anchor", {}).get("rollback_runbook_written") is True, "rollback runbook must be written")
    require(gap.get("gates", {}).get("real_measurement_gap_present") is True, "gap matrix must report real measurement gap")
    require(window_grant.get("real_measurement_window_granted") is True, "window grant must be granted")
    require(window_grant.get("real_measurement_open") is False, "window grant must remain precheck-only")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623",
        "transition_graph_defined_blocked_real_measurement",
        "real_measurement_authorization_window_granted_precheck_only",
        "real_measurement_authorization_window_request_package",
        "real_measurement_authorization_request_package",
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623",
        "real_measurement_gap_present: `true`",
        "real_measurement_window_granted: `true`",
        "production_branch_blocked: `true`",
        "production_token_measurement_allowed: `false`",
        "real_business_equivalence_measurement_allowed: `false`",
        "production_ready: `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in [
        "transition graph",
        "build_headroom_lcx_real_measurement_transition_graph.py",
        "validate_headroom_lcx_real_measurement_transition_graph.py",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "headroom_lcx_real_measurement_transition_graph=pass "
        "project_count=15 real_measurement_gap_present=true production_branch_blocked=true "
        "real_business_equivalence_measurement_allowed=false production_token_measurement_allowed=false "
        "measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
