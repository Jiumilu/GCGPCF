---
doc_id: GPCF-DOC-A705FE83D1
title: GFIS Assistant Repair Review Decision Draft No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-review-decision-draft-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-review-decision-draft-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Review Decision Draft No-write 规则

## 1. 定位

GFIS Assistant Repair Review Decision Draft 是 DKS-111 `Repair Intake Review Packet` 之后的审阅意见草稿。

它把 review packet 转成可展示的建议处置草稿，用于表达人工建议、metadata 边界备注、委员会议题备注或冻结风险备注。它不是人工确认，不是委员会决议，不是 DecisionRecord，不是 ConfirmationRecord，也不是 WAES Gate Result。

## 2. No-write 边界

Decision Draft 不得直接执行以下动作：

- 提交或持久化 evidence；
- 创建 Review Queue Item；
- 创建 ConfirmationRecord；
- 创建 DecisionRecord；
- 创建 KWE WorkItem；
- 创建 GapRecord 或 BountyRecord；
- 写入 WAES Gate Result；
- 推进 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 3. Draft 类型

| type | 说明 |
|---|---|
| human_action_draft | 人工建议动作草稿 |
| metadata_boundary_note | metadata-only 边界备注 |
| committee_agenda_note | 委员会议题备注 |
| freeze_note | 冻结风险备注 |
| blocked_hold_note | 阻断保持备注 |

## 4. Draft 状态

| status | 说明 |
|---|---|
| draft | 草稿 |
| needs_repair | 仍需补齐 |
| blocked | 阻断保持 |
| metadata_only | 仅 metadata 可展示 |

## 5. 建议处置

| disposition | 说明 |
|---|---|
| request_more_evidence | 建议补证 |
| keep_metadata_only | 建议保持 metadata-only |
| prepare_committee_agenda | 建议准备委员会材料 |
| keep_frozen | 建议保持冻结风险处理 |
| hold_blocked | 建议保持阻断 |

## 6. 允许展示动作

允许：

- show_decision_draft；
- show_reviewer_note；
- show_required_repair；
- show_metadata_boundary；
- show_committee_agenda_note；
- show_freeze_note；
- show_no_write_notice。

必须阻断：

- submit_evidence；
- persist_evidence；
- create_review_queue_item；
- create_confirmation_record；
- create_decision_record；
- create_kwe_work_item；
- create_gap_record；
- create_bounty_record；
- create_waes_gate_result；
- approve_business_write；
- promote_lifecycle；
- complete_committee_decision。

## 7. 与后续流程的关系

Decision Draft 只是 GFIS Assistant 可展示的意见草稿。后续如果确需形成人工确认、委员会决议、DecisionRecord、ConfirmationRecord、KWE 工单、WAES Gate Result 或业务写回，必须由独立受控流程完成，并由 Harness evidence 固化，不能由本草稿直接完成。
