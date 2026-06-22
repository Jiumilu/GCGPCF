---
doc_id: GPCF-DOC-659DE796AC
title: GFIS Assistant Repair Prompt Checklist No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-prompt-checklist-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-prompt-checklist-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Prompt Checklist No-write 规则

## 1. 定位

GFIS Assistant Repair Prompt Checklist 是 DKS-108 `GFIS Assistant WAES Guidance Packet` 之后的操作补证清单。

它把 guidance packet 中的门禁解释和补证提示转成可展示、可勾选、可追踪的 checklist 候选，帮助操作人员理解还缺哪些来源、证据、权限确认、metadata-only 处理或委员会材料。

## 2. No-write 边界

Checklist 只能展示补证要求，不得直接执行以下动作：

- 提交资料；
- 创建真实 KWE WorkItem；
- 创建 GapRecord 或 BountyRecord；
- 写入 WAES Gate Result；
- 改变 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 3. Checklist 项类型

| 类型 | 说明 |
|---|---|
| source_repair | 来源登记补齐 |
| evidence_repair | 证据补齐 |
| owner_confirmation | 责任人确认 |
| metadata_only_review | metadata-only 范围确认 |
| committee_material | 委员会材料准备 |
| freeze_risk_material | 冻结风险材料准备 |

## 4. Checklist 状态

| status | 说明 |
|---|---|
| open | 待处理 |
| ready_for_submission | 资料可提交为后续候选 |
| repair_required | 仍需补充 |
| blocked | 阻断保持 |

## 5. 允许展示动作

允许：

- show_repair_item；
- show_required_evidence；
- show_metadata_boundary；
- show_owner_confirmation；
- show_committee_material；
- show_freeze_risk_material。

必须阻断：

- submit_evidence；
- create_gap_record；
- create_bounty_record；
- create_kwe_work_item；
- create_waes_gate_result；
- approve_business_write；
- promote_lifecycle。

## 6. 与 GFIS Assistant 的关系

Repair Prompt Checklist 不是资料提交，不是验收通过，不是写回批准。

它只把 GFIS Assistant 的 WAES guidance 转成操作人员可读的候选清单。任何资料提交、缺口创建、门禁结果、工单、状态提升或业务写回，都必须进入后续受控流程。
