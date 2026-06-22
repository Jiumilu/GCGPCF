---
doc_id: GPCF-DOC-8290176C20
title: GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则
project: KDS
related_projects: [KDS, GFIS, WAES, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-acknowledgement-escalation-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则

## 目标

DKS-160 在 DKS-159 acknowledgement escalation preview 基础上，生成候选 SLA 预览。预览只展示 SLA 窗口、已耗时、剩余时间、逾期时间、风险、候选升级负责人和下一步建议。

## 不写入边界

本规则不得创建 SLA timer、escalation、reminder、escalation task、delivery acknowledgement、approval request、approval decision、Harness evidence、WAES gate result、KWE work item，不得修改 lifecycle、业务事实、业务写回、收益、积分或外部系统。

## 输入边界

输入来自 DKS-159 routing queue notification acknowledgement escalation digest delivery acknowledgement escalation preview，并保留 DKS-158 至 DKS-149 的 lineage。上游候选升级、通知、摘要、投递和确认记录仍只作为 no-write 预览引用。

## 输出边界

输出为 `sla_preview` candidate。所有 create 标志必须为 false，所有 `noWrite` 写入计数必须为 0。

## 验收口径

- SLA 预览数量为 6。
- Brain surface 为 2，PKC surface 为 1，GFIS Assistant surface 为 3。
- 候选升级负责人总数为 6。
- SLA reason 总数为 6。
- blocked SLA escalation 总数为 3。
- total overdue minutes 为 310。
- 所有 create/write 计数均为 0。
