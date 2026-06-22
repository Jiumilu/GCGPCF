---
doc_id: GPCF-DOC-0214F1962A
title: GFIS Assistant Repair Submission Intake No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-submission-intake-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-submission-intake-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Submission Intake No-write 规则

## 1. 定位

GFIS Assistant Repair Submission Intake 是 DKS-109 `Repair Prompt Checklist` 之后的提交意向候选包。

它把已处理或仍被阻断的 checklist 转成可审阅的 intake request，表达“用户准备提交什么、引用哪些 metadata/evidence hint、建议进入哪类人工路径”。它不是资料提交，不是 KWE 工单，不是 GapRecord，不是 BountyRecord，也不是 WAES Gate Result。

## 2. No-write 边界

Intake 只能作为提交前候选，不得直接执行以下动作：

- 提交 evidence；
- 持久化 evidence；
- 创建 GapRecord 或 BountyRecord；
- 创建 KWE WorkItem；
- 写入 WAES Gate Result；
- 推进 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 3. Intake 状态

| status | 说明 |
|---|---|
| draft | 仍在整理提交意向 |
| ready_for_review | 可供人工审阅提交意向 |
| repair_required | 提交意向仍缺少必要引用 |
| blocked | 由于委员会、冻结或敏感边界保持阻断 |

## 4. 推荐路径

| route | 说明 |
|---|---|
| human_review | 建议人工审阅 |
| committee_review | 建议委员会审阅 |
| metadata_boundary_review | 建议 metadata-only 边界审阅 |
| freeze_review | 建议冻结风险审阅 |
| blocked_hold | 保持阻断，不进入提交 |

## 5. 允许展示动作

允许：

- show_intake_summary；
- show_required_refs；
- show_metadata_boundary；
- show_recommended_route；
- show_blocked_reason。

必须阻断：

- submit_evidence；
- persist_evidence；
- create_gap_record；
- create_bounty_record；
- create_kwe_work_item；
- create_waes_gate_result；
- approve_business_write；
- promote_lifecycle；
- complete_committee_decision。

## 6. 与后续流程的关系

Repair Submission Intake 只能作为人工审阅前的候选输入。

后续如果确需提交资料，必须进入单独的受控提交流程；如果确需创建缺口、悬赏、KWE 工单、WAES Gate Result 或业务写回，必须分别通过 KWE、WAES、Harness evidence 和人工/委员会确认，不得由 GFIS Assistant 直接完成。
