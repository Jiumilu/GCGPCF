#!/usr/bin/env python3
"""Build Headroom LCX authorization negative fixtures."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json"
NEGATIVE_FIXTURES_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001.md"

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


def completed_candidate(template: dict) -> dict:
    candidate = deepcopy(template)
    values = {
        "authorized_window_id": "LCX-MEASURE-20260622-EXAMPLE",
        "authorized_by": "GPCF-WAES-APPROVER-EXAMPLE",
        "authorized_at": "2026-06-22T00:00:00+08:00",
        "sanitized_production_token_ledger": "docs/harness/evidence/example-sanitized-ledger-id-only.json",
        "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-EXAMPLE",
        "waes_harness_admission_decision": "admitted_for_sanitized_measurement_precheck",
    }
    for field, value in values.items():
        candidate["authorization_fields"][field]["value"] = value
    candidate["required_false_until_completed"]["authorization_complete"] = True
    return candidate


def main() -> int:
    template = load_json(TEMPLATE_JSON)
    require(template.get("scope", {}).get("project_count") == 15, "template must cover 15 projects")
    require(set(template.get("authorization_fields", {})) == set(REQUIRED_FIELDS), "template fields mismatch")

    base = completed_candidate(template)
    cases = []

    missing_authorized_by = deepcopy(base)
    del missing_authorized_by["authorization_fields"]["authorized_by"]
    cases.append(
        {
            "case_id": "missing_authorized_by",
            "expected_rejection_reason": "missing_required_field",
            "candidate": missing_authorized_by,
        }
    )

    unresolved_placeholder = deepcopy(base)
    unresolved_placeholder["authorization_fields"]["rollback_plan_id"]["value"] = "REQUIRED_USER_INPUT"
    cases.append(
        {
            "case_id": "unresolved_placeholder",
            "expected_rejection_reason": "placeholder_not_replaced",
            "candidate": unresolved_placeholder,
        }
    )

    ledger_inline_sensitive = deepcopy(base)
    ledger_inline_sensitive["authorization_fields"]["sanitized_production_token_ledger"]["value"] = {
        "inline_raw_text": "example unredacted customer contract body marker",
        "contains_sensitive_original": True,
    }
    cases.append(
        {
            "case_id": "ledger_inline_sensitive_material",
            "expected_rejection_reason": "sanitized_ledger_must_be_reference_only",
            "candidate": ledger_inline_sensitive,
        }
    )

    missing_waes_decision = deepcopy(base)
    missing_waes_decision["authorization_fields"]["waes_harness_admission_decision"]["value"] = ""
    cases.append(
        {
            "case_id": "missing_waes_harness_decision",
            "expected_rejection_reason": "waes_harness_decision_required",
            "candidate": missing_waes_decision,
        }
    )

    production_gate_true = deepcopy(base)
    production_gate_true["required_false_until_completed"]["production_admission_gate"] = True
    production_gate_true["required_false_until_completed"]["production_ready"] = True
    cases.append(
        {
            "case_id": "production_gate_true_attempt",
            "expected_rejection_reason": "template_cannot_grant_production",
            "candidate": production_gate_true,
        }
    )

    incomplete_scope = deepcopy(base)
    incomplete_scope["scope"]["projects"] = PROJECTS[:-1]
    incomplete_scope["scope"]["project_count"] = 14
    cases.append(
        {
            "case_id": "incomplete_project_scope",
            "expected_rejection_reason": "project_group_scope_must_be_15",
            "candidate": incomplete_scope,
        }
    )

    cross_project_memory_claim = deepcopy(base)
    cross_project_memory_claim["scope"]["not_allowed_by_this_template"] = [
        item for item in cross_project_memory_claim["scope"]["not_allowed_by_this_template"] if item != "accepted_or_integrated_or_production_ready_upgrade"
    ]
    cross_project_memory_claim["scope"]["cross_project_memory_as_business_fact"] = True
    cases.append(
        {
            "case_id": "cross_project_memory_business_fact_claim",
            "expected_rejection_reason": "memory_cannot_be_business_fact_source",
            "candidate": cross_project_memory_claim,
        }
    )

    fixtures = {
        "fixture_id": "HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622",
        "date": "2026-06-22",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_template": template.get("template_id"),
        "case_count": len(cases),
        "cases": cases,
        "expected_result": {
            "rejected": len(cases),
            "accepted": 0,
            "production_token_measurement_allowed": False,
            "production_admission_gate": False,
            "accepted_status": False,
            "integrated": False,
            "production_ready": False,
        },
    }

    evidence = {
        "evidence_id": "HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001",
        "date": "2026-06-22",
        "status": "negative_fixtures_generated_no_measurement",
        "scope": "authorization_fixture_rejection_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "fixture_path": NEGATIVE_FIXTURES_JSON.relative_to(ROOT).as_posix(),
        "case_count": len(cases),
        "expected_rejected": len(cases),
        "expected_accepted": 0,
        "gates": {
            "negative_fixture_generation_gate": True,
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
    }

    write_json(NEGATIVE_FIXTURES_JSON, fixtures)
    write_json(EVIDENCE_JSON, evidence)

    case_rows = "\n".join(
        f"| `{case['case_id']}` | `{case['expected_rejection_reason']}` | reject |" for case in cases
    )
    EVIDENCE_MD.write_text(
        f"""---
