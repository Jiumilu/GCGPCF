#!/usr/bin/env python3
"""Build Headroom LCX external receipt precheck evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

TEMPLATE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.json"
EXPECTED_RECEIPT = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-precheck-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-precheck-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md"

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


def receipt_status(template: dict[str, Any]) -> dict[str, Any]:
    expected_ref = EXPECTED_RECEIPT.relative_to(ROOT).as_posix()
    required_fields = template.get("required_receipt_fields", [])
    if not EXPECTED_RECEIPT.exists():
        return {
            "expected_receipt_path": expected_ref,
            "external_receipt_recorded": False,
            "receipt_instance_valid": False,
            "missing_required_fields": required_fields,
            "invalid_false_fields": [],
            "status": "blocked_missing_external_receipt_instance",
        }

    receipt = load_json(EXPECTED_RECEIPT)
    missing = [field for field in required_fields if field not in receipt]
    false_fields = [
        "production_proxy_started",
        "production_sdk_enabled",
        "real_kds_write",
        "external_api_write",
        "database_migration",
        "permission_change",
        "accepted",
        "integrated",
        "production_ready",
    ]
    invalid_false = [field for field in false_fields if receipt.get(field) is not False]
    return {
        "expected_receipt_path": expected_ref,
        "external_receipt_recorded": True,
        "receipt_instance_valid": not missing and not invalid_false,
        "missing_required_fields": missing,
        "invalid_false_fields": invalid_false,
        "status": "receipt_instance_valid_precheck_only" if not missing and not invalid_false else "blocked_invalid_external_receipt_instance",
    }


def build_precheck() -> dict[str, Any]:
    template = load_json(TEMPLATE)
    status = receipt_status(template)
    blocked = status["status"] != "receipt_instance_valid_precheck_only"

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001",
        "date": "2026-06-23",
        "status": status["status"],
        "scope": "external_receipt_instance_precheck_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "template_evidence_id": template.get("evidence_id"),
        "template_status": template.get("status"),
        "receipt_check": status,
        "pre_execution_decision": {
            "can_open_real_measurement": False,
            "blocked": blocked,
            "blocker": status["status"] if blocked else "waes_harness_final_receipt_decision_required",
            "real_measurement_open": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "real_kds_write": False,
            "external_api_write": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_external_receipt_recorded": not status["external_receipt_recorded"],
            "not_real_measurement_execution": True,
            "not_production_proxy_start": True,
            "not_production_sdk_enablement": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
    }


def write_outputs(precheck: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(precheck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    decision_rows = [
        f"| {key} | `{str(value).lower() if isinstance(value, bool) else value}` |"
        for key, value in precheck["pre_execution_decision"].items()
    ]
    receipt = precheck["receipt_check"]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-20260623",
            "title: Headroom LCX Real Measurement External Receipt Precheck Evidence",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Receipt Precheck Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-20260623`",
            "",
            "## 当前结论",
            "",
            f"`{precheck['status']}`",
            "",
            "本轮只检查正式外部回执实例是否存在且字段完整。当前不会打开真实测量窗口，不会启动生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。",
            "",
            "## 回执实例检查",
            "",
            "| item | value |",
            "|---|---|",
            f"| expected_receipt_path | `{receipt['expected_receipt_path']}` |",
            f"| external_receipt_recorded | `{str(receipt['external_receipt_recorded']).lower()}` |",
            f"| receipt_instance_valid | `{str(receipt['receipt_instance_valid']).lower()}` |",
            f"| missing_required_field_count | `{len(receipt['missing_required_fields'])}` |",
            f"| invalid_false_field_count | `{len(receipt['invalid_false_fields'])}` |",
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Precheck 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Receipt Precheck 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- 外部授权回执模板 evidence",
            "- 预期正式外部回执路径",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_precheck.py`",
            "- 检查正式外部回执实例是否存在且满足模板字段。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.md`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 正式外部回执实例未回填，真实测量继续阻断。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_precheck.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 precheck evidence 和 validator 即可回退，不影响模板和授权链。",
            "- 禁止恢复为生产执行状态。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 本轮确认缺正式外部 receipt，保持 blocked_missing_external_receipt_instance。",
            "",
            "### 下一轮",
            "",
            "- 需要用户提供正式外部回执实例，或继续生成 receipt completed 填写包。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    precheck = build_precheck()
    write_outputs(precheck)
    print(
        "headroom_lcx_real_measurement_external_receipt_precheck=generated "
        f"status={precheck['status']} project_count=15 external_receipt_recorded="
        f"{str(precheck['receipt_check']['external_receipt_recorded']).lower()} "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
