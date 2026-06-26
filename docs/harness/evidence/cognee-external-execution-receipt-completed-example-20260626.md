---
doc_id: GPCF-DOC-DA2F4BB221
title: Cognee 外部执行回执 completed 样例 2026-06-26
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-external-execution-receipt-completed-example-20260626.md
source_path: docs/harness/evidence/cognee-external-execution-receipt-completed-example-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 外部执行回执 completed 样例 2026-06-26

## 1. 当前结论

`cognee_external_execution_receipt_completed_example = prepared`

本文只提供 completed 回执样例，用于真实外部执行发生后对齐字段与格式。它不是实际执行回执，不证明外部执行已经发生。

## 2. 样例来源

- receipt JSON: `fixtures/cognee/cognee-external-execution-receipt.completed.example.json`
- linked intake: `fixtures/cognee/cognee-external-execution-integration-intake.pending.json`

## 3. 样例字段

| field | value |
|---|---|
| `receipt_id` | `COGNEE-EXT-RECEIPT-20260626-001` |
| `execution_entry_id` | `COGNEE-EXT-ENTRY-20260626-001` |
| `execution_target` | `cognee_self_hosted_validation_gateway_staging` |
| `execution_owner` | `lujunxiang` |
| `authorized_at` | `2026-06-26T10:15:00+08:00` |
| `executed_at` | `2026-06-26T10:42:00+08:00` |
| `record_count` | `5` |
| `execution_count` | `5` |
| `error_count` | `0` |
| `rollback_triggered` | `false` |
| `sample_only` | `true` |

## 4. 受控边界

| field | value |
|---|---|
| `sample_boundary` | `completed_example_only_not_actual_execution_receipt` |
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |

## 5. 非声明

- 不声明该样例等于真实执行回执
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
