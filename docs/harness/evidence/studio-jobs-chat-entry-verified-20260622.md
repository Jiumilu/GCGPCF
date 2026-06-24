---
doc_id: GPCF-DOC-5C7D184EA2
title: Studio Jobs Chat 入口补齐验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-jobs-chat-entry-verified-20260622.md
source_path: docs/harness/evidence/studio-jobs-chat-entry-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio Jobs Chat 入口补齐验证证据

## 证据摘要

Evidence ID: `STUDIO-JOBS-CHAT-ENTRY-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-007` 的真实结果：`chat` 主界面已补齐 `Jobs` 可见入口，并完成 `chat -> jobs -> chat` 双向导航验证。

本轮关键事实如下：

1. 在 `PageSidebarNav.vue` 中新增了仅对 `chat` 主界面显示的 `Jobs` 入口。
2. 扩展组件测试，验证 `Jobs` 与 `Kanban` 两个主工作台入口都只在 `chat` 主界面显示。
3. 新增组件测试，验证点击 `Jobs` 后跳转到 `hermes.jobs`。
4. 真实运行态里，`chat -> jobs` 与 `jobs -> chat` 都已验证通过。
5. 复验过程中发现默认凭据提醒弹窗会挡住聊天页入口点击，需要先关闭；该问题属于独立运行态干扰项，不应混写成 `Jobs` 导航缺陷。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue
Scope: Chat 主界面补齐 Jobs 可见入口，并验证 chat -> jobs -> chat 双向导航
Tools used: manual, in-app-browser, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 定向单测通过 + 真实浏览器双向点击通过 + 运行态截图
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | `chat` 主界面新增 `Jobs` 按钮，仅在 `active === 'chat'` 时显示 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue` |
| 组件测试 | `PageSidebarNav` 单测扩展为 `Jobs + Kanban` 显示条件与跳转测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/page-sidebar-nav.test.ts` |
| 测试命令 | `npm test -- tests/client/page-sidebar-nav.test.ts` | 结果：`1 passed / 3 tests passed` |
| 运行态截图 | `chat` 主界面出现 `任务` 入口 | `docs/harness/evidence/assets/studio-chat-jobs-entry-20260622.png` |
| 运行态截图 | 从 `chat` 入口点击后进入 `Jobs` | `docs/harness/evidence/assets/studio-jobs-from-chat-entry-20260622.png` |

## 运行态复验

### 路径 1：Chat -> Jobs

真实浏览器复验结果：

1. 已登录 `Studio`
2. 进入 `chat` 页面后，若存在默认凭据提醒弹窗，先点击 `稍后提醒`
3. 聊天主界面导航区域出现 `任务` 按钮
4. 点击 `任务` 后进入 `http://127.0.0.1:8649/#/hermes/jobs`
5. 页面出现 `定时任务 / 创建任务` 等 `Jobs` 工作台元素

### 路径 2：Jobs -> Chat

真实浏览器复验结果：

1. 在 `Jobs` 页面点击 `返回`
2. 页面回到 `http://127.0.0.1:8649/#/hermes/chat`
3. 聊天主界面重新出现 `新建对话 / 搜索 / 历史 / 任务 / 看板 / 单聊 / 群聊`

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `chat` 主界面与 `Jobs` 工作台都保持真实可达 | 后续补更多工作台入口一致性 |
| G2 Design Tokens | partial | 本轮仅补入口，不涉及统一令牌 | 继续对齐项目群令牌规范 |
| G3 Component Consistency | pass | `chat -> jobs -> chat` 双向导航闭环已打通 | 后续处理 `Channels` |
| G4 Evidence And Governance | partial | 本轮补的是入口层，不覆盖业务 evidence / audit 全链 | 继续补业务证据链 |
| G5 AI Fact Separation | partial | `chat` 与工作台入口边界继续改善，但双域治理规则仍未全量落地 | 继续按 WAES 母框架治理 |
| G6 Accessibility | partial | 本轮未补完整键盘导航与焦点顺序验证 | 后续补键盘路径 |
| G7 Responsive And Text Robustness | pass | 新入口在真实聊天页已可见且未破坏既有布局 | 后续补移动端细节复验 |
| G8 Runtime Verification | pass | 定向单测和真实浏览器双向点击都通过 | 运行态证据成立 |
| G9 Scope Control | pass | 仅修改一个导航组件和一份测试 | 无额外页面级扩改 |

## 结论

本轮最小目标已经真实达成：

1. `chat` 主界面现在有 `Jobs` 可见入口
2. `chat -> jobs` 真实可点、真实可达
3. `jobs -> chat` 真实可点、真实可回

至此，`AppSidebar` Agent 主组里最核心的两个工作台入口 `Jobs` 与 `Kanban` 都已经补进 `chat` 主界面。整体 UI 门禁状态仍保持 `ui_partial`，因为 `Channels`、可访问性、令牌和项目群级规范化事项尚未全部关闭。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `default_credential_prompt_can_interfere_with_nav_clicks`
- `project_group_ui_gate_still_partial`

## 下一步建议

1. 建立下一轮，只补 `chat -> channels` 可见入口。
2. 单独登记默认凭据提醒弹窗对聊天主界面交互的干扰，不与工作台入口问题混写。
3. 继续保持“一轮只补一个入口”的节奏。
