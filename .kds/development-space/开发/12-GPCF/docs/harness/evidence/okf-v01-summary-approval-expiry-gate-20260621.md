---
doc_id: GPCF-DOC-82F7D65D59
title: OKF v0.1 Summary Approval Expiry Gate
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
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Approval Expiry Gate

generated_at: 2026-10-12T07:07:19.521207+00:00

## Summary

| metric | value |
| --- | --- |
| status | pass |
| as_of | 2026-06-21 |
| max_pending_days | 14 |
| requests | 1 |
| json | `docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.json` |

## Requests

| request | status | age_days | reason |
| --- | --- | ---: | --- |
| `docs/harness/evidence/okf-v01-summary-approval-request-OKF-SUM-20260620-001.md` | active_pending | 1 | within_pending_review_window |

## Fixtures

| fixture | expected_status | actual_status | age_days | actual_reason | status |
| --- | --- | --- | ---: | --- | --- |
| expired_pending_request | expired_blocked | expired_blocked | 22 | pending_request_expired | pass |

## Boundary

- This gate validates pending approval request freshness only.
- It does not approve summaries.
- It does not modify OKF concepts.
- Expired pending requests must be recreated or explicitly re-confirmed before ledger update.
