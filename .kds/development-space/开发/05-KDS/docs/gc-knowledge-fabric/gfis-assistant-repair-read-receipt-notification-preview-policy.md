---
doc_id: GPCF-DOC-044F1AC606
title: GFIS Assistant Repair Read Receipt Notification Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-read-receipt-notification-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-read-receipt-notification-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Read Receipt Notification Preview No-write 规则

## 目标

本规则定义 DKS-120 的 GFIS Assistant Repair Read Receipt Notification Preview。

它把 DKS-119 的 read receipt preview 转成本地通知预览，用于说明界面可以如何提示用户“已查看某个候选回执解释”，但该提示仍然只是候选显示，不是真实通知、真实回执或治理证据。

Notification preview 可以说明：

- 来源 read receipt preview。
- 来源 audit trace、event preview、action guard 和 read model。
- 通知提示的本地展示类型。
- 通知原因和下一步候选提示。
- 哪些真实动作仍然被禁止。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| notification preview | 只能用于本地展示候选 |
| Notification | 不创建真实 Notification |
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
DKS-119 read receipt preview
→ DKS-120 notification preview
→ UI 展示通知候选
→ 保持 no-write
```

禁止链路：

```text
notification preview
→ Notification
→ ReadReceipt
→ Harness evidence
→ EventRecord
→ WAES Gate Result
→ KWE WorkItem
→ KDS lifecycle accepted
→ GFIS 正式写回
```

## Notification 类型

| notification_type | 用途 |
| --- | --- |
| display_notification_preview | 普通只读查看提示 |
| repair_notification_preview | 修复提示查看提示 |
| metadata_boundary_notification_preview | metadata-only 边界查看提示 |
| committee_notification_preview | 委员会提示查看提示 |
| freeze_notification_preview | 冻结提示查看提示 |
| blocked_write_notification_preview | 写回阻断查看提示 |

## Notification 状态

| notification_status | 含义 |
| --- | --- |
| notification_preview_only | 仅通知预览 |
| blocked_notification_preview | 阻断通知预览 |
| metadata_notification_preview | metadata-only 通知预览 |
| repair_notification_preview_status | 修复提示通知预览 |
| committee_notification_preview_status | 委员会提示通知预览 |
| freeze_notification_preview_status | 冻结提示通知预览 |

## Notification 决策

| notification_decision | 含义 |
| --- | --- |
| show_notification_preview_only | 只显示通知预览 |
| show_repair_notification_preview | 显示修复通知预览 |
| show_metadata_boundary_notification_preview | 显示 metadata-only 通知预览 |
| show_committee_notification_preview | 显示委员会通知预览 |
| show_freeze_notification_preview | 显示冻结通知预览 |
| show_blocked_write_notification_preview | 显示写回阻断通知预览 |

## 必填字段

Notification preview 必须具备：

- `notificationPreviewId`
- `readReceiptPreviewRef`
- `auditTraceRef`
- `eventPreviewRef`
- `actionGuardRef`
- `readModelRef`
- `tenantId`
- `projectId`
- `surface`
- `notificationType`
- `notificationStatus`
- `notificationDecision`
- `notificationSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `notificationNoteRefs`
- `nextStepCandidateRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_read_receipt_notification_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表：

- 真实 Notification 已创建。
- 真实 ReadReceipt 已创建。
- Harness evidence 已固化。
- WAES 已通过。
- KWE 工单已生成。
- KDS lifecycle 已提升。
- GFIS/GPC/ERP/MES 已写回。
- 收益、积分、额度、悬赏已确认。
