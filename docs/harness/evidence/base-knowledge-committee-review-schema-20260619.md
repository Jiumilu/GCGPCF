---
doc_id: GPCF-DOC-F861799E08
title: Base Knowledge Committee Review Schema
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
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Base Knowledge Committee Review Schema

日期：2026-06-19

状态：`schema_dry_run_only`

This schema defines the fields required for future committee review of hard-stop base knowledge candidates.

## Summary

- schema_id：`BKC-COMMITTEE-REVIEW-SCHEMA-20260619`
- source_queue_evidence_id：`BKC-COMMITTEE-REVIEW-QUEUE-20260619`
- source_queue_type：`committee_review`
- source_queue_item_count：`10`
- field_count：`15`
- required_field_count：`14`

## Fields

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

## Controls

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

## Boundary

- This file defines schema only and does not create human confirmation facts.
- This file defines schema only and does not create committee decisions.
- No real KDS API, WAES, GFIS, GPC, PVAOS, finance, settlement, RAG admission, or production write is performed.
- Any future use of this schema still requires explicit human or committee action and a separate controlled evidence record.
