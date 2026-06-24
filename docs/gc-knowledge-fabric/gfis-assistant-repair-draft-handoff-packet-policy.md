---
doc_id: GPCF-DOC-1AA2080A82
title: GFIS Assistant Repair Draft Handoff Packet No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-draft-handoff-packet-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-draft-handoff-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Draft Handoff Packet No-write 规则

## 1. 定位

GFIS Assistant Repair Draft Handoff Packet 是 DKS-112 `Repair Review Decision Draft` 之后的移交候选包。

它把审阅意见草稿整理为可交给后续受控流程的候选输入，说明建议交给人工审阅、metadata 边界审阅、委员会准备、冻结关注或阻断保持。它不是实际移交，不创建 KWE WorkItem，不创建人工队列、委员会队列、ConfirmationRecord、DecisionRecord 或 WAES Gate Result。

## 2. No-write 边界

Handoff Packet 不得直接执行以下动作：

- 提交或持久化 evidence；
- 创建 Handoff Record；
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

## 3. Handoff 类型

| type | 说明 |
|---|---|
| human_review_handoff | 人工审阅移交候选 |
| metadata_boundary_handoff | metadata-only 边界移交候选 |
| committee_agenda_handoff | 委员会议题移交候选 |
| freeze_review_handoff | 冻结关注移交候选 |
| blocked_hold_handoff | 阻断保持移交候选 |

## 4. Handoff 状态

| status | 说明 |
|---|---|
| draft | 候选包草稿 |
| ready_for_handoff_review | 可供移交前审阅 |
| needs_repair | 仍需补齐 |
| blocked | 阻断保持 |
| metadata_only | 仅 metadata 可展示 |

## 5. 建议目标

| target | 说明 |
|---|---|
| kwe_human_review_candidate | 建议进入 KWE 人工审阅候选 |
| metadata_boundary_review_candidate | 建议进入 metadata 边界审阅候选 |
| committee_agenda_candidate | 建议进入委员会议题候选 |
| freeze_review_candidate | 建议进入冻结审阅候选 |
| blocked_hold_candidate | 建议保持阻断候选 |

## 6. 允许展示动作

允许：

- show_handoff_packet；
- show_target_candidate；
- show_required_repair；
- show_metadata_boundary；
- show_committee_agenda_note；
- show_freeze_note；
- show_no_write_notice。

必须阻断：

- submit_evidence；
- persist_evidence；
- create_handoff_record；
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

Handoff Packet 只是 GFIS Assistant 可展示的移交候选包。后续如果确需进入 KWE、人工审阅、委员会、冻结流程或任何业务写回，必须由独立受控流程创建正式记录，并由 Harness evidence 固化，不能由本候选包直接完成。
