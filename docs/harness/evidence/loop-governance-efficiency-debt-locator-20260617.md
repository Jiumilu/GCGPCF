---
doc_id: GPCF-DOC-7FB5D5F117
title: Loop Governance Efficiency Debt Locator Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
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
loop_round_efficiency_audit=pass total_rounds=294 audit_checked=30 hard_checked=5 audit_missing_truth_fields=2 audit_missing_five_segment=18 audit_batch_generated_counted=0 hard_missing_truth_fields=0 hard_missing_five_segment=0 hard_batch_generated_counted=0 duplicate_fingerprint_groups=1 high_similarity_adjacent_pairs=3 max_consecutive_sequence=184 risk=review_required
```

## Locator Summary

| Backlog Item | Located Count | Rule |
|---|---:|---|
| LEDB-001 | 2 | Missing one or more truth fields |
| LEDB-002 | 18 | Missing one or more five-part round markers |

## LEDB-001 Affected Rounds

| Round | Missing Fields |
|---|---|
| `loop-round-GPCF-L4-GFIS-REPAIR-202.md` | declared_rounds, substantive_rounds, generated_items, batch_generated, substance_gate, stop_type |
| `loop-round-GPCF-L4-GFIS-REPAIR-203.md` | declared_rounds, substantive_rounds, generated_items, batch_generated, substance_gate, stop_type |

## LEDB-002 Affected Rounds

| Round | Missing Segments |
|---|---|
| `loop-round-GPCF-L4-GFIS-REPAIR-195.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-196.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-197.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-198.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-199.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-200.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-201.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-202.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-203.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-204.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-205.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-206.md` | action |
| `loop-round-GPCF-L4-GFIS-REPAIR-207.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-208.md` | action, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-209.md` | action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-210.md` | input, action, output, check, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-211.md` | input, action, feedback |
| `loop-round-GPCF-L4-GFIS-REPAIR-212.md` | action, check |

## Non-Claims

- This locator does not rewrite historical round records.
- This locator does not prove GFIS runtime SOP E2E passed.
- This locator does not create source-of-record, runtime primary key, review
  queue, runtime intake, WAES review, verified artifact, accepted, or
  integrated status.
- This locator does not authorize production write, external API write, schema
  sync, bench migrate, deployment, permission change, commit, or push.
