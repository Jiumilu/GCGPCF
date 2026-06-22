---
doc_id: GPCF-DOC-B30625918B
title: 底座知识委员会审查队列
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
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 底座知识委员会审查队列

日期：2026-06-19

状态：`candidate_only`

本队列包含硬停止写回候选；任何下游动作前都必须先完成委员会审查。

## 摘要

- evidence_id：`BKC-COMMITTEE-REVIEW-QUEUE-20260619`
- source_evidence_id：`BKC-DRY-RUN-SUMMARY-20260618`
- source_round：`GPCF-KDS-DKS-044`
- current_round：`GPCF-KDS-DKS-045`
- queue_type：`committee_review`
- item_count：`10`

## 队列项

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
