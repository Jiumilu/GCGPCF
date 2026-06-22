---
doc_id: GPCF-DOC-EA8F4D165E
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批确认摘要候选投递后的接收确认预览边界。

接收确认预览承接 DKS-133 acknowledgement digest delivery preview，只展示候选投递确认人、候选确认方式、确认边界、阻断确认数量和下一步建议。它不是正式 acknowledgement，不创建 read receipt，不创建 notification，不创建 delivery，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-133 acknowledgement digest delivery preview 引用。
- DKS-132 acknowledgement digest preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条接收确认预览必须包含：

- deliveryAcknowledgementPreviewId。
- deliveryPreviewRefs。
- acknowledgementType。
- acknowledgementStatus。
- acknowledgementDecision。
- acknowledgementScope。
- candidateAcknowledgerRefs。
- acknowledgementMethodRefs。
- blockedAcknowledgementCount。
- boundaryRefs。
- reasonRefs。
- acknowledgementNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 接收确认类型

- team_delivery_ack_preview：团队投递接收确认预览。
- project_delivery_ack_preview：项目投递接收确认预览。
- governance_delivery_ack_preview：治理投递接收确认预览。
- external_blocked_delivery_ack_preview：外部阻断投递接收确认预览。
- committee_delivery_ack_preview：委员会投递接收确认预览。
- freeze_delivery_ack_preview：冻结投递接收确认预览。

## 5. 硬边界

接收确认预览必须满足：

- createsDeliveryAcknowledgement = false。
- createsDelivery = false。
- createsNotification = false。
- createsDigest = false。
- createsAcknowledgement = false。
- createsReadReceipt = false。
- createsReminder = false。
- createsEscalationTask = false。
- createsApprovalRequest = false。
- createsApprovalDecision = false。
- createsHarnessEvidence = false。
- createsWaesGateResult = false。
- createsKweWorkItem = false。
- persistsEvidence = false。
- approvesBusinessWrite = false。
- promotesLifecycle = false。
- completesCommitteeDecision = false。

## 6. No-write 守卫

以下写入计数必须全部为 0：

- writesGfis / writesGpc / writesErp / writesMes。
- writesDeliveryAcknowledgement / writesDelivery / writesNotification。
- writesDigest / writesAcknowledgement / writesReadReceipt。
- writesReminder / writesEscalationTask。
- writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_acknowledgement_preview.py`

通过条件：

- 6 条 delivery acknowledgement preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 acknowledgementType、acknowledgementStatus、acknowledgementScope 均被覆盖。
- 每条预览必须有 deliveryPreviewRefs、candidateAcknowledgerRefs、acknowledgementMethodRefs 和 boundaryRefs。
- deliveryPreviewRefs 必须包含在 sourceDeliveryPreviewRefs 中。
- blockedAcknowledgementCount 不能超过候选确认人数量。
- 所有投递确认、投递、通知、摘要、确认、阅读回执、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
