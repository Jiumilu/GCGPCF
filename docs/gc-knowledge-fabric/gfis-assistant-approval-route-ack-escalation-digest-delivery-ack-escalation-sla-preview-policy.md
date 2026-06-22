---
doc_id: GPCF-DOC-876AB37106
title: GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则
project: KDS
related_projects: [GFIS, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则

## 目标

本规则定义 DKS-148 的 acknowledgement escalation SLA preview。该预览承接 DKS-147 acknowledgement escalation preview，只展示候选 SLA 窗口、已用分钟、剩余分钟、逾期分钟、SLA 风险、候选升级责任人和下一步候选动作。

该能力不创建真实 SLA timer、escalation、reminder、escalation task、delivery acknowledgement、approval request、approval decision、Harness evidence、WAES gate result、KWE work item、KDS lifecycle 或任何业务写回。

## 输入边界

- 必须引用至少一个 DKS-147 acknowledgement escalation preview。
- 必须保留 DKS-146 delivery acknowledgement preview、DKS-145 delivery preview、DKS-144 digest preview 的 lineage。
- 外部共享、委员会、冻结类 SLA 只能展示 metadata boundary，不得产生真实计时器或逾期结论。

## 输出边界

- 输出仅为 SLA preview candidate。
- `blockedActions` 必须覆盖全部禁止动作。
- 所有 `creates*`、`persists*`、`approves*`、`promotes*`、`completes*` 字段必须为 `false`。
- 所有 `noWrite` 计数必须为 `0`。

## 验收口径

- fixture 覆盖 6 条 SLA preview：team、project、governance、external blocked、committee、freeze。
- Brain 2 条、PKC 1 条、GFIS Assistant 3 条。
- total owners = 6。
- total reasons = 6。
- total blocked SLA escalations = 3。
- 所有 create/write 类计数为 0。
