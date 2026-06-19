---
doc_id: GPCF-DOC-C13F879695
title: Base Knowledge Writeback Candidate Ledger
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md
source_path: docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Base Knowledge Writeback Candidate Ledger

日期：2026-06-18

状态：`candidate_only`

## Candidate Ledger

| candidate_id | fixture_id | base_knowledge_id | target | reason | candidate_status | required_confirmation | write_authority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WBC-DKS-044-001 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-002 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | automationEffectivenessRate | automation_not_effective_yet | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-003 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-004 | FIX-BKC-LIMITED-001 | BKC-HBLC-IND-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-005 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | sourceRefs | source_refs_missing | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-006 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-007 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-008 | FIX-BKC-REVENUE-VETO-001 | BKC-HBLC-ORD-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-009 | FIX-BKC-REVENUE-VETO-001 | BKC-HBLC-ORD-202606-0002 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-010 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-011 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | automationEffectivenessRate | automation_not_effective_yet | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-012 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-013 | FIX-BKC-LEDGER-ORPHAN-001 | BKC-HBLC-LEDGER-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | manual_or_committee_required | none_dry_run_only |
| WBC-DKS-044-014 | FIX-BKC-LEDGER-ORPHAN-001 | BKC-HBLC-LEDGER-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | manual_or_committee_required | none_dry_run_only |

## Controls

- Candidate rows do not close gaps.
- Candidate rows do not create score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger writes.
- Candidate rows must be confirmed by the proper human, KDS, WAES, or committee process before any downstream action.
