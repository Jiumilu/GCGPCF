#!/usr/bin/env python3
"""Validate the Headroom LCX objective coverage matrix evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md"
COMP = ROOT / "docs/harness/evidence/headroom-lcx-completion-audit-20260623.json"
GRAPH = ROOT / "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json"
GAP = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
TRANS = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json"
FIELD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json"
RUNNER = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json"
RUNTIME = ROOT / "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json"


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
    matrix = load_json(E_JSON)
    completion = load_json(COMP)
    graph = load_json(GRAPH)
    gap = load_json(GAP)
    trans = load_json(TRANS)
    field = load_json(FIELD)
    runner = load_json(RUNNER)
    md = read(E_MD)
    loop = read(LOOP)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require(matrix.get("evidence_id") == "HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-20260623", "invalid evidence id")
    require(matrix.get("status") == "objective_coverage_matrix_defined_partial", "invalid status")
    require(matrix.get("objective") == "完成完整真实功能图谱：真实业务等价授权测量，以及生产级运行/成本/回滚图谱。", "objective mismatch")
    require(matrix.get("project_count") == 15, "project count mismatch")
    require(matrix.get("project_group_scope") == [
        "GPCF", "KDS", "Brain", "WAES", "GFIS", "GPC", "PVAOS", "Edge", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "Studio", "WAS"
    ], "project scope mismatch")
    require(len(matrix.get("rows", [])) == 6, "row count mismatch")

    states = [row.get("state") for row in matrix.get("rows", [])]
    require(states.count("blocked") == 1, "blocked rows mismatch")
    require(states.count("proven_controlled_only") == 3, "controlled rows mismatch")
    require(states.count("proven") == 1, "proven rows mismatch")
    require(states.count("false_guard") == 1, "false guard rows mismatch")

    current = matrix.get("current_state", {})
    require(current.get("graph_status") == "controlled_pending_real_measurement", "graph status mismatch")
    require(current.get("production_branch_blocked") is True, "production branch blocked mismatch")
    require(current.get("production_token_measurement_allowed") is False, "production token flag mismatch")
    require(current.get("measured_production_tokens") is False, "measured tokens mismatch")
    require(current.get("production_admission_gate") is False, "production gate mismatch")
    require(current.get("accepted") is False, "accepted mismatch")
    require(current.get("integrated") is False, "integrated mismatch")
    require(current.get("production_ready") is False, "production ready mismatch")

    for phrase in [
        "real_measurement_authorization_window_and_waes_harness_decision_remain_precheck_only",
        "headroom-lcx-real-measurement-authorization-window-request-20260623.json",
        "production_runtime_graph_is_controlled_only_and_production_branch_remains_blocked",
        "cost_graph_is_replayable_but_not_production_measured",
        "headroom-lcx-cost-bridge-20260623.json",
        "rollback_plan_exists_but_does_not_open_production_branch",
        "accepted_integrated_and_production_ready_remain_false",
    ]:
        require(phrase in md, f"md missing phrase: {phrase}")

    require(completion.get("evidence_id") == "HEADROOM-LCX-COMPLETION-AUDIT-20260623", "completion evidence mismatch")
    require(graph.get("graph_id") == "HEADROOM-LCX-GRAPH-MANIFEST-20260623", "graph id mismatch")
    require(gap.get("gap_id") == "HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623", "gap id mismatch")
    require(trans.get("transition_graph_id") == "HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623", "transition id mismatch")
    require(field.get("field_map_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623", "field map mismatch")
    require(runner.get("contract_id") == "HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623", "runner contract mismatch")
    require(RUNTIME.exists(), "production runtime graph evidence missing")

    print(
        "headroom_lcx_objective_coverage_matrix=pass "
        "project_count=15 proven_count=1 controlled_only_count=3 blocked_count=1 false_guard_count=1 "
        "production_token_measurement_allowed=false measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
