---
doc_id: GPCF-DOC-DDBD7C90C2
title: {项目名} 循环状态模板
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/loop-state-template.md
source_path: templates/loop-state-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# {项目名} 循环状态模板

> 复制此模板到项目仓 `docs/harness/loop-state.md`，替换 `{...}` 占位符。

## 当前循环

| 字段 | 值 |
|---|---|
| project | {项目名} |
| project_code | {项目代号，如 WA/GP/KD} |
| loop.round | {本轮序号，从 1 开始} |
| loop.current_step | {not_started / loop_ready / loop_running / evidence_ready / audit_ready / harness_review / accepted / integrated} |
| loop.last_entry | {上一轮输入：问题/需求/缺口} |
| loop.last_exit | {上一轮输出：文件 + 功能描述} |
| loop.gate_result | {pass / partial / fail} |
| loop.blockers | {阻塞项，无则填"无"} |
| loop.next_target | {下一轮目标} |

## 循环历史

| 轮次 | Round ID | 日期 | 输入摘要 | 输出摘要 | 门禁 | 证据完整率 | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | GPCF-{XX}-LR-001 | | | | | | |
