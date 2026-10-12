---
doc_id: GPCF-DOC-E9D4362ECF
title: OKF v0.1 Summary Approval Negative Fixtures
project: KDS
related_projects: [GPCF, KDS, WAME]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
source_path: docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Approval Negative Fixtures

generated_at: 2026-10-12T06:31:26.532973+00:00

## Summary

| metric | value |
| --- | --- |
| status | pass |
| fixtures | 4 |
| json | `docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.json` |

## Results

| fixture | expected_status | actual_status | actual_reason | status |
| --- | --- | --- | --- | --- |
| missing_required_fields | fail | fail | missing_fields:source_path,kds_path,requested_summary_scope,confirmer,confirmation_date,owner_approval,sensitivity_review,approved_summary_scope | pass |
| partial_confirmation | fail | fail | partial_confirmation:sensitivity_review,approved_summary_scope | pass |
| sensitivity_not_pass | fail | fail | sensitivity_review_not_pass | pass |
| pending_request_allowed | pending_review | pending_review | awaiting_human_confirmation | pass |

## Boundary

- These fixtures validate the approval-request gate only.
- They do not approve summaries.
- They do not modify OKF concepts.
- Temporary files are used only during validation.
