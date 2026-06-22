---
doc_id: GPCF-DOC-1B6A1276BB
title: GFIS Assistant Repair Read Model Action Guard No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-read-model-action-guard-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-read-model-action-guard-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Read Model Action Guard No-write 规则

## 1. 定位

GFIS Assistant Repair Read Model Action Guard 是 DKS-115 `Repair Admission Read Model` 之后的按钮级 / 动作级门禁模型。

它定义 Brain、PKC、GFIS Assistant 在只读视图中可以展示哪些动作提示，以及哪些动作必须被阻断。它不是按钮点击回执，不创建 Review Queue Item，不创建 KWE WorkItem，不创建 ConfirmationRecord / DecisionRecord，不写 WAES Gate Result，不推进 KDS lifecycle，不写 GFIS / GPC / ERP / MES。

## 2. 动作类型

| action_kind | 说明 |
|---|---|
| display_only | 只读展示动作 |
| repair_prompt | 补齐提示动作 |
| metadata_boundary_prompt | metadata-only 边界提示动作 |
| committee_note_prompt | 委员会议题提示动作 |
| freeze_note_prompt | 冻结关注提示动作 |
| blocked_write_action | 必须阻断的写动作 |

## 3. Guard 状态

| guard_status | 说明 |
|---|---|
| allowed_display_only | 仅允许展示 |
| repair_prompt_only | 仅允许展示补齐提示 |
| metadata_prompt_only | 仅允许展示 metadata 边界提示 |
| committee_prompt_only | 仅允许展示委员会议题提示 |
| freeze_prompt_only | 仅允许展示冻结提示 |
| blocked_no_write | 阻断，不允许执行 |

## 4. 允许展示动作

允许展示：

- view_admission_summary；
- view_handoff_summary；
- view_missing_requirements；
- view_metadata_boundary；
- view_committee_note；
- view_freeze_note；
- view_no_write_notice；
- view_next_step_candidate。

这些动作只能触发展示，不得产生回执、队列、工单、证据、门禁结果或业务写回。

## 5. 必须阻断动作

必须阻断：

- create_read_receipt；
- create_admission_record；
- create_review_queue_item；
- create_kwe_work_item；
- create_confirmation_record；
- create_decision_record；
- create_waes_gate_result；
- persist_evidence；
- approve_business_write；
- promote_lifecycle；
- complete_committee_decision。

## 6. No-write 边界

Action Guard 不得直接执行以下动作：

- 创建 action receipt；
- 创建 read receipt；
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
