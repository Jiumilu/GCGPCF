---
doc_id: GPCF-DOC-527915D070
title: GFIS Assistant Repair Admission Read Model No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-admission-read-model-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-admission-read-model-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Admission Read Model No-write 规则

## 1. 定位

GFIS Assistant Repair Admission Read Model 是 DKS-114 `Repair Handoff Review Admission` 之后的只读展示模型。

它把 admission packet 转换为 Brain、PKC、GFIS Assistant 可读取的展示视图，说明当前候选的审阅方向、阻断原因、metadata-only 边界、缺口提示和 no-write 警示。它不是 KWE 队列，不是正式 AdmissionRecord，不是 ConfirmationRecord / DecisionRecord，不写 WAES Gate Result，不推进 KDS lifecycle，也不写 GFIS / GPC / ERP / MES。

## 2. 视图类型

| view_type | 说明 |
|---|---|
| brain_governance_read | Brain 治理视图 |
| pkc_owner_read | PKC 个人/团队授权视图 |
| gfis_assistant_read | GFIS Assistant 只读解释视图 |
| committee_candidate_read | 委员会议题候选只读视图 |
| freeze_candidate_read | 冻结关注候选只读视图 |

## 3. 可见性模式

| visibility_mode | 说明 |
|---|---|
| own_project_only | 仅本项目授权可见 |
| metadata_only | 只展示 metadata，不展示原件正文 |
| governance_summary | 只展示治理摘要 |
| committee_authorized | 仅委员会授权视图 |
| freeze_authorized | 仅冻结审阅授权视图 |

## 4. 展示规则

Read Model 可以展示：

- admission 状态和决定；
- handoff 摘要；
- target candidate；
- missing requirement refs；
- blocked reason refs；
- metadata ref bundle；
- no-write notice；
- 下一步候选提示。

Read Model 不得展示：

- 原始合同、金融凭证、POD、质量争议原文；
- 未授权单位明细；
- 可被误认为正式写回、正式确认或委员会裁决的状态；
- KDS accepted / published 完成结论；
- 收益、积分、额度、悬赏确认结果。

## 5. No-write 边界

Read Model 不得直接执行以下动作：

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

## 6. 后续关系

Read Model 只能作为 Brain / PKC / GFIS Assistant 的只读解释材料。任何真实工单、队列、裁决、证据、门禁结果或业务写回，必须由后续独立受控流程创建，并经 Harness evidence 固化。
