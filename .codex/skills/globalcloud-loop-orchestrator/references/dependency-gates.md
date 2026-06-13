---
doc_id: GPCF-DOC-7D1942C7DD
title: GlobalCloud Loop Dependency Gates
project: GPCF
related_projects: [WAES, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/dependency-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/dependency-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Dependency Gates

## 目标

每轮 Loop 必须说明对其它项目的影响，避免单项目推进破坏项目群主线。

## 必备记录

- 上游依赖。
- 下游影响。
- 接口或数据契约变化。
- 阻塞传播范围。
- 版本兼容要求。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 跨项目影响未登记 | `partial` |
| 已知上游阻塞未解决 | `blocked` |
| 接口破坏未通知下游 | `rework_required` |
| 依赖清单完整 | 可进入下一门禁 |
