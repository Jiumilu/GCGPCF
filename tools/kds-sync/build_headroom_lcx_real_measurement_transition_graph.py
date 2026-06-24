#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement transition graph evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependency
    raise SystemExit(f"PyYAML is required: {exc}") from exc


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-001.md"

GRAPH_JSON = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
GAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-request-20260623.json"
WINDOW_REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
WINDOW_GRANT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
P5_JSON = EVIDENCE_DIR / "headroom-lcx-p5-production-admission-package-20260621.json"


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


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a YAML object")
    return data


def build_graph() -> dict[str, Any]:
    graph = load_json(GRAPH_JSON)
    gap = load_json(GAP_JSON)
    request = load_json(REQUEST_JSON)
    window_request = load_json(WINDOW_REQUEST_JSON)
    window_grant = load_json(WINDOW_GRANT_JSON)
    precheck = load_json(PRECHECK_JSON)
    p5 = load_json(P5_JSON)
    rollback_text = read(ROLLBACK_MD)
    policy = load_yaml(ROOT / "loop/context/headroom/policy.yaml")
    request_field_values = {
        binding["field"]: binding["current_value"]
        for binding in request.get("field_bindings", [])
        if isinstance(binding, dict) and "field" in binding and "current_value" in binding
    }

    nodes = [
        {
            "node_id": "current_controlled_graph",
            "status": "controlled",
            "evidence": "HEADROOM-LCX-GRAPH-MANIFEST-20260623",
        },
        {
            "node_id": "real_measurement_gap_matrix",
            "status": "blocked",
            "evidence": "HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623",
        },
        {
            "node_id": "real_measurement_authorization_request_package",
            "status": "precheck_only",
            "evidence": request["evidence_id"],
        },
        {
            "node_id": "real_measurement_authorization_window_request_package",
            "status": "requested_not_granted",
            "evidence": window_request["evidence_id"],
        },
        {
            "node_id": "rollback_runbook",
            "status": "controlled_no_production",
            "evidence": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
        },
        {
            "node_id": "sanitized_precheck",
            "status": "admitted_for_sanitized_measurement_precheck",
            "evidence": precheck["evidence_id"],
        },
        {
            "node_id": "real_measurement_authorization_window",
            "status": "granted_precheck_only",
            "evidence": window_grant["evidence_id"],
        },
        {
            "node_id": "waes_harness_decision",
            "status": "precheck_only",
            "evidence": precheck["waes_harness_admission_decision"],
        },
        {
            "node_id": "sanitized_token_ledger",
            "status": "present",
            "evidence": request_field_values["sanitized_production_token_ledger"],
        },
        {
            "node_id": "production_proxy_enablement",
            "status": "blocked",
            "evidence": "production_proxy_and_sdk_flags_remain_false",
        },
        {
            "node_id": "real_business_equivalence_measurement",
            "status": "synthetic_only",
            "evidence": "HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622",
        },
        {
            "node_id": "production_branch",
            "status": "blocked",
            "evidence": p5["evidence_id"],
        },
    ]

    edges = [
        {
            "from": "current_controlled_graph",
            "to": "real_measurement_gap_matrix",
            "relation": "current_graph_exposes_real_measurement_gaps",
            "allowed": True,
        },
        {
            "from": "real_measurement_gap_matrix",
            "to": "real_measurement_authorization_request_package",
            "relation": "gap_matrix_creates_precheck_only_request_package",
            "allowed": True,
        },
        {
            "from": "real_measurement_authorization_request_package",
            "to": "real_measurement_authorization_window_request_package",
            "relation": "request_package_records_window_request_only",
            "allowed": True,
        },
        {
            "from": "real_measurement_authorization_window_request_package",
            "to": "sanitized_precheck",
            "relation": "window_request_remains_sanitized_only",
            "allowed": True,
        },
        {
            "from": "sanitized_precheck",
            "to": "real_measurement_authorization_window",
            "relation": "requires_authorized_window",
            "allowed": True,
        },
        {
            "from": "real_measurement_authorization_window",
            "to": "waes_harness_decision",
            "relation": "requires_waes_harness_admission",
            "allowed": False,
        },
        {
            "from": "waes_harness_decision",
            "to": "sanitized_token_ledger",
            "relation": "may_reference_sanitized_ledger_only",
            "allowed": True,
        },
        {
            "from": "sanitized_token_ledger",
            "to": "production_proxy_enablement",
            "relation": "production_proxy_remains_blocked_until_future_authorization",
            "allowed": False,
        },
        {
            "from": "production_proxy_enablement",
            "to": "real_business_equivalence_measurement",
            "relation": "real_measurement_requires_non_synthetic_equivalence",
            "allowed": False,
        },
        {
            "from": "real_business_equivalence_measurement",
            "to": "production_branch",
            "relation": "production_branch_requires_real_business_equivalence_and_authorized_measurement",
            "allowed": False,
        },
        {
            "from": "rollback_runbook",
            "to": "production_branch",
            "relation": "rollback_runbook_guards_not_opens_production",
            "allowed": False,
        },
    ]

    transition_requirements = [
        {
            "requirement_id": "requested_window_id",
            "current_value": window_request["requested_window_id"],
            "future_value": "requested_only_not_granted",
            "maps_to": "real_measurement_authorization_window_request_package",
        },
        {
            "requirement_id": "requested_by",
            "current_value": window_request["requested_by"],
            "future_value": "requested_only_not_granted",
            "maps_to": "real_measurement_authorization_window_request_package",
        },
        {
            "requirement_id": "requested_at",
            "current_value": window_request["requested_at"],
            "future_value": "requested_only_not_granted",
            "maps_to": "real_measurement_authorization_window_request_package",
        },
        {
            "requirement_id": "authorized_window_id",
            "current_value": window_grant["authorized_window_id"],
            "future_value": "granted_precheck_only",
            "maps_to": "real_measurement_authorization_window",
        },
        {
            "requirement_id": "authorized_by",
            "current_value": window_grant["authorized_by"],
            "future_value": "granted_precheck_only",
            "maps_to": "real_measurement_authorization_window",
        },
        {
            "requirement_id": "authorized_at",
            "current_value": window_grant["authorized_at"],
            "future_value": "granted_precheck_only",
            "maps_to": "real_measurement_authorization_window",
        },
        {
            "requirement_id": "sanitized_production_token_ledger",
            "current_value": "present_sanitized_only",
            "future_value": "authorized_for_read_only_measurement_metadata",
            "maps_to": "sanitized_token_ledger",
        },
        {
            "requirement_id": "rollback_plan_id",
            "current_value": "present",
            "future_value": "required",
            "maps_to": "rollback_runbook",
        },
        {
            "requirement_id": "waes_harness_admission_decision",
            "current_value": precheck["waes_harness_admission_decision"],
            "future_value": "future_admitted_for_real_measurement_only_if_authorized",
            "maps_to": "waes_harness_decision",
        },
        {
            "requirement_id": "real_business_equivalence_measurement",
            "current_value": "synthetic_only",
            "future_value": "real_business_equivalence_proven",
            "maps_to": "real_business_equivalence_measurement",
        },
    ]

    return {
        "transition_graph_id": "HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623",
        "status": "transition_graph_defined_blocked_real_measurement",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": graph["scope"]["project_ids"],
        },
        "current_state": {
            "graph_status": graph["status"],
            "gap_status": gap["status"],
            "production_branch_blocked": True,
            "real_measurement_window_granted": True,
            "real_measurement_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "nodes": nodes,
        "edges": edges,
        "transition_requirements": transition_requirements,
        "blocking_summary": {
            "real_measurement_gap_present": True,
            "production_branch_blocked": True,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "real_business_equivalence_measurement_allowed": False,
        },
        "rollback_anchor": {
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_runbook_written": "Headroom LCX Rollback Plan 20260622-001" in rollback_text,
        },
        "policy_false_gates": {
            "production_admission_gate": policy.get("production_admission_gate", False),
            "measured_production_tokens": policy.get("measured_production_tokens", False),
            "accepted": policy.get("accepted", False),
            "integrated": policy.get("integrated", False),
            "production_ready": policy.get("production_ready", False),
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "real_business_equivalence_proven": False,
            "production_ready": False,
            "accepted": False,
            "integrated": False,
        },
        "source_refs": {
            "graph_manifest": "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
            "gap_matrix": "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
            "rollback_plan": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            "measurement_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json",
            "window_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
            "window_grant": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json",
            "precheck": "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
        },
    }


