---
doc_id: GPCF-DOC-8A54D0E2C1
title: Studio Kanban Chat 入口补齐验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-kanban-chat-entry-verified-20260622.md
source_path: docs/harness/evidence/studio-kanban-chat-entry-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Studio Kanban Chat 入口补齐验证证据

## 证据摘要

Evidence ID: `STUDIO-KANBAN-CHAT-ENTRY-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-005` 的真实结果：`chat` 主界面已补齐 `Kanban` 可见入口，并完成双向导航验证。

本轮关键事实如下：

1. 在 `PageSidebarNav.vue` 中新增了仅对 `chat` 主界面显示的 `Kanban` 入口。
2. 新增组件测试，验证“只在 `chat` 显示”和“点击后跳到 `hermes.kanban`”两项行为。
3. 已在真实运行态中复验 `chat -> kanban`。
4. 已在真实运行态中复验 `kanban -> chat`。
5. 本轮目标已达成，但整体 UI 门禁仍保持 `ui_partial`，因为设计令牌、可访问性、证据链和工作台规范化事项尚未全部关闭。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue
Scope: Chat 主界面补齐 Kanban 可见入口，并验证 chat -> kanban -> chat 双向导航
Tools used: manual, in-app-browser, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 定向单测通过 + 真实浏览器双向点击通过 + 运行态截图
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | `chat` 主界面新增 `Kanban` 按钮，仅在 `active === 'chat'` 时显示 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue` |
| 组件测试 | 新增 `PageSidebarNav` 单测，覆盖显示条件与跳转行为 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/page-sidebar-nav.test.ts` |
| 测试命令 | `npm test -- tests/client/page-sidebar-nav.test.ts` | 结果：`1 passed / 2 tests passed` |
| 运行态截图 | `chat` 主界面出现 `看板` 入口 | `docs/harness/evidence/assets/studio-chat-kanban-entry-20260622.png` |
| 运行态截图 | 从 `chat` 入口点击后进入 `Kanban` | `docs/harness/evidence/assets/studio-kanban-from-chat-entry-20260622.png` |

## 运行态复验

### 路径 1：Chat -> Kanban

真实浏览器复验结果：

1. 已登录 `Studio`
2. 刷新 `chat` 页面后，左侧聊天导航区域出现 `看板` 按钮
3. 点击 `看板` 后进入 `http://127.0.0.1:8649/#/hermes/kanban?board=default`
4. 页面出现 `看板 / 新建任务 / 状态列` 等工作台元素

### 路径 2：Kanban -> Chat

真实浏览器复验结果：

1. 在 `Kanban` 页面点击 `返回`
2. 页面回到 `http://127.0.0.1:8649/#/hermes/chat`
3. 聊天主界面重新出现 `新建对话 / 搜索 / 历史 / 看板 / 单聊 / 群聊`

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `chat` 主界面与 `Kanban` 工作台都保持真实可达 | 后续补更多工作台入口一致性 |
| G2 Design Tokens | partial | 本轮仅补入口，不涉及统一令牌 | 继续对齐项目群令牌规范 |
| G3 Component Consistency | pass | `chat -> kanban -> chat` 双向导航闭环已打通 | 后续推广到其他专业工作台 |
| G4 Evidence And Governance | partial | 本轮补的是入口层，不覆盖业务 evidence / audit 全链 | 继续补真实任务数据和证据入口 |
| G5 AI Fact Separation | partial | `chat` 与工作台入口边界已改善，但双域治理规则仍未全量落地 | 继续按 WAES 母框架治理 |
| G6 Accessibility | partial | 本轮未补完整键盘导航与焦点顺序验证 | 后续补键盘路径 |
| G7 Responsive And Text Robustness | pass | 新入口在真实聊天页已可见且未破坏既有布局 | 后续补移动端细节复验 |
| G8 Runtime Verification | pass | 定向单测和真实浏览器双向点击都通过 | 后续仅在扩展工作台入口时再复验 |
| G9 Scope Control | pass | 仅修改一个导航组件和一份测试 | 无额外页面级扩改 |

## 结论

本轮最小目标已经真实达成：

1. `chat` 主界面现在有 `Kanban` 可见入口
2. `chat -> kanban` 真实可点、真实可达
3. `kanban -> chat` 真实可点、真实可回

因此，第 005 轮应视为“入口可达性修复已完成”。但整体 UI 质量状态仍不能升为 `ui_ready`，因为项目群级统一规范还有未关闭项。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `project_group_ui_gate_still_partial`

## 下一步建议

1. 把同样的入口闭环规则推广到其他专业工作台类页面。
2. 继续补工作台导航的键盘可达性验证。
3. 继续按项目群统一规范处理令牌、证据入口和 AI/操作双域边界。
