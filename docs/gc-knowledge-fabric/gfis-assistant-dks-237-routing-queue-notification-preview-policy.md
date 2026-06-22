---
doc_id: GPCF-DOC-3464C6CC83
title: GFIS Assistant DKS-237 Routing Queue Notification Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-237-routing-queue-notification-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-237-routing-queue-notification-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-237 Routing Queue Notification Preview No-write 规则

## 定位

本文件定义 DKS-237 的本地 dry-run 预览规则。DKS-237 从 DKS-236 routing queue preview 派生，只展示候选通知类型、候选通知渠道、候选收件人、所需证据、通知原因、阻塞通知数和下一步候选动作。

## 硬边界

- 不创建 notification、notification delivery、message 或 inbox item。
- 不发送 external notification。
- 不创建 routing queue、queue item、approval assignment 或 approval lock。
- 不创建 approval packet、approval request 或 approval decision。
- 不创建 committee decision 或 freeze action。
- 不创建 Harness evidence、WAES gate result 或 KWE work item。
- 不提升 KDS lifecycle，不写入 KDS fact / accepted fact。
- 不写 GFIS / GPC / ERP / MES，不调用外部 API。

## 验证

专项验证脚本：`scripts/gfis/validate_gfis_assistant_dks_237_routing_queue_notification_preview.py`。

验证必须证明：

- 6 条 notification preview 均包含上游 routing queue / approval packet / resolution option / breach review 引用。
- Brain 2 条、PKC 1 条、GFIS Assistant 3 条。
- 总候选渠道 6 个，总候选收件人 6 个，总所需 evidence 6 个，总通知原因 6 个。
- 阻塞通知数为 3。
- 所有 creates* / sendsExternalNotification / locksApprover 字段为 false。
- 所有 noWrite 计数为 0。
