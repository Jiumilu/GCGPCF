---
doc_id: GPCF-DOC-C43B7FBE3A
title: GFIS Assistant Repair Notification Snooze Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Preview No-write 规则

## 目标

本规则定义 DKS-122 的 GFIS Assistant Repair Notification Snooze Preview。

它把 DKS-121 的 dismissal preview 转成本地延后提醒预览，用于说明界面可以如何提示用户“稍后提醒某个通知候选”。Snooze preview 仍然只是本地候选显示，不是真实 SnoozeRecord、真实定时任务、真实 Notification 状态变更、真实回执或治理证据。

Snooze preview 可以说明：

- 来源 dismissal preview。
- 来源 notification preview、read receipt preview、audit trace、event preview、action guard 和 read model。
- 延后提醒候选的本地展示类型。
- 延后原因、保留原因、阻断原因和下一步候选提示。
- 哪些真实动作仍然被禁止。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| snooze preview | 只能用于本地展示候选 |
| SnoozeRecord | 不创建真实 SnoozeRecord |
| scheduled reminder | 不创建真实定时任务或提醒 |
| DismissalRecord | 不创建真实 DismissalRecord |
| Notification | 不创建、不关闭、不修改真实 Notification |
| ReadReceipt | 不创建真实 ReadReceipt |
| audit trace record | 不创建真实 audit trace record |
| EventRecord | 不创建真实 EventRecord |
| ActionReceipt | 不创建真实 ActionReceipt |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES Gate Result | 不创建 WAES gate result |
| KWE WorkItem | 不创建 KWE work item |
| KDS lifecycle | 不提升、不冻结、不发布、不 accepted |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 收益/积分/额度/悬赏 | 不确认、不分配、不结算 |
| 外部 API | 不调用真实外部 API |

## 标准链路

```text
DKS-121 dismissal preview
→ DKS-122 snooze preview
→ UI 展示延后提醒候选
→ 保持 no-write
```

禁止链路：

```text
snooze preview
→ SnoozeRecord
→ scheduled reminder
→ Notification 状态变更
→ DismissalRecord
→ ReadReceipt
→ Harness evidence
→ EventRecord
→ WAES Gate Result
→ KWE WorkItem
→ KDS lifecycle accepted
→ GFIS 正式写回
```

## Snooze 类型

| snooze_type | 用途 |
| --- | --- |
| snooze_display_notification_preview | 普通只读查看提示的延后提醒预览 |
| snooze_repair_notification_preview | 修复提示的延后提醒预览 |
| retain_metadata_boundary_snooze_preview | metadata-only 边界提示的保留延后预览 |
| retain_committee_snooze_preview | 委员会提示的保留延后预览 |
| block_freeze_snooze_preview | 冻结提示禁止延后预览 |
| retain_blocked_write_snooze_preview | 写回阻断提示的保留延后预览 |

## Snooze 状态

| snooze_status | 含义 |
| --- | --- |
| snooze_preview_only | 仅延后提醒预览 |
| deferred_snooze_preview | 稍后提醒预览 |
| retained_snooze_preview | 保留延后提醒候选预览 |
| blocked_snooze_preview | 阻断延后提醒预览 |
| metadata_boundary_snooze_retained_preview | metadata-only 边界保留延后预览 |
| freeze_snooze_blocked_preview | 冻结提示延后阻断预览 |

## Snooze 决策

| snooze_decision | 含义 |
| --- | --- |
| show_snooze_preview_only | 只显示延后提醒预览 |
| show_repair_snooze_preview | 显示修复延后提醒预览 |
| show_metadata_snooze_retained_preview | 显示 metadata-only 保留延后预览 |
| show_committee_snooze_retained_preview | 显示委员会保留延后预览 |
| show_freeze_snooze_blocked_preview | 显示冻结延后阻断预览 |
| show_blocked_write_snooze_retained_preview | 显示写回阻断保留延后预览 |

## 必填字段

Snooze preview 必须具备：

- `snoozePreviewId`
- `dismissalPreviewRef`
- `notificationPreviewRef`
- `readReceiptPreviewRef`
- `auditTraceRef`
- `eventPreviewRef`
- `actionGuardRef`
- `readModelRef`
- `tenantId`
- `projectId`
- `surface`
- `snoozeType`
- `snoozeStatus`
- `snoozeDecision`
- `snoozeSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `snoozeNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_snooze_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表：

- 真实 SnoozeRecord 已创建。
- 真实定时任务或提醒已创建。
- 真实 DismissalRecord 已创建。
- 真实 Notification 已关闭或修改。
- 真实 ReadReceipt 已创建。
- Harness evidence 已固化。
- WAES 已通过。
- KWE 工单已生成。
- KDS lifecycle 已提升。
- GFIS/GPC/ERP/MES 已写回。
- 收益、积分、额度、悬赏已确认。
