#!/usr/bin/env python3
"""Build a target-level coverage matrix for the Headroom LCX objective."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/12-GPCF"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-objective-coverage-matrix-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-objective-coverage-matrix-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md"
KDS_OUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-objective-coverage-matrix-20260623.json"
KDS_OUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-objective-coverage-matrix-20260623.md"
KDS_OUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md"

OBJECTIVE = "完成完整真实功能图谱：真实业务等价授权测量，以及生产级运行/成本/回滚图谱。"
PROJECT_IDS = ["GPCF", "KDS", "Brain", "WAES", "GFIS", "GPC", "PVAOS", "Edge", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "Studio", "WAS"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def md_table(rows: list[dict[str, Any]]) -> str:
    lines = ["| objective_item | state | evidence | blocking_reason |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['objective_item']} | {row['state']} | {' ; '.join(row['evidence'])} | {row['blocking_reason']} |")
    return "\n".join(lines)


def build_rows() -> list[dict[str, Any]]:
    return [
        {
            "objective_item": "real_business_equivalence_authorized_measurement",
            "state": "blocked",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.json",
                "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json",
            ],
            "blocking_reason": "real_measurement_authorization_window_and_waes_harness_decision_remain_precheck_only",
        },
        {
            "objective_item": "production_runtime_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json",
                "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json",
            ],
            "blocking_reason": "production_runtime_graph_is_controlled_only_and_production_branch_remains_blocked",
        },
        {
            "objective_item": "production_cost_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
                "docs/harness/evidence/headroom-loop-cost-observation-20260621.json",
                "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json",
                "docs/harness/evidence/headroom-lcx-cost-bridge-20260623.json",
            ],
            "blocking_reason": "cost_graph_is_replayable_but_not_production_measured",
        },
        {
            "objective_item": "production_rollback_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            ],
            "blocking_reason": "rollback_plan_exists_but_does_not_open_production_branch",
        },
        {
            "objective_item": "project_group_scope_15_domains",
            "state": "proven",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-project-group-application-router-20260621.md",
                "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md",
            ],
            "blocking_reason": "none",
        },
        {
            "objective_item": "accepted_integrated_production_ready_guard",
            "state": "false_guard",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-completion-audit-20260623.json",
                "docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.md",
            ],
            "blocking_reason": "accepted_integrated_and_production_ready_remain_false",
        },
    ]


def build_matrix() -> dict[str, Any]:
    completion = read_json(EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.json")
    graph = read_json(EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json")
    gap = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json")
    transition = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json")
    field_map = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json")
    runner = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json")
    runtime_graph = read_json(EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.json")
    cost_model = read_json(EVIDENCE_DIR / "headroom-cost-sensitivity-model-20260621.json")
    answer_gate = read_json(EVIDENCE_DIR / "headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json")
    window_request = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json")
    next_stage_package = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json")
    authorization_chain_replay = read_json(EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-chain-replay-20260623.json")

    rows = build_rows()
    return {
        "evidence_id": "HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-20260623",
        "status": "objective_coverage_matrix_defined_partial",
        "date": "2026-06-23",
        "objective": OBJECTIVE,
        "project_group_scope": PROJECT_IDS,
        "project_count": 15,
        "rows": rows,
        "supporting_evidence": {
            "completion_audit": completion.get("evidence_id"),
            "graph_manifest": graph.get("graph_id"),
            "gap_matrix": gap.get("gap_id"),
            "transition_graph": transition.get("transition_graph_id"),
            "authorization_field_map": field_map.get("field_map_id"),
            "authorization_window_request": window_request.get("evidence_id"),
            "next_stage_authorization_package": next_stage_package.get("evidence_id"),
            "approval_signed_bundle": "HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623",
            "authorization_chain_replay": authorization_chain_replay.get("evidence_id"),
            "authorization_boundary_review": "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623",
            "runner_contract": runner.get("contract_id"),
            "runtime_graph": runtime_graph.get("runtime_graph_id"),
            "cost_model": cost_model.get("evidence_id"),
            "answer_gate": answer_gate.get("evidence_id"),
        },
        "current_state": {
            "graph_status": completion.get("current_state", {}).get("graph_status"),
            "real_measurement_gap_present": completion.get("current_state", {}).get("real_measurement_gap_present"),
            "production_branch_blocked": completion.get("current_state", {}).get("production_branch_blocked"),
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "waes_harness_admission_decision": completion.get("current_state", {}).get("waes_harness_admission_decision"),
            "authorization_window_id": completion.get("current_state", {}).get("authorization_window_id"),
            "next_stage_authorization_package_status": next_stage_package.get("status"),
            "rollback_plan_id": completion.get("current_state", {}).get("rollback_plan_id"),
        },
        "summary": {
            "proven_count": sum(1 for r in rows if r["state"] == "proven"),
            "controlled_only_count": sum(1 for r in rows if r["state"] == "proven_controlled_only"),
            "blocked_count": sum(1 for r in rows if r["state"] == "blocked"),
            "false_guard_count": sum(1 for r in rows if r["state"] == "false_guard"),
            "project_count": 15,
        },
        "non_claims": {
            "real_business_equivalence_proven": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "real_kds_api_write": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    current_state_lines = "\n".join(
        f"| {k} | `{str(v).lower() if isinstance(v, bool) else v}` |" for k, v in matrix["current_state"].items()
    )
    support_lines = "\n".join(f"- `{k}`: `{v}`" for k, v in matrix["supporting_evidence"].items())
    non_claim_lines = "\n".join(f"- `{k}`: `{str(v).lower()}`" for k, v in matrix["non_claims"].items())
    parts = [
        "---",
        "doc_id: GPCF-DOC-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-20260623",
        "title: Headroom LCX Objective Coverage Matrix Evidence",
        "project: GPCF",
        "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.md",
        "source_path: docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Headroom LCX Objective Coverage Matrix Evidence",
        "",
        "## Evidence ID",
        "",
        "`HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-20260623`",
        "",
        "## 目标",
        "",
        OBJECTIVE,
        "",
        "## 覆盖矩阵",
        "",
        md_table(matrix["rows"]),
        "",
        "## 运行图",
        "",
        "- production runtime graph 已组合 route、cost、rollback、runtime contract 与 authorization boundary，但仍保持 blocked。",
        "",
        "## 支撑证据",
        "",
        support_lines,
        "",
        "## 当前状态",
        "",
        current_state_lines,
        "",
        "## 非声明",
        "",
        non_claim_lines,
        "",
        "## 下一步",
        "",
        "在真实测量授权窗口未打开前，目标覆盖矩阵只能作为 current blocked state 的审计映射，不能宣称 full runtime admission 或 production readiness。",
    ]
    return "\n".join(parts) + "\n"


def render_loop_round(matrix: dict[str, Any]) -> str:
    return dedent(
        f"""\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001
        title: "Loop Round: GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # Loop Round: GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-completion-audit-20260623.json`
        - `docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json`

        ## 动作

        - 将 Headroom LCX 的用户目标拆成目标级覆盖矩阵，区分已证明、受控证明、阻断和 false guard。
        - 把真实业务等价授权测量与生产级运行/成本/回滚图谱的当前状态映射到可验证条目。
        - 将下一阶段授权包纳入同一审计层，保证窗口请求、桥接包和 WAES/Harness precheck 可被同屏追踪。
        - 保持 accepted / integrated / production_ready 为 false。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.json`
        - `docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.md`
        - `tools/kds-sync/build_headroom_lcx_objective_coverage_matrix.py`
        - `tools/kds-sync/validate_headroom_lcx_objective_coverage_matrix.py`

        ## 检查

        ```bash
        python3 tools/kds-sync/validate_headroom_lcx_objective_coverage_matrix.py
        ```

        ## 反馈

        目标覆盖矩阵只是把 objective 拆成可验证条目；它确认了当前仍处于 blocked / precheck-only 状态，没有把真实测量授权打开。

        ## 下一轮

        继续等待 WAES/Harness 的真实测量授权裁决，或补齐能够打开 production branch 的新证据。

        ## 审计快照

        | 项 | 当前值 |
        |---|---|
        | project_count | `{matrix['project_count']}` |
        | proven_count | `{matrix['summary']['proven_count']}` |
        | controlled_only_count | `{matrix['summary']['controlled_only_count']}` |
        | blocked_count | `{matrix['summary']['blocked_count']}` |
        | false_guard_count | `{matrix['summary']['false_guard_count']}` |
        | production_token_measurement_allowed | `false` |
        | measured_production_tokens | `false` |
        | production_admission_gate | `false` |
        | accepted | `false` |
        | integrated | `false` |
        | production_ready | `false` |
        """
    )


def main() -> int:
    matrix = build_matrix()
    OUT_JSON.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_OUT_JSON.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(matrix), encoding="utf-8")
    KDS_OUT_MD.write_text(render_markdown(matrix), encoding="utf-8")
    OUT_LOOP.write_text(render_loop_round(matrix), encoding="utf-8")
    KDS_OUT_LOOP.write_text(render_loop_round(matrix), encoding="utf-8")
    print(
        "headroom_lcx_objective_coverage_matrix=written "
        f"project_count={matrix['project_count']} "
        f"proven_count={matrix['summary']['proven_count']} "
        f"controlled_only_count={matrix['summary']['controlled_only_count']} "
        f"blocked_count={matrix['summary']['blocked_count']} "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
