---
doc_id: GPCF-DOC-2F6C9B14A8
title: Studio Kanban 运行态验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-kanban-runtime-verified-20260622.md
source_path: docs/harness/evidence/studio-kanban-runtime-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Studio Kanban 运行态验证证据

## 证据摘要

Evidence ID: `STUDIO-KANBAN-RUNTIME-VERIFIED-20260622`

本证据用于记录 `Studio/KanbanView` 在获得登录授权后的真实运行态验证结果。

本轮关键事实如下：

1. 使用本地登录页显示的默认凭据 `admin / 123456` 可以登录 `Studio`。
2. 登录后应用默认跳到 `/#/hermes/chat`，并弹出“请修改默认账户和密码”提醒。
3. 认证后重新访问 `/#/hermes/kanban`，在执行一次 `reload()` 后，真实 `KanbanView` 成功渲染。
4. 已补齐桌面态与移动态截图，并验证无水平溢出。
5. 当前仍存在一个真实运行问题：从活跃 `chat` 态切到 `kanban` 时，URL 已切换但内容未立即切换，刷新后才稳定进入 `KanbanView`。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue
Scope: Studio Kanban 登录后运行态、桌面/移动端与最小键盘焦点路径验证
Tools used: manual, in-app-browser
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 登录成功 + 运行态页面截图 + 移动端截图 + 最小键盘焦点检查
Status ceiling: ui_evidence_candidate
```

## 运行态证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 登录成功 | 登录后进入应用主界面 | URL 先落到 `http://127.0.0.1:8649/#/hermes/chat` |
| 默认密码提醒 | 登录后弹出默认账户密码提醒 | “请修改默认账户和密码 / 稍后提醒 / 去修改” |
| 目标页最终可达 | 刷新后进入 `KanbanView` | 最终 URL：`http://127.0.0.1:8649/#/hermes/kanban?board=default` |
| 桌面截图 | 1280x720 运行态截图 | `docs/harness/evidence/assets/studio-kanban-desktop-20260622.png` |
| 移动截图 | 390x844 运行态截图 | `docs/harness/evidence/assets/studio-kanban-mobile-20260622.png` |
| 桌面指标 | 页面标题与目标控件存在 | `title=看板`、`hasNewTask=true`、`overflowX=false` |
| 移动指标 | 移动端无水平溢出 | `390x844`、`scrollWidth=390`、`overflowX=false` |
| 键盘焦点 | 打开“新建任务”后焦点直接落到 `任务标题` 输入框 | `INPUT placeholder=任务标题` |

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 真实运行态出现 `看板` 标题、板选择、过滤、状态列与 `新建任务`；页面快照与代码结构一致 | 后续补充含真实任务数据的结构截图 |
| G2 Design Tokens | partial | 运行态与本地令牌体系一致，但页面仍沿用 Studio 自身状态色和黑白水墨体系 | 与项目群统一状态/治理/AI 令牌做正式映射 |
| G3 Component Consistency | pass | 运行态页头、筛选器、按钮、列、弹窗使用一致词汇和交互框架 | 后续与 WAES 母框架词汇表逐项对表 |
| G4 Evidence And Governance | partial | 运行态工作台存在对象工作区和任务详情入口，但当前空板场景还未展示 source record / receipt / audit 链 | 需在有任务数据场景下补验证 |
| G5 AI Fact Separation | partial | 当前 `KanbanView` 本身不混写 AI 内容，但登录后主应用默认落到 chat，说明工作台与 AI 主界面边界仍需治理约束 | 需形成 WAES 母框架映射清单并补工作台内 AI 分区验证 |
| G6 Accessibility | partial | 最小键盘焦点验证通过：打开 `新建任务` 后焦点落到 `任务标题` 输入框；但 `Tab` 连续推进未得到稳定证明 | 需补完整表单 `Tab` 顺序、关闭与回退路径 |
| G7 Responsive And Text Robustness | pass | 已补 `1280x720` 和 `390x844` 截图；两态均 `overflowX=false` | 后续补含真实任务卡片的移动态长文本验证 |
| G8 Runtime Verification | partial | 登录后 `reload()` 可进入 `KanbanView`，说明目标页真实可达；但 `chat -> kanban` 存在路由切换需刷新才能稳定生效的问题 | 应把该路由/渲染偏差列入后续修复项 |
| G9 Scope Control | pass | 本轮只做登录、页面访问、截图与文档记录，未修改 `Studio` 代码 | 下一轮若修复路由问题，仍需保持最小页面范围 |

## 真实发现

### 发现 1：运行态已可进入

这是本轮最关键的正向事实。`KanbanView` 不再是仅靠代码审计判断存在，而是已经进入真实运行态并完成桌面/移动截图。

### 发现 2：路由切换存在偏差

本轮观察到：

1. 登录后默认进入 `chat`。
2. 认证后直接把 URL 改到 `/#/hermes/kanban` 时，页面内容一度仍保持 `chat` 内容。
3. 执行一次 `reload()` 后才稳定进入 `KanbanView`。

这说明当前至少存在一条“URL 已切换但视图未即时切换”的真实问题，后续应进入页面级修复清单。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `runtime_verified_with_reload_note`

## 下一步建议

1. 建立 `GPCF-UI-STUDIO-WORKBENCH-004`，只针对 `chat -> kanban` 路由/渲染偏差做最小修复验证。
2. 在修复前，不应把当前状态提升为 `ui_ready`。
3. 修复后再补“含真实任务数据”的工作台截图与详情抽屉验证。
