#!/usr/bin/env python3
"""Build the Headroom production-token authorization package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTAKE_GATE = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.json"
LEDGER_TEMPLATE = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.md"


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
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_markdown(result: dict) -> str:
    return f"""---
doc_id: GPCF-DOC-ED41C98974
title: Headroom Production Token Authorization Package
project: KDS
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-production-token-authorization-package-20260621.md
source_path: docs/harness/evidence/headroom-production-token-authorization-package-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Production Token Authorization Package

## Evidence ID

`{result["evidence_id"]}`

## 结论

本包定义 Headroom 生产 token 实测采集的授权申请内容和放行条件。

`authorization_package_gate | {str(result["gate"]["authorization_package_gate"]).lower()}`，`authorization_status | {result["authorization"]["status"]}`，`production_admission_gate | false`。

当前未获得授权窗口、审批人、审批时间或真实脱敏生产 token 台账，因此本包是 pending 授权申请，不是生产实测或生产准入证明。

## 申请范围

| 项 | 当前值 |
|---|---|
| projects_requested | {len(result["requested_scope"]["projects"])} |
| measurement_window | pending |
| token_source | provider billing export or sanitized runtime usage ledger |
| telemetry | off |
| raw_prompt_storage | forbidden |
| external_api_write_allowed | false |
| kds_write_allowed | false |
| rollback_plan_required | true |

## 放行条件

| 条件 | 当前值 |
|---|---|
| authorized_window_present | false |
| approver_present | false |
| approval_timestamp_present | false |
| sanitized_ledger_present | false |
| rollback_plan_present | false |
| negative_fixture_gate_passed | true |
| authorization_package_gate | false |
| production_admission_gate | false |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不保存 raw prompt、raw completion、secret 或 authorization header。
- 不升级 accepted、integrated 或 production_ready。
"""


def main() -> int:
    intake = load_json(INTAKE_GATE)
    ledger_template = load_json(LEDGER_TEMPLATE)
    require(intake["gate"]["production_token_intake_gate"] is False, "intake gate must remain blocked")
    require(ledger_template["measured_production_tokens"] is False, "template must not claim production tokens")
    result = {
        "evidence_id": "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-PACKAGE-20260621",
        "date": "2026-06-21",
        "status": "authorization_package_defined_pending",
        "source_evidence": [rel(INTAKE_GATE), rel(LEDGER_TEMPLATE)],
        "requested_scope": {
            "projects": PROJECTS,
            "token_source": "provider_billing_export_or_sanitized_runtime_usage_ledger",
            "measurement_window": None,
            "telemetry": "off",
            "raw_prompt_storage": "forbidden",
            "external_api_write_allowed": False,
            "kds_write_allowed": False,
            "rollback_plan_required": True,
        },
        "authorization": {
            "status": "pending",
            "authorized_window_id": None,
            "authorized_by": None,
            "authorized_at": None,
            "scope": "project_group_production_token_measurement",
        },
        "gate": {
            "authorized_window_present": False,
            "approver_present": False,
            "approval_timestamp_present": False,
            "sanitized_ledger_present": False,
            "rollback_plan_present": False,
            "negative_fixture_gate_passed": True,
            "authorization_package_gate": False,
            "production_admission_gate": False,
        },
        "next_required_action": "obtain explicit human authorization window before collecting sanitized production token ledger",
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_production_token_authorization_package=pass "
        "authorization_status=pending authorization_package_gate=false "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
