---
doc_id: GPCF-DOC-D2EC468041
title: GFIS Assistant Repair Notification Snooze Queue View Share Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-view-share-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-view-share-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue View Share Preview No-write 规则

## 目标

本规则定义 DKS-126 的 GFIS Assistant Repair Notification Snooze Queue View Share Preview。

它基于 DKS-125 的 saved view preview 生成本地共享预览，用于说明 Brain / PKC / GFIS Assistant 可以如何展示“个人到团队、团队到项目、surface 默认视图、治理审阅、外部共享阻断、委员会事项”的候选共享形态。View share preview 只是本地候选说明，不是真实 ShareLink、ACL 授权、ExternalSharePermission、PublicationApproval、SavedView、ViewPreference、FilterState、Notification 状态变更、回执或治理证据。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| view share preview | 只能用于本地展示候选 |
| ShareLink | 不创建真实分享链接 |
| ACL Grant | 不创建真实 ACL 授权 |
| ExternalSharePermission | 不创建真实外部共享权限 |
| PublicationApproval | 不创建真实发布审批 |
| SavedView / ViewPreference | 不创建真实保存视图或视图偏好 |
| FilterState / QueueItem | 不创建真实筛选状态或队列项 |
| Notification | 不创建、不关闭、不修改真实 Notification |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES / KWE / KDS | 不创建门禁结果、工单或状态变化 |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 外部 API | 不调用真实外部 API |

## Share 类型

| share_type | 用途 |
| --- | --- |
| personal_to_team_share_preview | 个人视图共享给团队候选 |
| team_to_project_share_preview | 团队视图共享给项目候选 |
| surface_default_share_preview | surface 默认视图共享候选 |
| governance_review_share_preview | 治理审阅共享候选 |
| external_share_blocked_preview | 外部共享阻断候选 |
| committee_share_preview | 委员会事项共享候选 |

## 必填字段

View share preview 必须具备：

- `sharePreviewId`
- `savedViewPreviewRef`
- `filterPreviewRef`
- `queuePreviewRef`
- `tenantId`
- `projectId`
- `surface`
- `shareType`
- `shareStatus`
- `shareDecision`
- `shareScope`
- `sourceSavedViewPreviewRefs`
- `sourceFilterPreviewRefs`
- `sourceQueuePreviewRefs`
- `sourceSnoozePreviewRefs`
- `shareSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `shareNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` / `modifies*` / `persists*` / `approves*` / `promotes*` / `completes*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_view_share_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表真实 ShareLink、ACL 授权、外部共享权限、发布审批、SavedView、ViewPreference、Notification、Harness evidence、WAES/KWE/KDS 或业务系统写入已发生。
