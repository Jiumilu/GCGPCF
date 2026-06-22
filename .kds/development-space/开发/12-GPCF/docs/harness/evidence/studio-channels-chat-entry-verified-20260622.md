---
doc_id: GPCF-DOC-718A85136C
title: Studio Channels Chat 入口补齐验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-channels-chat-entry-verified-20260622.md
source_path: docs/harness/evidence/studio-channels-chat-entry-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Studio Channels Chat 入口补齐验证证据

## 证据摘要

Evidence ID: `STUDIO-CHANNELS-CHAT-ENTRY-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-008` 的真实结果：`chat` 主界面已补齐 `Channels` 可见入口，并完成 `chat -> channels -> chat` 双向导航验证。

本轮关键事实如下：

1. 在 `PageSidebarNav.vue` 中新增了仅对 `chat` 主界面显示的 `Channels` 入口。
2. 扩展组件测试，验证 `Jobs`、`Kanban`、`Channels` 三个主工作台入口都只在 `chat` 主界面显示。
3. 新增组件测试，验证点击 `Channels` 后跳转到 `hermes.channels`。
4. 真实 `Safari` 运行态里，`chat -> channels` 与 `channels -> chat` 都已验证通过。
5. 复验过程中仍存在默认凭据提醒弹窗，需要先关闭后再点击主界面工作台入口；该问题属于独立运行态干扰项，不应混写成 `Channels` 导航缺陷。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue
Scope: Chat 主界面补齐 Channels 可见入口，并验证 chat -> channels -> chat 双向导航
Tools used: manual, safaridriver, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 定向单测通过 + 真实 Safari 双向点击通过 + 运行态截图
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | `chat` 主界面新增 `Channels` 按钮，仅在 `active === 'chat'` 时显示 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue` |
| 组件测试 | `PageSidebarNav` 单测扩展为 `Jobs + Kanban + Channels` 显示条件与跳转测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/page-sidebar-nav.test.ts` |
| 测试命令 | `npm test -- tests/client/page-sidebar-nav.test.ts` | 结果：`1 passed / 4 tests passed` |
| 运行态截图 | `chat` 主界面出现 `频道` 入口 | `docs/harness/evidence/assets/studio-chat-channels-entry-20260622.png` |
| 运行态截图 | 从 `chat` 入口点击后进入 `Channels` | `docs/harness/evidence/assets/studio-channels-from-chat-entry-20260622.png` |
| 运行态截图 | 从 `Channels` 页面点击 `返回` 后回到 `chat` | `docs/harness/evidence/assets/studio-chat-from-channels-return-20260622.png` |

## 运行态复验

### 路径 1：Chat -> Channels

真实 `Safari` 浏览器复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 若进入登录页，则使用默认凭据 `admin / 123456` 登录
3. 若存在默认凭据提醒弹窗，先点击 `稍后提醒`
4. 聊天主界面导航区域出现 `频道` 按钮
5. 点击 `频道` 后进入 `http://127.0.0.1:8649/#/hermes/channels`
6. 页面出现 `频道 / Telegram / Discord / Slack / WhatsApp` 等 `Channels` 工作台元素

### 路径 2：Channels -> Chat

真实 `Safari` 浏览器复验结果：

1. 在 `Channels` 页面点击 `返回`
2. 页面回到 `http://127.0.0.1:8649/#/hermes/chat`
3. 聊天主界面重新出现 `新建对话 / 搜索 / 历史 / 任务 / 看板 / 频道 / 单聊 / 群聊`

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | `chat` 主界面与 `Channels` 工作台都保持真实可达 | 后续补更多工作台入口一致性 |
| G2 Design Tokens | partial | 本轮仅补入口，不涉及统一令牌 | 继续对齐项目群令牌规范 |
| G3 Component Consistency | pass | `chat -> channels -> chat` 双向导航闭环已打通 | 后续转入更外围入口一致性或键盘路径 |
| G4 Evidence And Governance | partial | 本轮补的是入口层，不覆盖业务 evidence / audit 全链 | 继续补业务证据链 |
| G5 AI Fact Separation | partial | `chat` 与工作台入口边界继续改善，但双域治理规则仍未全量落地 | 继续按 WAES 母框架治理 |
| G6 Accessibility | partial | 本轮未补完整键盘导航与焦点顺序验证 | 后续补键盘路径 |
| G7 Responsive And Text Robustness | pass | 新入口在真实聊天页已可见且未破坏既有布局 | 后续补移动端细节复验 |
| G8 Runtime Verification | pass | 定向单测和真实 Safari 双向点击都通过 | 运行态证据成立 |
| G9 Scope Control | pass | 仅修改一个导航组件和一份测试 | 无额外页面级扩改 |

## 结论

本轮最小目标已经真实达成：

1. `chat` 主界面现在有 `Channels` 可见入口
2. `chat -> channels` 真实可点、真实可达
3. `channels -> chat` 真实可点、真实可回

至此，`AppSidebar` Agent 主组里当前最核心的三个并列工作台入口 `Jobs`、`Kanban`、`Channels` 都已经补进 `chat` 主界面。整体 UI 门禁状态仍保持 `ui_partial`，因为可访问性、移动端细节、令牌和项目群级规范化事项尚未全部关闭。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `default_credential_prompt_can_interfere_with_nav_clicks`
- `project_group_ui_gate_still_partial`

## 下一步建议

1. 从“核心工作台入口缺口”转入“键盘路径 / 焦点顺序 / 移动端细节”复验。
2. 单独登记默认凭据提醒弹窗对聊天主界面交互的干扰，不与工作台入口问题混写。
3. 若继续扩入口一致性，应单独审计 `Agent` 组中非核心工作台的可见性策略，而不是并入本轮结论。
