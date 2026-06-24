---
doc_id: GPCF-DOC-5A9D73C1E4
title: Studio Kanban 运行入口门禁证据
project: GPCF
related_projects: [GPC, WAES, XGD, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-kanban-runtime-entry-gate-20260622.md
source_path: docs/harness/evidence/studio-kanban-runtime-entry-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio Kanban 运行入口门禁证据

## 证据摘要

Evidence ID: `STUDIO-KANBAN-RUNTIME-ENTRY-GATE-20260622`

本证据用于验证 `GPCF-UI-STUDIO-WORKBENCH-001` 之后的下一步是否已经进入真实页面运行态。

本轮直接验证对象：

- 本地前端地址：`http://127.0.0.1:8649`
- 目标路由：`/#/hermes/kanban`
- 目标页面：`KanbanView`

本轮验证结论：

1. 本地 `8649` 前端可访问。
2. 访问 `/#/hermes/kanban` 后，页面会回退到 `/#/` 登录页。
3. 当前 `KanbanView` 的真实运行态验证被认证前置门禁阻断。
4. 因此本轮 UI gate 状态应为 `ui_blocked`，而不是 `ui_ready` 或 `ui_partial`。

## Required Summary

```text
UI gate status: ui_blocked
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue
Scope: Studio Kanban 工作台运行入口门禁与真实页面可达性验证
Tools used: manual, in-app-browser, npm run harness:check
Tools unavailable: playwright_not_started, impeccable_not_invoked, figma_not_verified
Verification: 本地前端访问验证 + 登录前置截图 + harness gate 探测
Status ceiling: ui_evidence_candidate
```

## 核心证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 浏览器访问 | 目标地址可打开 | `http://127.0.0.1:8649/#/hermes/kanban` |
| URL 事实 | 实际位置回退 | 浏览器最终 `location = http://127.0.0.1:8649/#/` |
| 页面文本 | 登录前置出现 | `Hermes Web UI / 输入用户名和密码以继续 / 默认登录名：admin，默认密码：123456 / 登录` |
| 截图证据 | 登录前置截图 | `docs/harness/evidence/assets/studio-kanban-login-gate-20260622.png` |
| 代码锚点 | 登录跳转规则 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts` 中非 public 路由要求 token；`LoginView.vue:17-19`、`22-57`、`62-99` 显示登录逻辑和默认凭据提示 |
| 仓库 harness | 仓库 gate 探测 | `npm run harness:check` 失败，原因是现有聊天链变更未补 `docs/chat-chain-changes/*.md` 片段，属于当前脏工作区其它变更，不是本轮 Kanban 入口探测直接引起 |

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | not_applicable | 未进入 `KanbanView` 真实运行页，本轮只验证入口门禁 | 登录后补页面结构截图 |
| G2 Design Tokens | not_applicable | 本轮未进入目标页运行态 | 登录后补真实页面颜色与令牌比对 |
| G3 Component Consistency | not_applicable | 本轮未进入目标页运行态 | 登录后补真实页面组件一致性检查 |
| G4 Evidence And Governance | pass | 认证前置被显式暴露，没有伪装成目标页已可达 | 登录后继续检查目标页证据/审计区 |
| G5 AI Fact Separation | not_applicable | 本轮停在登录页 | 登录后检查 AI 与事实分区 |
| G6 Accessibility | partial | 登录页表单与按钮可见；但本轮不是目标页验证 | 如继续，用登录后目标页补完整 a11y 路径 |
| G7 Responsive And Text Robustness | partial | 登录页桌面态可见，且提示文本未溢出；未做移动态 | 登录后补目标页桌面/移动验证 |
| G8 Runtime Verification | fail | 目标页运行态未进入；认证门禁阻断 | 需要明确授权后执行登录并继续验证 |
| G9 Scope Control | pass | 本轮只做访问探测、截图和文档取证，未改 `Studio` 代码 | 下一轮仍保持只验证不改代码，或在授权后做小范围页面改造 |

## 非声明事项

- 本证据不证明 `KanbanView` 运行态已通过。
- 本证据不证明默认凭据一定可以成功登录，只证明登录页显式展示了该提示。
- 本证据不授权自动登录。
- 本证据不覆盖 `Studio` 其它工作台页。

## 下一步建议

1. 如需继续真实 `KanbanView` 运行态验证，需要用户明确授权使用本地登录页显示的默认凭据或提供其它有效登录方式。
2. 登录后应立即补桌面截图、移动端截图、键盘路径和目标页真实 URL 状态。
3. `harness:check` 的现有失败项应与本轮 UI 验证分开登记，避免把其它脏工作区问题误判为 `KanbanView` 页面阻断。
