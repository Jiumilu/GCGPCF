---
doc_id: GPCF-DOC-1AB33594
title: design
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: in_progress
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-panorama-operation-normalization/design.md
source_path: openspec/changes/spaceai-panorama-operation-normalization/design.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-panorama-operation-normalization · Design

## 1. 操作契约（先定语义，再改实现）

每个用户动作必须只有三种终局：成功（有可见结果）、失败（有原因 + 可恢复）、被门禁拦下（说明缺什么）。
**禁止假成功**：数据未落库、回投未确认、AI 无结果时，不得提示成功。

- B0 用 6 例护栏锁住语义（先红后绿：先写会红的测试，再改实现转绿）。
- B1 修六组 P0：假成功、反馈通道（Toast 与视图解耦）、派单门禁、CWME 回投门禁、驾驶 Esc、AI 结果可见。

## 2. 键盘与 Esc 分层（单一契约）

- Esc 逐层退出：面板 → 卡片配置 → 帮助；每层只处理自己那层，不得一次全关。
- 键位集中在 `panorama/keys.ts` 注册表；`?` 打开帮助，帮助内容由注册表渲染（不再手写两份）。
- 键盘作用域：输入框聚焦时不劫持快捷键；驾驶模式退出用常驻胶囊 + Esc 双通道。
- 演示态互斥：大屏 / 巡演 / 回放 / 驾驶互斥，开启一个自动停其他（并有测试）。

## 3. 偏好键收口

- 统一前缀 `gc.pano.*`，共 22 键登记在 `docs/panorama-prefs.md`；
- 读取做合并冲突保护（B4b）：非法值回落默认、版本字段兼容旧键；
- 导出前脱敏（B4）：不导出敏感字段。

## 4. 入口收敛与命令面板

- D1–D7 入口收敛：同一动作只保留一处主入口，小应用不重复工具栏 5 项；
- ⌘K 命令面板 28 条命令，覆盖导航/演示/卡片/帮助；命令即入口，减少工具栏膨胀。

## 5. 组件拆分边界（与 F-024 / spaceai-platform-panorama-convergence 的关系）

- 本变更把「视图级」大块拆为组件（PanoramaHelp / PanoramaPalette / PanoramaBubbles），
  把「状态与逻辑」外提为组合式（useFeedback / useCardConfig / useCameraModes / useCardOrder / useDemoModes）；
- 不改变模板结构与视觉语义（拆分前先有测试）；
- 与 `spaceai-platform-panorama-convergence` 的 8 域收敛**不重复记账**：那条线记纯模块与行为基线，本线记操作规范与视图拆分。

## 6. 验收口径

- 单测：本变更相关 35 例；全仓 136 文件 / 1251 例；`pnpm typecheck` 0；
- e2e：`panorama-operate.spec.ts` 5/5（真实 Chrome），并断言 0 页面错误；
- 结构指标：组件 3711 行、panorama `use*` 组合式 11 个；
- **人工验收缺口**（不在自动断言内）：派单确认/失败保留、CWME 回投确认/30s 幂等，需真实气泡与面板状态。

## 7. 已知取舍

- 先修语义与门禁（用户可感知的事故），再做 i18n 与剩余组件外提；
- B5 剩余四大块（卡片列 / 飞翔 / CWME / 控制器）与约 600 行中文硬编码留待下一轮；
- 不引入新状态管理库、不改接口契约、不改数据库。
