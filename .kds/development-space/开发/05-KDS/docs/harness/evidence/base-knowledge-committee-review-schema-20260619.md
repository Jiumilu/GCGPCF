---
doc_id: GPCF-DOC-F861799E08
title: 底座知识委员会审查 Schema
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md
source_path: docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 底座知识委员会审查 Schema

日期：2026-06-19

状态：`schema_dry_run_only`

本 schema 定义未来委员会审查硬停止底座知识候选所需字段。

## 摘要

- schema_id：`BKC-COMMITTEE-REVIEW-SCHEMA-20260619`
- source_queue_evidence_id：`BKC-COMMITTEE-REVIEW-QUEUE-20260619`
- source_queue_type：`committee_review`
- source_queue_item_count：`10`
- field_count：`15`
- required_field_count：`14`

## 字段

| field | type | required | enum | description |
| --- | --- | --- | --- | --- |
| queueItemId | string | true | - | 复核记录绑定的候选队列项 ID。 |
| sourceCandidateId | string | true | - | 来自 DKS-044 的写回候选 ID。 |
| baseKnowledgeId | string | true | - | 底座知识对象 ID。 |
| committeeSessionId | string | true | - | 委员会复核会议或批次 ID。 |
| committeeMembers | array | true | - | 参与复核成员清单。 |
| conflictOfInterestDeclared | boolean | true | - | 是否完成利益冲突申明。 |
| severity | string | true | general, major | 复核严重度。 |
| decisionMethod | string | true | majority_vote, chair_recorded_majority | 裁决方式。 |
| decision | string | true | reject, request_more_evidence, approve_repair_candidate, approve_penalty_candidate | 委员会裁决候选结果。 |
| scoreImpactCandidate | string | true | none, knowledge_only_adjustment, potential_value_adjustment, formal_value_adjustment, deduct_partial, deduct_full | 积分影响候选。 |
| revenuePoolImpactCandidate | string | true | none, record_potential_only, formal_income_after_receipt, exclude_self_purchased_quota | 收益池影响候选。 |
| writebackOpinion | string | true | do_not_write, candidate_after_human_confirmation, candidate_after_evidence_repair | 写回意见。 |
| appealAllowed | boolean | true | - | 是否允许申诉。 |
| filingRequired | boolean | true | - | 是否需要备案。 |
| reviewNotes | string | false | - | 委员会复核说明。 |

## 控制边界

| control | value |
| --- | --- |
| candidateOnly | true |
| createsConfirmationFact | false |
| createsCommitteeDecision | false |
| realKdsApiWrite | false |
| waesWrite | false |
| businessLedgerWrite | false |
| settlementWrite | false |
| ragAdmission | false |
| acceptedOrIntegratedUpgrade | false |

## 边界

- 本文件仅定义 schema，不创建人工确认事实。
- 本文件仅定义 schema，不创建委员会决议。
- 本轮不执行真实 KDS API、WAES、GFIS、GPC、PVAOS、财务、结算、RAG 准入或生产写入。
- 未来使用本 schema 仍需明确的人工或委员会动作，并形成单独受控证据记录。
