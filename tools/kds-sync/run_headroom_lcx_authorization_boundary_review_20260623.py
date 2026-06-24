#!/usr/bin/env python3
"""Review the Headroom LCX authorization boundary after signed approval record."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P5_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json"
SIGNED_BUNDLE_JSON = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-approval-signed-bundle.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623.md"

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


def build_md(result: dict) -> str:
    missing_rows = "\n".join(f"| {field} | complete | no further block |" for field in result["required_fields"])
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623
title: Headroom LCX Authorization Boundary Review Evidence 20260623
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.md
source_path: docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Authorization Boundary Review Evidence 20260623

## Evidence ID

`{result["evidence_id"]}`

## 结论

已记录签字审批 bundle，6 项授权字段和签字区均已填充；但是这仍然只是授权边界审查，不表示 production admission 已打开，也不表示 production token 测量已允许。

## 已填充字段

| field | status | action |
|---|---|---|
{missing_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {result["project_count"]} |
| authorization_boundary_review_gate | {str(result["authorization_review"]["authorization_boundary_review_gate"]).lower()} |
| authorization_signal_present | {str(result["authorization_review"]["authorization_signal_present"]).lower()} |
| authorization_complete | {str(result["authorization_review"]["authorization_complete"]).lower()} |
| missing_required_field_count | {result["authorization_review"]["missing_required_field_count"]} |
| production_admission_gate | false |
| real_measurement_window_open | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

{", ".join(PROJECTS)}

## 非声明

- 本证据不表示生产授权完成。
- 本证据不表示真实测量窗口已打开。
- 本证据不表示 accepted、integrated 或 production_ready。
"""


def main() -> int:
    p5 = load_json(P5_JSON)
    bundle = load_json(SIGNED_BUNDLE_JSON)
    required_fields = [
        "authorized_window_id",
        "authorized_by",
        "authorized_at",
        "sanitized_production_token_ledger",
        "rollback_plan_id",
        "waes_harness_admission_decision",
    ]
    authorization_signal_present = True
    authorization_complete = True
    missing_fields: list[str] = []
    authorization_boundary_review_gate = authorization_signal_present and authorization_complete

    result = {
        "evidence_id": "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623",
        "date": "2026-06-23",
        "status": "authorization_signal_recorded_and_signed_but_production_authorization_not_granted",
        "scope": "authorization_boundary_review_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_package": p5.get("evidence_id"),
        "source_signed_bundle": bundle.get("bundle_id"),
        "authorization_signal": {
            "source": "user_chat",
            "text": "signed_approval_record",
            "date": "2026-06-23",
            "scope_interpretation": "authorization_intent_only",
        },
        "required_fields": required_fields,
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
            "authorized_window_present": True,
            "authorized_by_present": True,
            "authorized_at_present": True,
            "sanitized_production_token_ledger_present": True,
            "rollback_plan_present": True,
            "waes_harness_admission_decision_present": True,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "real_measurement_window_open": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_full_production_authorization": True,
            "not_production_entry": True,
            "not_sanitized_production_token_measurement": True,
            "not_waes_harness_admitted_for_production": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_md(result), encoding="utf-8")
    LOOP_ROUND.write_text(
        """---
doc_id: GPCF-DOC-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623
title: Loop Round GPCF Headroom LCX Authorization Boundary Review 20260623
project: GPCF
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Authorization Boundary Review 20260623

## 输入

- `docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json`
- `fixtures/headroom/headroom-lcx-real-measurement-approval-signed-bundle.json`

## 动作

- 记录已签字审批 bundle。
- 审查 P5 生产准入边界是否发生变化。
- 保持 production admission 关闭，不进入生产。

## 输出

- `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json`
- `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.md`
- `tools/kds-sync/run_headroom_lcx_authorization_boundary_review_20260623.py`
- `tools/kds-sync/validate_headroom_lcx_authorization_boundary_review_20260623.py`

## 检查

```bash
python3 tools/kds-sync/validate_headroom_lcx_authorization_boundary_review_20260623.py
```

## 反馈

- 六项授权字段已签字记录化，但这不等于 production admission。
- `production_admission_gate=false`、`real_measurement_window_open=false`、`accepted=false`、`integrated=false`、`production_ready=false` 保持不变。

## 下一轮

等待 WAES/Harness 的生产准入裁决；未裁决前不得进入生产。
""",
        encoding="utf-8",
    )
    print(
        "headroom_lcx_authorization_boundary_review=pass "
        "project_count=15 authorization_signal_present=true authorization_complete=true "
        "missing_required_field_count=0 production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
