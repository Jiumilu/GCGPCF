---
doc_id: GPCF-DOC-87A94990FE
title: 底座知识人工确认队列
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
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# 底座知识人工确认队列

日期：2026-06-19

状态：`candidate_only`

本队列包含非硬停止写回候选；任何下游动作前仍需人工确认。

## 摘要

- evidence_id：`BKC-HUMAN-CONFIRMATION-QUEUE-20260619`
- source_evidence_id：`BKC-DRY-RUN-SUMMARY-20260618`
- source_round：`GPCF-KDS-DKS-044`
- current_round：`GPCF-KDS-DKS-045`
- queue_type：`human_confirmation`
- item_count：`4`

## 队列项

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

## 控制边界

- 队列行均为 candidate-only，不确认事实、不关闭缺口、不写入任何系统。
- 本轮不执行积分结算、收益分配、悬赏发布、RAG 准入、指挥舱强引用或业务台账写入。
- 本轮不执行真实 KDS API、WAES、GFIS、GPC、PVAOS、财务、结算或生产写入。
- 委员会行仅为审查候选；本证据不完成委员会决议。
