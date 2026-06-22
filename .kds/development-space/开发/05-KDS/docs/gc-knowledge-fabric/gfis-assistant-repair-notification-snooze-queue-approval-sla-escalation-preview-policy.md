---
doc_id: GPCF-DOC-4C95606CD2
title: GFIS Assistant Repair Notification Snooze Queue Approval SLA Escalation Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval SLA Escalation Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批 SLA 升级预览边界。

审批 SLA 升级预览承接 DKS-129 approval SLA preview，只展示候选升级队列、升级等级、责任边界、阻断原因和下一步建议。它不是正式升级排程，不创建提醒，不分配升级负责人，不创建 KWE 工单，不创建 WAES 结果，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-129 approval SLA preview 引用。
- DKS-128 approval route preview 引用。
- DKS-127 share approval preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条审批 SLA 升级预览必须包含：

- escalationPreviewId。
- slaPreviewRef。
- routePreviewRef。
- escalationType。
- escalationStatus。
- escalationDecision。
- escalationScope。
- escalationLevel。
- candidateOwnerRefs。
- responsibilityBoundaryRefs。
- reasonRefs。
- escalationNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 升级类型

- watch_escalation_preview：观察型升级预览。
- urgent_escalation_preview：紧急升级预览。
- governance_escalation_preview：治理升级预览。
- external_blocked_escalation_preview：外部共享阻断升级预览。
- committee_escalation_preview：委员会升级预览。
- freeze_escalation_preview：冻结升级预览。

## 5. 硬边界

审批 SLA 升级预览必须满足：

- createsEscalationSchedule = false。
- createsEscalationTask = false。
- assignsEscalationOwner = false。
- createsReminder = false。
- createsApprovalRoute = false。
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
- writesEscalationSchedule / writesEscalationTask / writesEscalationOwner / writesReminder。
- writesApprovalRoute / writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-sla-escalation-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-sla-escalation-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_sla_escalation_preview.py`

通过条件：

- 6 条 escalation preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 escalationType、escalationStatus、escalationScope 均被覆盖。
- 每条预览必须有候选负责人引用和责任边界引用。
- 所有升级、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
