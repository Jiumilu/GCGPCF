---
doc_id: GPCF-DOC-2C100F2DD6
title: GFIS Assistant Repair Notification Snooze Queue Approval SLA Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval SLA Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批 SLA 预览边界。

审批 SLA 预览承接 DKS-128 approval route preview，只展示候选审批时限、剩余时间、超时风险和升级建议。它不是正式 SLA 计时器，不创建提醒，不排程升级，不分配升级负责人，不创建审批请求，不创建审批决定，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-128 approval route preview 引用。
- DKS-127 share approval preview 引用。
- DKS-122 至 DKS-126 snooze queue 预览引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条审批 SLA 预览必须包含：

- slaPreviewId。
- routePreviewRef。
- approvalPreviewRef。
- slaType。
- slaStatus。
- slaDecision。
- slaScope。
- dueWindowMinutes / elapsedMinutes / remainingMinutes。
- escalationLevel。
- reasonRefs。
- slaNoteRefs。
- escalationCandidateRefs。
- blockedActions。
- noWrite。

## 4. SLA 类型

- standard_sla_preview：标准审批 SLA 预览。
- urgent_sla_preview：紧急审批 SLA 预览。
- governance_sla_preview：治理审阅 SLA 预览。
- external_blocked_sla_preview：外部共享阻断 SLA 预览。
- committee_sla_preview：委员会审查 SLA 预览。
- freeze_sla_preview：冻结审查 SLA 预览。

## 5. 硬边界

审批 SLA 预览必须满足：

- createsSlaTimer = false。
- createsReminder = false。
- schedulesEscalation = false。
- assignsEscalationOwner = false。
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
- writesSlaTimer / writesReminder / writesEscalationSchedule / writesEscalationOwner。
- writesApprovalRoute / writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-sla-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-sla-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-sla-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_sla_preview.py`

通过条件：

- 6 条 SLA preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 slaType、slaStatus、slaScope 均被覆盖。
- 所有计时器、提醒、升级、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
