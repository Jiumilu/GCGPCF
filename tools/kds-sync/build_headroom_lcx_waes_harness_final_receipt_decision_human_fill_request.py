#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision human fill request for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

REQUEST = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-request-20260623.json"
RESPONSE_TEMPLATE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.template.json"
TARGET_RESPONSE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001.md"

MUST_REPLACE_REQUIRED = [
    "decision_maker",
    "decision_role",
    "decided_at",
    "decision_value",
    "decision_reason",
]

MUST_REMAIN_FALSE = [
    "can_open_real_measurement",
    "real_measurement_open",
    "measured_production_tokens",
    "accepted",
    "integrated",
    "production_ready",
]

VERIFY_COMMANDS = [
    "python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_response_template.py",
    "python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_request.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_intake.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_precheck.py",
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
    request = load_json(REQUEST)
    response_template = load_json(RESPONSE_TEMPLATE)
    require(
        request.get("status") == "waes_harness_final_receipt_decision_requested_pending",
        "request must remain pending",
    )
    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001",
        "date": "2026-06-23",
        "status": "waes_harness_final_receipt_decision_human_fill_request_ready",
        "scope": "human_fill_request_only_no_decision_recorded",
        "project_count": 15,
        "source_request": REQUEST.relative_to(ROOT).as_posix(),
        "response_template_path": RESPONSE_TEMPLATE.relative_to(ROOT).as_posix(),
        "target_response_path": TARGET_RESPONSE.relative_to(ROOT).as_posix(),
        "required_fields": list(response_template.keys()),
        "must_replace_required_placeholders": MUST_REPLACE_REQUIRED,
        "allowed_decision_values": [
            "admitted_for_next_precheck_only",
            "rejected_requires_rework",
            "deferred_pending_additional_evidence",
        ],
        "must_remain_false": MUST_REMAIN_FALSE,
        "verification_commands_after_fill": VERIFY_COMMANDS,
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


def write_outputs(evidence: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    replace_rows = [f"| `{field}` |" for field in evidence["must_replace_required_placeholders"]]
    false_rows = [f"| `{field}` | `false` |" for field in evidence["must_remain_false"]]
    command_rows = [f"| `{command}` |" for command in evidence["verification_commands_after_fill"]]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in evidence["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Human Fill Request",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Human Fill Request",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-20260623`",
            "",
            "## 当前结论",
            "",
            "`waes_harness_final_receipt_decision_human_fill_request_ready`",
            "",
            "本文把 WAES/Harness final receipt decision 的人工回填要求单独收束成请求包。它不创建正式 decision response，也不打开真实测量窗口。",
            "",
            "## 必须替换的占位字段",
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Human Fill Request 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Human Fill Request 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- WAES/Harness final receipt decision request",
            "- WAES/Harness final receipt decision response template",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_human_fill_request.py`",
            "- 生成 WAES/Harness final decision 人工回填请求包。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.md`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 等待 WAES/Harness 独立回填 final decision response。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_human_fill_request.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 human fill request evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- response template 和 human fill request 均已就位，final decision 仍 pending。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立回填 final decision response。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_request()
    write_outputs(evidence)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_human_fill_request=generated "
        "status=waes_harness_final_receipt_decision_human_fill_request_ready "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