def write_outputs(graph: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_JSON.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    OUTPUT_MD.write_text(
        "\n".join(
            [
                "---",
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623",
                "title: Headroom LCX Real Measurement Transition Graph Evidence",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md",
                "source_path: docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Headroom LCX Real Measurement Transition Graph Evidence",
                "",
                "## Evidence ID",
                "",
                "`HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623`",
                "",
                "## 结论",
                "",
                "当前图谱已经稳定地停留在受控态，真实测量转移图已明确所有需要跨越的条件，但 production branch 仍然 blocked。",
                "status: transition_graph_defined_blocked_real_measurement",
                "",
                "## 授权窗口",
                "",
                f"- real_measurement_authorization_window_status: `granted_precheck_only`",
                "- real_measurement_authorization_window_granted_precheck_only: `true`",
                f"- real_measurement_window_granted: `{str(graph['current_state']['real_measurement_window_granted']).lower()}`",
                f"- real_measurement_window_grant_evidence: `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623`",
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
                "## 转移要求",
                "",
                "| requirement_id | current_value | future_value | maps_to |",
                "|---|---|---|---|",
                *[f"| {req['requirement_id']} | {req['current_value']} | {req['future_value']} | {req['maps_to']} |" for req in graph["transition_requirements"]],
                "",
                "## 当前状态",
                "",
                "- real_measurement_gap_present: `true`",
                "- production_branch_blocked: `true`",
                "- production_branch_open: `false`",
                "- real_business_equivalence_measurement_allowed: `false`",
                "- production_token_measurement_allowed: `false`",
                "- measured_production_tokens: `false`",
                "- production_admission_gate: `false`",
                "- accepted: `false`",
                "- integrated: `false`",
                "- production_ready: `false`",
                "",
                "## 非声明",
                "",
                "- 本证据不表示真实测量已执行。",
                "- 本证据不表示真实业务等价性已证明。",
                "- 本证据不表示生产分支已打开。",
                "- 本证据不表示 accepted、integrated 或 production_ready。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    OUTPUT_LOOP.write_text(
        "\n".join(
            [
                "---",
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-LOOP-001",
                "title: Loop Round GPCF Headroom LCX Real Measurement Transition Graph 001",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-001.md",
                "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-001.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Loop Round GPCF Headroom LCX Real Measurement Transition Graph 001",
                "",
                "## 输入",
                "",
                "- 当前已有 graph manifest、rollback plan、real measurement gap matrix 和 authorization request package。",
                "- 需要把当前态到未来真实测量态的转移条件明确成状态图，并显式包含授权请求包。",
                "",
                "## 动作",
                "",
                "1. 汇总 graph manifest、gap matrix、rollback plan、measurement precheck 与 authorization request package。",
                "2. 生成 real measurement transition graph evidence，包含 authorization request package 节点。",
                "3. 生成 validator，确认转移边仍 blocked 且 production branch 未开启。",
                "",
                "## 输出",
                "",
                "- `tools/kds-sync/build_headroom_lcx_real_measurement_transition_graph.py`",
                "- `tools/kds-sync/validate_headroom_lcx_real_measurement_transition_graph.py`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md`",
                "- real_measurement_authorization_window_granted_precheck_only",
                "",
                "## 检查",
                "",
                "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_transition_graph.py`",
                "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_transition_graph.py`",
                "- `python3 tools/kds-sync/check_document_pollution.py`",
                "- `python3 tools/kds-sync/validate_kds_token.py`",
                "- `python3 tools/kds-sync/loop_document_gate.py --check-only`",
                "",
                "## 反馈",
                "",
                "转移图明确了 current_controlled_graph 到 production_branch 之间所有仍 blocked 的边和未来要求。",
                "",
                "## 下一轮",
                "",
                "若未来授权窗口出现，可直接把 transition_requirements 映射成执行 runner 输入字段。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    graph = build_graph()
    write_outputs(graph)
    print(
        "headroom_lcx_real_measurement_transition_graph=generated "
        "project_count=15 "
        "real_measurement_gap_present=true "
        "production_branch_blocked=true "
        "real_business_equivalence_measurement_allowed=false "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
