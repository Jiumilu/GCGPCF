---
doc_id: GPCF-DOC-7797BB4F55
title: 底座知识人工确认模板
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md
source_path: docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# 底座知识人工确认模板

日期：2026-06-19

状态：`blank_template_only`

本文件基于 DKS-046 人工确认 schema，为未来人工确认提供空白记录。

## 摘要

- template_id：`BKC-HUMAN-CONFIRMATION-TEMPLATE-20260619`
- source_schema_id：`BKC-HUMAN-CONFIRMATION-SCHEMA-20260619`
- source_queue_evidence_id：`BKC-HUMAN-CONFIRMATION-QUEUE-20260619`
- template_type：`human_confirmation_template`
- record_count：`4`

## 空白记录

| template_record_id | source_queue_item_id | source_candidate_id | template_status | downstream_allowed |
| --- | --- | --- | --- | --- |
| T-DKS-044-001 | Q-DKS-044-001 | WBC-DKS-044-001 | blank_template_only | false |
| T-DKS-044-002 | Q-DKS-044-002 | WBC-DKS-044-002 | blank_template_only | false |
| T-DKS-044-003 | Q-DKS-044-003 | WBC-DKS-044-003 | blank_template_only | false |
| T-DKS-044-004 | Q-DKS-044-004 | WBC-DKS-044-004 | blank_template_only | false |

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
