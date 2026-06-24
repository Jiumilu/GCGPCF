---
doc_id: GPCF-DOC-C351276EE9
title: GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Acknowledgement Digest Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批确认摘要预览边界。

确认摘要预览承接 DKS-131 approval escalation acknowledgement preview，只聚合候选确认预览、确认覆盖数、阻断确认数、责任边界和下一步建议。它不是正式摘要记录，不创建 acknowledgement，不创建 read receipt，不创建 digest 记录，不写 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-131 approval escalation acknowledgement preview 引用。
- DKS-130 approval SLA escalation preview 引用。
- KWE approval route packet 与 committee policy 引用。

## 3. 输出

每条确认摘要预览必须包含：

- digestPreviewId。
- acknowledgementPreviewRefs。
- digestType。
- digestStatus。
- digestDecision。
- digestScope。
- coverageCount。
- blockedAckCount。
- candidateAcknowledgerRefs。
- boundaryRefs。
- reasonRefs。
- digestNoteRefs。
- nextStepCandidateRefs。
- blockedActions。
- noWrite。

## 4. 摘要类型

- team_ack_digest_preview：团队确认摘要预览。
- project_ack_digest_preview：项目确认摘要预览。
- governance_ack_digest_preview：治理确认摘要预览。
- external_blocked_ack_digest_preview：外部阻断确认摘要预览。
- committee_ack_digest_preview：委员会确认摘要预览。
- freeze_ack_digest_preview：冻结确认摘要预览。

## 5. 硬边界

确认摘要预览必须满足：

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
- writesDigest / writesAcknowledgement / writesReadReceipt。
- writesReminder / writesEscalationTask。
- writesApprovalRequest / writesApprovalDecision。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-acknowledgement-digest-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-acknowledgement-digest-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_preview.py`

通过条件：

- 6 条 digest preview 覆盖 Brain、PKC、GFIS Assistant。
- 6 类 digestType、digestStatus、digestScope 均被覆盖。
- 每条预览必须有 acknowledgementPreviewRefs、candidateAcknowledgerRefs 和 boundaryRefs。
- coverageCount 必须等于 acknowledgementPreviewRefs 数量。
- 所有摘要、确认、阅读回执、提醒、审批、证据、写回、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
