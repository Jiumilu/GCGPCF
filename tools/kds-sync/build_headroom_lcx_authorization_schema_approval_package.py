#!/usr/bin/env python3
"""Build Headroom LCX authorization schema and human approval package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json"
NEGATIVE_FIXTURES_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json"
SCHEMA_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json"
APPROVAL_PACKAGE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001.md"

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


def main() -> int:
    auth_template = load_json(AUTH_TEMPLATE_JSON)
    negative_fixtures = load_json(NEGATIVE_FIXTURES_JSON)
    require(auth_template.get("scope", {}).get("projects") == PROJECTS, "authorization template must cover 15 projects")
    require(negative_fixtures.get("case_count") == 7, "negative fixture count must be 7")

    schema = {
        "schema_id": "HEADROOM-LCX-AUTHORIZATION-SCHEMA-20260622",
        "schema_version": "v1.0",
        "scope": {
            "project_count": len(PROJECTS),
            "projects": PROJECTS,
            "exact_project_scope_required": True,
        },
        "required_fields": REQUIRED_FIELDS,
        "field_rules": {
            "authorized_window_id": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "prefix": "LCX-MEASURE-",
            },
            "authorized_by": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "human_approver_required": True,
            },
            "authorized_at": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "requires_timezone": True,
            },
            "sanitized_production_token_ledger": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "reference_only": True,
                "forbid_inline_raw_text": True,
            },
            "rollback_plan_id": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "must_reference_controlled_plan": True,
            },
            "waes_harness_admission_decision": {
                "required": True,
                "type": "string",
                "must_not_equal": "REQUIRED_USER_INPUT",
                "allowed_values": ["admitted_for_sanitized_measurement_precheck", "blocked"],
                "must_reference_evidence": True,
            },
        },
        "hard_false_until_waes_harness_admits": [
            "production_token_measurement_allowed",
            "production_proxy_started",
            "production_sdk_enabled",
            "production_external_api_write",
            "kds_api_write",
            "sensitive_material_processed",
            "measured_production_tokens",
            "production_admission_gate",
            "accepted",
            "integrated",
            "production_ready",
        ],
    }

    approval_package = {
        "package_id": "HEADROOM-LCX-HUMAN-APPROVAL-PACKAGE-TEMPLATE-20260622",
        "schema_id": schema["schema_id"],
        "purpose": "human_approval_package_before_rerunning_authorized_measurement_precheck",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "authorization_fields": {
            field: "REQUIRED_USER_INPUT" for field in REQUIRED_FIELDS
        },
        "human_attestations": {
            "telemetry_off_confirmed": "REQUIRED_USER_INPUT",
            "sanitized_ledger_reference_only": "REQUIRED_USER_INPUT",
            "no_sensitive_raw_material": "REQUIRED_USER_INPUT",
            "no_real_kds_write": "REQUIRED_USER_INPUT",
            "no_external_api_write": "REQUIRED_USER_INPUT",
            "rollback_plan_reviewed": "REQUIRED_USER_INPUT",
            "waes_harness_evidence_attached": "REQUIRED_USER_INPUT",
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
        "evidence_id": "HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001",
        "date": "2026-06-22",
        "status": "schema_and_approval_package_generated_no_authorization_completion",
        "scope": "schema_template_only_no_measurement",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_authorization_template": auth_template.get("template_id"),
        "source_negative_fixture": negative_fixtures.get("fixture_id"),
        "schema_path": SCHEMA_JSON.relative_to(ROOT).as_posix(),
        "approval_package_template_path": APPROVAL_PACKAGE_JSON.relative_to(ROOT).as_posix(),
        "required_field_count": len(REQUIRED_FIELDS),
        "human_attestation_count": len(approval_package["human_attestations"]),
        "gates": {
            "authorization_schema_gate": True,
            "approval_package_template_gate": True,
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

    write_json(SCHEMA_JSON, schema)
    write_json(APPROVAL_PACKAGE_JSON, approval_package)
    write_json(EVIDENCE_JSON, evidence)

    EVIDENCE_MD.write_text(
        f"""---
doc_id: GPCF-DOC-90DF124EDC
title: Headroom LCX Authorization Schema Approval Package Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, Edge, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md
source_path: docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Authorization Schema Approval Package Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-20260622`

## 结论

已生成授权字段 schema 与人工审批包模板。本 evidence 不构成授权完成，不允许采集生产 token，不允许启动生产代理，不允许真实 KDS 或外部 API 写入。

## 输出

| artifact | path |
|---|---|
| authorization schema | `{SCHEMA_JSON.relative_to(ROOT).as_posix()}` |
| approval package template | `{APPROVAL_PACKAGE_JSON.relative_to(ROOT).as_posix()}` |

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| required_field_count | {len(REQUIRED_FIELDS)} |
| human_attestation_count | {len(approval_package["human_attestations"])} |
| authorization_schema_gate | true |
| approval_package_template_gate | true |
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
doc_id: GPCF-DOC-5939F2B7C2
title: Loop Round GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001

## 输入

- 上轮输出：授权模板负向 fixtures 7/7 rejected。
- 本轮目标：建立授权字段 schema 与人工审批包 validator。
- 本轮边界：不补写授权事实、不伪造审批、不采集生产 token、不启动生产代理、不写 KDS、不触达外部 API、不升级 accepted、integrated 或 production_ready。

## 动作

1. 读取授权模板和负向 fixtures。
2. 生成授权字段 schema。
3. 生成人工审批包模板。
4. 建立 validator，验证 schema、审批包和生产门禁均保持 false。

## 输出

- `fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json`
- `fixtures/headroom/headroom-lcx-human-approval-package-template.json`
- `tools/kds-sync/build_headroom_lcx_authorization_schema_approval_package.py`
- `tools/kds-sync/validate_headroom_lcx_authorization_schema_approval_package.py`
- `docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json`
- `docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_authorization_schema_approval_package.py
python3 tools/kds-sync/validate_headroom_lcx_authorization_schema_approval_package.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

schema 与人工审批包模板只提供结构化授权入口，不构成授权完成。生产测量仍需 6 个字段和 WAES/Harness evidence。

## 下一轮

若用户补齐审批包，可进入审批包实例 precheck；否则继续建立审批包负向样例。
""",
        encoding="utf-8",
    )

    print(
        "headroom_lcx_authorization_schema_approval_package=generated "
        f"project_count=15 required_field_count={len(REQUIRED_FIELDS)} "
        f"human_attestation_count={len(approval_package['human_attestations'])} "
        "authorization_complete=false production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
