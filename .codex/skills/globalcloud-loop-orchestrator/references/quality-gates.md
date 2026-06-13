---
doc_id: GPCF-DOC-E2C4007859
title: GlobalCloud Loop Quality Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/quality-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/quality-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Quality Gates

## Definition of Done

每轮 Loop 的 Done 必须同时满足：

- 本轮目标与输出一一对应。
- 关键路径有测试、检查或人工复现记录。
- 质量问题和遗留风险已登记。
- 相关文档、evidence、Git 记录已更新。

## 质量 evidence

| evidence | 要求 |
|---|---|
| `quality-check-{ID}.md` | 质量检查项、结果、缺陷、豁免 |
| `test-result-{ID}.md` | 自动化或人工测试结果 |
| `defect-log-{ID}.md` | 缺陷、严重度、处理状态 |

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 无质量 evidence | `partial` |
| P0/P1 缺陷未关闭 | `blocked` |
| 质量 evidence 通过 | 可进入下一门禁 |
