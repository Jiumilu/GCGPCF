---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623
title: Headroom LCX Real Measurement Authorization Signoff Template Evidence
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement Authorization Signoff Template Evidence

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623`

## 结论

这是一个可签字的授权包模板，不是授权完成，不是真实测量，不打开 production branch。

## 模板路径

`fixtures/headroom/headroom-lcx-real-measurement-authorization-signoff-template.json`

## 计数

| item | value |
|---|---|
| required_field_count | 6 |
| required_signature_field_count | 6 |

## 需要签字的 6 个字段

| field | required | current placeholder | signing note |
|---|---|---|---|
| `authorized_window_id` | required | `REQUIRED_USER_INPUT` | 绑定真实授权窗口 ID |
| `authorized_by` | required | `REQUIRED_USER_INPUT` | 绑定授权人或治理角色 |
| `authorized_at` | required | `REQUIRED_USER_INPUT` | 绑定带时区的授权时间 |
| `sanitized_production_token_ledger` | required | `REQUIRED_USER_INPUT` | 只允许脱敏账本引用 |
| `rollback_plan_id` | required | `REQUIRED_USER_INPUT` | 绑定回滚预案或 runbook ID |
| `waes_harness_admission_decision` | required | `REQUIRED_USER_INPUT` | 绑定 WAES/Harness 裁决证据 |

## 签署区

| item | value |
|---|---|
| signer_name | `REQUIRED_USER_INPUT` |
| signer_role | `REQUIRED_USER_INPUT` |
| signed_at | `REQUIRED_USER_INPUT` |
| signature_method | `REQUIRED_USER_INPUT` |
| signature_statement | `REQUIRED_USER_INPUT` |
| signature_intent | `approve_open_real_measurement_window_or_reject_or_defer` |

## 签署后仍必须保持的 false 项

| item | value |
|---|---|
| authorization_complete | `false` |
| real_measurement_window_open | `false` |
| production_token_measurement_allowed | `false` |
| production_proxy_started | `false` |
| production_sdk_enabled | `false` |
| production_external_api_write | `false` |
| kds_api_write | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本模板不表示授权完成。
- 本模板不表示真实测量已执行。
- 本模板不表示生产分支已打开。
- 本模板不表示 accepted、integrated 或 production_ready。
