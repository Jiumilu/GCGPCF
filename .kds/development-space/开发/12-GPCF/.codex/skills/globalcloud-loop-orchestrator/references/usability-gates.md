---
doc_id: GPCF-DOC-221282A70B
title: GlobalCloud Loop Usability Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/usability-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/usability-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Usability Gates

## 可用性定义

可用不是“文件存在”，而是目标用户可以按说明完成关键任务。

## 每轮最小可用性 evidence

- 关键路径复现步骤。
- 运行命令或访问入口。
- 截图、录屏、日志或人工试用记录。
- 失败场景和恢复方式。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 无可用性 evidence | `partial` |
| 关键路径不可复现 | `blocked` |
| 只完成文档但无使用路径 | `partial` |
| 可用性验证通过 | 可进入客户满意门禁 |
