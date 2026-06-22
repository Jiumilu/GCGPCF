---
doc_id: GPCF-DOC-5B7A12D4E9
title: Studio 默认凭据提醒非阻断化验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-prompt-nonblocking-verified-20260622.md
source_path: docs/harness/evidence/studio-default-credential-prompt-nonblocking-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Studio 默认凭据提醒非阻断化验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-PROMPT-NONBLOCKING-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-010` 的真实结果：`DefaultCredentialPrompt` 已从阻断式居中模态改为非阻断浮层提醒，默认凭据提醒仍然存在，但不再直接卡住 `chat` 主界面的首个关键操作。

本轮关键事实如下：

1. 原实现使用 `NModal` 居中遮挡主界面，并在运行态中会阻断用户立即点击工作台入口。
2. 当前实现已改为右下角固定浮层提醒，不再渲染模态遮罩。
3. 桌面端真实 `Safari` 运行态中，提醒存在时仍可从 `chat` 主界面点击进入 `Channels`。
4. 移动端真实 `Safari` 运行态中，提醒存在时仍可打开汉堡菜单，菜单内仍可见 `任务 / 看板 / 频道`。
5. 该变更只解决“阻断主界面操作”的问题，不声明“默认凭据治理问题已关闭”。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue
Scope: 将默认凭据提醒从阻断模态改为非阻断浮层，并复验 chat 主界面关键操作仍可继续
Tools used: manual, vitest, safaridriver
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 组件单测通过 + chat 导航回归通过 + 真实 Safari 桌面/移动端复验
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | `DefaultCredentialPrompt` 由 `NModal` 改为固定浮层提醒 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue` |
| 组件测试 | 新增“本会话可关闭且不再阻断页面”的测试，并保留“跳转到账户设置”的测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts` |
| 回归测试 | `chat` 主界面工作台入口回归 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/page-sidebar-nav.test.ts` |
| 测试命令 | `npm test -- tests/client/default-credential-prompt.test.ts` | 结果：`1 passed / 3 tests passed` |
| 测试命令 | `npm test -- tests/client/page-sidebar-nav.test.ts` | 结果：`1 passed / 4 tests passed` |
| 运行态截图 | 桌面端默认凭据提醒改为右下角浮层 | `docs/harness/evidence/assets/studio-default-credential-prompt-desktop-20260622.png` |
| 运行态截图 | 桌面端提醒存在时成功进入 `Channels` | `docs/harness/evidence/assets/studio-default-credential-prompt-channels-20260622.png` |
| 运行态截图 | 移动端提醒存在时仍可打开汉堡菜单 | `docs/harness/evidence/assets/studio-default-credential-prompt-mobile-menu-20260622.png` |

## 运行态复验

### 路径 1：桌面端提醒存在时继续进入 Channels

真实 `Safari` 运行态复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 使用默认凭据 `admin / 123456` 登录
3. 页面右下角出现默认凭据提醒浮层
4. DOM 中未发现 `.n-modal-mask` 模态遮罩
5. 在提醒存在的情况下，仍可点击左侧 `频道`
6. 页面成功进入 `http://127.0.0.1:8649/#/hermes/channels`

### 路径 2：移动端提醒存在时继续打开菜单

真实 `Safari` 390px 视口复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 默认凭据提醒以底部浮层形式出现
3. 左上角汉堡按钮仍可点击
4. 点击后侧栏展开，出现 `新建对话 / 搜索 / 历史 / 任务 / 看板 / 频道`
5. 说明该提醒不再阻断移动端主导航入口

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 提醒从阻断模态改为边角浮层，主界面关键区恢复可操作 | 后续可继续细化浮层在不同壳层的定位策略 |
| G2 Design Tokens | pass | 复用现有深色背景、边框、文字与按钮令牌 | 如需进一步统一，可将该类提醒抽象为共享告警浮层样式 |
| G3 Component Consistency | partial | 提醒动作仍与设置页跳转语义一致 | 后续统一系统级提醒、阻断态、告警浮层的视觉词汇 |
| G4 Evidence And Governance | pass | 明确区分“凭据治理问题仍存在”与“UI 阻断已解除” | 后续单独治理默认凭据问题本身 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议与业务事实混用 | 无 |
| G6 Accessibility | partial | 浮层可见、可关闭、可跳转，但未补完整读屏与 Escape 路径证据 | 后续补更细的键盘与读屏验证 |
| G7 Responsive And Text Robustness | partial | 桌面端良好，移动端不再阻断主导航，但底部浮层仍占据一定可视空间 | 后续评估更紧凑的移动端呈现策略 |
| G8 Runtime Verification | pass | 组件单测、导航回归、真实 Safari 桌面/移动端都已验证 | 运行态证据成立 |
| G9 Scope Control | pass | 仅修改提醒组件及其单测，未扩改无关页面 | 无额外扩面 |

## 结论

本轮最小目标已经真实达成：

1. 默认凭据提醒不再以模态遮罩方式卡住 `chat` 主界面。
2. 桌面端提醒存在时仍可继续进入工作台页面。
3. 移动端提醒存在时仍可继续打开主导航菜单。

本轮状态保持 `ui_partial`，原因不是本次修复无效，而是：

1. 默认凭据治理问题本身仍未关闭。
2. 移动端浮层仍占用一定底部空间，尚可继续优化。
3. 项目群级 UI 统一规范仍在持续推进中。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `default_credential_risk_still_exists_but_is_no_longer_modal_blocking`
- `mobile_prompt_still_occupies_viewport_space`

## 下一步建议

1. 将“默认凭据提醒浮层在移动端的占位压缩策略”作为下一步微调项。
2. 若要继续治理默认凭据问题，应在账户设置或首次登录流程中处理，不再让提醒长期常驻。
3. 将该类系统级提醒的非阻断模式纳入专业工作台类统一组件规范。
