---
doc_id: GPCF-DOC-8C1E4A92D7
title: Studio Kanban 操作工作台 UI Gate 证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-kanban-workbench-ui-gate-20260622.md
source_path: docs/harness/evidence/studio-kanban-workbench-ui-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Studio Kanban 操作工作台 UI Gate 证据

## 证据摘要

Evidence ID: `STUDIO-KANBAN-UI-GATE-20260622`

本证据用于把 `WAES -> Studio` 首条正式实施主线第一次真正落到页面级审计对象。

本轮目标页固定为：

- 项目：`Studio`
- 路由：`/hermes/kanban`
- 页面组件：`packages/client/src/views/hermes/KanbanView.vue`
- 页面类型：`operation-workbench`

本证据只证明：

1. `Studio` 已有一个真实工作台页被纳入 Loop UI gate。
2. 本页已经按 G1-G9 进行结构化审计。
3. 本页当前状态是 `ui_partial`，不是口头“已完成”。

本证据不证明：

1. `WAES -> Studio` 已完成继承改造。
2. `Studio` 已完成真实浏览器验收或移动端验收。
3. `Studio` 已达到 `accepted`、`integrated` 或 `production_ready`。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue
Scope: Studio Kanban 工作台页及其任务卡片/任务抽屉支持组件的首轮页面级 UI gate 审计
Tools used: manual, npm run build
Tools unavailable: browser_not_started, playwright_not_started, impeccable_not_invoked, accessibility_tool_not_invoked
Verification: 代码结构人工审计 + Studio 仓 npm run build 通过
Status ceiling: ui_evidence_candidate
```

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `KanbanView.vue:236-370` 具备页头、主操作、过滤、状态条、按状态分栏和任务抽屉；`KanbanTaskDrawer.vue:368-557` 形成详情侧抽屉 | 下一轮补浏览器截图，验证视觉骨架是否与代码一致 |
| G2 Design Tokens | partial | `theme.ts:3-79`、`variables.scss:7-56` 有 Studio 自身令牌；但 `KanbanTaskCard.vue:78-86`、`KanbanView.vue:410-428`、`KanbanTaskDrawer.vue:741-779` 仍直接写入状态色 | 将状态、治理、AI 语义映射到项目群统一令牌层，减少硬编码状态色 |
| G3 Component Consistency | pass | `KanbanView.vue:239-280` 统一使用 `NSelect/NButton`；`KanbanTaskCard.vue:68-158` 与 `KanbanTaskDrawer.vue:694-964` 复用同一视觉词汇和边框/标签风格 | 后续再对比 WAES 母框架组件词汇表 |
| G4 Evidence And Governance | partial | `KanbanTaskDrawer.vue:374-419`、`470-546`、`529-536` 已展示状态、父子关系、runs、comments、events、log、diagnostics | 仍缺 source record、evidence backlink、audit receipt、confirmer、confirmation time 的显式区块 |
| G5 AI Fact Separation | partial | `KanbanTaskDrawer.vue:121-142`、`470-487`、`552-557` 能回看 session 与结果摘要，但 AI 输出与业务事实还没有显式分区 | 增加 AI 建议标签、来源、可驳回/人工接管状态，不与系统事实混写 |
| G6 Accessibility | partial | `KanbanView.vue:286-304`、`457-460` 的状态 chip 有 `aria-pressed` 与 `focus-visible`；文本区 `KanbanTaskCard.vue:94-99`、`153-157`、`KanbanTaskDrawer.vue:782-788` 具备长文本换行 | `KanbanTaskCard.vue:40-62`、`KanbanTaskDrawer.vue:477-485` 仍是点击型 `div`，缺少键盘语义和可聚焦交互 |
| G7 Responsive And Text Robustness | partial | `KanbanView.vue:519-535` 已对移动端 header 做换行；`KanbanTaskCard.vue:94-99`、`KanbanTaskDrawer.vue:945-948` 已处理长文本和输入宽度 | 尚未真实验证 768px 以下工作台主区、抽屉与状态栏的联动表现 |
| G8 Runtime Verification | partial | `2026-06-22` 在 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` 执行 `npm run build` 通过，产出 `KanbanView` 构建物 `dist/client/assets/js/KanbanView-CFtVKaRX.js` 与 `dist/client/assets/css/KanbanView-BwOZf_JP.css` | 仍需 browser/Playwright 页面访问、桌面/移动截图、键盘路径验证 |
| G9 Scope Control | pass | 本轮只新增 GPCF evidence 与 loop round；未修改 `Studio` 页面代码；审计范围限定在 `KanbanView`、`KanbanTaskCard`、`KanbanTaskDrawer` | 下一轮若开始改造，仍需保持页面级最小改动 |

## UI Caveats

- `runtime_not_verified`
- `mobile_not_verified`
- `a11y_manual_only`
- `figma_not_verified`

## 结论

本轮结论如下：

1. `Studio/KanbanView` 已可被认定为 `Studio` 首个真实 `操作工作台页` 验证对象。
2. 当前最强结论只能到 `ui_partial`。
3. 本页已经具备工作台骨架、状态分层、任务详情与运行上下文入口，适合承接 `WAES -> Studio` 的下一轮母框架继承评估。
4. 当前主要缺口集中在统一令牌映射、证据/审计语义补齐、AI 建议与事实隔离、浏览器运行验证。

## 下一轮建议

1. 启动 `Studio/KanbanView` 浏览器级验证，补齐桌面与移动端截图证据。
2. 基于 `WAES专业工作台母框架升级方案` 为本页建立“母框架映射清单”。
3. 只在完成浏览器验证后，才进入首轮页面级优化设计或改造清单。
