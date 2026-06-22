---
doc_id: GPCF-DOC-F856849B9E
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Preview No-write 规则

## 目标

本规则定义 DKS-136 的 GFIS Assistant repair notification snooze queue approval acknowledgement digest delivery acknowledgement escalation SLA preview。

它承接 DKS-135 的 delivery acknowledgement escalation preview，只展示候选升级的 SLA 窗口、剩余分钟、超时分钟、SLA 风险等级、升级负责人候选和下一步候选，不创建真实 SLA 计时器、升级任务、提醒、投递确认、通知、摘要、审批、KWE 工单、WAES 结果、Harness evidence、KDS 状态提升或业务系统写回。

## 输入边界

- DKS-135 delivery acknowledgement escalation preview。
- DKS-134 delivery acknowledgement preview。
- DKS-133 acknowledgement digest delivery preview。
- `okf/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-preview-policy.yaml`。
- `okf/kwe-approval-route-packet-policy.yaml`。
- `okf/waes-gate-policy.yaml`。

## 输出字段

- `slaPreviewId`
- `escalationPreviewRefs`
- `deliveryAcknowledgementPreviewRefs`
- `surface`
- `slaType`
- `slaStatus`
- `slaDecision`
- `slaScope`
- `slaWindowMinutes`
- `elapsedMinutes`
- `remainingMinutes`
- `overdueMinutes`
- `slaRisk`
- `candidateEscalationOwnerRefs`
- `slaReasonRefs`
- `blockedSlaEscalationCount`
- `boundaryRefs`
- `sourceEscalationPreviewRefs`
- `slaSummaryRef`
- `nextStepCandidateRefs`
- `blockedActions`
- `noWrite`

## 强边界

- SLA preview 不是 SLA timer。
- SLA preview 不是 escalation task。
- SLA preview 不是 reminder。
- SLA preview 不是 delivery acknowledgement。
- SLA preview 不是 approval request。
- SLA preview 不是 approval decision。
- SLA preview 不是 WAES gate result。
- SLA preview 不是 KWE work item。
- SLA preview 不是 Harness evidence。
- SLA preview 不是 KDS lifecycle change。
- SLA preview 不是 GFIS/GPC/ERP/MES 写回。

## no-write 规则

所有预览对象必须满足：

- `createsSlaTimer = false`
- `createsEscalation = false`
- `createsReminder = false`
- `createsEscalationTask = false`
- `createsDeliveryAcknowledgement = false`
- `createsApprovalRequest = false`
- `createsApprovalDecision = false`
- `createsWaesGateResult = false`
- `createsKweWorkItem = false`
- `createsHarnessEvidence = false`
- `promotesLifecycle = false`
- `approvesBusinessWrite = false`
- `writesGfis = 0`
- `writesGpc = 0`
- `writesErp = 0`
- `writesMes = 0`
- `writesExternalApi = 0`

## SLA 计算规则

- `remainingMinutes = max(slaWindowMinutes - elapsedMinutes, 0)`。
- `overdueMinutes = max(elapsedMinutes - slaWindowMinutes, 0)`。
- `blockedSlaEscalationCount` 不得超过 `candidateEscalationOwnerRefs.length`。
- `overdueMinutes > 0` 的对象只能显示为候选升级风险，不得创建真实升级、提醒或审批。

## 展示面

- Brain：可展示治理视图、团队视图和冻结候选视图。
- PKC：可展示个人/项目待确认 SLA 候选。
- GFIS Assistant：可展示字段解释、证据缺口、升级风险和 no-write 边界。

## 验收

- OKF YAML 可解析。
- TypeScript union 与 OKF 枚举一致。
- fixture 覆盖 6 类 SLA 预览。
- validator 证明所有写入计数为 0。
- 覆盖率清单纳入 OKF / Types / Validator / Fixture。
- 本轮不产生真实业务写回、真实 KDS 写入、真实 WAES 结果或 Harness evidence。
