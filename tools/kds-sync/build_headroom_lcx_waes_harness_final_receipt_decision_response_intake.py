#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision response intake for Headroom LCX."""

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

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001.md"

FALSE_FIELDS = [
    "can_open_real_measurement",
    "real_measurement_open",
    "measured_production_tokens",
    "accepted",
    "integrated",
    "production_ready",
]

ALLOWED_DECISIONS = {
    "admitted_for_next_precheck_only",
    "rejected_requires_rework",
    "deferred_pending_additional_evidence",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def validate_response(response: dict[str, Any], template: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in template.keys() if field not in response]
    invalid_false = [field for field in FALSE_FIELDS if response.get(field) is not False]
    invalid_fields: list[str] = []
    if response.get("request_evidence_id") != request.get("evidence_id"):
        invalid_fields.append("request_evidence_id")
    if response.get("receipt_id") != request.get("receipt_id"):
        invalid_fields.append("receipt_id")
    if response.get("decision_value") not in ALLOWED_DECISIONS:
        invalid_fields.append("decision_value")
    for field in ["decision_maker", "decision_role", "decided_at", "decision_reason"]:
        if "REQUIRED" in str(response.get(field, "")) or not str(response.get(field, "")).strip():
            invalid_fields.append(field)
    return {
        "response_instance_valid": not missing and not invalid_false and not invalid_fields,
        "missing_fields": missing,
        "invalid_false_fields": invalid_false,
        "invalid_fields": invalid_fields,
    }


def build_intake() -> dict[str, Any]:
    request = load_json(REQUEST)
    template = load_json(RESPONSE_TEMPLATE)
    require(request.get("status") == "waes_harness_final_receipt_decision_requested_pending", "request must remain pending")

    if TARGET_RESPONSE.exists():
        response = load_json(TARGET_RESPONSE)
        check = validate_response(response, template, request)
        status = "final_response_intake_valid_pending_chain_replay" if check["response_instance_valid"] else "blocked_invalid_final_response"
        recorded = True
    else:
        check = {
            "response_instance_valid": False,
            "missing_fields": list(template.keys()),
            "invalid_false_fields": [],
            "invalid_fields": ["final_response_file_missing"],
        }
        status = "response_intake_ready_missing_final_response"
        recorded = False

    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001",
        "date": "2026-06-23",
        "status": status,
        "scope": "final_response_intake_only_no_measurement",
        "source_request": REQUEST.relative_to(ROOT).as_posix(),
        "response_template_path": RESPONSE_TEMPLATE.relative_to(ROOT).as_posix(),
        "target_response_path": TARGET_RESPONSE.relative_to(ROOT).as_posix(),
        "final_response_recorded": recorded,
        "response_check": check,
        "pre_execution_decision": {
            "waes_harness_final_decision_recorded": recorded and check["response_instance_valid"],
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

    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in evidence["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Response Intake",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Response Intake",
            "",
            "## 当前结论",
            "",
            f"`{evidence['status']}`",
            "",
            "本文只校验 WAES/Harness final response 是否存在且字段合法。当前不打开真实测量窗口。",
            "",
            "## 执行前判定",
            "",
            "| item | value |",
            "|---|---|",
            *decision_rows,
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Response Intake 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Response Intake 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- final decision request",
            "- final decision response template",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_response_intake.py`",
            "- 建立 final response intake validator。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 等待 WAES/Harness 独立回填正式 response.json。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_response_intake.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 intake evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- final response intake 已就位，但正式 response 仍未记录。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立回填正式 response.json。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_intake()
    write_outputs(evidence)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_response_intake=generated "
        f"status={evidence['status']} final_response_recorded={str(evidence['final_response_recorded']).lower()} "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
