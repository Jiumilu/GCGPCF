---
doc_id: GPCF-DOC-D4ECD4EB84
title: GFIS Assistant DKS-196 Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-196-routing-queue-notification-acknowledgement-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-196-routing-queue-notification-acknowledgement-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-196 Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则

## 目标

承接 DKS-195 acknowledgement escalation preview，生成候选 SLA preview，用于 Brain、PKC 与 GFIS Assistant 展示 SLA 窗口、已耗时、剩余时间、逾期时间、SLA 风险、边界引用和下一步候选动作。

## 边界

- 只读预览，不创建真实 SLA timer、escalation、reminder 或 escalation task。
- 不创建 delivery acknowledgement、approval request、approval decision、KWE work item、WAES 结果或 Harness evidence。
- 不提升 KDS lifecycle，不写 GFIS/GPC/ERP/MES，不调用外部 API。

## 来源

- 来源对象必须引用 DKS-195 acknowledgement escalation preview。
- 每条 SLA preview 必须保留 delivery acknowledgement、delivery 与 digest lineage。

## 验收

- `scripts/gfis/validate_gfis_assistant_dks_196_routing_queue_notification_acknowledgement_escalation_digest_delivery_ack_escalation_sla_preview.py` 必须通过。
- coverage 矩阵必须登记 OKF、类型、validator 与 fixture。
