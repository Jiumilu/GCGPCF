#!/usr/bin/env python3
"""Build Headroom LCX external receipt human fill request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

INTAKE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-intake-20260623.json"
COMPLETED_TEMPLATE = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.template.json"
TARGET_COMPLETED_RECEIPT = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001.md"

MUST_REMAIN_FALSE = [
    "production_proxy_started",
    "production_sdk_enabled",
    "real_kds_write",
    "external_api_write",
    "database_migration",
    "permission_change",
    "real_measurement_open",
    "production_token_measurement_allowed",
    "measured_production_tokens",
    "accepted",
    "integrated",
    "production_ready",
]

MUST_REPLACE_REQUIRED = [
    "execution_operator",
    "execution_started_at",
    "execution_finished_at",
    "answer_equivalence",
    "waes_harness_receipt_decision",
    "rollback_exercised",
    "operator_note",
]

VERIFY_COMMANDS = [
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_intake.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_completion_package.py",
    "python3 tools/kds-sync/validate_headroom_lcx_completion_audit.py",
    "python3 tools/kds-sync/validate_headroom_lcx_objective_coverage_matrix.py",
    "python3 tools/kds-sync/check_document_pollution.py",
    "python3 tools/kds-sync/validate_kds_token.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_request() -> dict[str, Any]:
    intake = load_json(INTAKE)
    template = load_json(COMPLETED_TEMPLATE)
    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001",
        "date": "2026-06-23",
        "status": "human_fill_request_ready_no_completed_receipt_recorded",
        "scope": "human_fill_request_only_no_measurement",
        "project_count": 15,
        "source_intake": INTAKE.relative_to(ROOT).as_posix(),
        "completed_template_path": COMPLETED_TEMPLATE.relative_to(ROOT).as_posix(),
        "target_completed_receipt_path": TARGET_COMPLETED_RECEIPT.relative_to(ROOT).as_posix(),
        "current_intake_status": intake.get("status"),
        "required_fields": list(template.keys()),
        "must_replace_required_placeholders": MUST_REPLACE_REQUIRED,
        "must_remain_false": MUST_REMAIN_FALSE,
        "must_remain_values": {
            "telemetry": "off",
            "sensitive_material_attestation": "no_unsanitized_customer_contract_pod_financial_secret_or_production_credential_processed",
        },
        "forbidden_values": {
            field: True for field in MUST_REMAIN_FALSE
        },
        "verification_commands_after_fill": VERIFY_COMMANDS,
        "pre_execution_decision": {
            "completed_receipt_recorded": False,
            "receipt_instance_valid": False,
            "can_open_real_measurement": False,
            "real_measurement_open": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(request: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    command_rows = [f"| `{command}` |" for command in request["verification_commands_after_fill"]]
    false_rows = [f"| `{field}` | `false` |" for field in request["must_remain_false"]]
    replace_rows = [f"| `{field}` |" for field in request["must_replace_required_placeholders"]]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in request["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-20260623",
            "title: Headroom LCX Real Measurement External Receipt Human Fill Request",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Receipt Human Fill Request",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-20260623`",
            "",
            "## 当前结论",
            "",
            "`human_fill_request_ready_no_completed_receipt_recorded`",
            "",
            "本文是正式 completed receipt 的人工回填请求包。它不创建正式回执，不打开真实测量窗口。",
            "",
            "## 回填路径",
            "",
            "| item | path |",
            "|---|---|",
            f"| completed_template_path | `{request['completed_template_path']}` |",
            f"| target_completed_receipt_path | `{request['target_completed_receipt_path']}` |",
            "",
            "## 必须替换占位字段",
            "",
            "| field |",
            "|---|",
            *replace_rows,
            "",
            "## 必须保持 false 的字段",
            "",
            "| field | required_value |",
            "|---|---|",
            *false_rows,
            "",
            "## 回填后验证命令",
            "",
            "| command |",
            "|---|",
            *command_rows,
            "",
            "## 执行前判定",
            "",
            "| item | value |",
            "|---|---|",
            *decision_rows,
            "",
            "## 非声明",
            "",
            "- 不声明正式外部回执已经记录。",
            "- 不声明真实测量已经执行。",
            "- 不声明生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。",
            "- 不声明 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Human Fill Request 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Receipt Human Fill Request 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- completed receipt intake evidence",
            "- completed receipt template",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_human_fill_request.py`",
            "- 生成正式 receipt 人工回填请求包。",
            "- 不生成正式 completed receipt 实例。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.md`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 等待人工按请求包回填正式 completed receipt。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_human_fill_request.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 human fill request evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 已给出正式 receipt 回填字段、禁止值和验证命令。",
            "",
            "### 下一轮",
            "",
            "- 等待人工回填 completed receipt；回填后先跑 intake validator，不自动打开真实测量。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    request = build_request()
    write_outputs(request)
    print(
        "headroom_lcx_real_measurement_external_receipt_human_fill_request=generated "
        "status=human_fill_request_ready_no_completed_receipt_recorded "
        "completed_receipt_recorded=false real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
