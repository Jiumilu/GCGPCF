---
doc_id: GPCF-DOC-BF28CDAB3B
title: GFIS Assistant Repair Notification Snooze Queue Saved View Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-saved-view-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-saved-view-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Saved View Preview No-write 规则

## 目标

本规则定义 DKS-125 的 GFIS Assistant Repair Notification Snooze Queue Saved View Preview。

它基于 DKS-124 的 snooze queue filter preview 生成本地保存视图预览，用于说明 Brain / PKC / GFIS Assistant 可以如何展示“个人视图、团队视图、surface 默认视图、阻断项视图、委员会事项视图、冻结事项视图”的候选保存形态。Saved view preview 只是本地候选说明，不是真实 SavedView、ViewPreference、FilterState、QueueItem、SnoozeRecord、ScheduledReminder、Notification 状态变更、回执或治理证据。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| saved view preview | 只能用于本地展示候选 |
| SavedView | 不创建真实保存视图 |
| ViewPreference | 不创建真实视图偏好 |
| FilterState | 不创建真实筛选状态 |
| QueueItem | 不创建真实 QueueItem |
| SnoozeRecord | 不创建真实 SnoozeRecord |
| ScheduledReminder | 不创建真实定时任务或提醒 |
| Notification | 不创建、不关闭、不修改真实 Notification |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES / KWE / KDS | 不创建门禁结果、工单或状态变化 |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 外部 API | 不调用真实外部 API |

## Saved View 类型

| saved_view_type | 用途 |
| --- | --- |
| personal_saved_view_preview | 个人保存视图候选 |
| team_saved_view_preview | 团队保存视图候选 |
| surface_default_view_preview | surface 默认视图候选 |
| blocked_items_saved_view_preview | 阻断项保存视图候选 |
| committee_saved_view_preview | 委员会事项保存视图候选 |
| freeze_saved_view_preview | 冻结事项保存视图候选 |

## Saved View 状态

| saved_view_status | 含义 |
| --- | --- |
| saved_view_preview_only | 仅保存视图预览 |
| saved_view_contains_blocked_items | 保存视图候选包含阻断项 |
| saved_view_contains_retained_items | 保存视图候选包含保留项 |
| saved_view_metadata_boundary | 保存视图候选涉及 metadata-only 边界 |
| saved_view_committee_items | 保存视图候选涉及委员会事项 |
| saved_view_freeze_items | 保存视图候选涉及冻结事项 |

## 必填字段

Snooze queue saved view preview 必须具备：

- `savedViewPreviewId`
- `filterPreviewRef`
- `queuePreviewRef`
- `tenantId`
- `projectId`
- `surface`
- `savedViewType`
- `savedViewStatus`
- `savedViewDecision`
- `sourceFilterPreviewRefs`
- `sourceQueuePreviewRefs`
- `sourceSnoozePreviewRefs`
- `viewScope`
- `viewSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `viewNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` / `modifies*` / `persists*` / `approves*` / `promotes*` / `completes*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_saved_view_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表真实 SavedView、ViewPreference、FilterState、QueueItem、SnoozeRecord、定时提醒、Notification、Harness evidence、WAES/KWE/KDS 或业务系统写入已发生。
