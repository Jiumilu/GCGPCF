---
doc_id: GPCF-DOC-B30625918B
title: Base Knowledge Committee Review Queue
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md
source_path: docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Base Knowledge Committee Review Queue

日期：2026-06-19

状态：`candidate_only`

This queue contains hard-stop writeback candidates that require committee review before any downstream action.

## Summary

- evidence_id：`BKC-COMMITTEE-REVIEW-QUEUE-20260619`
- source_evidence_id：`BKC-DRY-RUN-SUMMARY-20260618`
- source_round：`GPCF-KDS-DKS-044`
- current_round：`GPCF-KDS-DKS-045`
- queue_type：`committee_review`
- item_count：`10`

## Queue Items

| queue_item_id | source_candidate_id | base_knowledge_id | target | reason | decision_band | hard_stop | next_action | queue_status | write_authority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-DKS-044-005 | WBC-DKS-044-005 | BKC-HBLC-ORD-202606-0001 | sourceRefs | source_refs_missing | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-006 | WBC-DKS-044-006 | BKC-HBLC-ORD-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-007 | WBC-DKS-044-007 | BKC-HBLC-ORD-202606-0001 | writebackClosureRate | gap_writeback_not_closed | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-008 | WBC-DKS-044-008 | BKC-HBLC-ORD-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-009 | WBC-DKS-044-009 | BKC-HBLC-ORD-202606-0002 | writebackClosureRate | gap_writeback_not_closed | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-010 | WBC-DKS-044-010 | BKC-HBLC-FEA-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-011 | WBC-DKS-044-011 | BKC-HBLC-FEA-202606-0002 | automationEffectivenessRate | automation_not_effective_yet | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-012 | WBC-DKS-044-012 | BKC-HBLC-FEA-202606-0002 | writebackClosureRate | gap_writeback_not_closed | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-013 | WBC-DKS-044-013 | BKC-HBLC-LEDGER-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| Q-DKS-044-014 | WBC-DKS-044-014 | BKC-HBLC-LEDGER-202606-0001 | writebackClosureRate | gap_writeback_not_closed | blocked_or_invalid | true | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |

## Boundary

| boundary | value |
| --- | --- |
| realKdsApiWrite | false |
| waesWrite | false |
| businessLedgerWrite | false |
| settlementWrite | false |
| ragAdmission | false |
| scoreSettlement | false |
| revenueAllocation | false |
| bountyPublication | false |
| committeeDecisionCompleted | false |

## Controls

- Queue rows are candidate-only and do not confirm facts, close gaps, or write any system.
- No score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger write is performed.
- No real KDS API, WAES, GFIS, GPC, PVAOS, finance, settlement, or production write is performed.
- Committee rows are review candidates only; committee decision is not completed in this evidence.
