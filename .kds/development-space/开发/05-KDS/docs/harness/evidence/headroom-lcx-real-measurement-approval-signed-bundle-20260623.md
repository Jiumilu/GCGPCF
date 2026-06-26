---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623
title: Headroom LCX Real Measurement Approval Signed Bundle Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement Approval Signed Bundle Evidence

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623`

## 结论

这是一份已记录签字值的受控审批 bundle。它确认审批字段与签字区已经填入，但不打开真实测量窗口，不启动生产代理，不写真实 KDS 或外部 API。

## 计数

| item | value |
|---|---|
| project_count | 15 |
| required_field_count | 6 |
| required_signature_field_count | 6 |
| human_attestation_count | 7 |

## 输出

| artifact | path |
|---|---|
| signed approval bundle | `fixtures/headroom/headroom-lcx-real-measurement-approval-signed-bundle.json` |

## 签字值

| field | value |
|---|---|
| authorized_window_id | `LCX-MEASURE-20260623-001` |
| authorized_by | `lujunxiang / 总架构师` |
| authorized_at | `2026-06-23T14:30:00+08:00` |
| sanitized_production_token_ledger | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` |
| rollback_plan_id | `HEADROOM-LCX-ROLLBACK-PLAN-20260622-001` |
| waes_harness_admission_decision | `admitted_for_sanitized_measurement_precheck` |
| signer_name | `lujunxiang` |
| signer_role | `总架构师` |
| signed_at | `2026-06-23T14:30:00+08:00` |
| signature_method | `typed_approval` |
| signature_statement | `I approve opening the real measurement window under the stated precheck-only constraints.` |

## 门禁

| 项 | 当前值 |
|---|---|
| authorization_complete | true |
| real_measurement_window_open | false |
| production_token_measurement_allowed | false |
| production_proxy_started | false |
| production_sdk_enabled | false |
| production_external_api_write | false |
| kds_api_write | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 本 bundle 不表示生产授权完成。
- 本 bundle 不表示真实测量已执行。
- 本 bundle 不表示 accepted、integrated 或 production_ready。
