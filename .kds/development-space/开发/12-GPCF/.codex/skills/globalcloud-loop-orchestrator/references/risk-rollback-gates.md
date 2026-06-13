---
doc_id: GPCF-DOC-1213F2E70E
title: GlobalCloud Loop Risk and Rollback Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/risk-rollback-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/risk-rollback-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Risk and Rollback Gates

## 风险等级

| 等级 | 含义 |
|---|---|
| P0 | 数据丢失、安全泄漏、生产不可用 |
| P1 | 主流程不可用、客户无法完成关键任务 |
| P2 | 局部功能退化、有替代路径 |
| P3 | 文档、体验或低风险改进 |

## 必备记录

- 影响范围。
- 风险等级。
- 回滚或撤销方案。
- 发布后观察点。
- 是否需要人工确认。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| P0/P1 无回滚方案 | `blocked` |
| 风险未登记 | `partial` |
| 需要人工确认但未确认 | `manual_confirmation_required` |
| 风险和回滚完整 | 可进入下一门禁 |
