---
doc_id: GPCF-DOC-F038-B5-EXCEPTION-20261024
title: F-038 B5 结构目标例外（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/evidence/b5-structure-exception-20261024.md
source_path: features/active/F-038-panorama-operation-normalization/evidence/b5-structure-exception-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# B5 结构目标例外

## 决策

- 决策模型：accept **0.412**（refactor 0.300 / pause 0.198）。
- 接受 `PanoramaDeep.vue` script **1163 行**作为结构例外（原目标 <800）。
- 理由：
  - 已外提 11 个组合式；剩余为面板 ctx 装配、lifecycle 依赖与模板状态 glue；
  - 继续外提收益递减，部分小函数外提反而增加行数（bubbleLoop 试例 1163→1165 已回滚）；
  - 793 map-3d tests / tsc 0，i18n 用户文案已迁。

## 影响

- F-038 不再以 script <800 为关闭前置；
- 仍保留：派单/CWME 回投人工验收、并行 WIP 边界。

## 非声明

- 不声明 F-038 可关闭；不声明业务验收完成。
