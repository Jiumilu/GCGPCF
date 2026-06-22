#!/usr/bin/env python3
"""Build Headroom LCX authorized measurement authorization template."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_REVIEW_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json"
PRECHECK_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json"
TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001.md"

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

REQUIRED_FIELDS = [
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_token_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
]

PLACEHOLDER = "REQUIRED_USER_INPUT"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    auth_review = load_json(AUTH_REVIEW_JSON)
    precheck = load_json(PRECHECK_JSON)
    missing_fields = auth_review.get("missing_fields", [])
    require(missing_fields == REQUIRED_FIELDS, "authorization boundary review must still list six missing fields")
    require(precheck.get("gates", {}).get("production_token_measurement_allowed") is False, "precheck must block measurement")

    template = {
        "template_id": "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621",
        "purpose": "collect_complete_human_authorization_before_any_sanitized_production_token_measurement",
        "scope": {
            "project_count": len(PROJECTS),
            "projects": PROJECTS,
            "allowed_next_action_after_completion": "rerun_authorized_measurement_precheck_only",
            "not_allowed_by_this_template": [
                "production_proxy_start",
                "production_sdk_enablement",
                "real_kds_api_write",
                "external_api_write",
                "sensitive_raw_material_processing",
                "accepted_or_integrated_or_production_ready_upgrade",
            ],
        },
        "authorization_fields": {
            "authorized_window_id": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "stable_window_identifier",
                "example": "LCX-MEASURE-YYYYMMDD-001",
            },
            "authorized_by": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "human_approver_or_governance_role",
                "example": "GPCF/WAES named approver",
            },
            "authorized_at": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "ISO-8601 timestamp with timezone",
                "example": "2026-06-21T00:00:00+08:00",
            },
            "sanitized_production_token_ledger": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "path_to_sanitized_ledger_or_evidence_id",
                "must_not_include": ["raw prompt", "raw completion", "secret", "credential", "customer contract text"],
            },
            "rollback_plan_id": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "controlled_rollback_plan_or_runbook_id",
                "minimum_contents": ["disable proxy", "disable SDK", "delete temporary cache", "retain evidence"],
            },
            "waes_harness_admission_decision": {
                "value": PLACEHOLDER,
                "required": True,
                "format": "WAES/Harness decision evidence id",
                "allowed_values": ["admitted_for_sanitized_measurement_precheck", "blocked"],
            },
        },
        "required_false_until_completed": {
            "authorization_complete": False,
            "production_token_measurement_allowed": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }

    evidence = {
        "evidence_id": "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001",
        "date": "2026-06-21",
        "status": "authorization_template_generated_no_measurement",
        "scope": "template_only_no_authorization_completion",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_authorization_review": auth_review.get("evidence_id"),
        "source_precheck": precheck.get("evidence_id"),
        "template_path": TEMPLATE_JSON.relative_to(ROOT).as_posix(),
        "required_fields": REQUIRED_FIELDS,
        "placeholder": PLACEHOLDER,
        "gates": {
            "authorization_template_generated": True,
            "authorization_complete": False,
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
            "template_is_not_authorization": True,
            "not_authorized_measurement": True,
            "not_production_entry": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_step": "user_or_governance_owner_fills_template_then_rerun_precheck",
    }

    write_json(TEMPLATE_JSON, template)
    write_json(EVIDENCE_JSON, evidence)

    field_rows = "\n".join(f"| `{field}` | required | `{PLACEHOLDER}` |" for field in REQUIRED_FIELDS)
    EVIDENCE_MD.write_text(
        f"""---
doc_id: GPCF-DOC-09531740E7
title: Headroom LCX Authorized Measurement Authorization Template Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md
source_path: docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX Authorized Measurement Authorization Template Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621`

## 结论

已生成授权字段模板和审计包。本文件不构成授权完成，不允许采集生产 token，不允许启动生产代理，不允许真实 KDS 或外部 API 写入。

## 模板路径

`{TEMPLATE_JSON.relative_to(ROOT).as_posix()}`

## 必填字段

| field | required | current placeholder |
|---|---|---|
{field_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| authorization_template_generated | true |
| authorization_complete | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

{", ".join(PROJECTS)}

## 下一步

由授权人补齐模板字段，并附 WAES/Harness 准入裁决后，重新运行授权测量前置检查。
""",
        encoding="utf-8",
    )

    LOOP_ROUND.write_text(
        """---
doc_id: GPCF-DOC-40025385F7
title: Loop Round GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001

## 输入

- 上轮输出：授权测量 precheck blocked，缺 6 个授权字段。
- 本轮目标：生成可填写、可校验、可审计的授权字段模板包。
- 本轮边界：不补写授权事实、不伪造审批、不采集生产 token、不启动生产代理、不写 KDS、不触达外部 API、不升级 accepted、integrated 或 production_ready。

## 动作

1. 读取 authorization boundary review 和 authorized measurement precheck evidence。
2. 生成授权字段模板 JSON。
3. 生成模板 evidence 和 validator。
4. 更新 evidence index、Loop 控制板和成本评估模型。

## 输出

- `fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json`
- `tools/kds-sync/build_headroom_lcx_authorized_measurement_authorization_template.py`
- `tools/kds-sync/validate_headroom_lcx_authorized_measurement_authorization_template.py`
- `docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.json`
- `docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_authorized_measurement_authorization_template.py
python3 tools/kds-sync/validate_headroom_lcx_authorized_measurement_authorization_template.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

模板包已生成，但模板不是授权本身。所有生产、测量、写入和验收状态仍保持 blocked/false。

## 下一轮

若用户提供完整字段和 WAES/Harness 准入裁决，则重新运行 authorized measurement precheck；否则只能继续完善负向 fixtures 和审计口径。
""",
        encoding="utf-8",
    )

    print(
        "headroom_lcx_authorized_measurement_authorization_template=pass "
        "project_count=15 required_field_count=6 authorization_complete=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
