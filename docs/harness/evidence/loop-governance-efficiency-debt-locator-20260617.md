---
doc_id: GPCF-DOC-7FB5D5F117
title: Loop Governance Efficiency Debt Locator Evidence
project: GPCF
related_projects: [GPCF, GFIS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md
source_path: docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Governance Efficiency Debt Locator Evidence

Evidence ID: `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`

This evidence locates the concrete audit-window round records behind `LEDB-001`
and `LEDB-002`.

`total_rounds` is an observed baseline. Forward drift is allowed only when the
affected record lists still match the current audit window and the hard window
remains clean.

## Source Signal

```text
loop_round_efficiency_audit=pass total_rounds=335 audit_checked=30 hard_checked=5 audit_missing_truth_fields=0 audit_missing_five_segment=0 audit_batch_generated_counted=0 hard_missing_truth_fields=0 hard_missing_five_segment=0 hard_batch_generated_counted=0 duplicate_fingerprint_groups=0 high_similarity_adjacent_pairs=0 max_consecutive_sequence=186 risk=review_required
```

## Locator Summary

| Backlog Item | Located Count | Rule |
|---|---:|---|
| LEDB-001 | 0 | Missing one or more truth fields |
| LEDB-002 | 0 | Missing one or more five-part round markers |

## LEDB-001 Affected Rounds

| Round | Missing Fields |
|---|---|
| - | - |

## LEDB-002 Affected Rounds

| Round | Missing Segments |
|---|---|
| - | - |

## Non-Claims

- This locator does not rewrite historical round records.
- This locator does not prove GFIS runtime SOP E2E passed.
- This locator does not create source-of-record, runtime primary key, review
  queue, runtime intake, WAES review, verified artifact, accepted, or
  integrated status.
- This locator does not authorize production write, external API write, schema
  sync, bench migrate, deployment, permission change, commit, or push.
