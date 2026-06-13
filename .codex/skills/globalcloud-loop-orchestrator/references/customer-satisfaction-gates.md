---
doc_id: GPCF-DOC-879AE787BD
title: GlobalCloud Loop Customer Satisfaction Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/customer-satisfaction-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/customer-satisfaction-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Customer Satisfaction Gates

## 客户满意定义

客户满意度用于判断成果是否值得继续扩大，不用于替代技术验收。

## 必备记录

- 反馈对象：用户、客户、业务负责人或代理验收人。
- 反馈结论：满意 / 部分满意 / 不满意 / 未收集。
- 关键意见：最多 5 条。
- 下一轮处理：采纳、拒绝或待确认。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 未收集且无豁免 | `partial` |
| 明确不满意 | `rework_required` |
| 存在 P0/P1 客户问题 | `blocked` |
| 满意且无高优先级问题 | 可申请 `accepted` |
