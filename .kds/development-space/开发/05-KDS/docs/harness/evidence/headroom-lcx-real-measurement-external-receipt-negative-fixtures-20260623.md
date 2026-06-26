---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623
title: Headroom LCX Real Measurement External Receipt Negative Fixtures
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement External Receipt Negative Fixtures

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623`

## 当前结论

`negative_fixtures_ready_no_completed_receipt_recorded`

本轮只生成 completed receipt 负向 fixtures，不生成正式 completed receipt，不打开真实测量窗口。

## 负向样本

| case_id | mutated_field | expected_result |
|---|---|---|
| production_proxy_started_true | `production_proxy_started` | `reject` |
| production_sdk_enabled_true | `production_sdk_enabled` | `reject` |
| real_kds_write_true | `real_kds_write` | `reject` |
| external_api_write_true | `external_api_write` | `reject` |
| database_migration_true | `database_migration` | `reject` |
| permission_change_true | `permission_change` | `reject` |
| accepted_true | `accepted` | `reject` |
| integrated_true | `integrated` | `reject` |
| production_ready_true | `production_ready` | `reject` |
| telemetry_on | `telemetry` | `reject` |
| sensitive_material_attestation_unverified | `sensitive_material_attestation` | `reject` |

## 计数

| item | value |
|---|---|
| fixture_count | `11` |
| expected_rejected_count | `11` |
| expected_accepted_count | `0` |

## 执行前判定

| item | value |
|---|---|
| completed_receipt_instance_created | `false` |
| can_open_real_measurement | `false` |
| real_measurement_open | `false` |
| measured_production_tokens | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 不声明正式外部回执已经记录。
- 不声明真实测量已经执行。
- 不声明生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。
- 不声明 accepted、integrated 或 production_ready。
