---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623
title: Headroom LCX 真实测量授权字段映射证据
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 真实测量授权字段映射证据

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623`

## 结论

当前已经存在的预检/审批实例字段，可以直接映射到未来真实测量 runner 输入，但现在仍然只是 precheck-only。
status: authorization_field_map_defined_precheck_only

## 字段映射

| field | current_value | source_evidence | future_runner_input | future_action |
|---|---|---|---|---|
| authorized_window_id | LCX-MEASURE-20260622-001 | `HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622` | `authorized_window_id` | bind a real measurement window before any execution |
| authorized_by | lujunxiang / GPCF owner | `HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622` | `authorized_by` | bind approving owner before any execution |
| authorized_at | 2026-06-22T08:42:06+08:00 | `HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622` | `authorized_at` | bind approval timestamp before any execution |
| sanitized_production_token_ledger | fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json | `HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-20260622` | `sanitized_production_token_ledger` | allow metadata-only ledger reads for cost replay |
| rollback_plan_id | HEADROOM-LCX-ROLLBACK-PLAN-20260622-001 | `HEADROOM-LCX-ROLLBACK-PLAN-20260622-001` | `rollback_plan_id` | attach rollback runbook identifier before any measurement execution |
| waes_harness_admission_decision | admitted_for_sanitized_measurement_precheck | `HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621` | `waes_harness_admission_decision` | keep precheck-only until a new WAES/Harness decision is issued |

## 未来 runner 输入

`authorized_window_id`, `authorized_by`, `authorized_at`, `sanitized_production_token_ledger`, `rollback_plan_id`, `waes_harness_admission_decision`

## 执行门禁

- executable_now: `false`
- requires_real_measurement_authorization_window: `true`
- requires_waes_harness_decision: `true`
- requires_sanitized_token_ledger_metadata_only: `true`
- requires_rollback_plan_id: `true`
- requires_no_production_proxy: `true`
- requires_no_real_kds_write: `true`
- requires_no_external_api_write: `true`
- production_ready: `false`

## 非声明

- 本证据不表示真实测量已执行。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产分支已打开。
- 本证据不表示 accepted、integrated 或 production_ready。
