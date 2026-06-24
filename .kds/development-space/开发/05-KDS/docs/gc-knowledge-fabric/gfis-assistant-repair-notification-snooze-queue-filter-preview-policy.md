---
doc_id: GPCF-DOC-B59C5F0206
title: GFIS Assistant Repair Notification Snooze Queue Filter Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-filter-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-filter-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Filter Preview No-write 规则

## 目标

本规则定义 DKS-124 的 GFIS Assistant Repair Notification Snooze Queue Filter Preview。

它基于 DKS-123 的 snooze queue preview 生成本地筛选预览，用于说明 Brain / PKC / GFIS Assistant 可以如何按 surface、阻断项、保留项、metadata-only 边界、委员会事项和冻结事项展示延后提醒候选。Filter preview 只是本地视图，不是真实 FilterState、QueueItem、SnoozeRecord、ScheduledReminder、Notification 状态变更、回执或治理证据。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| filter preview | 只能用于本地展示候选 |
| FilterState | 不创建真实筛选状态 |
| QueueItem | 不创建真实 QueueItem |
| SnoozeRecord | 不创建真实 SnoozeRecord |
| ScheduledReminder | 不创建真实定时任务或提醒 |
| DismissalRecord | 不创建真实 DismissalRecord |
| Notification | 不创建、不关闭、不修改真实 Notification |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES / KWE / KDS | 不创建门禁结果、工单或状态变化 |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 外部 API | 不调用真实外部 API |

## Filter 类型

| filter_type | 用途 |
| --- | --- |
| surface_filter_preview | 按 Brain / PKC / GFIS Assistant surface 展示 |
| blocked_items_filter_preview | 只展示阻断项候选 |
| retained_items_filter_preview | 只展示保留项候选 |
| metadata_boundary_filter_preview | 只展示 metadata-only 边界候选 |
| committee_filter_preview | 只展示委员会事项候选 |
| freeze_filter_preview | 只展示冻结事项候选 |

## Filter 状态

| filter_status | 含义 |
| --- | --- |
| filter_preview_only | 仅筛选预览 |
| filter_contains_blocked_items | 筛选结果含阻断项 |
| filter_contains_retained_items | 筛选结果含保留项 |
| filter_metadata_boundary | 筛选结果为 metadata-only 边界 |
| filter_committee_items | 筛选结果为委员会事项 |
| filter_freeze_items | 筛选结果为冻结事项 |

## 必填字段

Snooze queue filter preview 必须具备：

- `filterPreviewId`
- `queuePreviewRef`
- `tenantId`
- `projectId`
- `surface`
- `filterType`
- `filterStatus`
- `filterDecision`
- `sourceQueuePreviewRefs`
- `sourceSnoozePreviewRefs`
- `filteredSnoozePreviewRefs`
- `filterSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `filterNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` / `modifies*` / `persists*` / `approves*` / `promotes*` / `completes*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_filter_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表真实 FilterState、QueueItem、SnoozeRecord、定时提醒、Notification、Harness evidence、WAES/KWE/KDS 或业务系统写入已发生。
