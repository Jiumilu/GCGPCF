---
doc_id: GPCF-DOC-AB74993636
title: GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Breach Review Preview No-write 规则
project: KDS
related_projects: [GFIS, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Approval Packet Routing Queue Notification Acknowledgement Escalation Digest Delivery Acknowledgement Escalation SLA Breach Review Preview No-write 规则

## 目标

本规则定义 DKS-149 的 acknowledgement escalation SLA breach review preview。该预览承接 DKS-148 SLA preview，只展示候选 breach review 类型、候选严重度、候选审查路径、候选 reviewer、证据缺口、阻断计数和下一步候选动作。

该能力不创建真实 breach record、dispute、committee case、freeze request、reminder、approval request、approval decision、Harness evidence、WAES gate result、KWE work item、KDS lifecycle 或任何业务写回。

## 输入边界

- 必须引用至少一个 DKS-148 SLA preview。
- 必须保留 DKS-147 acknowledgement escalation preview 的 lineage。
- 外部共享、委员会、冻结类 breach review 只能展示候选审查边界，不得产生真实争议、委员会事项或冻结请求。

## 输出边界

- 输出仅为 breach review preview candidate。
- `blockedActions` 必须覆盖全部禁止动作。
- 所有 `creates*`、`persists*`、`approves*`、`promotes*`、`completes*` 字段必须为 `false`。
- 所有 `noWrite` 计数必须为 `0`。

## 验收口径

- fixture 覆盖 6 条 breach review preview：team、project、governance、external blocked、committee、freeze。
- Brain 2 条、PKC 1 条、GFIS Assistant 3 条。
- total reviewers = 6。
- total evidence gaps = 6。
- total breach reasons = 6。
- total blocked reviews = 3。
- total overdue minutes = 45。
- 所有 create/write 类计数为 0。
