---
doc_id: GPCF-DOC-D846CB64BC
title: GFIS Assistant Repair Action Guard Event Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-action-guard-event-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-action-guard-event-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Action Guard Event Preview No-write 规则

## 1. 定位

GFIS Assistant Repair Action Guard Event Preview 是 DKS-116 `Read Model Action Guard` 之后的本地事件预览模型。

它用于说明用户点击只读按钮时，界面可以展示怎样的候选事件预览、阻断原因、下一步候选说明和 no-write 警示。它不是 EventRecord，不是 ActionReceipt，不是 ReadReceipt，不创建 KWE WorkItem，不写 WAES Gate Result，不持久化 evidence，不推进 KDS lifecycle，不写 GFIS / GPC / ERP / MES。

## 2. Preview 类型

| preview_type | 说明 |
|---|---|
| display_event_preview | 只读展示事件预览 |
| repair_prompt_event_preview | 补齐提示事件预览 |
| metadata_boundary_event_preview | metadata 边界提示事件预览 |
| committee_note_event_preview | 委员会议题提示事件预览 |
| freeze_note_event_preview | 冻结关注提示事件预览 |
| blocked_write_event_preview | 被阻断写动作事件预览 |

## 3. Preview 状态

| preview_status | 说明 |
|---|---|
| preview_only | 仅预览 |
| blocked_preview | 阻断预览 |
| metadata_only_preview | metadata-only 预览 |
| repair_required_preview | 需补齐预览 |
| committee_preview | 委员会议题预览 |
| freeze_preview | 冻结关注预览 |

## 4. No-write 边界

Event Preview 不得直接执行以下动作：

- 创建 EventRecord；
- 创建 ActionReceipt；
- 创建 ReadReceipt；
- 创建 AdmissionRecord；
- 创建 Review Queue Item；
- 创建 KWE WorkItem；
- 创建 ConfirmationRecord；
- 创建 DecisionRecord；
- 写入 WAES Gate Result；
- 持久化 evidence；
- 推进 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 5. 后续关系

Event Preview 只能作为用户点击前后的本地解释材料。任何真实事件、回执、队列、工单、证据、门禁结果或业务写回，都必须由后续独立受控流程创建，并经 Harness evidence 固化。
