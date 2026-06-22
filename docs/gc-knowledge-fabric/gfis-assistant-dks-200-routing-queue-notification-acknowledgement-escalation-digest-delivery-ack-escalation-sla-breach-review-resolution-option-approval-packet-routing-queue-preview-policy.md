---
doc_id: GPCF-DOC-34D70D18D2
title: GFIS Assistant DKS-200 Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-200-routing-queue-notification-acknowledgement-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-200-routing-queue-notification-acknowledgement-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-200 Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Preview No-write 规则

## 目标

本规则定义 DKS-200 的 GFIS Assistant approval packet routing queue preview。它只把 DKS-199 的 approval packet preview 转成可审阅的候选路由队列视图，用于 Brain、PKC 与 GFIS Assistant 展示候选队列槽位、候选处理人、所需证据、路由原因与阻断路由数量。

## 输入

- DKS-199 approval packet preview fixture。
- DKS-198 resolution option preview 引用。
- DKS-197 SLA breach review preview 引用。
- WAES/KWE/GFIS no-write 契约。

## 输出

- `routingQueuePreviewId`：本地候选路由队列预览编号。
- `approvalPacketPreviewRefs`：来源 approval packet preview。
- `routingQueueSlot` / `routingQueuePriority`：候选队列槽位与优先级。
- `candidateAssigneeRefs`：候选处理人引用。
- `queueReasonRefs`：候选入队原因。
- `blockedRouteCount`：阻断路由数量。
- `blockedActions` 与 `noWrite`：必须阻断的创建、写入、确认与状态提升动作。

## 硬边界

DKS-200 不创建真实 routing queue、queue item、approval assignment、approval lock、approval packet、approval request、approval decision、committee decision、freeze action、Harness evidence、WAES result 或 KWE work item。

DKS-200 不写入 GFIS/GPC/ERP/MES，不提升 KDS lifecycle，不生成 accepted fact，不调用外部 API。

## 验证

专项验证脚本：

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_200_routing_queue_notification_acknowledgement_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_preview.py
```

验收口径：

- `routing_queues=6`。
- `brain=2`、`pkc=1`、`gfis_assistant=3`。
- `creates_*` 全部为 `0`。
- `writes_*` 全部为 `0`。
