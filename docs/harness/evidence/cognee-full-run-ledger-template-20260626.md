---
doc_id: GPCF-DOC-41D9B30C5E
title: Cognee 全量运行账本模板 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-full-run-ledger-template-20260626.md
source_path: docs/harness/evidence/cognee-full-run-ledger-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 全量运行账本模板 2026-06-26

## 1. 当前结论

`cognee_full_run_ledger_template = prepared`

本文为 Cognee full-run 候选阶段建立可审计账本模板。当前账本状态为 `template_only`，不表示全量运行已经发生。

## 2. 模板文件

- JSON: `fixtures/cognee/cognee-full-run-ledger-template.json`
- validator: `tools/kds-sync/validate_cognee_full_run_ledger_template.py`
- source admission package: `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`

## 3. 账本字段

| field | current_value |
|---|---|
| `ledger_id` | `COGNEE-FULL-RUN-LEDGER-YYYYMMDD-NNN` |
| `ledger_scope` | `cognee_full_run_candidate` |
| `source_external_execution_receipt` | `REQUIRED_REAL_EXTERNAL_EXECUTION_RECEIPT` |
| `batch_count` | `0` |
| `record_count` | `0` |
| `successful_record_count` | `0` |
| `failed_record_count` | `0` |
| `excluded_record_count` | `0` |
| `full_run_ledger_status` | `template_only` |

## 4. 账本成立条件

| item | requirement |
|---|---|
| external execution receipt | 必须是真实外部执行回执，不接受样例回执 |
| object coverage | 必须连接全量对象覆盖 evidence |
| scenario coverage | 必须连接全量场景覆盖 evidence |
| batch records | 每个 batch 必须有真实 `execution_receipt_id`、时间、计数和 operator note |
| exception records | 失败、排除和回滚必须有可审计记录 |

## 5. 状态边界

| field | value |
|---|---|
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 6. 非声明

- 不声明账本模板等于真实账本
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
