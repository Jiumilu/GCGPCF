#!/usr/bin/env python3
"""Build Headroom LCX P5 production admission request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.md"

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

REQUIRED_EVIDENCE = [
    "docs/harness/evidence/headroom-lcx-controlled-package-20260621.json",
    "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json",
    "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json",
    "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json",
    "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json",
    "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.json",
    "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json",
    "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json",
]

REQUIRED_AUTHORIZATION_ITEMS = [
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


def load_json(rel: str) -> dict:
    path = ROOT / rel
    require(path.exists(), f"missing evidence: {rel}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{rel} must contain JSON object")
    return data


def main() -> int:
    evidence_chain = []
    for rel in REQUIRED_EVIDENCE:
        data = load_json(rel)
        evidence_chain.append(
            {
                "path": rel,
                "evidence_id": data.get("evidence_id"),
                "production_admission_gate": data.get("gates", data.get("gate", {})).get("production_admission_gate")
                if isinstance(data.get("gates", data.get("gate", {})), dict)
                else False,
            }
        )

    auth_package = load_json("docs/harness/evidence/headroom-production-token-authorization-package-20260621.json")
    action_queue = load_json("docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json")
    pending_actions = [item for item in action_queue.get("actions", []) if item.get("gate") is False]
    all_prior_non_production = all(item.get("production_admission_gate") is False for item in evidence_chain)
    p5_package_gate = len(evidence_chain) == len(REQUIRED_EVIDENCE) and len(pending_actions) == 6 and all_prior_non_production

    result = {
        "evidence_id": "HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001",
        "date": "2026-06-21",
        "status": "production_admission_request_package_generated_pending_authorization",
        "scope": "request_package_only_no_production_entry",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "evidence_chain": evidence_chain,
        "required_authorization_items": REQUIRED_AUTHORIZATION_ITEMS,
        "pending_action_count": len(pending_actions),
        "pending_actions": pending_actions,
        "authorization_snapshot": auth_package.get("authorization", {}),
        "requested_scope": auth_package.get("requested_scope", {}),
        "admission_decision": {
            "request_package_generated": True,
            "authorization_window_present": False,
            "sanitized_production_token_ledger_present": False,
            "rollback_plan_present": False,
            "waes_harness_admission_decision_present": False,
            "p5_request_package_gate": p5_package_gate,
            "production_admission_gate": False,
        },
        "gates": {
            "p5_production_admission_package_gate": p5_package_gate,
            "request_package_generated": True,
            "prior_p0_p4_evidence_present": True,
            "pending_actions_registered": True,
            "authorization_window_present": False,
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
            "not_production_entry": True,
            "not_authorized_window": True,
            "not_sanitized_production_token_measurement": True,
            "not_waes_harness_admitted": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_round": "GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001",
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pending_rows = "\n".join(
        f"| {item['action_id']} | {item['title']} | {item['owner']} | {item['status']} | false |"
        for item in pending_actions
    )
    evidence_rows = "\n".join(
        f"| {item['path']} | {item['evidence_id']} | false |"
        for item in evidence_chain
    )
    md = f"""---
doc_id: GPCF-DOC-74613D61D3
title: Headroom LCX P5 Production Admission Package Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P5 Production Admission Package Evidence

## Evidence ID

`HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621`

## 结论

P5 生产准入申请包已生成，但没有进入生产。当前仍缺授权窗口、审批人、审批时间、脱敏生产 token 台账、回滚计划和 WAES/Harness 准入裁决，因此 `production_admission_gate=false`。

## P0-P4 Evidence Chain

| path | evidence_id | production_admission_gate |
|---|---|---:|
{evidence_rows}

## Pending Authorization Actions

| action_id | title | owner | status | gate |
|---|---|---|---|---:|
{pending_rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| p5_production_admission_package_gate | {str(p5_package_gate).lower()} |
| request_package_generated | true |
| pending_action_count | {len(pending_actions)} |
| authorization_window_present | false |
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

`GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001`：等待人工授权窗口与 WAES/Harness 裁决；未授权前不得进入生产。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    print(
        "headroom_lcx_p5_production_admission_package=pass "
        "project_count=15 pending_action_count=6 request_package_generated=true "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
