#!/usr/bin/env python3
"""Build Headroom LCX external receipt intake evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

COMPLETION_PACKAGE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json"
NEGATIVE_FIXTURES = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.json"
COMPLETED_RECEIPT = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-intake-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-intake-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001.md"

FALSE_FIELDS = [
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def validate_receipt(receipt: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    required_fields = list(template.keys())
    missing_fields = [field for field in required_fields if field not in receipt]
    invalid_false_fields = [field for field in FALSE_FIELDS if receipt.get(field) is not False]
    invalid_fields: list[str] = []
    if receipt.get("telemetry") != "off":
        invalid_fields.append("telemetry")
    if receipt.get("sensitive_material_attestation") != "no_unsanitized_customer_contract_pod_financial_secret_or_production_credential_processed":
        invalid_fields.append("sensitive_material_attestation")
    if "REQUIRED" in str(receipt.get("execution_operator", "")):
        invalid_fields.append("execution_operator")
    if "REQUIRED" in str(receipt.get("waes_harness_receipt_decision", "")):
        invalid_fields.append("waes_harness_receipt_decision")
    valid = not missing_fields and not invalid_false_fields and not invalid_fields
    return {
        "receipt_instance_valid": valid,
        "missing_fields": missing_fields,
        "invalid_false_fields": invalid_false_fields,
        "invalid_fields": invalid_fields,
    }


def build_intake() -> dict[str, Any]:
    completion = load_json(COMPLETION_PACKAGE)
    negative = load_json(NEGATIVE_FIXTURES)
    template = completion.get("completed_template", {})
    require(isinstance(template, dict), "completion package template must be an object")

    if COMPLETED_RECEIPT.exists():
        receipt = load_json(COMPLETED_RECEIPT)
        receipt_check = validate_receipt(receipt, template)
        status = "receipt_intake_valid_precheck_only" if receipt_check["receipt_instance_valid"] else "blocked_invalid_completed_receipt"
        recorded = True
    else:
        receipt_check = {
            "receipt_instance_valid": False,
            "missing_fields": list(template.keys()),
            "invalid_false_fields": [],
            "invalid_fields": ["completed_receipt_file_missing"],
        }
        status = "intake_validator_ready_missing_completed_receipt"
        recorded = False

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001",
        "date": "2026-06-23",
        "status": status,
        "scope": "formal_receipt_intake_validator_no_measurement",
        "project_count": 15,
        "source_completion_package": COMPLETION_PACKAGE.relative_to(ROOT).as_posix(),
        "source_negative_fixtures": NEGATIVE_FIXTURES.relative_to(ROOT).as_posix(),
        "expected_completed_receipt_path": COMPLETED_RECEIPT.relative_to(ROOT).as_posix(),
        "negative_fixture_count": negative.get("fixture_count"),
        "negative_fixture_expected_accepted_count": negative.get("expected_accepted_count"),
        "completed_receipt_recorded": recorded,
        "receipt_check": receipt_check,
        "intake_rules": {
            "required_fields_match_completion_template": True,
            "negative_fixtures_must_reject_all": negative.get("expected_accepted_count") == 0,
            "telemetry_must_remain_off": True,
            "no_unsanitized_sensitive_material": True,
            "production_and_write_flags_must_remain_false": True,
            "accepted_integrated_production_ready_must_remain_false": True,
            "intake_does_not_open_measurement": True,
        },
        "pre_execution_decision": {
            "completed_receipt_recorded": recorded,
            "receipt_instance_valid": receipt_check["receipt_instance_valid"],
            "can_open_real_measurement": False,
            "real_measurement_open": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(intake: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(intake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rule_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in intake["intake_rules"].items()
    ]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in intake["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-20260623",
            "title: Headroom LCX Real Measurement External Receipt Intake Evidence",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Receipt Intake Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-20260623`",
            "",
            "## 当前结论",
            "",
            f"`{intake['status']}`",
            "",
            "本轮只建立正式 completed receipt 的 intake validator。当前不创建正式回执，不打开真实测量窗口。",
            "",
            "## Intake 规则",
            "",
            "| rule | value |",
            "|---|---|",
            *rule_rows,
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Intake 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Receipt Intake 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- completed receipt 填写包",
            "- completed receipt 负向 fixtures",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_intake.py`",
            "- 建立正式 completed receipt intake validator。",
            "- 不生成正式 completed receipt 实例。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.md`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 正式 completed receipt 尚未由人工回填。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_intake.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 intake evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- Intake validator ready，但 formal receipt 仍 missing。",
            "",
            "### 下一轮",
            "",
            "- 等待人工填写正式 completed receipt，或生成最终人工回填请求。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    intake = build_intake()
    write_outputs(intake)
    print(
        "headroom_lcx_real_measurement_external_receipt_intake=generated "
        f"status={intake['status']} completed_receipt_recorded={str(intake['completed_receipt_recorded']).lower()} "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
