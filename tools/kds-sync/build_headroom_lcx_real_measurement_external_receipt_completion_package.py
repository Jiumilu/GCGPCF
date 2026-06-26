#!/usr/bin/env python3
"""Build Headroom LCX external receipt completion package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

RECEIPT_TEMPLATE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.json"
PRECHECK = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-precheck-20260623.json"
COMPLETED_TEMPLATE = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.template.json"
FORBIDDEN_COMPLETED_RECEIPT = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md"

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


def build_completed_template(receipt_template: dict[str, Any]) -> dict[str, Any]:
    base = dict(receipt_template["receipt_template"])
    base.update(
        {
            "receipt_id": "HEADROOM-LCX-EXT-AUTH-RECEIPT-20260623-001",
            "execution_operator": "REQUIRED_HUMAN_OPERATOR_NAME",
            "execution_started_at": "REQUIRED_EXTERNAL_START_TIMESTAMP_WITH_TIMEZONE",
            "execution_finished_at": "REQUIRED_EXTERNAL_FINISH_TIMESTAMP_WITH_TIMEZONE",
            "sensitive_material_attestation": "no_unsanitized_customer_contract_pod_financial_secret_or_production_credential_processed",
            "answer_equivalence": "REQUIRED_WAES_HARNESS_EQUIVALENCE_DECISION",
            "waes_harness_receipt_decision": "REQUIRED_WAES_HARNESS_RECEIPT_DECISION",
            "rollback_exercised": "REQUIRED_BOOLEAN_WITH_EVIDENCE_IF_TRUE",
            "operator_note": "REQUIRED_EXTERNAL_OPERATOR_NOTE_NO_SENSITIVE_RAW_TEXT",
        }
    )
    return base


def build_package() -> dict[str, Any]:
    receipt_template = load_json(RECEIPT_TEMPLATE)
    precheck = load_json(PRECHECK)
    completed_template = build_completed_template(receipt_template)

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001",
        "date": "2026-06-23",
        "status": "completion_package_ready_no_completed_receipt_recorded",
        "scope": "completion_template_only_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "source_template": RECEIPT_TEMPLATE.relative_to(ROOT).as_posix(),
        "source_precheck": PRECHECK.relative_to(ROOT).as_posix(),
        "completed_template_path": COMPLETED_TEMPLATE.relative_to(ROOT).as_posix(),
        "forbidden_completed_receipt_path_until_human_fill": FORBIDDEN_COMPLETED_RECEIPT.relative_to(ROOT).as_posix(),
        "current_precheck_status": precheck.get("status"),
        "completed_template": completed_template,
        "negative_validation_rules": {
            "must_not_create_completed_receipt_automatically": True,
            "telemetry_must_remain_off": True,
            "no_unsanitized_sensitive_material": True,
            "production_proxy_started_must_be_false": True,
            "production_sdk_enabled_must_be_false": True,
            "real_kds_write_must_be_false": True,
            "external_api_write_must_be_false": True,
            "database_migration_must_be_false": True,
            "permission_change_must_be_false": True,
            "accepted_must_be_false": True,
            "integrated_must_be_false": True,
            "production_ready_must_be_false": True,
        },
        "pre_execution_decision": {
            "external_receipt_recorded": False,
            "completed_receipt_instance_created": False,
            "can_open_real_measurement": False,
            "real_measurement_open": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(package: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    COMPLETED_TEMPLATE.write_text(json.dumps(package["completed_template"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rule_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in package["negative_validation_rules"].items()
    ]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in package["pre_execution_decision"].items()
    ]

    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-20260623",
            "title: Headroom LCX Real Measurement External Receipt Completion Package",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Receipt Completion Package",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-20260623`",
            "",
            "## 当前结论",
            "",
            "`completion_package_ready_no_completed_receipt_recorded`",
            "",
            "本轮只生成正式外部回执 completed 填写包，不生成正式 completed receipt 实例，不打开真实测量窗口。",
            "",
            "## 输出路径",
            "",
            "| item | path |",
            "|---|---|",
            f"| completed_template_path | `{package['completed_template_path']}` |",
            f"| forbidden_completed_receipt_path_until_human_fill | `{package['forbidden_completed_receipt_path_until_human_fill']}` |",
            "",
            "## 负向校验规则",
            "",
            "| rule | required |",
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
            "- 不声明生产代理或生产 SDK 已启动。",
            "- 不声明真实 KDS 写入或外部 API 写入。",
            "- 不声明 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Completion Package 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Receipt Completion Package 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- 外部授权回执模板",
            "- 外部回执实例预检 evidence",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_completion_package.py`",
            "- 生成 completed receipt 填写模板和负向校验规则。",
            "- 不生成正式 completed receipt 实例。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md`",
            "- `fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.template.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 需要人工按模板填写正式 completed receipt，当前不得自动生成。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_completion_package.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 completion package 和 template 即可回退。",
            "- 禁止恢复为生产执行状态。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 本轮只产生填写包，正式 receipt 仍未记录。",
            "",
            "### 下一轮",
            "",
            "- 等待人工提供 completed receipt，或继续生成 completed receipt 负向 fixtures。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    package = build_package()
    write_outputs(package)
    print(
        "headroom_lcx_real_measurement_external_receipt_completion_package=generated "
        "status=completion_package_ready_no_completed_receipt_recorded project_count=15 "
        "completed_receipt_instance_created=false real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
