---
doc_id: GPCF-DOC-CF3A246F25
title: 基础知识闭环评分试运行汇总
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md
source_path: docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 基础知识闭环评分试运行汇总

日期：2026-06-18

状态：`dry_run_evidence_only`

## 概要

- evidence_id：`BKC-DRY-RUN-SUMMARY-20260618`
- source_round：`GPCF-KDS-DKS-044`
- fixture_count：`6`
- expected_hard_stops：`4`
- writeback_candidate_count：`14`

## 决策分档

| decision_band | count |
| --- | --- |
| blocked_or_invalid | 4 |
| limited_report_candidate | 1 |
| repair_candidate | 1 |

## 边界

| boundary | value |
| --- | --- |
| realKdsApiWrite | false |
| waesWrite | false |
| businessLedgerWrite | false |
| settlementWrite | false |
| ragAdmission | false |

## 写回候选预览

| candidate_id | fixture_id | base_knowledge_id | target | reason | candidate_status | decision_band | hard_stop | write_authority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WBC-DKS-044-001 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | repair_candidate | false | none_dry_run_only |
| WBC-DKS-044-002 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | automationEffectivenessRate | automation_not_effective_yet | candidate_only | repair_candidate | false | none_dry_run_only |
| WBC-DKS-044-003 | FIX-BKC-REPAIR-001 | BKC-HBLC-FEA-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | repair_candidate | false | none_dry_run_only |
| WBC-DKS-044-004 | FIX-BKC-LIMITED-001 | BKC-HBLC-IND-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | limited_report_candidate | false | none_dry_run_only |
| WBC-DKS-044-005 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | sourceRefs | source_refs_missing | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-006 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-007 | FIX-BKC-BLOCK-001 | BKC-HBLC-ORD-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-008 | FIX-BKC-REVENUE-VETO-001 | BKC-HBLC-ORD-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-009 | FIX-BKC-REVENUE-VETO-001 | BKC-HBLC-ORD-202606-0002 | writebackClosureRate | gap_writeback_not_closed | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-010 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-011 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | automationEffectivenessRate | automation_not_effective_yet | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-012 | FIX-BKC-RAG-MISMATCH-001 | BKC-HBLC-FEA-202606-0002 | writebackClosureRate | gap_writeback_not_closed | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-013 | FIX-BKC-LEDGER-ORPHAN-001 | BKC-HBLC-LEDGER-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | candidate_only | blocked_or_invalid | true | none_dry_run_only |
| WBC-DKS-044-014 | FIX-BKC-LEDGER-ORPHAN-001 | BKC-HBLC-LEDGER-202606-0001 | writebackClosureRate | gap_writeback_not_closed | candidate_only | blocked_or_invalid | true | none_dry_run_only |

## 控制边界

- This evidence is generated from local fixtures only.
- All writeback rows are candidate-only and require manual or committee confirmation.
- No real KDS API, WAES write, GFIS/GPC/PVAOS business ledger write, RAG admission, settlement, bounty release, revenue allocation, or AI quota allocation is performed.
- Hard-stop rows remain blocked even when the calculated score is above a lower decision band.
