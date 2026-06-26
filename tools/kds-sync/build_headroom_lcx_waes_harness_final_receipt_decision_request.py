#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision request for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"

INTAKE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-intake-20260623.json"
PRECHECK = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-precheck-20260623.json"
COMPLETED_RECEIPT = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-request-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-request-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001.md"

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


def build_request() -> dict[str, Any]:
    intake = load_json(INTAKE)
    precheck = load_json(PRECHECK)
    receipt = load_json(COMPLETED_RECEIPT)
    require(intake.get("status") == "receipt_intake_valid_precheck_only", "intake must be valid precheck-only")
    require(precheck.get("status") == "receipt_instance_valid_precheck_only", "precheck must be valid precheck-only")
    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001",
        "date": "2026-06-23",
        "status": "waes_harness_final_receipt_decision_requested_pending",
        "scope": "decision_request_only_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "source_intake": INTAKE.relative_to(ROOT).as_posix(),
        "source_precheck": PRECHECK.relative_to(ROOT).as_posix(),
        "source_completed_receipt": COMPLETED_RECEIPT.relative_to(ROOT).as_posix(),
        "receipt_id": receipt.get("receipt_id"),
        "receipt_valid_precheck_only": True,
        "requested_decision": "waes_harness_final_receipt_decision",
        "allowed_decision_values": [
            "admitted_for_next_precheck_only",
            "rejected_requires_rework",
            "deferred_pending_additional_evidence",
        ],
        "decision_pending": True,
        "required_waes_harness_checks": [
            "receipt_fields_match_completion_template",
            "negative_fixtures_rejected_count_11_accepted_count_0",
            "telemetry_off",
            "no_unsanitized_sensitive_material",
            "no_production_proxy_or_sdk",
            "no_real_kds_or_external_api_write",
            "no_database_migration_or_permission_change",
            "accepted_integrated_production_ready_false",
            "measurement_window_not_opened",
        ],
        "pre_execution_decision": {
            "waes_harness_final_decision_recorded": False,
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

    check_rows = [f"| `{item}` |" for item in request["required_waes_harness_checks"]]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in request["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Request",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-request-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-request-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Request",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-20260623`",
            "",
            "## 当前结论",
            "",
            "`waes_harness_final_receipt_decision_requested_pending`",
            "",
            "本文只请求 WAES/Harness 对 Headroom LCX completed receipt 作最终 receipt decision。本文不代表裁决已经完成，也不打开真实测量窗口。",
            "",
            "## 裁决请求",
            "",
            "| item | value |",
            "|---|---|",
            f"| receipt_id | `{request['receipt_id']}` |",
            f"| receipt_valid_precheck_only | `{str(request['receipt_valid_precheck_only']).lower()}` |",
            f"| requested_decision | `{request['requested_decision']}` |",
            f"| decision_pending | `{str(request['decision_pending']).lower()}` |",
            "",
            "## WAES/Harness 必查项",
            "",
            "| check |",
            "|---|",
            *check_rows,
            "",
            "## 执行前判定",
            "",
            "| item | value |",
            "|---|---|",
            *decision_rows,
            "",
            "## 非声明",
            "",
            "- 不声明 WAES/Harness final decision 已完成。",
            "- 不声明真实测量窗口已经打开。",
            "- 不声明生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。",
            "- 不声明 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Request 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-REQUEST-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Request 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- completed receipt",
            "- external receipt intake evidence",
            "- external receipt precheck evidence",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_request.py`",
            "- 生成 WAES/Harness final receipt decision request。",
            "- 不生成 final decision，不打开真实测量窗口。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-request-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-request-20260623.md`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 等待 WAES/Harness 独立裁决。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_request.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 decision request evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- Receipt 已 valid precheck-only，但 final decision 仍 pending。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立给出 final receipt decision。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    request = build_request()
    write_outputs(request)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_request=generated "
        "status=waes_harness_final_receipt_decision_requested_pending "
        "decision_pending=true real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
