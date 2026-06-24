#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement authorization field map evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-001.md"

GRAPH_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
GAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-measurement-admission-request-20260622.json"
PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
APPROVAL_JSON = EVIDENCE_DIR / "headroom-lcx-approval-instance-precheck-20260622.json"
AUTH_TEMPLATE_MD = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-authorization-template-20260621.md"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"


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


def build_map() -> dict[str, Any]:
    graph = load_json(GRAPH_JSON)
    gap = load_json(GAP_JSON)
    request = load_json(REQUEST_JSON)
    precheck = load_json(PRECHECK_JSON)
    approval = load_json(APPROVAL_JSON)
    auth_template = read(AUTH_TEMPLATE_MD)
    rollback_text = read(ROLLBACK_MD)

    field_map = [
        {
            "field": "authorized_window_id",
            "current_value": approval["authorized_window_id"],
            "source_evidence": approval["evidence_id"],
            "future_runner_input": "authorized_window_id",
            "future_action": "bind a real measurement window before any execution",
        },
        {
            "field": "authorized_by",
            "current_value": approval["authorized_by"],
            "source_evidence": approval["evidence_id"],
            "future_runner_input": "authorized_by",
            "future_action": "bind approving owner before any execution",
        },
        {
            "field": "authorized_at",
            "current_value": approval["authorized_at"],
            "source_evidence": approval["evidence_id"],
            "future_runner_input": "authorized_at",
            "future_action": "bind approval timestamp before any execution",
        },
        {
            "field": "sanitized_production_token_ledger",
            "current_value": approval["sanitized_production_token_ledger"],
            "source_evidence": request["evidence_id"],
            "future_runner_input": "sanitized_production_token_ledger",
            "future_action": "allow metadata-only ledger reads for cost replay",
        },
        {
            "field": "rollback_plan_id",
            "current_value": approval["rollback_plan_id"],
            "source_evidence": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "future_runner_input": "rollback_plan_id",
            "future_action": "attach rollback runbook identifier before any measurement execution",
        },
        {
            "field": "waes_harness_admission_decision",
            "current_value": approval["waes_harness_admission_decision"],
            "source_evidence": precheck["evidence_id"],
            "future_runner_input": "waes_harness_admission_decision",
            "future_action": "keep precheck-only until a new WAES/Harness decision is issued",
        },
    ]

    future_inputs = [item["future_runner_input"] for item in field_map]

    return {
        "field_map_id": "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623",
        "status": "authorization_field_map_defined_precheck_only",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": graph["scope"]["project_ids"],
        },
        "current_state": {
            "real_measurement_gap_present": gap["gates"]["real_measurement_gap_present"],
            "production_branch_blocked": graph["current_state"]["production_branch_blocked"],
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "field_map": field_map,
        "future_runner_inputs": future_inputs,
        "execution_guard": {
            "executable_now": False,
            "requires_real_measurement_authorization_window": True,
            "requires_waes_harness_decision": True,
            "requires_sanitized_token_ledger_metadata_only": True,
            "requires_rollback_plan_id": True,
            "requires_no_production_proxy": True,
            "requires_no_real_kds_write": True,
            "requires_no_external_api_write": True,
        },
        "rollback_anchor": {
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_runbook_written": "Headroom LCX Rollback Plan 20260622-001" in rollback_text,
        },
        "source_refs": {
            "graph_transition": "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
            "gap_matrix": "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
            "approval_instance": "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json",
            "authorization_template": "docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md",
            "rollback_plan": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "business_answer_equivalence_proven": False,
        },
        "notes": [
            "This field map only aligns current precheck artifacts to future runner inputs.",
            "It does not authorize production measurement or real business equivalence measurement.",
            "It remains precheck-only until WAES/Harness issues a new decision.",
            "All production gates remain false.",
        ],
    }


def write_outputs(field_map: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_JSON.write_text(json.dumps(field_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    OUTPUT_MD.write_text(
        "\n".join(
            [
                "---",
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623",
                "title: Headroom LCX Real Measurement Authorization Field Map Evidence",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md",
                "source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Headroom LCX Real Measurement Authorization Field Map Evidence",
                "",
                "## Evidence ID",
                "",
                "`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623`",
                "",
                "## 结论",
                "",
                "当前已经存在的预检/审批实例字段，可以直接映射到未来真实测量 runner 输入，但现在仍然只是 precheck-only。",
                "status: authorization_field_map_defined_precheck_only",
                "",
                "## 字段映射",
                "",
                "| field | current_value | source_evidence | future_runner_input | future_action |",
                "|---|---|---|---|---|",
                *[f"| {row['field']} | {row['current_value']} | `{row['source_evidence']}` | `{row['future_runner_input']}` | {row['future_action']} |" for row in field_map["field_map"]],
                "",
                "## 未来 runner 输入",
                "",
                "`authorized_window_id`, `authorized_by`, `authorized_at`, `sanitized_production_token_ledger`, `rollback_plan_id`, `waes_harness_admission_decision`",
                "",
                "## 执行门禁",
                "",
                "- executable_now: `false`",
                "- requires_real_measurement_authorization_window: `true`",
                "- requires_waes_harness_decision: `true`",
                "- requires_sanitized_token_ledger_metadata_only: `true`",
                "- requires_rollback_plan_id: `true`",
                "- requires_no_production_proxy: `true`",
                "- requires_no_real_kds_write: `true`",
                "- requires_no_external_api_write: `true`",
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
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-LOOP-001",
                "title: Loop Round GPCF Headroom LCX Real Measurement Authorization Field Map 001",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-001.md",
                "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-001.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Loop Round GPCF Headroom LCX Real Measurement Authorization Field Map 001",
                "",
                "## 输入",
                "",
                "- 当前已有 transition graph、gap matrix 和 rollback plan。",
                "- 需要把六个授权字段对齐到未来 runner 输入。",
                "",
                "## 动作",
                "",
                "1. 汇总 approval instance、precheck、authorization template 与 rollback plan。",
                "2. 生成 authorization field map evidence。",
                "3. 生成 validator，确认仍只是 precheck-only。",
                "",
                "## 输出",
                "",
                "- `tools/kds-sync/build_headroom_lcx_real_measurement_authorization_field_map.py`",
                "- `tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_field_map.py`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md`",
                "",
                "## 检查",
                "",
                "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_authorization_field_map.py`",
                "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_field_map.py`",
                "- `python3 tools/kds-sync/check_document_pollution.py`",
                "- `python3 tools/kds-sync/validate_kds_token.py`",
                "- `python3 tools/kds-sync/loop_document_gate.py --check-only`",
                "",
                "## 反馈",
                "",
                "授权字段已映射到未来 runner 输入，但当前仍然只适用于 sanitized precheck。",
                "",
                "## 下一轮",
                "",
                "若未来授权窗口出现，可把未来 runner 输入直接绑定到真实测量执行逻辑。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    field_map = build_map()
    write_outputs(field_map)
    print(
        "headroom_lcx_real_measurement_authorization_field_map=generated "
        "project_count=15 executable_now=false "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
