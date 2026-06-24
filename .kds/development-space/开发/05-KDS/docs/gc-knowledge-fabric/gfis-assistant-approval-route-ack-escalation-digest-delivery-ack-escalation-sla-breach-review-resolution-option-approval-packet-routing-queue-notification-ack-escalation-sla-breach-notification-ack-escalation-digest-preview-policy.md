---
doc_id: GPCF-DOC-BE3C49D63F
title: GFIS Assistant Routing Queue Notification Acknowledgement Escalation Digest Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-sla-breach-notification-ack-escalation-digest-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-approval-route-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-sla-breach-notification-ack-escalation-digest-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Routing Queue Notification Acknowledgement Escalation Digest Preview No-write 规则

## 定位

本文件定义 DKS-168：Routing Queue Notification Acknowledgement Escalation Digest Preview No-write。

该对象只把 DKS-167 的 escalation preview 转为候选 digest preview，用于 Brain、PKC 与 GFIS Assistant 展示候选摘要通道、候选摘要接收人、摘要原因、阻断摘要数量与下一步建议。

文件名沿用压缩命名，完整语义以本文档 title、OKF `purpose` 与 LOOP 记录为准。

## 输入

- DKS-167 escalation preview fixture。
- DKS-166 acknowledgement preview 引用。
- DKS-165 notification preview 引用。
- DKS-164 routing queue preview 引用。
- DKS-163 approval packet preview 引用。
- DKS-162 resolution option preview 引用。
- DKS-161 breach review preview 引用。
- GC-Knowledge Fabric AI 候选边界、WAES 门禁、KWE 人工确认与 Harness evidence 规则。

## 输出字段

每条 digest preview 必须包含：

- digestPreviewId。
- escalationPreviewRefs / acknowledgementPreviewRefs / notificationPreviewRefs / routingQueuePreviewRefs。
- approvalPacketPreviewRefs / resolutionOptionPreviewRefs / breachReviewPreviewRefs。
- tenantId / projectId / surface。
- digestType / digestStatus / digestDecision / digestScope。
- digestChannel / digestPriority。
- candidateDigestRecipientRefs。
- requiredEvidenceRefs。
- digestReasonRefs。
- blockedDigestCount。
- boundaryRefs / sourceEscalationPreviewRefs。
- digestSummaryRef / lineageHintRefs / reasonRefs / digestNoteRefs / nextStepCandidateRefs。
- blockedActions。
- creates* flags。
- noWrite 计数。

## No-write 边界

DKS-168 严格禁止：

- 创建 digest 或 digest delivery。
- 创建 escalation、timeout event 或 KWE work item。
- 创建 notification、acknowledgement、receipt、read receipt。
- 更新 delivery status 或发送外部通知。
- 创建 approval assignment、approval lock、approval packet、approval request 或 approval decision。
- 创建 committee decision 或 freeze action。
- 写入 WAES、Harness evidence、KDS lifecycle、KDS fact 或 accepted fact。
- 执行 GFIS、GPC、ERP、MES 或外部 API 写入。

所有 `creates*` / `updates*` 必须为 `false`，所有 `noWrite` 写入计数必须为 `0`。

## 验收口径

本轮 dry-run 夹具必须满足：

- digest preview 总数：6。
- Brain surface：2。
- PKC surface：1。
- GFIS Assistant surface：3。
- digest channel 总数：6。
- candidate digest recipient 总数：6。
- required evidence 总数：6。
- digest reason 总数：6。
- blocked digest 总数：3。
- digest / digest delivery / escalation / timeout / KWE / notification / acknowledgement / receipt / read receipt / delivery status / external send / approval / committee / freeze / Harness / WAES / KDS / business writes 全部为 0。

## 后续提升条件

如需把 digest preview 转为真实摘要、真实摘要投递、真实升级、真实 KWE 工单、真实通知或任何业务写回，必须另行进入 WAES 门禁、KWE 工单、人工确认与 Harness evidence，不得由本 preview 自动提升。
