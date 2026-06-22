#!/usr/bin/env python3
"""Review Headroom LCX authorization boundary after user authorization signal."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P5_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.md"

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

AUTHORIZATION_SIGNAL = {
    "source": "user_chat",
    "text": "给予授权",
    "date": "2026-06-21",
    "scope_interpretation": "authorization_intent_only",
}

REQUIRED_FIELDS = [
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_token_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
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
    p5 = load_json(P5_JSON)
    missing_fields = list(REQUIRED_FIELDS)
    authorization_signal_present = True
    authorization_complete = False
    authorization_boundary_review_gate = authorization_signal_present and not authorization_complete

    result = {
        "evidence_id": "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260621",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001",
        "date": "2026-06-21",
        "status": "authorization_signal_recorded_but_incomplete",
        "scope": "authorization_boundary_review_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_package": p5.get("evidence_id"),
        "authorization_signal": AUTHORIZATION_SIGNAL,
        "required_fields": REQUIRED_FIELDS,
        "missing_fields": missing_fields,
        "authorization_review": {
            "authorization_signal_present": authorization_signal_present,
            "authorization_complete": authorization_complete,
            "missing_required_field_count": len(missing_fields),
            "authorization_boundary_review_gate": authorization_boundary_review_gate,
            "production_admission_gate": False,
        },
        "gates": {
            "authorization_boundary_review_gate": authorization_boundary_review_gate,
            "authorization_signal_present": authorization_signal_present,
            "authorization_complete": authorization_complete,
            "authorized_window_present": False,
            "authorized_by_present": False,
            "authorized_at_present": False,
            "sanitized_production_token_ledger_present": False,
            "rollback_plan_present": False,
            "waes_harness_admission_decision_present": False,
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
            "not_full_production_authorization": True,
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
        "next_required_user_input": {
            "authorized_window_id": "required",
            "authorized_by": "required",
            "authorized_at": "required",
            "sanitized_production_token_ledger": "required",
            "rollback_plan_id": "required",
            "waes_harness_admission_decision": "required",
        },
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    missing_rows = "\n".join(f"| {field} | missing | required |" for field in missing_fields)
    md = f"""---
doc_id: GPCF-DOC-7974880641
title: Headroom LCX Authorization Boundary Review Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.md
source_path: docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX Authorization Boundary Review Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260621`

## 结论

已记录用户授权信号：`给予授权`。该信号证明存在人工授权意向，但尚未满足 P5 生产准入所需的完整字段。因此本轮只完成授权边界审查，`production_admission_gate=false`。

## 缺失字段

| field | status | action |
|---|---|---|
{missing_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| authorization_boundary_review_gate | true |
| authorization_signal_present | true |
| authorization_complete | false |
| missing_required_field_count | {len(missing_fields)} |
| authorized_window_present | false |
| authorized_by_present | false |
| authorized_at_present | false |
| sanitized_production_token_ledger_present | false |
| rollback_plan_present | false |
| waes_harness_admission_decision_present | false |
| production_proxy_started | false |
| production_sdk_enabled | false |
| production_external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

{", ".join(PROJECTS)}

## 下一步

补齐 6 项缺失字段后，才能进入 `GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-001`。未补齐前不得进入生产。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(
        "headroom_lcx_authorization_boundary_review=pass "
        "project_count=15 authorization_signal_present=true authorization_complete=false "
        "missing_required_field_count=6 production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
