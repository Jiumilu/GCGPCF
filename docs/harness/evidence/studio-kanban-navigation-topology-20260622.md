---
doc_id: GPCF-DOC-BF2C4E0A91
title: Studio Kanban 导航拓扑复核证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-kanban-navigation-topology-20260622.md
source_path: docs/harness/evidence/studio-kanban-navigation-topology-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio Kanban 导航拓扑复核证据

## 证据摘要

Evidence ID: `STUDIO-KANBAN-NAVIGATION-TOPOLOGY-20260622`

本证据用于复核 `GPCF-UI-STUDIO-WORKBENCH-003` 中“`chat -> kanban` 需 `reload()` 才能进入”的暂时性判断，并将问题收敛到真实可复现的导航拓扑缺口。

本轮关键事实如下：

1. 使用浏览器自动化的同 Tab `URL` 直跳方式，`#/hermes/chat` 与 `#/hermes/kanban` 都出现了“`hash` 变化但视图未同步切换”的现象，因此该路径不能再作为产品缺陷证据。
2. 使用页面内真实点击时，`Kanban` 页的 `返回` 链接可以稳定进入 `chat` 页面。
3. `chat` 页面采用 `PageSidebarNav`，其可见入口只有“新建对话 / 搜索 / 历史 / 饲料 / 单聊 / 群聊”，没有 `Kanban` 入口。
4. `Kanban` 页采用 `AppSidebar`，其中存在 `hermes.kanban` 导航项。
5. 因此当前真实问题不是“路由必须刷新”，而是“聊天主界面缺少到 `Kanban` 的可见入口，工作台可达性依赖深链、历史返回或非聊天页侧边栏”。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue
Scope: Studio Kanban 导航拓扑复核与聊天主界面到工作台的入口可达性验证
Tools used: manual, in-app-browser
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: URL 直跳复核 + 页面内真实点击 + 代码导航结构对照
Status ceiling: ui_evidence_candidate
```

## 运行态与代码对照证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 直跳复核 | `#/hermes/chat` 直跳后，`hash` 已变但页面仍停留在 `Kanban` 视图 | 说明自动化直跳路径不可靠，不能直接当作产品缺陷 |
| 页面内真实点击 | 从 `Kanban` 页点击 `返回` 后稳定进入 `chat` 页面 | 运行态观察：`hash=#/hermes/chat`，页面出现 `新建对话 / 搜索 / 历史 / 单聊 / 群聊` |
| 聊天页 DOM 复核 | `chat` 页面 `a[href="#/hermes/kanban"]` 计数为 `0` | 运行态 DOM 快照 |
| 根布局控制 | `App.vue` 中 `hermes.chat` 等页面被纳入 `usesPageSidebar`，因此 `chat` 页隐藏 `AppSidebar` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/App.vue` |
| 工作台侧边栏入口 | `AppSidebar.vue` 明确提供 `hermes.kanban` 导航项 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/AppSidebar.vue` |
| 聊天页侧边栏入口 | `PageSidebarNav.vue` 只提供聊天、历史、群聊等入口，没有 `Kanban` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue` |

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `KanbanView` 本页结构仍保持真实可达和可运行 | 后续补含真实任务数据的结构截图 |
| G2 Design Tokens | partial | 本轮不新增令牌映射证据 | 继续执行项目群统一令牌映射 |
| G3 Component Consistency | partial | `Kanban` 页与 `chat` 页使用了两套导航壳层，且入口拓扑不对称：`Kanban -> chat` 有入口，`chat -> kanban` 无入口 | 需统一专业工作台与聊天主界面的导航基线 |
| G4 Evidence And Governance | partial | 本轮只复核导航拓扑，不覆盖 receipt / audit / source record | 后续在真实任务数据场景补验证 |
| G5 AI Fact Separation | partial | 当前问题已从“路由异常”收敛为“聊天主界面与工作台入口边界未统一” | 需按 WAES 母框架定义工作台/AI 双域入口规范 |
| G6 Accessibility | partial | 本轮未新增完整键盘路径验证 | 后续补导航与表单完整键盘路径 |
| G7 Responsive And Text Robustness | pass | 本轮未推翻第 003 轮桌面/移动端无水平溢出证据 | 后续补真实任务长文本验证 |
| G8 Runtime Verification | pass | `Kanban` 真实运行、`Kanban -> chat` 页面内导航真实有效；第 003 轮 `reload` 判断被收敛为直跳路径伪缺陷 | 后续如修导航，只需复验入口可达性 |
| G9 Scope Control | pass | 本轮仅复核导航与文档证据，不改 `Studio` 代码 | 下一轮若改代码，只限导航入口层 |

## 纠偏结论

### 结论 1：第 003 轮中的 `reload` 观察不能继续作为产品缺陷

本轮复核发现，浏览器自动化的同 Tab `URL` 直跳会同时影响 `chat` 和 `kanban`，因此此前“`chat -> kanban` 需要 `reload()`”只能算测试路径上的不稳定现象，不应继续写成产品问题。

### 结论 2：当前真实问题是导航入口拓扑不完整

当前应用的壳层结构是：

1. `chat` 相关页面走 `PageSidebarNav`
2. `Kanban` 等专业工作台走 `AppSidebar`

结果是：

1. 专业工作台页能够回到 `chat`
2. 聊天主界面缺少进入 `Kanban` 的可见入口

这会造成专业工作台在日常使用中的发现性和连续工作路径不足。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `runtime_deeplink_transition_inconclusive_but_in_app_navigation_verified`

## 下一步建议

1. 建立 `GPCF-UI-STUDIO-WORKBENCH-005`，只处理 `chat` 主界面到 `Kanban` 的可见入口补齐。
2. 补齐后复验两条路径：`chat -> kanban` 与 `kanban -> chat` 都应可通过应用内真实点击完成。
3. 在修复前，不应把当前问题继续表述为“路由需刷新”，应统一改写为“聊天页缺少专业工作台入口”。
