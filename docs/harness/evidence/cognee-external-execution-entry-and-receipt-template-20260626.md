---
doc_id: GPCF-DOC-8C7F2F6006
title: Cognee 外部执行入口与回执模板 2026-06-26
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-external-execution-entry-and-receipt-template-20260626.md
source_path: docs/harness/evidence/cognee-external-execution-entry-and-receipt-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 外部执行入口与回执模板 2026-06-26

## 1. 外部执行入口定义

| item | value |
|---|---|
| execution_entry_id | `COGNEE-EXT-ENTRY-20260626-001` |
| execution_scope | `cognee_p4_external_execution_validation_only` |
| trigger_precondition | `authorization_complete=true` |
| required_precheck | `cognee_p4_real_writeback_live_output=pass` |
| required_command_pack | `LIVE-002 fixed command pack` |
| failure_exit | `stop_external_execution_and_revert_to_precheck_004` |
| full_run_claim_allowed | `false` |

## 2. 执行前命令

```bash
python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py \
  --require-complete-signoff

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

## 3. 最小外部执行回执模板

| field | required_value_or_rule |
|---|---|
| `receipt_id` | `COGNEE-EXT-RECEIPT-<YYYYMMDD>-<NNN>` |
| `execution_entry_id` | `COGNEE-EXT-ENTRY-20260626-001` |
| `authorized_by` | 必须来自 LIVE-002 签核结果 |
| `authorized_at` | 必须来自 LIVE-002 签核窗口内时间 |
| `executed_at` | 真实执行时间 |
| `execution_target` | 外部执行层或外部写入适配层标识 |
| `record_count` | 至少记录本次批次涉及条数 |
| `execution_count` | 至少记录本次真实执行条数 |
| `error_count` | 失败数，允许为 `0` |
| `rollback_triggered` | `true` 或 `false` |
| `rollback_evidence` | 若触发回滚则必须提供 |
| `forbidden_claims` | 必须保留 `accepted/integrated/production_ready/full_run` 禁止声明 |

## 4. 监控基线

| metric | baseline |
|---|---|
| `record_count` | `5` |
| `execution_count` | `5` |
| `live_execution_ready_rate` | `1.0` |
| `error_count` | `0` 作为目标值 |
| `rollback_triggered` | 默认 `false`，若为 `true` 必须附回滚证据 |

## 5. 回滚入口

| item | value |
|---|---|
| rollback_entry | `return_to_GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004` |
| rollback_condition | `signature_conflict or external_execution_failure or evidence_mismatch` |
| rollback_result | `authorization_complete remains true but execution result invalidated for production admission` |
| rollback_claim_boundary | `does_not_upgrade accepted integrated production_ready full_run` |

## 6. 禁止声明

- 不声明 `Cognee 已全量运行`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
