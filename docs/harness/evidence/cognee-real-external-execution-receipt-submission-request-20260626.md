---
doc_id: GPCF-DOC-8F9F2F5A0D
title: Cognee 真实外部执行回执提交请求包 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-real-external-execution-receipt-submission-request-20260626.md
source_path: docs/harness/evidence/cognee-real-external-execution-receipt-submission-request-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 真实外部执行回执提交请求包 2026-06-26

## 1. 当前结论

`cognee_real_external_execution_receipt_submission_request = requested_pending_real_receipt`

本文向 `external_execution_operator` 固化真实外部执行回执提交要求。当前只是提交请求，不表示真实回执已经收到。

## 2. 请求文件

- JSON: `fixtures/cognee/cognee-real-external-execution-receipt-submission-request.json`
- validator: `tools/kds-sync/validate_cognee_real_external_execution_receipt_submission_request.py`
- source responsibility assignment: `docs/harness/evidence/cognee-real-external-execution-receipt-responsibility-assignment-20260626.md`
- source receipt intake: `docs/harness/evidence/cognee-real-external-execution-receipt-intake-20260626.md`

## 3. 必交材料

| artifact_id | description | required |
|---|---|---|
| `REAL_RECEIPT_REF` | `path_or_identifier_of_real_external_execution_receipt` | `true` |
| `REAL_RECEIPT_ID` | `unique_receipt_id_from_external_execution` | `true` |
| `EXECUTED_AT` | `real_execution_timestamp` | `true` |
| `EXECUTION_COUNTS` | `record_count_execution_count_error_count` | `true` |
| `ROLLBACK_STATUS` | `rollback_triggered_and_rollback_evidence_if_any` | `true` |
| `OPERATOR_NOTE` | `plain_summary_from_execution_operator` | `true` |

## 4. 禁止材料

| artifact | reason |
|---|---|
| `fixtures/cognee/cognee-external-execution-receipt.completed.example.json` | 样例不是实际回执 |
| `docs/harness/evidence/cognee-external-execution-receipt-completed-example-20260626.md` | 样例 evidence 不能关闭 GAP-001 |
| `template_only_receipt` | 模板不能替代真实执行 |
| `screenshot_without_receipt_fields` | 截图不能替代结构化回执字段 |

## 5. 状态边界

| field | value |
|---|---|
| `submission_status` | `requested_pending_real_receipt` |
| `gap_001_ready` | `false` |
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 6. 非声明

- 不声明真实回执已经收到
- 不声明 GAP-001 已关闭
- 不声明 readiness 已变为 ready
- 不声明 `Cognee 已全量运行`
