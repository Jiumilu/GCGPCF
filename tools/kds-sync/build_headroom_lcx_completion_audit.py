#!/usr/bin/env python3
"""Build a completion audit for the Headroom LCX project-group graph."""

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

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md"
KDS_OUTPUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.json"
KDS_OUTPUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.md"
KDS_OUTPUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md"

GRAPH_MANIFEST = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
GAP_MATRIX = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
TRANSITION_GRAPH = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
AUTH_FIELD_MAP = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
WINDOW_REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
NEXT_STAGE_PACKAGE = EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json"
AUTHORIZATION_CHAIN_REPLAY = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-chain-replay-20260623.json"
RUNNER_CONTRACT = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json"
RUNTIME_GRAPH = EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.json"
ROUTER = EVIDENCE_DIR / "headroom-project-group-application-router-20260621.md"
COST_MODEL = EVIDENCE_DIR / "headroom-cost-sensitivity-model-20260621.json"
ROLLBACK = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
BLOCKER_INVENTORY = EVIDENCE_DIR / "headroom-lcx-remaining-blocker-inventory-20260623.json"

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


def md_table(rows: list[tuple[str, str, str]]) -> str:
    lines = ["| requirement_id | state | evidence |", "|---|---|---|"]
    for requirement_id, state, evidence in rows:
        lines.append(f"| {requirement_id} | {state} | {evidence} |")
    return "\n".join(lines)


