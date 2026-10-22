---
doc_id: GPCF-DOC-353529D8
title: proposal
project: KDS
related_projects: [KDS, GPCF, SpaceAI]
domain: openspec
status: in_progress
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-panorama-operation-normalization/proposal.md
source_path: openspec/changes/spaceai-panorama-operation-normalization/proposal.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-panorama-operation-normalization · Proposal

> **追溯补建（2026-10-22）**：全景态势操作流程规范化的审计、方案与 B0–B5f 执行已于 2026-10-22 完成
> （13 个本地提交），但当时未建 OpenSpec 变更。本文按实际交付补齐；B5 剩余四大块与 i18n 未完成，状态 **in_progress**。

## Why

全景态势是 SpaceAI 指挥舱第一视图，但操作流程长期靠逐条反馈修补：同一动作多处入口、
Esc 退出行为不一致、失败操作仍提示成功（假成功）、演示态互相打架、偏好键散乱。
2026-10-22 对 4 个域做全量审计（地图工具 / 卡片数据 / 导航对象处置 / CWME）：
**143 项操作、106 条问题**，其中 P0 级问题集中在「假成功」「门禁缺失」「反馈通道错位」。

不做的后果：用户看到「操作成功」但数据没落、派单/CWME 回投可绕过确认、键盘操作互相打断——
这些是「界面看起来正常、实际出错」的典型事故。

## What Changes

- 审计与方案：4 份域审计 + 操作总索引 + 方案 v2.3（N1–N12 操作规范、B0–B5 批次、20 项决策模型判定、Q1–Q8 授权问答）。
- B0：操作契约护栏 6 例（先红后绿）。
- B1：六组 P0 修复（假成功 / 反馈通道 / 派单门禁 / CWME 回投门禁 / 驾驶 Esc / AI 结果可见）。
- B2：Esc 分层单一契约、键位注册表 + ? 帮助、键盘作用域、演示态互斥、持续能力胶囊、共享组件可选契约。
- B3：入口收敛 D1–D7、死代码与假字段清理、⌘K 命令面板（28 条命令）。
- B4：偏好键收口 `gc.pano.*`（22 键登记表）、审计待补队列、导出脱敏、卡片可访问性。
- B5a–B5f：组件切片（PanoramaHelp / PanoramaPalette / PanoramaBubbles）与 6 个组合式外提，组件 3955 → 3711 行。

### New Capabilities

- `spaceai-panorama-operation-normalization`：操作契约（成功/失败/门禁/反馈）、键盘与 Esc 分层、演示态互斥、
  偏好键命名与合并保护、组件拆分边界。

### Modified Capabilities

- `spaceai-platform-panorama-convergence`（已有变更）：其「PanoramaDeep 拆分」目标在本变更的 B5 系列继续推进；
  本变更只记录操作规范化与外提，不重复该变更的 8 域收敛承诺。

## 三层对齐（契约 → 工具链 → 应用链）

| 层 | 契约 | 本仓实现 | 证据 |
|---|---|---|---|
| 契约层 | 操作成功/失败语义、Esc 分层、键位注册表、偏好键 `gc.pano.*` | `plugins/map-3d/src/panorama/{keys,prefRead,useCardConfig,…}.ts`、`docs/panorama-prefs.md` | 操作契约测试 6 例（先红后绿）；22 键登记表 |
| 工具链 | 契约护栏测试、e2e 动线、文档复核 | `plugins/map-3d/tests/panorama-operate.test.ts` 等 35 例；`e2e/panorama-operate.spec.ts` | 全仓 136 文件 / 1251 例；e2e 5/5（真实 Chrome） |
| 应用链 | 全景态势实际操作 | `PanoramaDeep.vue`（3711 行）+ `components/Panorama{Help,Palette,Bubbles}.vue` | `.harness/runs/20261022-panorama-ops/01–21` |

## Impact

- Project：SpaceAI；仓：`GlobalCloud SpaceAI Platform`。
- 触及：`plugins/map-3d`（视图 / 组件 / 组合式 / 测试）、`e2e/`、`docs/`、`.harness/runs/`。
- 不改：接口契约、数据库 schema、权限模型；不新增业务功能。
- 非目标：B5 剩余四大块（卡片列 / 飞翔 / CWME / 控制器）外提；i18n 约 600 行；人工验收（派单 / CWME 回投真实状态）。
- authorization：老卢 2026-10-22 确认方案方向与 Q1–Q8 授权项。confirmation：业务验收、生产发布**未确认**；
  状态 partial / 待验收。
