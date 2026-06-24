---
doc_id: GPCF-DOC-87A94990FE
title: 基础知识人工确认队列
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md
source_path: docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 基础知识人工确认队列

日期：2026-06-19

状态：`candidate_only`

This queue contains non-hard-stop writeback candidates that still require human confirmation before any downstream action.

## 概要

- evidence_id：`BKC-HUMAN-CONFIRMATION-QUEUE-20260619`
- source_evidence_id：`BKC-DRY-RUN-SUMMARY-20260618`
- source_round：`GPCF-KDS-DKS-044`
- current_round：`GPCF-KDS-DKS-045`
- queue_type：`human_confirmation`
- item_count：`4`

## 队列项目

| queue_item_id | source_candidate_id | base_knowledge_id | target | reason | decision_band | hard_stop | next_action | queue_status | write_authority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-DKS-044-001 | WBC-DKS-044-001 | BKC-HBLC-FEA-202606-0001 | evidencePassRate | evidence_level_below_reuse_threshold | repair_candidate | false | manual_source_and_gap_confirmation | candidate_only | none_dry_run_only |
| Q-DKS-044-002 | WBC-DKS-044-002 | BKC-HBLC-FEA-202606-0001 | automationEffectivenessRate | automation_not_effective_yet | repair_candidate | false | manual_source_and_gap_confirmation | candidate_only | none_dry_run_only |
| Q-DKS-044-003 | WBC-DKS-044-003 | BKC-HBLC-FEA-202606-0001 | writebackClosureRate | gap_writeback_not_closed | repair_candidate | false | manual_source_and_gap_confirmation | candidate_only | none_dry_run_only |
| Q-DKS-044-004 | WBC-DKS-044-004 | BKC-HBLC-IND-202606-0001 | writebackClosureRate | gap_writeback_not_closed | limited_report_candidate | false | manual_source_and_gap_confirmation | candidate_only | none_dry_run_only |

## 边界

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

## 控制

- Queue rows are candidate-only and do not confirm facts, close gaps, or write any system.
- No score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger write is performed.
- No real KDS API, WAES, GFIS, GPC, PVAOS, finance, settlement, or production write is performed.
- Committee rows are review candidates only; committee decision is not completed in this evidence.