def build_completion_audit() -> dict[str, Any]:
    graph = load_json(GRAPH_MANIFEST)
    gap = load_json(GAP_MATRIX)
    transition = load_json(TRANSITION_GRAPH)
    field_map = load_json(AUTH_FIELD_MAP)
    window_request = load_json(WINDOW_REQUEST)
    next_stage_package = load_json(NEXT_STAGE_PACKAGE)
    authorization_chain_replay = load_json(AUTHORIZATION_CHAIN_REPLAY)
    runner = load_json(RUNNER_CONTRACT)
    runtime_graph = load_json(RUNTIME_GRAPH)
    cost_model = load_json(COST_MODEL)
    cost_bridge = load_json(EVIDENCE_DIR / "headroom-lcx-cost-bridge-20260623.json")
    blocker_inventory = load_json(BLOCKER_INVENTORY)

    project_count = graph.get("scope", {}).get("project_count")
    project_ids = graph.get("scope", {}).get("project_ids", [])
    route_count = len(graph.get("project_routes", []))
    gap_items = gap.get("missing_requirements", [])
    blocked_count = sum(1 for item in gap_items if item.get("current_status") in {"blocked", "missing", "not_proven", "granted_precheck_only"})

    requirements = [
        {
            "requirement_id": "route_graph_coverage",
            "state": "proven",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-project-group-application-router-20260621.md",
                "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md",
            ],
        },
        {
            "requirement_id": "cost_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
                "docs/harness/evidence/headroom-loop-cost-observation-20260621.json",
                "docs/harness/evidence/headroom-lcx-cost-bridge-20260623.json",
            ],
        },
        {
            "requirement_id": "rollback_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            ],
        },
        {
            "requirement_id": "authorization_measurement",
            "state": "precheck_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json",
                "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
                "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.json",
                "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json",
            ],
        },
        {
            "requirement_id": "real_business_equivalence_measurement",
            "state": "blocked",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
                "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json",
                "docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.json",
            ],
        },
        {
            "requirement_id": "production_runtime_graph",
            "state": "proven_controlled_only",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json",
                "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json",
            ],
        },
        {
            "requirement_id": "accepted_integrated_production_ready",
            "state": "false",
            "evidence": [
                "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
                "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
                "docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.md",
            ],
        },
    ]

    audit = {
        "evidence_id": "HEADROOM-LCX-COMPLETION-AUDIT-20260623",
        "status": "controlled_partial_completion_audit",
        "date": "2026-06-23",
        "objective": "完成完整真实功能图谱：真实业务等价授权测量，以及生产级运行/成本/回滚图谱。",
        "project_group_scope": PROJECT_IDS,
        "project_count": project_count,
        "route_count": route_count,
        "requirements": requirements,
        "supporting_evidence": {
            "graph_manifest": graph.get("graph_id"),
            "gap_matrix": gap.get("gap_id"),
            "transition_graph": transition.get("transition_graph_id"),
            "authorization_field_map": field_map.get("field_map_id"),
            "authorization_window_request": window_request.get("evidence_id"),
            "next_stage_authorization_package": next_stage_package.get("evidence_id"),
            "approval_signed_bundle": "HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623",
            "authorization_chain_replay": authorization_chain_replay.get("evidence_id"),
            "authorization_boundary_review": "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623",
            "remaining_blocker_inventory": blocker_inventory.get("evidence_id"),
            "runner_contract": runner.get("contract_id"),
            "runtime_graph": runtime_graph.get("runtime_graph_id"),
            "cost_model": cost_model.get("evidence_id"),
            "cost_bridge": cost_bridge.get("evidence_id"),
        },
        "current_state": {
            "graph_status": graph.get("status"),
            "real_measurement_gap_present": gap.get("blocking_state", {}).get("production_token_measurement_allowed") is False,
            "production_branch_blocked": gap.get("blocking_state", {}).get("production_branch_open") is False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "waes_harness_admission_decision": graph.get("authorization", {}).get("waes_harness_admission_decision"),
            "authorization_window_id": graph.get("authorization", {}).get("authorized_window_id"),
            "authorization_window_request_status": graph.get("authorization", {}).get("authorization_window_request_status"),
            "next_stage_authorization_package_status": next_stage_package.get("status"),
            "rollback_plan_id": graph.get("authorization", {}).get("rollback_plan_id"),
        },
        "summary": {
            "proven_count": 1,
            "controlled_only_count": 3,
            "partial_count": 1,
            "blocked_count": blocked_count,
            "false_guard_count": 1,
            "project_count": project_count,
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
    return audit


def render_markdown(audit: dict[str, Any]) -> str:
    requirements = audit["requirements"]
    rows = [
        (item["requirement_id"], item["state"], " ; ".join(item["evidence"]))
        for item in requirements
    ]
    evidence_lines = "\n".join(
        f"- `{key}`: `{value}`" for key, value in audit["supporting_evidence"].items()
    )
    current_state_lines = "\n".join(
        f"| {key} | `{str(value).lower() if isinstance(value, bool) else value}` |"
        for key, value in audit["current_state"].items()
    )
    non_claim_lines = "\n".join(
        f"- `{key}`: `{str(value).lower()}`" for key, value in audit["non_claims"].items()
    )
    parts = [
        "---",
        "doc_id: GPCF-DOC-HEADROOM-LCX-COMPLETION-AUDIT-20260623",
        "title: Headroom LCX Completion Audit Evidence",
        "project: GPCF",
        "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-completion-audit-20260623.md",
        "source_path: docs/harness/evidence/headroom-lcx-completion-audit-20260623.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Headroom LCX Completion Audit Evidence",
        "",
        "## Evidence ID",
        "",
        "`HEADROOM-LCX-COMPLETION-AUDIT-20260623`",
        "",
        "## 结论",
        "",
        "Headroom 的项目群图谱已完成受控化收口，但当前仍处于 `controlled_partial_completion_audit`。",
        "15 域路由、成本图、回滚图和生产 runtime graph 已成型；真实业务等价授权测量、生产分支开放和真实生产 token 测量仍未打开。",
        "",
        "## 审计项",
        "",
        md_table(rows),
        "",
        "## 支撑证据",
        "",
        evidence_lines,
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
        "只有在 WAES/Harness 另行裁决并补齐真实测量授权后，才可以把 completion audit 从 partial 推进到真实测量执行。",
    ]
    return "\n".join(parts) + "\n"


def render_loop_round(audit: dict[str, Any]) -> str:
    return dedent(
        f"""\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-COMPLETION-AUDIT-001
        title: "Loop Round: GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # Loop Round: GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json`
        - `docs/harness/evidence/headroom-project-group-application-router-20260621.md`

        ## 动作

        - 将当前 Headroom 图谱收束为 completion audit，区分已证明的图谱层和仍被门禁阻断的层。
        - 固化 15 域覆盖、成本图、回滚图、授权预检和真实业务等价测量缺口。
        - 保持 `accepted=false`、`integrated=false`、`production_ready=false`。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-completion-audit-20260623.json`
        - `docs/harness/evidence/headroom-lcx-completion-audit-20260623.md`
        - `tools/kds-sync/build_headroom_lcx_completion_audit.py`
        - `tools/kds-sync/validate_headroom_lcx_completion_audit.py`

        ## 检查

        ```bash
        python3 tools/kds-sync/validate_headroom_lcx_completion_audit.py
        ```

        ## 反馈

        Headroom 图谱已完成受控收口，但 completion audit 仍然显示真实业务等价授权测量未打开、生产分支仍被阻断、生产 token 仍未测量。

        ## 下一轮

        等待 WAES/Harness 对真实测量授权窗口和 admission decision 做出新的裁决。

        ## 审计快照

        | 项 | 当前值 |
        |---|---|
        | project_count | `{audit["project_count"]}` |
        | route_count | `{audit["route_count"]}` |
        | blocked_count | `{audit["summary"]["blocked_count"]}` |
        | production_token_measurement_allowed | `false` |
        | measured_production_tokens | `false` |
        | production_admission_gate | `false` |
        | accepted | `false` |
        | integrated | `false` |
        | production_ready | `false` |
        """
    ).strip() + "\n"


def main() -> int:
    audit = build_completion_audit()
    OUTPUT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_OUTPUT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(audit), encoding="utf-8")
    KDS_OUTPUT_MD.write_text(render_markdown(audit), encoding="utf-8")
    OUTPUT_LOOP.write_text(render_loop_round(audit), encoding="utf-8")
    KDS_OUTPUT_LOOP.write_text(render_loop_round(audit), encoding="utf-8")
    print(
        "headroom_lcx_completion_audit=written "
        f"project_count={audit['project_count']} "
        f"route_count={audit['route_count']} "
        f"blocked_count={audit['summary']['blocked_count']} "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
