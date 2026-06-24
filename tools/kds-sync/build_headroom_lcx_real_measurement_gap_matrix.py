#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement gap matrix evidence."""

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

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-001.md"

GRAPH_JSON = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
MEASUREMENT_REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-measurement-admission-request-20260622.json"
WINDOW_REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
WINDOW_GRANT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
P5_PACKAGE_JSON = EVIDENCE_DIR / "headroom-lcx-p5-production-admission-package-20260621.json"


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


def build_matrix() -> dict[str, Any]:
    graph = load_json(GRAPH_JSON)
    precheck = load_json(PRECHECK_JSON)
    request = load_json(MEASUREMENT_REQUEST_JSON)
    window_request = load_json(WINDOW_REQUEST_JSON)
    window_grant = load_json(WINDOW_GRANT_JSON)
    p5 = load_json(P5_PACKAGE_JSON)
    rollback_text = read(ROLLBACK_MD)
    policy = load_yaml(ROOT / "loop/context/headroom/policy.yaml")

    missing_requirements = [
        {
            "requirement_id": "real_measurement_authorization_window",
            "needed_for": "true_real_business_equivalence_measurement",
            "current_status": "granted_precheck_only",
            "blocking_evidence": "real_measurement_window_granted_but_open_remains_false",
        },
        {
            "requirement_id": "real_measurement_waes_harness_decision",
            "needed_for": "open_production_branch_for_measurement",
            "current_status": "blocked",
            "blocking_evidence": "waes_harness_admission_decision_is_precheck_only",
        },
        {
            "requirement_id": "real_measurement_token_ledger",
            "needed_for": "real_token_cost_and_saving_replay",
            "current_status": "missing",
            "blocking_evidence": "only_sanitized_precheck_ledger_exists",
        },
        {
            "requirement_id": "production_proxy_or_sdk_enablement",
            "needed_for": "actual_runtime_measurement_path",
            "current_status": "blocked",
            "blocking_evidence": "production_proxy_and_sdk_flags_remain_false",
        },
        {
            "requirement_id": "real_business_equivalence_measurement",
            "needed_for": "production_level_answer_equivalence_graph",
            "current_status": "not_proven",
            "blocking_evidence": "equivalence_layer_is_synthetic_only",
        },
    ]

    return {
        "gap_id": "HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623",
        "status": "real_measurement_gap_matrix_defined_no_measurement",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": graph["scope"]["project_ids"],
            "measurement_mode": "sanitized_metadata_only",
        },
        "current_graph_state": {
            "graph_id": graph["graph_id"],
            "graph_status": graph["status"],
            "production_branch": graph["layers"][-1]["status"],
            "real_business_equivalence_scope": graph["scope"]["real_business_equivalence_scope"],
        },
        "blocking_state": {
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "real_measurement_window_granted": True,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
        },
        "existing_supporting_evidence": {
            "precheck_evidence_id": precheck["evidence_id"],
            "request_evidence_id": request["evidence_id"],
            "window_request_evidence_id": window_request["evidence_id"],
            "window_grant_evidence_id": window_grant["evidence_id"],
            "p5_package_evidence_id": p5["evidence_id"],
            "rollback_plan_evidence_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
        },
        "missing_requirements": missing_requirements,
        "rollback_plan_integrity": {
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_runbook_written": "Headroom LCX Rollback Plan 20260622-001" in rollback_text,
        },
        "non_claims": {
            "real_business_equivalence_proven": False,
            "real_measurement_open": False,
            "production_branch_open": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "gates": {
            "gap_matrix_defined": True,
            "real_measurement_gap_present": True,
            "production_branch_blocked": True,
            "rollback_plan_present": True,
            "waes_precheck_only": precheck["waes_harness_admission_decision"] == "admitted_for_sanitized_measurement_precheck",
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
        },
        "source_refs": {
            "graph_manifest": "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
            "rollback_plan": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            "measurement_request": "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json",
            "window_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
            "window_grant": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json",
            "precheck": "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
        },
        "policy_false_gates": {
            "production_admission_gate": policy.get("production_admission_gate", False),
            "measured_production_tokens": policy.get("measured_production_tokens", False),
            "accepted": policy.get("accepted", False),
            "integrated": policy.get("integrated", False),
            "production_ready": policy.get("production_ready", False),
        },
    }


