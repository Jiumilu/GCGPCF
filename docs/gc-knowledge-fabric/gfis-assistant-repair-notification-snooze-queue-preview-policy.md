---
doc_id: GPCF-DOC-2B7F6FCEBF
title: GFIS Assistant Repair Notification Snooze Queue Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Preview No-write 规则

## 目标

本规则定义 DKS-123 的 GFIS Assistant Repair Notification Snooze Queue Preview。

它把 DKS-122 的 snooze preview 聚合成本地队列预览，用于说明 Brain / PKC / GFIS Assistant 可以如何展示多条延后提醒候选的排序、分组、优先级和可见性。Snooze queue preview 仍然只是本地候选显示，不是真实 QueueItem、SnoozeRecord、ScheduledReminder、Notification 状态变更、回执或治理证据。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| snooze queue preview | 只能用于本地展示候选 |
| QueueItem | 不创建真实 QueueItem |
| SnoozeRecord | 不创建真实 SnoozeRecord |
| ScheduledReminder | 不创建真实定时任务或提醒 |
| DismissalRecord | 不创建真实 DismissalRecord |
| Notification | 不创建、不关闭、不修改真实 Notification |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES / KWE / KDS | 不创建门禁结果、工单或状态变化 |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 外部 API | 不调用真实外部 API |

## Queue 类型

| queue_type | 用途 |
| --- | --- |
| brain_snooze_queue_preview | Brain 本地延后提醒队列预览 |
| pkc_snooze_queue_preview | PKC 本地延后提醒队列预览 |
| gfis_assistant_snooze_queue_preview | GFIS Assistant 本地延后提醒队列预览 |

## Queue 状态

| queue_status | 含义 |
| --- | --- |
| queue_preview_only | 仅队列预览 |
| queue_contains_blocked_items | 队列含阻断项预览 |
| queue_contains_retained_items | 队列含保留项预览 |

## 必填字段

Snooze queue preview 必须具备：

- `queuePreviewId`
- `tenantId`
- `projectId`
- `surface`
- `queueType`
- `queueStatus`
- `queueDecision`
- `sourceSnoozePreviewRefs`
- `orderedSnoozePreviewRefs`
- `queueSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `queueNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表真实 QueueItem、SnoozeRecord、定时提醒、Notification、Harness evidence、WAES/KWE/KDS 或业务系统写入已发生。
