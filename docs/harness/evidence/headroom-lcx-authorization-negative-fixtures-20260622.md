---
doc_id: GPCF-DOC-72360135C4
title: Headroom LCX Authorization Negative Fixtures Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md
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

`fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json`

## 负向样例

| case_id | rejection_reason | expected |
|---|---|---|
| `missing_authorized_by` | `missing_required_field` | reject |
| `unresolved_placeholder` | `placeholder_not_replaced` | reject |
| `ledger_inline_sensitive_material` | `sanitized_ledger_must_be_reference_only` | reject |
| `missing_waes_harness_decision` | `waes_harness_decision_required` | reject |
| `production_gate_true_attempt` | `template_cannot_grant_production` | reject |
| `incomplete_project_scope` | `project_group_scope_must_be_15` | reject |
| `cross_project_memory_business_fact_claim` | `memory_cannot_be_business_fact_source` | reject |

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| case_count | 7 |
| expected_rejected | 7 |
| expected_accepted | 0 |
| authorization_complete | false |
| production_token_measurement_allowed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |
