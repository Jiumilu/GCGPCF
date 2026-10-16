---
doc_id: GPCF-OS-PANORAMA-STRUCTURE-SPEC-20261016
title: 全景态势模块化结构与行为基线
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-platform-panorama-convergence/specs/spaceai-platform-panorama-structure/spec.md
source_path: openspec/changes/spaceai-platform-panorama-convergence/specs/spaceai-platform-panorama-structure/spec.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

# 全景态势模块化结构与行为基线

能力标识：`spaceai-platform-panorama-structure`

## ADDED Requirements

### Requirement: 域边界与模块独立性
全景态势的状态与逻辑 SHALL 按域拆分为独立模块，置于 `plugins/map-3d/src/panorama/`；`PanoramaDeep.vue` SHALL 仅保留模板与装配职责。

每个域模块 SHALL 单一职责，且不依赖其它域模块的内部实现；跨域协作 MUST 经显式传入的状态或回调完成。

#### Scenario: 单域可独立测试
- **WHEN** 对任一新模块编写单元测试
- **THEN** 该测试 MUST 能在不挂载 `PanoramaDeep.vue` 的情况下运行并通过

#### Scenario: 组件职责收敛
- **WHEN** 抽取完成后检查 `PanoramaDeep.vue`
- **THEN** 其行数 SHALL 显著低于抽取前的 3351 行，且不包含域 1–8 的内部实现细节

### Requirement: 先测后抽的行为基线
每个域 SHALL 在其抽取提交之前具备覆盖该域公开契约的行为测试。

测试 MUST 断言公开契约与不变量，MUST NOT 断言内部函数名或实现细节。

#### Scenario: 抽取前测试为绿
- **WHEN** 某域开始抽取
- **THEN** 该域的测试 MUST 已在抽取前的代码上运行通过

#### Scenario: 抽取后行为不变
- **WHEN** 某域抽取完成
- **THEN** 同一组测试 MUST 仍然通过，且无需修改断言

### Requirement: 视觉与功能零变化
本轮 SHALL NOT 改变全景态势的 DOM 结构、类名、样式变量、交互路径与接口调用集合。

#### Scenario: 节点规模不劣化
- **WHEN** 在 1600×900 视口下比对抽取前后
- **THEN** DOM 节点数变化 MUST ≤ 5%

#### Scenario: 接口集合不变
- **WHEN** 进入全景态势并等待稳定
- **THEN** 14 个既有 `/RestFul` 端点 MUST 全部返回 200，且 MUST NOT 新增或移除端点依赖

#### Scenario: 无新增运行时错误
- **WHEN** 进入、操作、离开全景态势
- **THEN** MUST NOT 出现新增 console error、page error 或失败请求

### Requirement: 副作用可回收
域 5、6、8 持有的定时器、事件监听、`requestAnimationFrame` 与 Web Audio 节点 SHALL 在组件卸载时全部回收，MUST NOT 残留裸 `setInterval`。

#### Scenario: 卸载后副作用归零
- **WHEN** 挂载全景态势后卸载
- **THEN** 导出的活跃副作用计数 MUST 归零

#### Scenario: 反复进出不累积
- **WHEN** 连续进出全景态势 3 次
- **THEN** MUST NOT 出现回调在卸载后继续触发，且 JS 堆 MUST NOT 单调增长

### Requirement: 性能基线可复现
本轮 SHALL 记录抽取前后的性能基线，用于后续优化比对；性能数值 MUST NOT 作为本轮通过条件。

#### Scenario: 基线可复现
- **WHEN** 按 design.md 第 5、6 节的口径重跑测量
- **THEN** MUST 能产出同一组指标（DOM 节点数、JS 堆、进入耗时、有头与无头 FPS），并归档到 `harness/runs/<run-id>/evidence/`

### Requirement: 逐域可回滚
每个域的抽取 SHALL 独立提交，保证单域可回滚。

#### Scenario: 单域回滚
- **WHEN** 某域抽取后发现回归
- **THEN** MUST 能仅 revert 该域提交而保留其它域成果，且 MUST NOT 使用 reset/clean/force push
