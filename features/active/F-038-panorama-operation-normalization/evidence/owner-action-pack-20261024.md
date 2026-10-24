---
doc_id: GPCF-DOC-F038-OWNER-PACK-20261024
title: F-038 SpaceAI 属主动作包
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# F-038 属主动作包

## 已完成（可复核）

- map-3d tests 793 passed / 86 files；tsc 0；
- B5 已见 PanoramaBubbles / PanoramaCardColumn / PanoramaCtrl 组件与 usePanoEngine 等外提。

## 需 SpaceAI 属主

1. 继续 B5：把 PanoramaDeep script 1273 行降到 <800；
2. i18n：约 600 行中文硬编码迁 `T()`；
3. 人工验收：派单确认/失败保留、CWME 回投/30s 幂等；
4. 完成后跑 `pnpm vitest run plugins/map-3d/tests` + `tsc --noEmit`。

## GPCF 可提供

- 当前代码状态证据 `evidence/current-code-state-20261024.md`；
- 测试/类型基线。

## 非声明

- 不声明 F-038 可关闭；不声明人工验收已完成。
