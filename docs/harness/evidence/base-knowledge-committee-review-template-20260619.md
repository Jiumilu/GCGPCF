---
doc_id: GPCF-DOC-8066745911
title: 底座知识委员会审查模板
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-committee-review-template-20260619.md
source_path: docs/harness/evidence/base-knowledge-committee-review-template-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 底座知识委员会审查模板

日期：2026-06-19

状态：`blank_template_only`

本文件基于 DKS-046 委员会审查 schema，为未来委员会审查提供空白记录。

## 摘要

- template_id：`BKC-COMMITTEE-REVIEW-TEMPLATE-20260619`
- source_schema_id：`BKC-COMMITTEE-REVIEW-SCHEMA-20260619`
- source_queue_evidence_id：`BKC-COMMITTEE-REVIEW-QUEUE-20260619`
- template_type：`committee_review_template`
- record_count：`10`

## 空白记录

| template_record_id | source_queue_item_id | source_candidate_id | template_status | downstream_allowed |
| --- | --- | --- | --- | --- |
| T-DKS-044-005 | Q-DKS-044-005 | WBC-DKS-044-005 | blank_template_only | false |
| T-DKS-044-006 | Q-DKS-044-006 | WBC-DKS-044-006 | blank_template_only | false |
| T-DKS-044-007 | Q-DKS-044-007 | WBC-DKS-044-007 | blank_template_only | false |
| T-DKS-044-008 | Q-DKS-044-008 | WBC-DKS-044-008 | blank_template_only | false |
| T-DKS-044-009 | Q-DKS-044-009 | WBC-DKS-044-009 | blank_template_only | false |
| T-DKS-044-010 | Q-DKS-044-010 | WBC-DKS-044-010 | blank_template_only | false |
| T-DKS-044-011 | Q-DKS-044-011 | WBC-DKS-044-011 | blank_template_only | false |
| T-DKS-044-012 | Q-DKS-044-012 | WBC-DKS-044-012 | blank_template_only | false |
| T-DKS-044-013 | Q-DKS-044-013 | WBC-DKS-044-013 | blank_template_only | false |
| T-DKS-044-014 | Q-DKS-044-014 | WBC-DKS-044-014 | blank_template_only | false |

## 控制边界

| control | value |
| --- | --- |
| blankTemplateOnly | true |
| createsConfirmationFact | false |
| createsCommitteeDecision | false |
| realKdsApiWrite | false |
| waesWrite | false |
| businessLedgerWrite | false |
| settlementWrite | false |
| ragAdmission | false |
| acceptedOrIntegratedUpgrade | false |

## 边界

- 空白记录仅为模板，不包含真实确认或委员会决议。
- 预填身份字段仅用于保留到来源候选的可追溯性。
- 本轮不执行真实 KDS API、WAES、GFIS、GPC、PVAOS、财务、结算、RAG 准入或生产写入。
- 未来填报记录需要单独受控证据以及人工或委员会动作。
