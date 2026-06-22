#!/usr/bin/env python3
"""Build Headroom LCX approval package instance precheck."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json"
PACKAGE_TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-template.json"
INSTANCE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json"
NEGATIVE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md"

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


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    schema = load_json(SCHEMA_JSON)
    template = load_json(PACKAGE_TEMPLATE_JSON)
    require(schema.get("scope", {}).get("projects") == PROJECTS, "schema project scope mismatch")
    require(template.get("projects") == PROJECTS, "approval template project scope mismatch")

    instance = deepcopy(template)
    instance["instance_id"] = "HEADROOM-LCX-HUMAN-APPROVAL-PACKAGE-INSTANCE-PENDING-20260622"
    instance["instance_status"] = "pending_user_input"
    instance["created_at"] = "2026-06-22"
    instance["source_template"] = template.get("package_id")
    instance["schema_validation_expected"] = "blocked_placeholders"

    base_valid = deepcopy(template)
    base_valid["instance_id"] = "HEADROOM-LCX-HUMAN-APPROVAL-PACKAGE-INSTANCE-EXAMPLE"
    base_valid["authorization_fields"] = {
        "authorized_window_id": "LCX-MEASURE-20260622-EXAMPLE",
        "authorized_by": "GPCF-WAES-APPROVER-EXAMPLE",
        "authorized_at": "2026-06-22T00:00:00+08:00",
        "sanitized_production_token_ledger": "docs/harness/evidence/example-sanitized-ledger-id-only.json",
        "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-EXAMPLE",
        "waes_harness_admission_decision": "admitted_for_sanitized_measurement_precheck",
    }
    base_valid["human_attestations"] = {
        key: "confirmed" for key in template.get("human_attestations", {})
    }

    negative_cases = []
    missing_field = deepcopy(base_valid)
    del missing_field["authorization_fields"]["authorized_by"]
    negative_cases.append({"case_id": "missing_authorized_by", "expected_rejection_reason": "missing_required_field", "candidate": missing_field})

    placeholder_attestation = deepcopy(base_valid)
    placeholder_attestation["human_attestations"]["telemetry_off_confirmed"] = "REQUIRED_USER_INPUT"
    negative_cases.append({"case_id": "placeholder_attestation", "expected_rejection_reason": "placeholder_not_replaced", "candidate": placeholder_attestation})

    bad_window = deepcopy(base_valid)
    bad_window["authorization_fields"]["authorized_window_id"] = "MEASURE-20260622"
    negative_cases.append({"case_id": "bad_window_prefix", "expected_rejection_reason": "invalid_authorized_window_id", "candidate": bad_window})

    inline_ledger = deepcopy(base_valid)
    inline_ledger["authorization_fields"]["sanitized_production_token_ledger"] = {"raw_prompt": "do not store raw prompt"}
    negative_cases.append({"case_id": "inline_ledger_object", "expected_rejection_reason": "sanitized_ledger_must_be_reference_only", "candidate": inline_ledger})

    bad_waes = deepcopy(base_valid)
    bad_waes["authorization_fields"]["waes_harness_admission_decision"] = "approved"
    negative_cases.append({"case_id": "bad_waes_decision", "expected_rejection_reason": "waes_harness_decision_required", "candidate": bad_waes})

    production_true = deepcopy(base_valid)
    production_true["required_false_until_completed"]["production_admission_gate"] = True
    negative_cases.append({"case_id": "production_gate_true", "expected_rejection_reason": "approval_package_cannot_grant_production", "candidate": production_true})

    incomplete_scope = deepcopy(base_valid)
    incomplete_scope["project_count"] = 14
    incomplete_scope["projects"] = PROJECTS[:-1]
    negative_cases.append({"case_id": "incomplete_project_scope", "expected_rejection_reason": "project_group_scope_must_be_15", "candidate": incomplete_scope})

    negative = {
        "fixture_id": "HEADROOM-LCX-APPROVAL-INSTANCE-NEGATIVE-FIXTURES-20260622",
        "date": "2026-06-22",
        "case_count": len(negative_cases),
        "expected_rejected": len(negative_cases),
        "expected_accepted": 0,
        "cases": negative_cases,
    }

    evidence = {
        "evidence_id": "HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622",
        "task_id": "GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001",
        "date": "2026-06-22",
        "status": "approval_instance_precheck_blocked_pending_user_input",
        "scope": "approval_instance_precheck_only_no_measurement",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "schema_id": schema.get("schema_id"),
        "instance_path": INSTANCE_JSON.relative_to(ROOT).as_posix(),
        "negative_fixture_path": NEGATIVE_JSON.relative_to(ROOT).as_posix(),
        "negative_case_count": len(negative_cases),
        "current_instance_status": "blocked_placeholders",
        "gates": {
            "approval_instance_template_generated": True,
            "approval_instance_precheck_gate": False,
            "negative_instance_fixture_gate": True,
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

    write_json(INSTANCE_JSON, instance)
    write_json(NEGATIVE_JSON, negative)
    write_json(EVIDENCE_JSON, evidence)

    EVIDENCE_MD.write_text(
        f"""---
doc_id: GPCF-DOC-4D8C5F88C2
title: Headroom LCX Approval Instance Precheck Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, Edge, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md
source_path: docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Approval Instance Precheck Evidence

## Evidence ID

`HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622`

## 结论

已生成审批包待填写实例与负向实例。本 evidence 不构成授权完成；当前实例仍因 `REQUIRED_USER_INPUT` 占位符阻断，不允许采集生产 token 或启动生产代理。

## 输出

| artifact | path |
|---|---|
| pending approval instance | `{INSTANCE_JSON.relative_to(ROOT).as_posix()}` |
| negative instance fixtures | `{NEGATIVE_JSON.relative_to(ROOT).as_posix()}` |

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| negative_case_count | {len(negative_cases)} |
| approval_instance_template_generated | true |
| approval_instance_precheck_gate | false |
| negative_instance_fixture_gate | true |
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
doc_id: GPCF-DOC-4B6493F4B9
title: Loop Round GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001

## 输入

- 上轮输出：授权字段 schema 与人工审批包模板已生成。
- 本轮目标：建立审批包实例 precheck 与负向实例样例。
- 本轮边界：不补写授权事实、不伪造审批、不采集生产 token、不启动生产代理、不写 KDS、不触达外部 API、不升级 accepted、integrated 或 production_ready。

## 动作

1. 读取授权 schema 与审批包模板。
2. 生成待填写审批包实例。
3. 生成 7 个负向实例样例。
4. 建立 validator，验证待填写实例 blocked、负向实例全部 rejected。

## 输出

- `fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json`
- `fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json`
- `tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py`
- `tools/kds-sync/validate_headroom_lcx_approval_instance_precheck.py`
- `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json`
- `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py
python3 tools/kds-sync/validate_headroom_lcx_approval_instance_precheck.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

待填写实例当前 blocked，负向实例用于防止误授权进入生产测量。

## 下一轮

若用户填写审批包实例，可运行 approval instance validation；否则继续建立审批包实例填写说明和回滚清单。
""",
        encoding="utf-8",
    )

    print(
        "headroom_lcx_approval_instance_precheck=generated "
        f"project_count=15 negative_case_count={len(negative_cases)} "
        "approval_instance_precheck_gate=false authorization_complete=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
