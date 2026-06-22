#!/usr/bin/env python3
"""Build the Headroom LCX sanitized measurement admission request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APPROVAL_INSTANCE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json"
PRECHECK_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json"
LEDGER_JSON = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
ROLLBACK_PLAN_MD = ROOT / "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001.md"

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


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def main() -> int:
    approval = load_json(APPROVAL_INSTANCE_JSON)
    precheck = load_json(PRECHECK_JSON)
    ledger = load_json(LEDGER_JSON)
    require(ROLLBACK_PLAN_MD.exists(), "missing rollback plan")

    fields = approval.get("authorization_fields", {})
    precheck_gates = precheck.get("gates", {})
    current_decision = fields.get("waes_harness_admission_decision")
    waes_harness_admitted = current_decision == "admitted_for_sanitized_measurement_precheck"
    status = (
        "request_package_approved_for_sanitized_precheck_no_measurement"
        if waes_harness_admitted
        else "request_package_generated_admission_still_blocked"
    )
    request = {
        "evidence_id": "HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-20260622",
        "task_id": "GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001",
        "date": "2026-06-22",
        "status": status,
        "scope": "waes_harness_admission_request_only_no_measurement",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "requested_decision": "admitted_for_sanitized_measurement_precheck",
        "current_waes_harness_admission_decision": current_decision,
        "source_approval_instance": approval.get("instance_id"),
        "source_authorized_measurement_precheck": precheck.get("evidence_id"),
        "sanitized_production_token_ledger": fields.get("sanitized_production_token_ledger"),
        "rollback_plan_id": fields.get("rollback_plan_id"),
        "admission_preconditions": {
            "authorization_complete": precheck_gates.get("authorization_complete") is True,
            "missing_required_field_count_zero": precheck_gates.get("missing_required_field_count_zero") is True,
            "sanitized_ledger_exists": LEDGER_JSON.exists(),
            "sanitized_ledger_contains_no_raw_content": ledger.get("contains_raw_prompt") is False
            and ledger.get("contains_raw_completion") is False
            and ledger.get("contains_provider_secret") is False
            and ledger.get("contains_authorization_header") is False
            and ledger.get("contains_customer_contract_text") is False
            and ledger.get("sensitive_raw_text_stored") is False,
            "rollback_plan_exists": ROLLBACK_PLAN_MD.exists(),
            "telemetry_off_required": True,
            "waes_harness_decision_required": True,
            "human_approval_required": True,
        },
        "requested_measurement_boundary": {
            "allowed_content": "sanitized_token_ledger_metadata_only",
            "forbidden_content": [
                "raw_prompt",
                "raw_completion",
                "customer_contract",
                "pod",
                "financial_voucher",
                "secret",
                "production_credential",
            ],
            "allowed_actions_after_future_admission": [
                "read_sanitized_ledger_metadata",
                "calculate_token_saving_estimate",
                "write_harness_evidence",
            ],
            "forbidden_actions": [
                "production_proxy_start",
                "real_kds_api_write",
                "external_api_write",
                "database_migration",
                "permission_change",
                "headroom_learn_apply",
                "memory_as_kds_fact_source",
            ],
        },
        "gates": {
            "request_package_generated": True,
            "authorization_complete": precheck_gates.get("authorization_complete") is True,
            "waes_harness_admitted": waes_harness_admitted,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "next_required_decision": {
            "field": "waes_harness_admission_decision",
            "current_value": current_decision,
            "required_value_for_next_precheck": "admitted_for_sanitized_measurement_precheck",
            "decision_owner": "WAES/Harness human approval",
        },
    }
    OUTPUT_JSON.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""---
doc_id: GPCF-DOC-54C01FA442
title: Headroom LCX Measurement Admission Request 20260622
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md
source_path: docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Measurement Admission Request 20260622

## Evidence ID

`HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-20260622`

## 结论

本文件记录 WAES/Harness 脱敏测量准入申请包。当前裁决为 `{current_decision}`；这只允许进入脱敏测量 dry-run 预备阶段，不允许采集未脱敏生产 token、不允许启动生产代理、不允许写入真实 KDS API。

## 申请内容

| 项 | 当前值 |
|---|---|
| requested_decision | admitted_for_sanitized_measurement_precheck |
| current_waes_harness_admission_decision | {current_decision} |
| authorization_complete | {str(precheck_gates.get("authorization_complete") is True).lower()} |
| sanitized_ledger | {fields.get("sanitized_production_token_ledger")} |
| rollback_plan_id | {fields.get("rollback_plan_id")} |
| project_count | {len(PROJECTS)} |

## 申请准入边界

允许的未来测量动作仅限读取脱敏 token 台账元数据、计算节省估算、写入 Harness evidence。即使未来准入，也不得处理未脱敏原文、客户合同、POD、财务凭证、密钥或生产凭证。

## 门禁

| 项 | 当前值 |
|---|---|
| request_package_generated | true |
| authorization_complete | {str(precheck_gates.get("authorization_complete") is True).lower()} |
| waes_harness_admitted | {str(waes_harness_admitted).lower()} |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

{", ".join(PROJECTS)}

## 下一步

WAES/Harness 已批准进入脱敏测量 dry-run 预备阶段；下一轮只能建立 dry-run runner 骨架并验证边界，不得执行真实生产测量。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    loop = """---
doc_id: GPCF-DOC-4F8936D7E5
title: Loop Round GPCF Headroom LCX Measurement Admission Request 001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Measurement Admission Request 001

## 输入

- 用户要求进入下一步。
- 上一轮已补齐 6 个授权字段，`authorization_complete=true`。
- 当前 `waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck`。

## 动作

- 运行 `python3 tools/kds-sync/run_headroom_lcx_measurement_admission_request.py`。
- 刷新 WAES/Harness 脱敏测量准入申请包。
- 明确准入只覆盖脱敏测量 dry-run 预备阶段，不触发生产测量。

## 输出

- `docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json`
- `docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_measurement_admission_request.py`
- `python3 tools/kds-sync/validate_headroom_lcx_authorized_measurement_precheck.py`
- `python3 tools/kds-sync/validate_headroom_lcx_session_summary_declaration_boundary.py`

## 反馈

- 申请包已按 admitted-for-precheck 口径刷新。
- 当前仍不得进入未脱敏生产 token 测量或生产代理。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

建立脱敏测量 dry-run runner 骨架，但不得执行真实生产测量。
"""
    LOOP_ROUND.write_text(loop, encoding="utf-8")

    print(
        "headroom_lcx_measurement_admission_request=pass "
        f"project_count=15 current_waes_harness_admission_decision={current_decision} "
        f"waes_harness_admitted={str(waes_harness_admitted).lower()} production_token_measurement_allowed=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
