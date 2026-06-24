---
doc_id: GPCF-DOC-E9D4362ECF
title: OKF v0.1 摘要批准负向 fixtures 证据
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
source_path: docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# OKF v0.1 摘要批准负向 fixtures 证据

generated_at: 2026-06-22T01:41:15.779577+00:00

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| fixtures | 4 |
| json | `docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.json` |

## 结果

| fixture | expected_status | actual_status | actual_reason | status |
| --- | --- | --- | --- | --- |
| missing_required_fields | fail | fail | missing_fields:source_path,kds_path,requested_summary_scope,confirmer,confirmation_date,owner_approval,sensitivity_review,approved_summary_scope | pass |
| partial_confirmation | fail | fail | partial_confirmation:sensitivity_review,approved_summary_scope | pass |
| sensitivity_not_pass | fail | fail | sensitivity_review_not_pass | pass |
| pending_request_allowed | pending_review | pending_review | awaiting_human_confirmation | pass |

## 边界

- 这些 fixtures 只验证 approval-request gate。
- 它们不批准摘要。
- 它们不修改 OKF concepts。
- 临时文件仅在验证期间使用。
