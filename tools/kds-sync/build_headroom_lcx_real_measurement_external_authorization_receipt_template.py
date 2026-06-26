#!/usr/bin/env python3
"""Build Headroom LCX external authorization receipt template evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001.md"
OUT_FIXTURE = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt-template.json"

CHAIN_REPLAY = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-chain-replay-20260623.json"
WINDOW_GRANT = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
LEDGER = EVIDENCE_DIR / "headroom-lcx-sanitized-production-usage-ledger-20260623.json"

PROJECTS = [
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


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_receipt_template() -> dict[str, Any]:
    chain = load_json(CHAIN_REPLAY)
    grant = load_json(WINDOW_GRANT)
    ledger = load_json(LEDGER)
    ledger_ref = LEDGER.relative_to(ROOT).as_posix()

    require(chain.get("ledger_reference") == ledger_ref, "chain replay ledger mismatch")
    require(grant.get("sanitized_production_token_ledger") == ledger_ref, "window grant ledger mismatch")
    require(ledger.get("telemetry") == "off", "ledger telemetry must remain off")

    fields = {
        "receipt_id": "HEADROOM-LCX-EXT-AUTH-RECEIPT-YYYYMMDD-NNN",
        "authorized_window_id": grant.get("authorized_window_id"),
        "authorized_by": grant.get("authorized_by"),
        "authorized_at": grant.get("authorized_at"),
        "sanitized_production_usage_ledger": ledger_ref,
        "rollback_plan_id": grant.get("rollback_plan_id"),
        "waes_harness_admission_decision": grant.get("waes_harness_admission_decision"),
        "execution_operator": "REQUIRED_EXTERNAL_OPERATOR",
        "execution_started_at": "REQUIRED_EXTERNAL_TIMESTAMP_WITH_TIMEZONE",
        "execution_finished_at": "REQUIRED_EXTERNAL_TIMESTAMP_WITH_TIMEZONE",
        "telemetry": "off",
        "sensitive_material_attestation": "REQUIRED_NO_UNSANITIZED_SENSITIVE_MATERIAL",
        "production_proxy_started": False,
        "production_sdk_enabled": False,
        "real_kds_write": False,
        "external_api_write": False,
        "database_migration": False,
        "permission_change": False,
        "real_measurement_open": False,
        "production_token_measurement_allowed": False,
        "measured_production_tokens": False,
        "answer_equivalence": "REQUIRED_EXTERNAL_WAES_HARNESS_DECISION",
        "waes_harness_receipt_decision": "REQUIRED_EXTERNAL_RECEIPT_DECISION",
        "rollback_exercised": "REQUIRED_EXTERNAL_BOOLEAN",
        "evidence_refs": [
            "docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.json",
            "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json",
            ledger_ref,
        ],
        "accepted": False,
        "integrated": False,
        "production_ready": False,
    }

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001",
        "date": "2026-06-23",
        "status": "external_authorization_receipt_template_ready_no_execution",
        "scope": "external_receipt_template_only_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "receipt_status": "template_only_pending_external_receipt",
        "source_chain_replay": chain.get("evidence_id"),
        "source_window_grant": grant.get("evidence_id"),
        "sanitized_production_usage_ledger": ledger_ref,
        "required_receipt_fields": list(fields.keys()),
        "receipt_template": fields,
        "pre_execution_gates": {
            "chain_replay_exists": True,
            "authorization_window_granted": grant.get("real_measurement_window_granted") is True,
            "external_receipt_recorded": False,
            "real_measurement_open": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "real_kds_write": False,
            "external_api_write": False,
            "database_migration": False,
            "permission_change": False,
            "measured_production_tokens": False,
            "production_token_measurement_allowed": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "template_is_not_receipt": True,
            "receipt_is_not_execution": True,
            "not_real_measurement_execution": True,
            "not_production_proxy_start": True,
            "not_production_sdk_enablement": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_database_migration": True,
            "not_permission_change": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
    }


def write_outputs(template: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_FIXTURE.write_text(json.dumps(template["receipt_template"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    field_rows = [
        f"| `{field}` | `{json.dumps(value, ensure_ascii=False)}` |"
        for field, value in template["receipt_template"].items()
    ]
    gate_rows = [
        f"| {field} | `{str(value).lower()}` |"
        for field, value in template["pre_execution_gates"].items()
    ]

    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-20260623",
            "title: Headroom LCX Real Measurement External Authorization Receipt Template",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Authorization Receipt Template",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-20260623`",
            "",
            "## 当前结论",
            "",
            "`external_authorization_receipt_template_ready_no_execution`",
            "",
            "本文只建立 Headroom LCX 真实测量执行前的外部授权回执模板。它不代表外部回执已经记录，不代表真实测量已经执行，不打开生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。",
            "",
            "## 覆盖范围",
            "",
            "| item | value |",
            "|---|---|",
            f"| project_count | `{template['project_count']}` |",
            f"| projects | `{', '.join(template['projects'])}` |",
            f"| receipt_status | `{template['receipt_status']}` |",
            f"| sanitized_production_usage_ledger | `{template['sanitized_production_usage_ledger']}` |",
            "",
            "## 外部回执模板字段",
            "",
            "| field | template_value |",
            "|---|---|",
            *field_rows,
            "",
            "## 执行前门禁",
            "",
            "| gate | value |",
            "|---|---|",
            *gate_rows,
            "",
            "## 非声明",
            "",
            "- 模板不等于正式外部回执。",
            "- 正式外部回执不等于真实测量自动执行。",
            "- 不声明生产代理或生产 SDK 已启动。",
            "- 不声明真实 KDS 写入、外部 API 写入、数据库迁移或权限变更。",
            "- 不声明 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Authorization Receipt Template 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Authorization Receipt Template 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- Headroom LCX 授权链回放 evidence",
            "- Headroom LCX 授权窗口 grant",
            "- Headroom LCX 脱敏 usage ledger",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_authorization_receipt_template.py`",
            "- 生成真实测量执行前的外部授权回执模板。",
            "- 固定模板不等于回执、回执不等于执行、执行不等于 accepted/integrated/production_ready 的声明边界。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.md`",
            "- `fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt-template.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 外部真实回执尚未回填，真实测量窗口仍未打开。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_authorization_receipt_template.py`",
            "",
            "## recover",
            "",
            "- 回退方式：删除本轮模板 evidence、fixture 和 validator，不影响既有授权链回放。",
            "- 禁止恢复为生产执行状态。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 本轮只形成外部授权回执模板，不登记正式回执，不执行真实测量。",
            "",
            "### 下一轮",
            "",
            "- 若继续推进，只能基于外部回填的正式 receipt 做 precheck；否则保持 blocked / partial_controlled_not_production_ready。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    template = build_receipt_template()
    write_outputs(template)
    print(
        "headroom_lcx_real_measurement_external_authorization_receipt_template=generated "
        "project_count=15 receipt_status=template_only_pending_external_receipt "
        "real_measurement_open=false measured_production_tokens=false accepted=false "
        "integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
