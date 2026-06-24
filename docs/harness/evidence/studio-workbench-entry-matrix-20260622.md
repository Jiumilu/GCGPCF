---
doc_id: GPCF-DOC-6D92B5F4E7
title: Studio 工作台入口拓扑矩阵证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-workbench-entry-matrix-20260622.md
source_path: docs/harness/evidence/studio-workbench-entry-matrix-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 工作台入口拓扑矩阵证据

## 证据摘要

Evidence ID: `STUDIO-WORKBENCH-ENTRY-MATRIX-20260622`

本证据用于把第 005 轮的 `Kanban` 入口修复上升为 `Studio` 工作台入口治理矩阵，定位下一批应纳入 `chat` 主界面闭环的候选页面。

本轮关键事实如下：

1. `chat` 主界面当前使用 `PageSidebarNav`，其可见入口为 `新建对话 / 搜索 / 历史 / 看板 / 饲料 / 单聊 / 群聊`。
2. `AppSidebar` 的 Agent 分组中已有 `任务 / 看板 / 频道` 三个一组的主工作入口。
3. 真实运行态中，`Jobs` 与 `Channels` 页面都已经具备 `返回`，能够从工作台回到 `chat`。
4. 真实运行态中，`chat` 主界面当前只有 `Kanban` 入口，没有 `Jobs` 与 `Channels` 入口。
5. 因此 `Studio` 的工作台入口拓扑仍未完全对称，但下一步已可以从“泛化优化”收敛为“补齐 Jobs 与 Channels 的 chat 主入口策略”。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue
Scope: Studio 工作台入口矩阵审计，识别 chat 主界面与 Agent 工作台组的剩余入口缺口
Tools used: manual, in-app-browser
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: Router/AppSidebar/PageSidebarNav 静态对照 + Jobs/Channels 运行态抽查
Status ceiling: ui_evidence_candidate
```

## 入口拓扑矩阵

| Surface | Shell | chat -> surface | surface -> chat | 当前判定 |
|---|---|---|---|---|
| Chat | `PageSidebarNav` | n/a | n/a | 主入口 |
| Kanban | `AppSidebar` | yes | yes | 已闭环 |
| Jobs | `AppSidebar` | no | yes | 待补 chat 入口 |
| Channels | `AppSidebar` | no | yes | 待补 chat 入口 |

## 证据明细

| Type | Evidence | Path / Observation |
|---|---|---|
| Router 注册 | `hermes.jobs / hermes.kanban / hermes.channels` 都是独立 `route` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts` |
| Chat 壳层 | `PageSidebarNav` 当前仅补了 `Kanban`，未含 `Jobs` 与 `Channels` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue` |
| Workbench 壳层 | `AppSidebar` Agent 组现有 `任务 / 看板 / 频道` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/AppSidebar.vue` |
| Jobs 运行态 | `#/hermes/jobs` 页面存在 `返回`，并显示 `任务 / 看板 / 频道` 工作台组 | 真实浏览器抽查 |
| Channels 运行态 | `#/hermes/channels` 页面存在 `返回`，并显示 `任务 / 看板 / 频道` 工作台组 | 真实浏览器抽查 |
| Chat 运行态 | `#/hermes/chat` 页面当前 `hasJobsButton=false`、`hasKanbanButton=true`、`hasChannelsButton=false` | 真实浏览器抽查 |

## 候选页优先级

### P1：Jobs

理由：

1. `Jobs` 与 `Kanban` 同属 `AppSidebar` Agent 主组
2. 语义上更接近“任务执行工作台”
3. 与 `chat -> kanban -> chat` 闭环相邻，补齐成本低

### P2：Channels

理由：

1. `Channels` 也在 Agent 主组
2. 但页面内容更偏平台连接与配置，不如 `Jobs` 那样直接属于高频任务执行闭环
3. 应纳入统一规则，但可排在 `Jobs` 之后

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `Kanban/Jobs/Channels` 都是独立工作台页面 | 继续扩展矩阵到其他工作台 |
| G2 Design Tokens | partial | 本轮不涉及令牌调整 | 后续继续统一令牌 |
| G3 Component Consistency | partial | `Agent` 主组存在 3 个并列工作台，但 `chat` 主界面只暴露了其中 1 个 | 继续补齐剩余入口 |
| G4 Evidence And Governance | partial | 本轮仅做入口矩阵审计 | 后续继续做逐页证据 |
| G5 AI Fact Separation | partial | `chat` 与工作台关系更清晰，但仍未全量对称 | 继续治理双域边界 |
| G6 Accessibility | partial | 本轮未补键盘导航验证 | 后续补键盘路径 |
| G7 Responsive And Text Robustness | pass | 本轮无新布局破坏证据 | 后续按页面继续抽查 |
| G8 Runtime Verification | pass | `Jobs`、`Channels`、`Chat` 均做了运行态抽查 | 后续按实施项复验 |
| G9 Scope Control | pass | 本轮只审计，不扩改代码 | 下一轮再做最小实现 |

## 结论

第 005 轮之后，`Studio` 工作台入口治理已经不再模糊。

当前最清晰的下一步不是重新讨论 `Kanban`，而是：

1. 若继续推进主入口闭环，优先补 `Jobs`
2. 之后再补 `Channels`

这样可以把 `AppSidebar` Agent 组中最核心的三类页面，逐步对齐到 `chat` 主界面。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `workbench_entry_matrix_still_partial`

## 下一步建议

1. 建立 `GPCF-UI-STUDIO-WORKBENCH-007`，只补 `chat -> jobs` 可见入口。
2. `Channels` 建议作为后续一轮独立处理，而不是本轮顺手并入。
3. 继续保持“每轮只补一个入口”的节奏，避免把聊天壳层一次性改成高风险大改。
