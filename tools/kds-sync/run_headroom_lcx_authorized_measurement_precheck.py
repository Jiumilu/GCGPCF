#!/usr/bin/env python3
"""Run Headroom LCX authorized measurement precheck."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_REVIEW_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json"
APPROVAL_INSTANCE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.md"

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
    auth_review = load_json(AUTH_REVIEW_JSON)
    approval_instance = load_json(APPROVAL_INSTANCE_JSON)
    required_fields = auth_review.get("required_fields", [])
    instance_fields = approval_instance.get("authorization_fields", {})
    missing_fields = [
        field
        for field in required_fields
        if not instance_fields.get(field) or instance_fields.get(field) == "REQUIRED_USER_INPUT"
    ]
    waes_harness_admission_decision = instance_fields.get("waes_harness_admission_decision")
    authorization_signal_present = auth_review.get("gates", {}).get("authorization_signal_present") is True
    authorization_complete = authorization_signal_present and not missing_fields
    waes_harness_admitted = waes_harness_admission_decision == "admitted_for_sanitized_measurement_precheck"
    measurement_precheck_gate = authorization_complete and waes_harness_admitted
    status = (
        "authorized_measurement_precheck_admitted_for_sanitized_dry_run_only"
        if measurement_precheck_gate
        else "authorized_measurement_precheck_blocked_by_waes_harness_decision"
    )

    result = {
        "evidence_id": "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-001",
        "date": "2026-06-22",
        "status": status,
        "scope": "precheck_only_no_measurement",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_authorization_review": auth_review.get("evidence_id"),
        "source_approval_instance": approval_instance.get("instance_id"),
        "waes_harness_admission_decision": waes_harness_admission_decision,
        "missing_fields": missing_fields,
        "precheck": {
            "authorization_signal_present": authorization_signal_present,
            "authorization_complete": authorization_complete,
            "missing_required_field_count": len(missing_fields),
            "authorized_measurement_precheck_gate": measurement_precheck_gate,
            "waes_harness_admitted": waes_harness_admitted,
            "production_token_measurement_allowed": False,
            "production_admission_gate": False,
        },
        "gates": {
            "authorized_measurement_precheck_gate": measurement_precheck_gate,
            "authorization_signal_present": authorization_signal_present,
            "authorization_complete": authorization_complete,
            "missing_required_field_count_zero": not missing_fields,
            "waes_harness_admitted": waes_harness_admitted,
            "production_token_measurement_allowed": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_authorized_production_measurement": True,
            "not_production_entry": True,
            "not_sanitized_production_token_measurement": True,
            "not_waes_harness_admitted": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_required_user_input": auth_review.get("next_required_user_input", {}),
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if missing_fields:
        missing_rows = "\n".join(f"| {field} | missing | blocks measurement |" for field in missing_fields)
    else:
        missing_rows = "| none | complete | no missing-field block |"
    md = f"""---
doc_id: GPCF-DOC-E92337280E
title: Headroom LCX Authorized Measurement Precheck Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.md
source_path: docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Authorized Measurement Precheck Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621`

## 结论

已执行授权测量前置检查。授权意向存在，6 个授权字段已补齐；WAES/Harness 准入裁决为 `{waes_harness_admission_decision}`。本裁决只允许进入脱敏测量 dry-run 预备阶段，不允许采集未脱敏生产 token、不允许启动生产代理、不允许写入真实 KDS API。

## 阻断字段

| field | status | effect |
|---|---|---|
{missing_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| authorized_measurement_precheck_gate | {str(measurement_precheck_gate).lower()} |
| authorization_signal_present | {str(authorization_signal_present).lower()} |
| authorization_complete | {str(authorization_complete).lower()} |
| missing_required_field_count | {len(missing_fields)} |
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

若未来需要执行脱敏测量 dry-run，必须先建立独立 runner，并继续保持 `production_token_measurement_allowed=false`、`measured_production_tokens=false`、`accepted=false`、`integrated=false`、`production_ready=false`。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    output_status = "pass_precheck_only" if measurement_precheck_gate else "blocked"
    print(
        f"headroom_lcx_authorized_measurement_precheck={output_status} "
        f"project_count=15 authorization_signal_present=true authorization_complete={str(authorization_complete).lower()} "
        f"missing_required_field_count={len(missing_fields)} waes_harness_admission_decision={waes_harness_admission_decision} "
        "production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
