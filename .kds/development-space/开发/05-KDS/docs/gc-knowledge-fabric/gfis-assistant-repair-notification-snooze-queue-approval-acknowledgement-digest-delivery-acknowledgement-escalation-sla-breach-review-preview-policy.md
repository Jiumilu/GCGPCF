---
doc_id: GPCF-DOC-A097195A21
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Breach Review Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Breach Review Preview No-write 规则

## 目标

本规则定义 DKS-137 的 SLA breach review preview。

它承接 DKS-136 的 escalation SLA preview，只展示候选 breach review 类型、严重度、审查路径、候选责任人、候选补证要求和下一步建议，不创建真实 breach record、争议、委员会事项、冻结、提醒、审批、WAES 结果、KWE 工单、Harness evidence、KDS 状态提升或业务系统写回。

## 输入边界

- DKS-136 escalation SLA preview。
- DKS-135 delivery acknowledgement escalation preview。
- `okf/committee-policy.yaml`。
- `okf/waes-gate-policy.yaml`。
- `okf/kwe-approval-route-packet-policy.yaml`。

## 强边界

- breach review preview 不是 breach record。
- breach review preview 不是 dispute。
- breach review preview 不是 committee case。
- breach review preview 不是 freeze request。
- breach review preview 不是 approval decision。
- breach review preview 不是 WAES gate result。
- breach review preview 不是 KWE work item。
- breach review preview 不是 Harness evidence。
- breach review preview 不是 KDS lifecycle change。
- breach review preview 不是 GFIS/GPC/ERP/MES 写回。

## no-write 规则

所有预览对象必须满足：

- `createsBreachRecord = false`
- `createsDispute = false`
- `createsCommitteeCase = false`
- `createsFreezeRequest = false`
- `createsReminder = false`
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

## 审查计算规则

- `overdueMinutes` 必须来自 DKS-136 SLA preview 的候选值。
- `blockedReviewCount` 不得超过 `candidateReviewerRefs.length`。
- `evidenceGapRefs` 为空时只能展示为候选审查路径，不得生成正式缺口、工单或 evidence。
- `committee_required_candidate` 和 `freeze_required_candidate` 只能触发候选提示，不得创建委员会事项或冻结请求。

## 验收

- OKF YAML 可解析。
- TypeScript union 与 OKF 枚举一致。
- fixture 覆盖 6 类 breach review 预览。
- validator 证明所有写入计数为 0。
- 覆盖率清单纳入 OKF / Types / Validator / Fixture。
- 本轮不产生真实业务写回、真实 KDS 写入、真实 WAES 结果、KWE 工单或 Harness evidence。
