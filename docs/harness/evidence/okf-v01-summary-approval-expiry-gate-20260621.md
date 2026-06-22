---
doc_id: GPCF-DOC-82F7D65D59
title: OKF v0.1 摘要批准过期门禁
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md
source_path: docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# OKF v0.1 摘要批准过期门禁

generated_at: 2026-06-22T01:58:00.189676+00:00

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| as_of | 2026-06-21 |
| max_pending_days | 14 |
| requests | 1 |
| json | `docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.json` |

## 请求

| request | status | age_days | reason |
| --- | --- | ---: | --- |
| `docs/harness/evidence/okf-v01-summary-approval-request-OKF-SUM-20260620-001.md` | active_pending | 1 | within_pending_review_window |

## Fixtures

| fixture | expected_status | actual_status | age_days | actual_reason | status |
| --- | --- | --- | ---: | --- | --- |
| expired_pending_request | expired_blocked | expired_blocked | 22 | pending_request_expired | pass |

## 边界

- 本 gate 只验证 pending approval request 的时效性。
- 它不批准摘要。
- 它不修改 OKF concepts。
- 过期的 pending requests 必须重新创建，或在 ledger 更新前被明确重新确认。
