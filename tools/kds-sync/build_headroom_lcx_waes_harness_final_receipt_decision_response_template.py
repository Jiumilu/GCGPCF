#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision response template for Headroom LCX."""

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
FORBIDDEN_RESPONSE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001.md"

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


def build_template() -> dict[str, Any]:
    request = load_json(REQUEST)
    require(
        request.get("status") == "waes_harness_final_receipt_decision_requested_pending",
        "request must remain pending",
    )
    template = {
        "decision_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-20260623-001",
        "request_evidence_id": request.get("evidence_id"),
        "receipt_id": request.get("receipt_id"),
        "decision_maker": "REQUIRED_WAES_OR_HARNESS_DECISION_MAKER",
        "decision_role": "REQUIRED_WAES_OR_HARNESS_ROLE",
        "decided_at": "REQUIRED_DECISION_TIMESTAMP_WITH_TIMEZONE",
        "decision_value": "REQUIRED_ONE_OF_admitted_for_next_precheck_only_or_rejected_requires_rework_or_deferred_pending_additional_evidence",
        "decision_reason": "REQUIRED_DECISION_REASON_NO_SENSITIVE_RAW_TEXT",
        "linked_evidence_refs": [
            "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-request-20260623.json",
            "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.json",
            "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.json",
        ],
        "can_open_real_measurement": False,
        "real_measurement_open": False,
        "measured_production_tokens": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
    }
    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001",
        "date": "2026-06-23",
        "status": "final_receipt_decision_response_template_ready_pending_response",
        "scope": "decision_response_template_only_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "source_request": REQUEST.relative_to(ROOT).as_posix(),
        "response_template_path": RESPONSE_TEMPLATE.relative_to(ROOT).as_posix(),
        "target_response_path": FORBIDDEN_RESPONSE.relative_to(ROOT).as_posix(),
        "response_template": template,
        "allowed_decision_values": [
            "admitted_for_next_precheck_only",
            "rejected_requires_rework",
            "deferred_pending_additional_evidence",
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


def write_outputs(evidence: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RESPONSE_TEMPLATE.write_text(json.dumps(evidence["response_template"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in evidence["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Response Template",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Response Template",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-20260623`",
            "",
            "## 当前结论",
            "",
            "`final_receipt_decision_response_template_ready_pending_response`",
            "",
            "本文只建立 WAES/Harness final receipt decision 的响应模板。它不代表 WAES/Harness 已完成裁决，也不打开真实测量窗口。",
            "",
            "## 路径",
            "",
            "| item | path |",
            "|---|---|",
            f"| response_template_path | `{evidence['response_template_path']}` |",
            f"| target_response_path | `{evidence['target_response_path']}` |",
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Response Template 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-TEMPLATE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Response Template 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- WAES/Harness final receipt decision request",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_response_template.py`",
            "- 生成 WAES/Harness final receipt decision 响应模板。",
            "- 不生成正式 response，不打开真实测量窗口。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-template-20260623.md`",
            "- `fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.template.json`",
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
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_response_template.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 response template evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- request 和 response template 都已就位，final decision 仍 pending。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立回填 final decision response。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_template()
    write_outputs(evidence)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_response_template=generated "
        "status=final_receipt_decision_response_template_ready_pending_response "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
