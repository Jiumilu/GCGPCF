---
doc_id: GPCF-DOC-F3B417690E
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批确认摘要候选投递接收确认后的升级预览边界。

升级预览承接 DKS-134 delivery acknowledgement preview，只展示候选升级负责人、升级原因、升级范围、阻断升级数量、责任边界和下一步建议。它不是正式升级任务，不创建 reminder，不创建 escalation，不创建 approval request，不创建 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-134 delivery acknowledgement preview 引用。
- DKS-133 acknowledgement digest delivery preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条升级预览必须包含：

- escalationPreviewId。
- deliveryAcknowledgementPreviewRefs。
- escalationType。
- escalationStatus。
- escalationDecision。
- escalationScope。
- candidateEscalationOwnerRefs。
- escalationReasonRefs。
- blockedEscalationCount。
- boundaryRefs。
- reasonRefs。
- escalationNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 升级类型

- team_delivery_ack_escalation_preview：团队投递确认升级预览。
- project_delivery_ack_escalation_preview：项目投递确认升级预览。
- governance_delivery_ack_escalation_preview：治理投递确认升级预览。
- external_blocked_delivery_ack_escalation_preview：外部阻断投递确认升级预览。
- committee_delivery_ack_escalation_preview：委员会投递确认升级预览。
- freeze_delivery_ack_escalation_preview：冻结投递确认升级预览。

## 5. 硬边界

升级预览必须满足：

- createsEscalation = false。
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
- writesEscalation / writesDeliveryAcknowledgement / writesDelivery / writesNotification。
- writesDigest / writesAcknowledgement / writesReadReceipt。
- writesReminder / writesEscalationTask。
- writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_acknowledgement_escalation_preview.py`

通过条件：

- 6 条 escalation preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 escalationType、escalationStatus、escalationScope 均被覆盖。
- 每条预览必须有 deliveryAcknowledgementPreviewRefs、candidateEscalationOwnerRefs、escalationReasonRefs 和 boundaryRefs。
- deliveryAcknowledgementPreviewRefs 必须包含在 sourceDeliveryAcknowledgementPreviewRefs 中。
- blockedEscalationCount 不能超过候选升级负责人数量。
- 所有升级、投递确认、投递、通知、摘要、确认、阅读回执、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
