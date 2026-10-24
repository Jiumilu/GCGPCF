---
doc_id: GPCF-DOC-F038-CODE-STATE-20261024
title: F-038 当前代码状态复核（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/evidence/current-code-state-20261024.md
source_path: features/active/F-038-panorama-operation-normalization/evidence/current-code-state-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-038 当前代码状态复核

## 事实

- `plugins/map-3d/src/views/PanoramaDeep.vue`：**1904 行**；`<script setup>` 段 **1273 行**（目标 <800 未达）。
- 已外提组件/组合式（现行代码可见）：
  - `components/PanoramaBubbles.vue`
  - `components/PanoramaCardColumn.vue`
  - `components/PanoramaCtrl.vue`
  - `panorama/usePanoEngine.ts` 及 B5 系列 use* 组合式
- 与 10-22 证据相比，五块中至少气泡/卡列/控制器已有独立组件；`PanoramaDeep.vue` 仍保留装配与剩余状态机。

## 仍未满足（按 Feature 边界）

1. script <800 行未达；
2. i18n 约 600 行中文硬编码未迁；
3. 人工验收（派单/CWME 回投）未做。

## 结论

- F-038 仍 active；本轮不改 SpaceAI Platform 代码。
- 若继续，应先在 SpaceAI Platform 侧跑测试/typecheck 并确认并行 WIP 边界。

## 测试与类型检查（2026-10-24 复核）

- `pnpm vitest run plugins/map-3d/tests`：**793 passed / 86 files**。
- `pnpm exec tsc --noEmit -p plugins/map-3d/tsconfig.json`：**exit 0**。
- 说明：现有 map-3d 代码测试/类型健康；F-038 剩余为 B5 结构目标、i18n 与人工验收，不是回归。

## 边界

- 本轮未改 SpaceAI Platform 代码。

## B5 外提增量（2026-10-24）

- 新增 `panorama/usePanoNlu.ts`：B7 一句话上屏规则解析外提；
- `PanoramaDeep.vue` script 1273 → **1254** 行（目标 <800）；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## B5 外提增量 2（2026-10-24）

- 新增 `panorama/useCardFocus.ts`：A4/A5 聚焦与双击快捷动作外提；
- script 1254 → **1246** 行；793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## B5 外提增量 3（2026-10-24）

- 新增 `panorama/usePanoLayers.ts`：图层状态/ID/开关外提；
- script 1246 → **1238** 行；793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## B5 外提增量 4（2026-10-24）

- 新增 `panorama/usePanoSceneCards.ts`：场景谓词/左右卡列/配对并排外提；
- script 1238 → **1231** 行；793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## B5 外提增量 5（2026-10-24）

- 新增 `panorama/usePanoHud.ts`：值班时钟 + 悬停地图联动外提；
- script 1231 → **1222** 行；793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## B5 外提增量 6（2026-10-24）

- 新增 `panorama/usePanoPulse.ts`：数值闪动 + 心跳速率外提；
- script 1222 → **1209** 行；793 tests / tsc 0；SpaceAI main 本地提交（未 push）。