doc_id: GPCF-DOC-8C2733418D
title: Headroom LCX Authorization Negative Fixtures Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, Edge, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md
source_path: docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Authorization Negative Fixtures Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622`

## 结论

已生成授权模板负向 fixtures。本 evidence 只证明误授权样例可被 validator 拒绝，不构成授权完成，不允许采集生产 token，不允许启动生产代理，不允许真实 KDS 或外部 API 写入。

## Fixture 路径

`{NEGATIVE_FIXTURES_JSON.relative_to(ROOT).as_posix()}`

## 负向样例

| case_id | rejection_reason | expected |
|---|---|---|
{case_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| case_count | {len(cases)} |
| expected_rejected | {len(cases)} |
| expected_accepted | 0 |
| authorization_complete | false |
| production_token_measurement_allowed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |
""",
        encoding="utf-8",
    )

    LOOP_ROUND.write_text(
        """---
doc_id: GPCF-DOC-8917CE2B70
title: Loop Round GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001

## 输入

- 上轮输出：授权字段模板已生成，但未获得 6 个实际授权字段。
- 本轮目标：建立授权模板负向 fixtures 与误授权拦截 validator。
- 本轮边界：不补写授权事实、不伪造审批、不采集生产 token、不启动生产代理、不写 KDS、不触达外部 API、不升级 accepted、integrated 或 production_ready。

## 动作

1. 读取授权字段模板。
2. 生成 7 个负向授权样例。
3. 建立 validator，要求全部负向样例被拒绝。
4. 更新 evidence index、Loop 控制板和成本评估模型。

## 输出

- `fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json`
- `tools/kds-sync/build_headroom_lcx_authorization_negative_fixtures.py`
- `tools/kds-sync/validate_headroom_lcx_authorization_negative_fixtures.py`
- `docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.json`
- `docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_authorization_negative_fixtures.py
python3 tools/kds-sync/validate_headroom_lcx_authorization_negative_fixtures.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

负向 fixtures 必须全部 rejected；任何字段缺失、占位符未替换、敏感原文混入、WAES/Harness 裁决缺失、生产门禁误置 true 或项目范围不足都不得进入测量。

## 下一轮

若用户补齐完整授权字段，则重新运行 authorized measurement precheck；否则继续建立授权字段 schema 和人工审批包。
""",
        encoding="utf-8",
    )

    print(
        "headroom_lcx_authorization_negative_fixtures=generated "
        f"project_count=15 case_count={len(cases)} expected_rejected={len(cases)} "
        "expected_accepted=0 production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
