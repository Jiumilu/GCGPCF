---
doc_id: GPCF-DOC-827CB890B8
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Preview No-write 规则

## 目标

本规则定义 DKS-138 的 breach review resolution option preview。

它承接 DKS-137 的 SLA breach review preview，只展示候选处置选项、处置路径、候选执行人、所需证据和下一步建议，不创建真实 resolution、dispute update、committee decision、freeze action、approval decision、WAES 结果、KWE 工单、Harness evidence、KDS 状态提升或业务系统写回。

## 强边界

- resolution option preview 不是正式处置方案。
- resolution option preview 不是委员会裁决。
- resolution option preview 不是冻结动作。
- resolution option preview 不是争议处理结果。
- resolution option preview 不是 approval decision。
- resolution option preview 不是 WAES gate result。
- resolution option preview 不是 KWE work item。
- resolution option preview 不是 Harness evidence。
- resolution option preview 不是 KDS lifecycle change。
- resolution option preview 不是 GFIS/GPC/ERP/MES 写回。

## no-write 规则

所有预览对象必须满足：

- `createsResolution = false`
- `createsDisputeUpdate = false`
- `createsCommitteeDecision = false`
- `createsFreezeAction = false`
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

## 验收

- OKF YAML 可解析。
- TypeScript union 与 OKF 枚举一致。
- fixture 覆盖 6 类 resolution option 预览。
- validator 证明所有写入计数为 0。
- 覆盖率清单纳入 OKF / Types / Validator / Fixture。
- 本轮不产生真实业务写回、真实 KDS 写入、真实 WAES 结果、KWE 工单或 Harness evidence。
