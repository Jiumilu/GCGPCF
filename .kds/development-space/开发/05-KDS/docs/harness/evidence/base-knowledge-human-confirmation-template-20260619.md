---
doc_id: GPCF-DOC-7797BB4F55
title: 基础知识人工确认模板
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
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 基础知识人工确认模板

日期：2026-06-19

状态：`blank_template_only`

本文件基于 DKS-046 人工确认模式，提供未来人工确认所需的空白记录模板。

## 概要

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

## 控制项

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

- 空白记录仅作模板，不包含真实的确认或委员会决策。
- 预填身份字段仅保留与来源候选人的可追溯链路。
- 不会执行真实 KDS API、WAES、GFIS、GPC、PVAOS、财务入账、清算、RAG 入场或生产写入。
- 未来填充记录需另行提供受控证据并由人工或委员会处理。
