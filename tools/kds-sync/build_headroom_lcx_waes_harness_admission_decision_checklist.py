#!/usr/bin/env python3
"""Build WAES/Harness decision checklist and fixtures for Headroom LCX measurement admission."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUEST_JSON = ROOT / "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json"
APPROVAL_INSTANCE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json"
FIXTURES_JSON = ROOT / "fixtures/headroom/headroom-lcx-waes-harness-admission-decision-fixtures-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001.md"

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

REQUIRED_CHECKS = [
    "authorization_complete",
    "missing_required_field_count_zero",
    "sanitized_ledger_exists",
    "sanitized_ledger_contains_no_raw_content",
    "rollback_plan_exists",
    "telemetry_off_required",
    "waes_harness_decision_required",
    "human_approval_required",
    "no_real_kds_write",
    "no_external_api_write",
    "no_sensitive_material_processing",
    "no_production_proxy",
    "accepted_false",
    "integrated_false",
    "production_ready_false",
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


def base_positive(request: dict) -> dict:
    preconditions = request["admission_preconditions"]
    return {
        "decision": "admitted_for_sanitized_measurement_precheck",
        "project_count": 15,
        "projects": PROJECTS,
        "checks": {
            **preconditions,
            "no_real_kds_write": True,
            "no_external_api_write": True,
            "no_sensitive_material_processing": True,
            "no_production_proxy": True,
            "accepted_false": True,
            "integrated_false": True,
            "production_ready_false": True,
        },
        "allowed_actions": [
            "read_sanitized_ledger_metadata",
            "calculate_token_saving_estimate",
            "write_harness_evidence",
        ],
        "forbidden_actions": request["requested_measurement_boundary"]["forbidden_actions"],
        "evidence_refs": {
            "request": request["evidence_id"],
            "approval_instance": request["source_approval_instance"],
            "authorized_measurement_precheck": request["source_authorized_measurement_precheck"],
            "sanitized_ledger": request["sanitized_production_token_ledger"],
            "rollback_plan_id": request["rollback_plan_id"],
        },
    }


def main() -> int:
    request = load_json(REQUEST_JSON)
    approval = load_json(APPROVAL_INSTANCE_JSON)
    require(request.get("project_count") == 15 and request.get("projects") == PROJECTS, "request must cover 15 projects")
    require(request.get("current_waes_harness_admission_decision") == "blocked", "current decision must remain blocked")
    require(approval.get("authorization_fields", {}).get("waes_harness_admission_decision") == "blocked", "approval instance must remain blocked")

    positive = base_positive(request)
    cases = [
        {
            "case_id": "positive_sanitized_metadata_only",
            "expected": "admit_for_next_precheck_only",
            "candidate": positive,
        },
        {
            "case_id": "negative_raw_prompt_allowed",
            "expected": "reject",
            "expected_reason": "sensitive_material_not_allowed",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "no_sensitive_material_processing": False},
                "allowed_actions": positive["allowed_actions"] + ["read_raw_prompt"],
            },
        },
        {
            "case_id": "negative_real_kds_write",
            "expected": "reject",
            "expected_reason": "real_kds_write_not_allowed",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "no_real_kds_write": False},
                "allowed_actions": positive["allowed_actions"] + ["real_kds_api_write"],
            },
        },
        {
            "case_id": "negative_external_api_write",
            "expected": "reject",
            "expected_reason": "external_api_write_not_allowed",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "no_external_api_write": False},
                "allowed_actions": positive["allowed_actions"] + ["external_api_write"],
            },
        },
        {
            "case_id": "negative_production_proxy",
            "expected": "reject",
            "expected_reason": "production_proxy_not_allowed",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "no_production_proxy": False},
                "allowed_actions": positive["allowed_actions"] + ["production_proxy_start"],
            },
        },
        {
            "case_id": "negative_missing_human_approval",
            "expected": "reject",
            "expected_reason": "human_approval_required",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "human_approval_required": False},
            },
        },
        {
            "case_id": "negative_incomplete_project_scope",
            "expected": "reject",
            "expected_reason": "project_group_scope_must_be_15",
            "candidate": {
                **positive,
                "project_count": 14,
                "projects": PROJECTS[:-1],
            },
        },
        {
            "case_id": "negative_promotes_production_ready",
            "expected": "reject",
            "expected_reason": "production_status_upgrade_not_allowed",
            "candidate": {
                **positive,
                "checks": {**positive["checks"], "production_ready_false": False},
            },
        },
    ]

    fixtures = {
        "fixture_id": "HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-FIXTURES-20260622",
        "date": "2026-06-22",
        "project_count": 15,
        "projects": PROJECTS,
        "case_count": len(cases),
        "positive_case_count": 1,
        "negative_case_count": len(cases) - 1,
        "expected_admitted_for_next_precheck_only": 1,
        "expected_rejected": len(cases) - 1,
        "current_waes_harness_admission_decision": "blocked",
        "cases": cases,
    }

    checklist = {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-20260622",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001",
        "date": "2026-06-22",
        "status": "decision_checklist_generated_current_decision_blocked",
        "scope": "decision_checklist_and_fixtures_only_no_measurement",
        "project_count": 15,
        "projects": PROJECTS,
        "current_waes_harness_admission_decision": "blocked",
        "requested_future_decision": "admitted_for_sanitized_measurement_precheck",
        "required_checks": REQUIRED_CHECKS,
        "fixture_path": FIXTURES_JSON.relative_to(ROOT).as_posix(),
        "positive_case_count": 1,
        "negative_case_count": len(cases) - 1,
        "gates": {
            "decision_checklist_gate": True,
            "fixture_gate": True,
            "waes_harness_admitted": False,
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
    }

    write_json(FIXTURES_JSON, fixtures)
    write_json(EVIDENCE_JSON, checklist)

    rows = "\n".join(
        f"| `{case['case_id']}` | `{case['expected']}` | `{case.get('expected_reason', 'all_required_checks_pass')}` |"
        for case in cases
    )
    checks = "\n".join(f"- `{item}`" for item in REQUIRED_CHECKS)
    EVIDENCE_MD.write_text(
        f"""---
