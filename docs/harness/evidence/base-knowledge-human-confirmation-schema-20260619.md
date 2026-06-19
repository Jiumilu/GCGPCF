---
doc_id: GPCF-DOC-9C22552EEE
title: Base Knowledge Human Confirmation Schema
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md
source_path: docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Base Knowledge Human Confirmation Schema

日期：2026-06-19

状态：`schema_dry_run_only`

This schema defines the fields required for future manual confirmation of non-hard-stop base knowledge candidates.

## Summary

- schema_id：`BKC-HUMAN-CONFIRMATION-SCHEMA-20260619`
- source_queue_evidence_id：`BKC-HUMAN-CONFIRMATION-QUEUE-20260619`
- source_queue_type：`human_confirmation`
- source_queue_item_count：`4`
- field_count：`13`
- required_field_count：`12`

## Fields

| field | type | required | enum | description |
| --- | --- | --- | --- | --- |
| queueItemId | string | true | - | 确认记录绑定的候选队列项 ID。 |
| sourceCandidateId | string | true | - | 来自 DKS-044 的写回候选 ID。 |
| baseKnowledgeId | string | true | - | 底座知识对象 ID。 |
| confirmingUnit | string | true | - | 执行确认的人员或单位。 |
| confirmerRole | string | true | source_owner, project_owner, kds_operator, waes_reviewer, other_authorized | 确认人角色。 |
| sourceRefsReviewed | array | true | - | 已核验的来源、证据或台账引用。 |
| factStatus | string | true | confirmed, partially_confirmed, rejected, more_evidence_required | 候选事实状态。 |
| gapClosureOpinion | string | true | keep_open, ready_for_committee, ready_for_writeback_candidate, reject_candidate | 缺口处理意见。 |
| evidenceLevelAfterReview | string | true | L0_unknown, L1_claim, L2_documented, L3_verified, L4_authoritative | 复核后的证据等级。 |
| sensitiveDataCheck | string | true | clear, masked, contains_sensitive_needs_redaction | 敏感数据处理结果。 |
| ragAdmissionOpinion | string | true | not_allowed, limited_report_only, candidate_after_more_evidence | RAG 准入意见。 |
| nextAction | string | true | request_more_evidence, submit_to_committee, prepare_writeback_candidate, close_as_rejected | 下一步动作。 |
| reviewNotes | string | false | - | 人工确认说明。 |

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
