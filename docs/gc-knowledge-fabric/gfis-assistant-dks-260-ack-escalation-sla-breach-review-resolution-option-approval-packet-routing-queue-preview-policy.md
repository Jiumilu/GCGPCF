---
doc_id: GPCF-DOC-3EBE1B7048
title: GFIS Assistant DKS-260 摘要投递确认升级 SLA 违约审阅处置选项审批包路由队列预览策略
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-260 摘要投递确认升级 SLA 违约审阅处置选项审批包路由队列预览策略

## 定位

本文件定义 DKS-260 routing queue preview。它从 DKS-259 approval packet preview 派生，只展示候选 queue slot、queue priority、candidate assignee、required evidence、queue reason、阻断数量、边界和下一步建议。

## 上游输入

- `gfis-assistant-dks-259-ack-escalation-sla-breach-review-resolution-option-approval-packet-preview`

## 硬边界

DKS-260 不创建 routing queue、queue item、approval assignment、approval lock、approval packet、approval request、approval decision、committee decision、freeze action、WAES gate result、KWE work item、Harness evidence、KDS lifecycle 或任何业务写回。

## 验证

- Validator: `scripts/gfis/validate_gfis_assistant_dks_260_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_preview.py`
- Fixture: `fixtures/gfis/gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-dry-run.json`
- OKF: `okf/gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.yaml`