doc_id: GPCF-DOC-EE2D84B879
title: Headroom LCX WAES Harness Admission Decision Checklist 20260622
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, Edge, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md
source_path: docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX WAES Harness Admission Decision Checklist 20260622

## Evidence ID

`HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-20260622`

## 结论

本文件只生成 WAES/Harness 裁决清单与正负样例。当前 `waes_harness_admission_decision` 仍为 `blocked`，不得进入脱敏生产 token 测量。

## 必要检查项

{checks}

## 正负样例

| case_id | expected | reason |
|---|---|---|
{rows}

## 门禁

| 项 | 当前值 |
|---|---|
| decision_checklist_gate | true |
| fixture_gate | true |
| positive_case_count | 1 |
| negative_case_count | {len(cases) - 1} |
| current_waes_harness_admission_decision | blocked |
| waes_harness_admitted | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一步

只有人工明确批准正例语义，才允许把 approval instance 中的 `waes_harness_admission_decision` 改为 `admitted_for_sanitized_measurement_precheck` 并重新运行 authorized measurement precheck。
""",
        encoding="utf-8",
    )

    LOOP_ROUND.write_text(
        """---
doc_id: GPCF-DOC-B36D4C856B
title: Loop Round GPCF Headroom LCX WAES Harness Admission Decision Checklist 001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, Edge, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX WAES Harness Admission Decision Checklist 001

## 输入

- 用户要求进入下一步。
- 当前 measurement admission request 已生成，但 `waes_harness_admission_decision=blocked`。

## 动作

- 运行 `python3 tools/kds-sync/build_headroom_lcx_waes_harness_admission_decision_checklist.py`。
- 生成 WAES/Harness 裁决清单与正负样例。
- 保持当前 approval instance 的 blocked 状态。

## 输出

- `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md`
- `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json`
- `fixtures/headroom/headroom-lcx-waes-harness-admission-decision-fixtures-20260622.json`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_admission_decision_checklist.py`
- `python3 tools/kds-sync/validate_headroom_lcx_measurement_admission_request.py`

## 反馈

- 裁决清单和正负样例已生成。
- 当前仍不得进入脱敏生产 token 测量。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

等待用户是否明确批准正例语义，并决定是否修改 `waes_harness_admission_decision`。
""",
        encoding="utf-8",
    )

    print(
        "headroom_lcx_waes_harness_admission_decision_checklist=generated "
        "project_count=15 positive_case_count=1 negative_case_count=7 "
        "current_waes_harness_admission_decision=blocked "
        "waes_harness_admitted=false production_token_measurement_allowed=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
