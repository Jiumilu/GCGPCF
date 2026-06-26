---
doc_id: GPCF-DOC-3A8D1D4E72
title: Cognee 外部执行回执正式模板 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-external-execution-receipt-template-20260626.md
source_path: docs/harness/evidence/cognee-external-execution-receipt-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 外部执行回执正式模板 2026-06-26

## 1. 当前结论

`cognee_external_execution_receipt_template = prepared`

本文提供 Cognee 外部执行验证完成后的正式回执模板。它只定义真实执行完成后应当回填的字段，不代表外部执行已经发生。

## 2. 正式回执模板

| field | template_value | note |
|---|---|---|
| `receipt_id` | `COGNEE-EXT-RECEIPT-YYYYMMDD-NNN` | 唯一回执编号 |
| `execution_entry_id` | `COGNEE-EXT-ENTRY-20260626-001` | 对应 intake entry |
| `execution_scope` | `cognee_p4_external_execution_validation_only` | 固定范围 |
| `execution_target` | `cognee_self_hosted_validation_gateway_staging` | 与 intake 保持一致 |
| `execution_owner` | `lujunxiang` | 与 intake 保持一致 |
| `authorized_by` | `lujunxiang / WAES Duty Reviewer` | 来源于 LIVE-002 签核 |
| `authorized_at` | `2026-06-26T10:15:00+08:00` | 来源于签核完成时间 |
| `executed_at` | `REQUIRED_REAL_TIMESTAMP` | 真实执行完成时间 |
| `record_count` | `5` | 当前最小验证批次 |
| `execution_count` | `REQUIRED_REAL_INTEGER` | 实际执行条数 |
| `error_count` | `REQUIRED_REAL_INTEGER` | 实际错误数 |
| `rollback_triggered` | `REQUIRED_REAL_BOOLEAN` | 是否触发回滚 |
| `rollback_evidence` | `REQUIRED_IF_ROLLBACK_TRIGGERED` | 回滚触发时必填 |
| `operator_note` | `REQUIRED_REAL_OPERATOR_NOTE` | 真实执行摘要 |

## 3. 回执成立条件

| item | requirement |
|---|---|
| signoff | `pass_complete` |
| live rehearsal | `pass` |
| intake | `pass_complete` |
| executed_at | 必须落在授权窗口内 |
| execution_count | 默认应等于 `record_count=5`，偏差需解释 |
| error_count | 默认目标 `0`，非 0 必须附带处置说明 |

## 4. 状态边界

| field | value |
|---|---|
| `production_write` | `false_until_independent_production_receipt_exists` |
| `accepted` | `false_until_harness_acceptance` |
| `integrated` | `false_until_waes_integration_decision` |
| `production_ready` | `false_until_full_run_gate_closure` |

## 5. 非声明

- 不声明模板等于真实回执
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
