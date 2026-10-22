---
doc_id: GPCF-SPACEAI-PANORAMA-DESIGN-20261016
title: design
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: implemented
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-platform-panorama-convergence/design.md
source_path: openspec/changes/spaceai-platform-panorama-convergence/design.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## 1. 抽取口径（唯一硬约束）

**先建测试、后抽取**：每个域的行为基线测试必须先于该域的抽取提交存在，且测试在抽取前后均为绿。禁止"先抽完再补测试"。

**模板不动**：`PanoramaDeep.vue` 保留 `<template>` 与装配职责。本轮不改 DOM 结构、类名与样式变量——这是"视觉零变化"的判定基础。

**抽取只搬不改**：抽取过程中不修正被搬运逻辑的行为。发现的缺陷单独记账（记入 tasks 的"发现但不修"清单），不在本轮修。

## 2. 域划分与职责

PanoramaDeep.vue 现有 60 个 `// ──` 分段，按内聚度归并为 8 个域。新增目录 `plugins/map-3d/src/panorama/`，每个域一个 composable（或纯模块）：

| # | 模块 | 吸收的现有分段 | 形态 |
|---|---|---|---|
| 1 | `cards.ts` | 卡片多面数据、内容面清单、卡片分类体系(10 类)、卡片列计算 | 纯函数 + 常量 |
| 2 | `cardLayout.ts` | 场景完整布局、场景→卡片联动、B10 卡组 / B11 拼图 | 纯函数（输入场景 + 卡片集 → 布局） |
| 3 | `useCardPrefs.ts` | 拖拽位置(磁贴)、底图切换、卡片透明度、场景控制器状态 | composable（读写 store + 清洗） |
| 4 | `useReplay.ts` | 回放、B9 时间轴回放联动、轨迹回放 | composable（游标 + 截断） |
| 5 | `usePresentation.ts` | 大屏展示态、大屏轮巡、C12 多屏投放、C13 关联高亮、C14 态势色带 | composable |
| 6 | `useMapInteraction.ts` | 点选映射、地图移动检测、气泡系统、POI 聚合、视域分析/覆盖热力、右键菜单、空间检索、底图 | composable |
| 7 | `useFavorites.ts` | 资产层级导航、收藏夹、飞翔模式、快捷航线、分享/导入 | composable |
| 8 | `usePanoramaFx.ts` | A1 数据流动效、A2 心跳、A4 聚焦放大、A6 音效、A1 feed 监听、特效（环绕/运镜/驾驶） | composable |

**明确不抽取**（留在组件内）：数据加载与生命周期编排、视图/视图切换、多国语言响应式、模板内联交互。

## 3. 副作用收口（性能前置条件）

域 8 与域 5/6 持有定时器、事件监听、Web Audio 节点、`requestAnimationFrame` 与 Cesium 回调。抽取时必须：

- 全部副作用在 `onScopeDispose`/`onUnmounted` 中可回收，禁留裸 `setInterval`。
- 动画与音效受单一开关控制（沿用现有"可开关"语义，不新增开关）。
- 导出可测的"当前活跃副作用计数"（仅用于测试断言，不进入 UI）。

这是后续无 GPU 环境优化的前提：**不能回收的副作用无法优化**。

## 4. 测试策略

- 载体：Vitest + happy-dom；位置 `plugins/map-3d/tests/panorama-*.test.ts`；沿用仓内既有夹具与 `vitest.setup.ts` 的临时目录隔离规则（不得触碰运行库 `data/spaceai.db`）。
- 纯模块（域 1/2）覆盖到分支：卡片列计算、场景布局不变量（每场景两列铺满、左一=实时事件大卡）、分类体系、拼图/卡组。
- composable（域 3–8）用最小夹具驱动：断言公开状态与方法契约，不断言 DOM 细节。
- 副作用测试：挂载→卸载后断言活跃副作用归零。
- 数据一致性：涉及持久化的域，测试必须覆盖"坏数据清洗"（与平台既有 prefs 防御口径一致）。

## 5. 视觉零回归判定

在抽取前建立基线、抽取后比对：

- 环境：Playwright + Chromium，1600×900 与 1600×1000 两档；登录后在 SPA 内点侧栏进入全景态势（整页 `goto('/panorama')` 会丢会话，已验证）。
- 产物：两档截图 + DOM 节点数 + JS 堆 + FPS；写入 `harness/runs/<run-id>/evidence/`。
- 判定（2026-10-16 修订）：以**结构指标为主判据**——DOM 节点数变化 ≤ 5%、卡片数一致、接口集合一致（实测 27 个 `/RestFul`）、无**新增错误类型**；辅以目视确认关键要素在位（卡片列/地图/控制器/区域列表/底栏）与卡片数值一致。
- **像素 diff 不适用**：全景态势是实时变化视图（地图地块、事件流时间戳、时钟、未读报警数在两次采集间必然变化），实测差异达 58.44%（1600×900）与 4.22%（1600×1000），衡量的是采集时刻差异而非改动引起的变化。已实测记录于 `harness/runs/20261016-panorama-convergence/domain-1-record.json` 的 `protocol_correction`。
- 接口基线口径：实测进入全景态势共 **27** 个 `/RestFul` 端点（proposal 记载的 14 为组件内显式调用点数，两者口径不同，以实测集合为准）。

## 6. 性能基线（本轮产出，不作验收门槛）

记录并归档：JS 堆、DOM 节点数、进入耗时、FPS（有头，Apple M4）、FPS（无头 SwiftShader，代表无 GPU 环境）。用途是为后续优化提供可比基线；**本轮不以性能数值作为通过条件**，也不承诺优化幅度。

## 7. 风险与对策

| 风险 | 对策 |
|---|---|
| 抽取引入微妙行为变化（565 处响应式声明，跨域耦合） | 先测后抽；每域独立提交，可单独 revert |
| 模板依赖 script 内部实现细节 | 抽取后保留同名解构导出，模板零改动 |
| 3351 行文件在编辑中丢失内容 | 每域提交前后比对函数清单与行数差异，逐项核对 |
| 测试写成"实现镜像"（改实现就挂） | 断言公开契约与不变量，不断言内部函数名 |
| 无 GPU 环境下测量噪声 | FPS 仅作基线记录，判定标准用错误数与 DOM/接口一致性 |

## 8. 非目标

不新增业务功能；不改视觉与交互；不改接口契约与数据库；不做性能优化本身；不接入真实设备；不发布、不提升验收状态。
