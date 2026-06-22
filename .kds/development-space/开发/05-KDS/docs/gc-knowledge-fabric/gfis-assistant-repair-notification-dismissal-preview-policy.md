---
doc_id: GPCF-DOC-F7D68D144D
title: GFIS Assistant Repair Notification Dismissal Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-dismissal-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-dismissal-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Dismissal Preview No-write 规则

## 目标

本规则定义 DKS-121 的 GFIS Assistant Repair Notification Dismissal Preview。

它把 DKS-120 的 notification preview 转成本地关闭预览，用于说明界面可以如何提示用户“关闭、稍后处理或保留某个通知候选”。关闭预览仍然只是本地候选显示，不是真实 Notification 状态变更、真实 DismissalRecord、真实回执或治理证据。

Dismissal preview 可以说明：

- 来源 notification preview。
- 来源 read receipt preview、audit trace、event preview、action guard 和 read model。
- 用户关闭通知候选时的本地展示类型。
- 关闭原因、保留原因和下一步候选提示。
- 哪些真实动作仍然被禁止。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| dismissal preview | 只能用于本地展示候选 |
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
DKS-120 notification preview
→ DKS-121 dismissal preview
→ UI 展示关闭候选
→ 保持 no-write
```

禁止链路：

```text
dismissal preview
→ DismissalRecord
→ Notification 状态变更
→ ReadReceipt
→ Harness evidence
→ EventRecord
→ WAES Gate Result
→ KWE WorkItem
→ KDS lifecycle accepted
→ GFIS 正式写回
```

## Dismissal 类型

| dismissal_type | 用途 |
| --- | --- |
| dismiss_display_notification_preview | 普通只读查看提示的关闭预览 |
| defer_repair_notification_preview | 修复提示的稍后处理预览 |
| retain_metadata_boundary_notification_preview | metadata-only 边界提示的保留预览 |
| retain_committee_notification_preview | 委员会提示的保留预览 |
| block_freeze_notification_dismissal_preview | 冻结提示禁止关闭预览 |
| retain_blocked_write_notification_preview | 写回阻断提示的保留预览 |

## Dismissal 状态

| dismissal_status | 含义 |
| --- | --- |
| dismissal_preview_only | 仅关闭预览 |
| deferred_dismissal_preview | 稍后处理预览 |
| retained_notification_preview | 保留通知候选预览 |
| blocked_dismissal_preview | 阻断关闭预览 |
| metadata_boundary_retained_preview | metadata-only 边界保留预览 |
| freeze_dismissal_blocked_preview | 冻结提示关闭阻断预览 |

## Dismissal 决策

| dismissal_decision | 含义 |
| --- | --- |
| show_dismissal_preview_only | 只显示关闭预览 |
| show_defer_repair_preview | 显示修复稍后处理预览 |
| show_metadata_retained_preview | 显示 metadata-only 保留预览 |
| show_committee_retained_preview | 显示委员会保留预览 |
| show_freeze_dismissal_blocked_preview | 显示冻结关闭阻断预览 |
| show_blocked_write_retained_preview | 显示写回阻断保留预览 |

## 必填字段

Dismissal preview 必须具备：

- `dismissalPreviewId`
- `notificationPreviewRef`
- `readReceiptPreviewRef`
- `auditTraceRef`
- `eventPreviewRef`
- `actionGuardRef`
- `readModelRef`
- `tenantId`
- `projectId`
- `surface`
- `dismissalType`
- `dismissalStatus`
- `dismissalDecision`
- `dismissalSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `dismissalNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_notification_dismissal_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表：

- 真实 DismissalRecord 已创建。
- 真实 Notification 已关闭或修改。
- 真实 ReadReceipt 已创建。
- Harness evidence 已固化。
- WAES 已通过。
- KWE 工单已生成。
- KDS lifecycle 已提升。
- GFIS/GPC/ERP/MES 已写回。
- 收益、积分、额度、悬赏已确认。
