---
doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTHORIZATION-NEGATIVE-FIXTURES-20260626
title: Agent-Reach P9S Source Direct Authorization Negative Fixtures 2026-06-26
project: KDS
related_projects: [GFIS, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md
source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Agent-Reach P9S Source Direct Authorization Negative Fixtures 2026-06-26

- status: `p9_source_direct_authorization_negative_fixtures_pass`
- negative_case_count: `8`
- live_external_fetch_invoked: `False`
- completion_claim_allowed: `False`

## Negative Cases

- `expired_authorization` -> `authorization_expired`
- `method_out_of_scope` -> `allowed_methods_mismatch`
- `page_limit_too_high` -> `max_pages_per_entrypoint_mismatch`
- `target_limit_too_high` -> `max_targets_mismatch`
- `write_scope_not_evidence_only` -> `write_scope_not_evidence_only`
- `forbidden_action_missing` -> `forbidden_actions_missing`
- `redaction_missing` -> `redaction_not_true:redact_cookies`
- `required_field_missing` -> `authorization_missing_fields:authorized_by`

## Boundary

- This evidence validates negative authorization fixtures only.
- This evidence does not invoke live target-site fetch.
- This evidence does not write KDS canonical Markdown.
- This evidence does not write GFIS source-of-record.
- This evidence does not claim accepted, integrated, or production_ready status.
