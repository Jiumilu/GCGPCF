---
doc_id: GPCF-DOC-F038-B5-RESIDUAL-20261024
title: F-038 B5 剩余结构收口计划（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/evidence/b5-residual-plan-20261024.md
source_path: features/active/F-038-panorama-operation-normalization/evidence/b5-residual-plan-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# B5 剩余结构收口计划

## 现状

- `PanoramaDeep.vue` script **1163 行**（目标 <800，差约 363）。
- 已外提 11 个组合式（NLU/聚焦/图层/场景卡/HUD/Pulse/偏好同步/卡组/回放窗口/团队任务/模式）。
- `map-3d` 793 tests / tsc 0；i18n 用户文案已迁。

## 剩余块（估算）

| 块 | 估算行 | 说明 |
|---|---:|---|
| 面板 ctx 组装（card/fly/cwme/ctrl） | ~70 | 已由 build*Ctx 承载，调用点仍长 |
| lifeCycle 依赖装配 | ~50 | 40+ 回调注入 |
| 控制器/面板 composable 调用与解构 | ~150 | 多为一一映射 |
| 模板绑定/状态 glue | ~90 | 难以外提 |

## 选项

1. **接受 1163**：由 SpaceAI 属主登记结构例外，关闭 B5 目标（需授权）。
2. **继续逐块外提**：预计 20–30 轮，收益递减，且调用开销可能反增行数。
3. **装配尾重构**：把 20+ composable 调用收口到一个 `usePanoramaControllers(deps)`；一次性减少 ~100 行，但风险较高。

## 建议

- 先做选项 3 的试点（面板 ctx + 简单 composable 组），每步跑 793 tests + tsc；
- 若 3 轮内不能净减 ≥50 行，转选项 1 由属主裁定。

## 非声明

- 不声明 F-038 可关闭；不改 SpaceAI 代码。
