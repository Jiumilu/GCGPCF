---
doc_id: GPCF-DOC-5FD0A7402A
title: GlobalCloud Loop Evolution Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/evolution-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/evolution-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Evolution Gates

## 目标

Loop 必须把经验反馈到下一轮，而不是重复犯同类错误。

## 每轮复盘

- 本轮最大偏差。
- 本轮最高风险。
- 哪条规则需要补强。
- 哪个模板需要更新。
- 哪个技能需要调整。
- 下一轮必须避免的错误。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 无复盘记录 | `partial` |
| 同类问题连续出现 3 次 | `rework_required` |
| 复盘形成下一轮约束 | 可进入下一轮 |
