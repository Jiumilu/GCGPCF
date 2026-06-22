---
doc_id: GPCF-DOC-8E11A6C1C9
title: GFIS Assistant Repair Handoff Review Admission No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-handoff-review-admission-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-handoff-review-admission-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Handoff Review Admission No-write 规则

## 1. 定位

GFIS Assistant Repair Handoff Review Admission 是 DKS-113 `Repair Draft Handoff Packet` 之后的准入审查包。

它只判断 handoff packet 是否具备进入后续受控审阅候选的条件，包括人工审阅候选、metadata 边界审阅候选、委员会议题候选、冻结审阅候选或阻断保持候选。它不是正式审阅，不创建 KWE WorkItem，不创建 Review Queue Item，不创建 ConfirmationRecord / DecisionRecord，不写 WAES Gate Result，不推进 KDS lifecycle，不执行 GFIS / GPC / ERP / MES 写回。

## 2. 准入状态

| status | 说明 |
|---|---|
| admitted_candidate | 可作为后续审阅候选展示 |
| repair_required | 准入前需要补齐 |
| metadata_only_admitted | 仅 metadata 边界下可作为候选展示 |
| committee_agenda_blocked | 只能作为委员会议题候选，仍保持阻断 |
| freeze_review_blocked | 只能作为冻结审阅候选，仍保持阻断 |
| blocked_hold | 保持阻断，不进入任何真实队列 |

## 3. 准入决定

| decision | 说明 |
|---|---|
| allow_review_candidate | 允许展示为审阅候选 |
| require_repair | 要求补齐后再审 |
| metadata_only_review_candidate | 允许展示为 metadata 边界审阅候选 |
| prepare_committee_agenda_candidate | 仅准备委员会议题候选 |
| prepare_freeze_review_candidate | 仅准备冻结审阅候选 |
| hold_blocked | 保持阻断 |

## 4. 必查项

准入审查必须检查：

- handoff packet 引用完整；
- target candidate 与 handoff type 一致；
- metadata-only 边界不泄漏原文；
- blocked reason 有明确引用；
- required repair 不被当作已补齐；
- committee / freeze 只形成候选，不形成裁决；
- no-write guards 全部为 0。

## 5. No-write 边界

Admission Packet 不得直接执行以下动作：

- 创建 admission record；
- 创建 review queue item；
- 创建 KWE WorkItem；
- 创建 ConfirmationRecord；
- 创建 DecisionRecord；
- 创建 WAES Gate Result；
- 持久化 evidence；
- 提升 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 6. 后续关系

本准入包只给 Brain / PKC / GFIS Assistant 展示“可进入哪个候选审阅方向”的只读判断。任何真实工单、队列、裁决、证据、门禁结果或业务写回，都必须由后续独立受控流程创建并经 Harness evidence 固化。
