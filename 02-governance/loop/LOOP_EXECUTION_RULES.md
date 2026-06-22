---
doc_id: GPCF-DOC-04BF76145B
title: LOOP 执行规则
project: WAES
related_projects: [WAES]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_EXECUTION_RULES.md
source_path: 02-governance/loop/LOOP_EXECUTION_RULES.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP 执行规则

## 必读输入

每一轮 Loop 治理或执行在改文件之前，必须先读取当前仓库的执行说明和控制状态：

- `AGENTS.md`
- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `02-governance/loop/LOOP_AUTONOMY_POLICY.md`

如果上述任一文件缺失、为空或内部结论冲突，本轮必须停在治理修复，不得升级项目状态。

## 完成定义

Definition of Done：

只有满足以下适用条件时，Loop 轮次才可视为完成：

- 已声明范围和授权边界。
- 已记录输入、动作、输出、检查和反馈。
- 已列出验证命令或证据引用。
- 连续运行模式下已记录 `declared_rounds`、`substantive_rounds`、`generated_items`、`batch_generated`、`substance_gate` 和 `stop_type`。
- 当本轮不创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated 状态时，必须明确写出非声明边界。

## 不可绕过规则

- 文档或 validator 通过，不等于业务完成。
- 没有所需证据和人工授权，任何轮次都不得标记 `accepted` 或 `integrated`。
- 未取得明确授权并形成独立证据时，任何轮次都不得授权 production write、external API write、schema sync、bench migrate、deployment、permission change、commit 或 push。
