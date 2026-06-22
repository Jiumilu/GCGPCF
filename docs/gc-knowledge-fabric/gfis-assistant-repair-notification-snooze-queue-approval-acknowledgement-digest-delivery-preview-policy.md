---
doc_id: GPCF-DOC-AFA789266F
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批确认摘要候选投递预览边界。

候选投递预览承接 DKS-132 acknowledgement digest preview，只展示摘要候选应投递到哪些内部表面、候选接收人、候选通道、阻断投递数量、责任边界和下一步建议。它不是正式投递记录，不创建 notification，不创建 delivery，不创建 acknowledgement，不创建 read receipt，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-132 acknowledgement digest preview 引用。
- DKS-131 approval escalation acknowledgement preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条候选投递预览必须包含：

- deliveryPreviewId。
- digestPreviewRefs。
- deliveryType。
- deliveryStatus。
- deliveryDecision。
- deliveryScope。
- candidateRecipientRefs。
- candidateChannelRefs。
- blockedDeliveryCount。
- boundaryRefs。
- reasonRefs。
- deliveryNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 投递类型

- team_digest_delivery_preview：团队摘要投递预览。
- project_digest_delivery_preview：项目摘要投递预览。
- governance_digest_delivery_preview：治理摘要投递预览。
- external_blocked_digest_delivery_preview：外部阻断摘要投递预览。
- committee_digest_delivery_preview：委员会摘要投递预览。
- freeze_digest_delivery_preview：冻结摘要投递预览。

## 5. 硬边界

候选投递预览必须满足：

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
- writesDelivery / writesNotification。
- writesDigest / writesAcknowledgement / writesReadReceipt。
- writesReminder / writesEscalationTask。
- writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_preview.py`

通过条件：

- 6 条 delivery preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 deliveryType、deliveryStatus、deliveryScope 均被覆盖。
- 每条预览必须有 digestPreviewRefs、candidateRecipientRefs、candidateChannelRefs 和 boundaryRefs。
- digestPreviewRefs 必须包含在 sourceDigestPreviewRefs 中。
- blockedDeliveryCount 不能超过候选接收人数量。
- 所有投递、通知、摘要、确认、阅读回执、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
