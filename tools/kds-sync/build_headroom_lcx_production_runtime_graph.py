#!/usr/bin/env python3
"""Build the Headroom LCX production runtime graph evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/12-GPCF"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md"
KDS_OUTPUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.json"
KDS_OUTPUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.md"
KDS_OUTPUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md"

GRAPH_MANIFEST = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
COST_MODEL = EVIDENCE_DIR / "headroom-cost-sensitivity-model-20260621.json"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
RUNNER_CONTRACT = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json"
AUTH_REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-request-20260623.json"
TRANSITION_GRAPH = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
ANSWER_GATE = EVIDENCE_DIR / "headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json"

PROJECT_IDS = [
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


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_graph() -> dict[str, Any]:
    manifest = load_json(GRAPH_MANIFEST)
    cost_model = load_json(COST_MODEL)
    runner = load_json(RUNNER_CONTRACT)
    auth_request = load_json(AUTH_REQUEST)
    transition = load_json(TRANSITION_GRAPH)
    answer_gate = load_json(ANSWER_GATE)
    rollback_text = read_text(ROLLBACK_MD)

    nodes = [
        {
            "node_id": "current_controlled_graph",
            "status": "controlled",
            "evidence": manifest["graph_id"],
        },
        {
            "node_id": "runtime_route_layer",
            "status": "controlled",
            "evidence": "HEADROOM-LCX-GRAPH-MANIFEST-20260623",
        },
        {
            "node_id": "runtime_cost_layer",
            "status": "controlled",
            "evidence": cost_model["evidence_id"],
        },
        {
            "node_id": "runtime_rollback_layer",
            "status": "controlled_no_production",
            "evidence": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
        },
        {
            "node_id": "runtime_execution_contract",
            "status": "precheck_only",
            "evidence": runner["contract_id"],
        },
        {
            "node_id": "measurement_authorization_boundary",
            "status": "precheck_only",
            "evidence": auth_request["evidence_id"],
        },
        {
            "node_id": "real_business_equivalence_boundary",
            "status": "synthetic_only",
            "evidence": answer_gate["evidence_id"],
        },
        {
            "node_id": "production_branch",
            "status": "blocked",
            "evidence": "HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621",
        },
    ]

    edges = [
        {
            "from": "current_controlled_graph",
            "to": "runtime_route_layer",
            "relation": "graph_manifest_exposes_runtime_routes",
            "allowed": True,
        },
        {
            "from": "runtime_route_layer",
            "to": "runtime_cost_layer",
            "relation": "routes_feed_cost_observation_fields",
            "allowed": True,
        },
        {
            "from": "runtime_route_layer",
            "to": "runtime_execution_contract",
            "relation": "routes_feed_runtime_execution_contract",
            "allowed": True,
        },
        {
            "from": "runtime_execution_contract",
            "to": "measurement_authorization_boundary",
            "relation": "execution_contract_requires_sanitized_precheck_only",
            "allowed": True,
        },
        {
            "from": "measurement_authorization_boundary",
            "to": "real_business_equivalence_boundary",
            "relation": "authorization_boundary_keeps_synthetic_equivalence_only",
            "allowed": True,
        },
        {
            "from": "runtime_cost_layer",
            "to": "runtime_rollback_layer",
            "relation": "cost_replay_needs_rollback_plan_reference",
            "allowed": True,
        },
        {
            "from": "runtime_execution_contract",
            "to": "production_branch",
            "relation": "execution_contract_does_not_open_production_branch",
            "allowed": False,
        },
        {
            "from": "real_business_equivalence_boundary",
            "to": "production_branch",
            "relation": "synthetic_equivalence_does_not_open_production_branch",
            "allowed": False,
        },
        {
            "from": "runtime_rollback_layer",
            "to": "production_branch",
            "relation": "rollback_layer_guards_no_production_write",
            "allowed": False,
        },
    ]

    return {
        "runtime_graph_id": "HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623",
        "status": "production_runtime_graph_defined_controlled_only",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": PROJECT_IDS,
            "runtime_mode": "controlled_precheck_only",
        },
        "current_state": {
            "graph_status": manifest.get("status"),
            "production_branch_blocked": True,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "nodes": nodes,
        "edges": edges,
        "runtime_controls": {
            "execution_allowed_now": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "real_kds_api_write": False,
            "headroom_learn_apply": False,
            "memory_as_kds_fact_source": False,
        },
        "runtime_requirements": [
            {
                "requirement_id": "project_group_scope_15_domains",
                "state": "proven",
                "evidence": "HEADROOM-LCX-GRAPH-MANIFEST-20260623",
            },
            {
                "requirement_id": "cost_model_replayable",
                "state": "proven_controlled_only",
                "evidence": cost_model["evidence_id"],
            },
            {
                "requirement_id": "rollback_plan_bound",
                "state": "proven_controlled_only",
                "evidence": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            },
            {
                "requirement_id": "runtime_execution_precheck",
                "state": "precheck_only",
                "evidence": runner["contract_id"],
            },
            {
                "requirement_id": "authorization_boundary",
                "state": "precheck_only",
                "evidence": auth_request["evidence_id"],
            },
            {
                "requirement_id": "synthetic_equivalence_only",
                "state": "synthetic_only",
                "evidence": answer_gate["evidence_id"],
            },
            {
                "requirement_id": "production_branch_open",
                "state": "blocked",
                "evidence": "HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621",
            },
        ],
        "source_refs": {
            "graph_manifest": "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
            "cost_model": "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
            "rollback_plan": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            "runner_contract": "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json",
            "authorization_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json",
            "transition_graph": "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
            "answer_gate": "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json",
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "rollback_anchor": {
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_runbook_written": "Headroom LCX Rollback Plan 20260622-001" in rollback_text,
        },
        "transition_anchor": {
            "transition_graph_id": transition["transition_graph_id"],
            "transition_graph_status": transition["status"],
            "production_branch_blocked": transition["current_state"]["production_branch_blocked"],
        },
    }


def write_outputs(graph: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(graph, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_JSON.write_text(json_text, encoding="utf-8")
    KDS_OUTPUT_JSON.write_text(json_text, encoding="utf-8")

    md_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623",
            "title: Headroom LCX Production Runtime Graph Evidence",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Production Runtime Graph Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623`",
            "",
            "## 结论",
            "",
            "production runtime graph 已按 15 域路由、成本观察、回滚约束、执行契约和真实测量边界组合成受控图谱，但 production branch 仍保持 blocked。",
            "status: production_runtime_graph_defined_controlled_only",
            "",
            "## 节点",
            "",
            "| node_id | status | evidence |",
            "|---|---|---|",
            *[f"| {node['node_id']} | {node['status']} | `{node['evidence']}` |" for node in graph["nodes"]],
            "",
            "## 边",
            "",
            "| from | to | relation | allowed |",
            "|---|---|---|---|",
            *[f"| {edge['from']} | {edge['to']} | {edge['relation']} | `{str(edge['allowed']).lower()}` |" for edge in graph["edges"]],
            "",
            "## 运行约束",
            "",
            "| requirement_id | state | evidence |",
            "|---|---|---|",
            *[f"| {req['requirement_id']} | {req['state']} | `{req['evidence']}` |" for req in graph["runtime_requirements"]],
            "",
            "## 当前状态",
            "",
            "- production_branch_blocked: `true`",
            "- production_token_measurement_allowed: `false`",
            "- measured_production_tokens: `false`",
            "- production_admission_gate: `false`",
            "- accepted: `false`",
            "- integrated: `false`",
            "- production_ready: `false`",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实生产代理已启动。",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示生产分支已打开。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUTPUT_MD.write_text(md_text, encoding="utf-8")
    KDS_OUTPUT_MD.write_text(md_text, encoding="utf-8")

    loop_text = dedent(
        f"""\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001
        title: "Loop Round: GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # Loop Round: GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`
        - `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json`
        - `docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md`

        ## 动作

        - 将运行、成本、回滚与授权边界组合成生产 runtime graph。
        - 明确 15 域路由如何进入 runtime contract、cost observation 和 rollback boundary。
        - 保持 production branch blocked，避免把受控图谱写成生产开口。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json`
        - `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.md`
        - `tools/kds-sync/build_headroom_lcx_production_runtime_graph.py`
        - `tools/kds-sync/validate_headroom_lcx_production_runtime_graph.py`

        ## 检查

        ```bash
        python3 tools/kds-sync/validate_headroom_lcx_production_runtime_graph.py
        ```

        ## 反馈

        production runtime graph 已将 route、cost、rollback、execution contract 和 authorization boundary 组合到同一张受控图里，但 production branch 仍未打开。

        ## 下一轮

        若未来出现新的真实测量授权窗口，再把 runtime graph 中的 precheck-only 边升级为真实执行路径。

        ## 审计快照

        | 项 | 当前值 |
        |---|---|
        | project_count | `15` |
        | production_branch_blocked | `true` |
        | production_token_measurement_allowed | `false` |
        | measured_production_tokens | `false` |
        | production_admission_gate | `false` |
        | accepted | `false` |
        | integrated | `false` |
        | production_ready | `false` |
        """
    ).strip() + "\n"
    OUTPUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUTPUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    graph = build_graph()
    write_outputs(graph)
    print(
        "headroom_lcx_production_runtime_graph=generated "
        "project_count=15 production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
