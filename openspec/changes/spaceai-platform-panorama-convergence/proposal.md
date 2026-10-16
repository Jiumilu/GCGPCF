---
doc_id: GPCF-SPACEAI-PANORAMA-PROPOSAL-20261016
title: proposal
project: KDS
related_projects: [KDS, GPC, WAME, Brain, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-platform-panorama-convergence/proposal.md
source_path: openspec/changes/spaceai-platform-panorama-convergence/proposal.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## Why

全景态势（`plugins/map-3d/src/views/PanoramaDeep.vue`）已是 GlobalCloud SpaceAI Platform 的事实主界面：进入指挥舱后的第一视图，聚合三维地图、事件流、研判、处置与多屏投放。但它的工程形态已成为迭代瓶颈。

2026-10-16 实测（真实浏览器，非推测）：

| 维度 | 实测值 |
|---|---|
| 组件规模 | 3351 行（script 2361 / template 630），全仓最大单个 view，第二名 FocusDeep 2379 行 |
| 内部复杂度 | 410 个顶层函数、565 处响应式声明，25 个功能块（A1–A6 动效 / B7–B11 大屏 / C12–C15 投放联动）同处一文件 |
| 专项测试 | **0**：`map-3d/tests/` 四个测试文件无一覆盖 PanoramaDeep，全仓无测试引用 |
| 运行时内存 | JS 堆 290–373 MB（Apple M4 / Chrome，1600×900） |
| 渲染 | 有头 71 FPS；无 GPU 环境（SwiftShader）仅 4–5 FPS |
| 接口依赖 | 14 个 `/RestFul` 端点，横跨 3DMap / Brain / Focus / Alarm / Audit / Disposal / Notify 七域 |
| 改动方式 | 近 15 次提交中 5 次为用户反馈缺陷修复（加载慢、全屏不自适应、弹层重叠、卡片透明度、关闭操作），另有 3 次整批巡查修复 |

结论：**上一阶段靠人工逐条反馈驱动修补，缺少自动化回归约束**。在 3351 行、零测试的文件上做任何功能迭代，回归风险不可控；用户已确认实际部署环境包含**虚拟机/远程桌面（无独立显卡）**，后续性能优化同样需要这层基线保护。

## What Changes

- 按域把 PanoramaDeep 的状态与逻辑抽为 Vue 3 composable，置于 `plugins/map-3d/src/panorama/`；PanoramaDeep.vue 保留模板与装配职责。
- 先补行为基线测试（Vitest + happy-dom），锁住抽取域的当前行为，再实施抽取；测试覆盖卡片集合与场景布局、回放游标与截断、卡片配置持久化与清洗、投放内容生成。
- 显式清理副作用生命周期（定时器、监听、Web Audio、rAF），为后续性能优化建立可回收基础，不改变现有视觉与交互。
- 交付可复现的前后对照证据：单测结果 + 真实浏览器 1600×900 与 1280 两档截图对照 + 运行时指标（堆、DOM、FPS）。

### New Capabilities
- `spaceai-platform-panorama-structure`: 全景态势的模块化结构与行为基线——域边界、抽取后的公开契约、基线测试清单、视觉零回归判定口径。

### Modified Capabilities
无。不修改既有端点契约（`packages/protocol`）与插件装配契约（`packages/plugin-sdk`）。

## Impact

- Program：GlobalCloud SpaceAI；Project：SpaceAI；仓：`GlobalCloud SpaceAI Platform`（独立 Git 仓，远端 `GCSpaceAI`）。
- 只动 `plugins/map-3d/src/views/PanoramaDeep.vue` 与新增 `plugins/map-3d/src/panorama/**`、`plugins/map-3d/tests/**`；不动 `apps/server`、`packages/*`、其它插件。
- 运行库 `data/spaceai.db` 不改；不新增接口、不改 schema、不改权限模型。
- 非目标：新增业务功能、视觉改版、性能优化本身（本轮只建立其前置基线）、真实设备接入、生产发布、业务验收提升。
- authorization：用户 2026-10-16 确认方向 A「工程收敛」、场景含指挥中心大屏与虚拟机/远程桌面、按 OpsX Full Cycle 交付。confirmation：业务验收与生产发布未确认。
- 回滚：本轮改动集中在插件内，按 git revert 针对本轮提交撤销；不 reset/clean/force push。
- 文档门禁当前为 rework_required（`gpcf_2_feature_workspace`、`icp_project_registration`、`localization_debt`，均 GPCF 全局既有问题）；项目状态保持 partial，本地验证通过不提升验收状态。
