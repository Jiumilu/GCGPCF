---
doc_id: GPCF-DOC-81E3CE651A
title: GFIS Assistant Repair Notification Snooze Queue Share Approval Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-share-approval-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-share-approval-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Share Approval Preview No-write 规则

## 目标

本规则定义 DKS-127 的 GFIS Assistant Repair Notification Snooze Queue Share Approval Preview。

它基于 DKS-126 的 view share preview 生成本地审批候选预览，用于说明 Brain / PKC / GFIS Assistant 可以如何展示“团队审批、项目审批、治理审阅、外部共享阻断、委员会审批、冻结审批”的候选路径。Share approval preview 只是本地候选说明，不是真实 ApprovalRequest、ApprovalDecision、ShareLink、ACL 授权、ExternalSharePermission、PublicationApproval、Harness evidence、WAES Gate Result、KWE WorkItem 或业务写回。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| approval preview | 只能用于本地展示候选 |
| ApprovalRequest | 不创建真实审批请求 |
| ApprovalDecision | 不创建真实审批结论 |
| ShareLink / ACL | 不创建真实分享链接或 ACL 授权 |
| ExternalSharePermission | 不创建真实外部共享权限 |
| PublicationApproval | 不创建真实发布审批 |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES / KWE / KDS | 不创建门禁结果、工单或状态变化 |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 外部 API | 不调用真实外部 API |

## Approval 类型

| approval_type | 用途 |
| --- | --- |
| team_approval_preview | 团队内部共享审批候选 |
| project_approval_preview | 项目内部共享审批候选 |
| governance_review_approval_preview | 治理审阅审批候选 |
| external_share_blocked_approval_preview | 外部共享阻断审批候选 |
| committee_approval_preview | 委员会审批候选 |
| freeze_approval_preview | 冻结事项审批候选 |

## 必填字段

Share approval preview 必须具备：

- `approvalPreviewId`
- `sharePreviewRef`
- `savedViewPreviewRef`
- `tenantId`
- `projectId`
- `surface`
- `approvalType`
- `approvalStatus`
- `approvalDecision`
- `approvalScope`
- `sourceSharePreviewRefs`
- `sourceSavedViewPreviewRefs`
- `sourceSnoozePreviewRefs`
- `approvalSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `approvalNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` / `modifies*` / `persists*` / `approves*` / `promotes*` / `completes*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_share_approval_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表真实 ApprovalRequest、ApprovalDecision、ShareLink、ACL 授权、外部共享权限、发布审批、Harness evidence、WAES/KWE/KDS 或业务系统写入已发生。
