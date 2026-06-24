#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement runner contract evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-001.md"

FIELD_MAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
TRANSITION_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
GAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"


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


def build_contract() -> dict[str, Any]:
    field_map = load_json(FIELD_MAP_JSON)
    transition = load_json(TRANSITION_JSON)
    gap = load_json(GAP_JSON)
    precheck = load_json(PRECHECK_JSON)
    rollback_text = read(ROLLBACK_MD)

    allowed_inputs = [
        "authorized_window_id",
        "authorized_by",
        "authorized_at",
        "sanitized_production_token_ledger",
        "rollback_plan_id",
        "waes_harness_admission_decision",
    ]

    forbidden_inputs = [
        "raw_prompt",
        "raw_completion",
        "customer_contract",
        "pod",
        "financial_voucher",
        "secret",
        "production_credential",
        "production_proxy",
        "production_sdk",
        "real_kds_write",
        "external_api_write",
    ]

    return {
        "contract_id": "HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623",
        "status": "runner_contract_defined_precheck_only",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": transition["scope"]["project_ids"],
        },
        "current_state": {
            "real_measurement_gap_present": gap["gates"]["real_measurement_gap_present"],
            "production_branch_blocked": transition["current_state"]["production_branch_blocked"],
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "runner_contract": {
            "allowed_inputs": allowed_inputs,
            "forbidden_inputs": forbidden_inputs,
            "execution_mode": "precheck_only",
            "execution_allowed_now": False,
            "allowed_actions": [
                "read_sanitized_ledger_metadata",
                "calculate_token_saving_estimate",
                "write_harness_evidence",
            ],
            "forbidden_actions": [
                "production_proxy_start",
                "production_sdk_enable",
                "real_kds_api_write",
                "external_api_write",
                "database_migration",
                "permission_change",
                "headroom_learn_apply",
                "memory_as_kds_fact_source",
            ],
            "required_preconditions": [
                "real_measurement_authorization_window",
                "waes_harness_admission_decision",
                "sanitized_token_ledger_metadata_only",
                "rollback_plan_id",
                "no_production_proxy",
                "no_real_kds_write",
                "no_external_api_write",
                "no_sensitive_material",
            ],
        },
        "field_binding": [
            {
                "field": row["field"],
                "bound_from": row["source_evidence"],
                "runner_input": row["future_runner_input"],
                "binding_state": "precheck_only",
            }
            for row in field_map["field_map"]
        ],
        "transition_anchor": {
            "transition_graph_id": transition["transition_graph_id"],
            "transition_graph_status": transition["status"],
            "production_branch_blocked": True,
        },
        "rollback_anchor": {
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_runbook_written": "Headroom LCX Rollback Plan 20260622-001" in rollback_text,
        },
        "precheck_anchor": {
            "waes_harness_admission_decision": precheck["waes_harness_admission_decision"],
            "authorization_complete": precheck["precheck"]["authorization_complete"],
            "missing_required_field_count_zero": precheck["precheck"]["missing_required_field_count"] == 0,
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
            "This contract only defines the precheck-only runner boundary.",
            "It does not authorize execution, production measurement, or real business equivalence measurement.",
            "It can be wired to a runner only after a future WAES/Harness decision opens a real measurement window.",
        ],
    }


def write_outputs(contract: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_JSON.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    OUTPUT_MD.write_text(
        "\n".join(
            [
                "---",
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623",
                "title: Headroom LCX Real Measurement Runner Contract Evidence",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md",
                "source_path: docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Headroom LCX Real Measurement Runner Contract Evidence",
                "",
                "## Evidence ID",
                "",
                "`HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623`",
                "",
                "## 结论",
                "",
                "当前 runner contract 只定义未来真实测量执行的 precheck-only 边界，不打开 production branch。",
                "status: runner_contract_defined_precheck_only",
                "",
                "## 允许输入",
                "",
                "`authorized_window_id`, `authorized_by`, `authorized_at`, `sanitized_production_token_ledger`, `rollback_plan_id`, `waes_harness_admission_decision`",
                "",
                "## 禁止输入",
                "",
                "`raw_prompt`, `raw_completion`, `customer_contract`, `pod`, `financial_voucher`, `secret`, `production_credential`, `production_proxy`, `production_sdk`, `real_kds_write`, `external_api_write`",
                "",
                "## 允许动作",
                "",
                "- `read_sanitized_ledger_metadata`",
                "- `calculate_token_saving_estimate`",
                "- `write_harness_evidence`",
                "",
                "## 禁止动作",
                "",
                "- `production_proxy_start`",
                "- `production_sdk_enable`",
                "- `real_kds_api_write`",
                "- `external_api_write`",
                "- `database_migration`",
                "- `permission_change`",
                "- `headroom_learn_apply`",
                "- `memory_as_kds_fact_source`",
                "",
                "## 当前状态",
                "",
                "- execution_allowed_now: `false`",
                "- real_measurement_gap_present: `true`",
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
                "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-LOOP-001",
                "title: Loop Round GPCF Headroom LCX Real Measurement Runner Contract 001",
                "project: GPCF",
                "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
                "domain: docs",
                "status: controlled",
                "version: v1.0",
                "owner: GPCF",
                "kds_space: 开发",
                "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-001.md",
                "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-001.md",
                "sync_direction: bidirectional",
                "last_reviewed: 2026-06-23",
                "supersedes: []",
                "superseded_by: []",
                "---",
                "",
                "# Loop Round GPCF Headroom LCX Real Measurement Runner Contract 001",
                "",
                "## 输入",
                "",
                "- 当前已有 field map、transition graph、gap matrix 和 rollback plan。",
                "- 需要将 precheck-only 字段收敛成受控 runner contract。",
                "",
                "## 动作",
                "",
                "1. 汇总字段映射、转移图、缺口矩阵、审批预检与回滚锚点。",
                "2. 生成 runner contract evidence。",
                "3. 生成 validator，确认 contract 仍然 precheck-only。",
                "",
                "## 输出",
                "",
                "- `tools/kds-sync/build_headroom_lcx_real_measurement_runner_contract.py`",
                "- `tools/kds-sync/validate_headroom_lcx_real_measurement_runner_contract.py`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json`",
                "- `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md`",
                "",
                "## 检查",
                "",
                "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_runner_contract.py`",
                "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_runner_contract.py`",
                "- `python3 tools/kds-sync/check_document_pollution.py`",
                "- `python3 tools/kds-sync/validate_kds_token.py`",
                "- `python3 tools/kds-sync/loop_document_gate.py --check-only`",
                "",
                "## 反馈",
                "",
                "runner contract 已将未来执行边界和禁止项收敛清楚，但仍不是生产执行授权。",
                "",
                "## 下一轮",
                "",
                "若未来授权窗口出现，可把 contract 直接对接真实测量 runner。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    contract = build_contract()
    write_outputs(contract)
    print(
        "headroom_lcx_real_measurement_runner_contract=generated "
        "project_count=15 execution_allowed_now=false "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