def write_outputs(matrix: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_JSON.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    OUTPUT_MD.write_text(
        "\n".join(
            [
                "---",
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623",
                "title: Headroom LCX Real Measurement Gap Matrix Evidence",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.md",
                "source_path: docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Headroom LCX Real Measurement Gap Matrix Evidence",
                "",
                "## Evidence ID",
                "",
                "`HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623`",
                "",
                "## 结论",
                "",
                "当前图谱已经具备受控路由、成本、回滚和 synthetic equivalence 层，但真实业务等价授权测量仍未打开。",
                "status: real_measurement_gap_matrix_defined_no_measurement",
                "",
                "## 缺口",
                "",
                "| requirement_id | needed_for | current_status | blocking_evidence |",
                "|---|---|---|---|",
                *[f"| {row['requirement_id']} | {row['needed_for']} | {row['current_status']} | {row['blocking_evidence']} |" for row in matrix["missing_requirements"]],
                "",
                "## 当前状态",
                "",
                f"- project_count: `{matrix['scope']['project_count']}`",
                "- production_branch_open: `false`",
                f"- production_branch: `{matrix['current_graph_state']['production_branch']}`",
                "- real_measurement_gap_present: `true`",
                f"- real_measurement_window_granted: `{str(matrix['blocking_state']['real_measurement_window_granted']).lower()}`",
                "- production_branch_blocked: `true`",
                "- production_token_measurement_allowed: `false`",
                "- measured_production_tokens: `false`",
                "- production_admission_gate: `false`",
                "- accepted: `false`",
                "- integrated: `false`",
                "- production_ready: `false`",
                "",
                "## 支撑证据",
                "",
                f"- `window_request`: `{matrix['source_refs']['window_request']}`",
                f"- `window_grant`: `{matrix['source_refs']['window_grant']}`",
                "- `window_grant_json`: `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json`",
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
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-LOOP-001",
                "title: Loop Round GPCF Headroom LCX Real Measurement Gap Matrix 001",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-001.md",
                "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-001.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Loop Round GPCF Headroom LCX Real Measurement Gap Matrix 001",
                "",
                "## 输入",
                "",
                "- 当前已有 Headroom LCX graph manifest。",
                "- 需要把真实测量仍缺的条件与边界写成审计式缺口矩阵。",
                "",
                "## 动作",
                "",
                "1. 从 graph manifest、measurement request、precheck、P5 package 与 rollback plan 汇总缺口。",
                "2. 生成 real measurement gap matrix evidence。",
                "3. 生成 validator，确认 production branch 仍 blocked。",
                "",
                "## 输出",
                "",
                "- `tools/kds-sync/build_headroom_lcx_real_measurement_gap_matrix.py`",
                "- `tools/kds-sync/validate_headroom_lcx_real_measurement_gap_matrix.py`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.md`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json`",
                "",
                "## 检查",
                "",
                "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_gap_matrix.py`",
                "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_gap_matrix.py`",
                "- `python3 tools/kds-sync/check_document_pollution.py`",
                "- `python3 tools/kds-sync/validate_kds_token.py`",
                "- `python3 tools/kds-sync/loop_document_gate.py --check-only`",
                "",
                "## 反馈",
                "",
                "本轮把真实测量仍缺的授权、ledger、决策与启用边界明确下来，同时保持 production branch blocked。",
                "",
                "## 下一轮",
                "",
                "如果未来收到真实测量授权，可把缺口矩阵的 requirement_id 映射到实际授权字段和执行 runner。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    matrix = build_matrix()
    write_outputs(matrix)
    print(
        "headroom_lcx_real_measurement_gap_matrix=generated "
        "project_count=15 "
        "real_measurement_gap_present=true "
        "production_branch_blocked=true "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
