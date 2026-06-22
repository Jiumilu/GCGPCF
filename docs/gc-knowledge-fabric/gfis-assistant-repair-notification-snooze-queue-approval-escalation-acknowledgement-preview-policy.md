---
doc_id: GPCF-DOC-4A34D350C7
title: GFIS Assistant Repair Notification Snooze Queue Approval Escalation Acknowledgement Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Escalation Acknowledgement Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批升级确认预览边界。

升级确认预览承接 DKS-130 approval SLA escalation preview，只展示候选阅读确认、候选确认人、确认边界、确认风险和下一步建议。它不是正式确认记录，不创建 read receipt，不创建 acknowledgement，不分配确认人，不创建提醒，不创建 KWE 工单，不创建 WAES 结果，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-130 approval SLA escalation preview 引用。
- DKS-129 approval SLA preview 引用。
- DKS-128 approval route preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条升级确认预览必须包含：

- acknowledgementPreviewId。
- escalationPreviewRef。
- slaPreviewRef。
- ackType。
- ackStatus。
- ackDecision。
- ackScope。
- candidateAcknowledgerRefs。
- ackBoundaryRefs。
- reasonRefs。
- ackNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 确认类型

- watch_ack_preview：观察升级确认预览。
- urgent_ack_preview：紧急升级确认预览。
- governance_ack_preview：治理升级确认预览。
- external_blocked_ack_preview：外部阻断确认预览。
- committee_ack_preview：委员会确认预览。
- freeze_ack_preview：冻结确认预览。

## 5. 硬边界

升级确认预览必须满足：

- createsAcknowledgement = false。
- createsReadReceipt = false。
- assignsAcknowledger = false。
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
- writesAcknowledgement / writesReadReceipt / writesAcknowledgerAssignment。
- writesReminder / writesEscalationTask。
- writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-escalation-acknowledgement-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-escalation-acknowledgement-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_escalation_acknowledgement_preview.py`

通过条件：

- 6 条 acknowledgement preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 ackType、ackStatus、ackScope 均被覆盖。
- 每条预览必须有候选确认人引用和确认边界引用。
- 所有确认、阅读回执、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
