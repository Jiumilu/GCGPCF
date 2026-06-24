#!/usr/bin/env python3
"""Validate the Headroom LCX completion audit evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-completion-audit-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-completion-audit-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md"
GRAPH_MANIFEST = ROOT / "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json"
GAP_MATRIX = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
TRANSITION_GRAPH = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json"
AUTH_FIELD_MAP = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json"
RUNNER_CONTRACT = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json"
RUNTIME_GRAPH = ROOT / "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json"


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
    audit = load_json(EVIDENCE_JSON)
    graph = load_json(GRAPH_MANIFEST)
    gap = load_json(GAP_MATRIX)
    transition = load_json(TRANSITION_GRAPH)
    field_map = load_json(AUTH_FIELD_MAP)
    runner = load_json(RUNNER_CONTRACT)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(audit.get("evidence_id") == "HEADROOM-LCX-COMPLETION-AUDIT-20260623", "invalid evidence id")
    require(audit.get("status") == "controlled_partial_completion_audit", "invalid audit status")
    require(audit.get("project_count") == 15, "project count mismatch")
    require(audit.get("route_count") == 15, "route count mismatch")
    require(audit.get("project_group_scope") == [
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
    ], "project group scope mismatch")

    requirements = {item["requirement_id"]: item for item in audit.get("requirements", [])}
    require(requirements.get("route_graph_coverage", {}).get("state") == "proven", "route graph coverage must be proven")
    require(requirements.get("cost_graph", {}).get("state") == "proven_controlled_only", "cost graph state mismatch")
    require(requirements.get("rollback_graph", {}).get("state") == "proven_controlled_only", "rollback graph state mismatch")
    require(requirements.get("authorization_measurement", {}).get("state") == "precheck_only", "authorization measurement state mismatch")
    require(requirements.get("real_business_equivalence_measurement", {}).get("state") == "blocked", "equivalence state mismatch")
    require(requirements.get("production_runtime_graph", {}).get("state") == "proven_controlled_only", "production runtime graph state mismatch")
    require(requirements.get("accepted_integrated_production_ready", {}).get("state") == "false", "production readiness guard state mismatch")

    current_state = audit.get("current_state", {})
    require(current_state.get("graph_status") == "controlled_pending_real_measurement", "graph status mismatch")
    require(current_state.get("production_branch_blocked") is True, "production branch must remain blocked")
    require(current_state.get("production_token_measurement_allowed") is False, "production token measurement must remain false")
    require(current_state.get("measured_production_tokens") is False, "measured production tokens must remain false")
    require(current_state.get("production_admission_gate") is False, "production admission gate must remain false")
    require(current_state.get("accepted") is False, "accepted must remain false")
    require(current_state.get("integrated") is False, "integrated must remain false")
    require(current_state.get("production_ready") is False, "production_ready must remain false")

    for phrase in [
        "Headroom 的项目群图谱已完成受控化收口",
        "15 域路由、成本图、回滚图和生产 runtime graph 已成型",
        "真实业务等价授权测量、生产分支开放和真实生产 token 测量仍未打开",
        "controlled_partial_completion_audit",
        "route_graph_coverage",
        "real_business_equivalence_measurement",
        "HEADROOM-LCX-COST-BRIDGE-20260623",
        "HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623",
        "production_runtime_graph",
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in [
        "Headroom 图谱已完成受控收口",
        "python3 tools/kds-sync/validate_headroom_lcx_completion_audit.py",
        "accepted=false",
        "production_ready=false",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for phrase in [
        "graph_status\": \"controlled_pending_real_measurement\"",
        "\"production_branch_blocked\": true",
        "\"production_token_measurement_allowed\": false",
        "\"measured_production_tokens\": false",
        "\"production_ready\": false",
    ]:
        require(phrase in read(EVIDENCE_JSON), f"json missing phrase: {phrase}")

    require(graph.get("scope", {}).get("project_count") == 15, "graph manifest project count mismatch")
    require(len(graph.get("project_routes", [])) == 15, "graph manifest route count mismatch")
    require(gap.get("status") == "real_measurement_gap_matrix_defined_no_measurement", "gap matrix status mismatch")
    require(transition.get("status") == "transition_graph_defined_blocked_real_measurement", "transition graph status mismatch")
    require(field_map.get("status") == "authorization_field_map_defined_precheck_only", "field map status mismatch")
    require(runner.get("status") == "runner_contract_defined_precheck_only", "runner contract status mismatch")
    require(RUNTIME_GRAPH.exists(), "runtime graph evidence missing")

    print(
        "headroom_lcx_completion_audit=pass "
        "project_count=15 "
        "route_count=15 "
        "blocked_count=5 "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
