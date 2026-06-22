---
doc_id: GPCF-DOC-9F2A7D61B3
title: Studio 默认凭据登录分流验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-login-redirect-verified-20260622.md
source_path: docs/harness/evidence/studio-default-credential-login-redirect-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Studio 默认凭据登录分流验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-LOGIN-REDIRECT-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-012` 的真实结果：默认凭据用户登录后不再先进入 `chat` 主界面再靠浮层提醒补救，而是直接进入账户设置页的治理入口，并在页内看到修改密码/修改用户名引导。

本轮关键事实如下：

1. 登录页在密码登录成功后会拉取当前用户信息。
2. 若用户仍满足 `requiresCredentialChange=true`，前端直接路由到 `#/hermes/settings?tab=account&reason=default-credentials`。
3. 账户设置页顶部新增页内治理引导卡片，明确给出 `修改密码` 与 `修改用户名` 两个动作。
4. 在账户设置页 `tab=account` 场景下，原有 `DefaultCredentialPrompt` 不再重复出现。
5. 本轮不声明默认凭据问题已经治理完成，只声明“首次登录后的 UI 引导路径”已经从 `chat` 面补救改为“直达治理入口”。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/LoginView.vue
Scope: 默认凭据登录后直接分流到账户设置治理入口，并在该页用页内引导替代重复浮层
Tools used: manual, vitest, safaridriver
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 登录分流单测通过 + 提醒静默回归通过 + 真实 Safari 桌面/移动端登录复验
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | 登录成功后按 `requiresCredentialChange` 分流到账户设置页 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/LoginView.vue` |
| 代码修改 | 账户设置页新增默认凭据治理引导卡片 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue` |
| 代码修改 | 账户设置页 `tab=account` 时默认凭据浮层静默 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue` |
| 组件测试 | 登录页新增“默认凭据用户登录后跳转到账户设置”的测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/login-view.test.ts` |
| 组件测试 | 默认凭据浮层新增“账户设置页不再弹出”的测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts` |
| 测试命令 | `npm test -- tests/client/login-view.test.ts` | 结果：`1 passed / 5 tests passed` |
| 测试命令 | `npm test -- tests/client/default-credential-prompt.test.ts` | 结果：`1 passed / 4 tests passed` |
| 测试命令 | `npm test -- tests/client/page-sidebar-nav.test.ts` | 结果：`1 passed / 4 tests passed` |
| 运行态截图 | 桌面端默认凭据登录后直接落到账户设置页并显示治理引导 | `docs/harness/evidence/assets/studio-default-credential-login-redirect-settings-20260622.png` |
| 运行态截图 | 移动端默认凭据登录后直接落到账户设置页并显示治理引导 | `docs/harness/evidence/assets/studio-default-credential-login-redirect-settings-mobile-20260622.png` |

## 运行态复验

### 路径 1：桌面端默认凭据登录分流

真实 `Safari` 运行态复验结果：

1. 打开 `http://127.0.0.1:8649/#/`
2. 输入默认凭据 `admin / 123456`
3. 登录成功后页面直接进入 `http://127.0.0.1:8649/#/hermes/settings?tab=account&reason=default-credentials`
4. 页面标题为 `设置`
5. 页内出现 `请修改默认账户和密码` 引导卡片，并提供 `修改密码 / 修改用户名`
6. DOM 中不存在 `.credential-prompt` 重复浮层

### 路径 2：移动端默认凭据登录分流

真实 `Safari` 390px 视口复验结果：

1. 打开 `http://127.0.0.1:8649/#/`
2. 输入默认凭据 `admin / 123456`
3. 登录成功后页面同样直接进入 `#/hermes/settings?tab=account&reason=default-credentials`
4. 移动端也能看到页内治理引导卡片与 `修改密码 / 修改用户名` 动作
5. 不再先落到 `chat` 主界面，也不再叠加默认凭据浮层

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 默认凭据用户从登录页直接进入治理入口，而不是先进入聊天主界面 | 后续可继续梳理首次登录后的更完整治理路径 |
| G2 Design Tokens | pass | 引导卡片沿用现有告警边框、背景和按钮令牌 | 无 |
| G3 Component Consistency | pass | 登录分流、页内引导、账户动作三者语义一致 | 后续可将治理引导卡片纳入系统级模式库 |
| G4 Evidence And Governance | pass | UI 结论严格限定为“分流到治理入口”，未冒充治理完成 | 后续治理默认凭据问题本体 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 事实边界 | 无 |
| G6 Accessibility | partial | 引导卡片可见且动作明确，但未补更细的焦点管理证据 | 后续补键盘进入模态与读屏验证 |
| G7 Responsive And Text Robustness | pass | 桌面端与移动端都能直接进入同一治理入口页 | 后续验证更窄屏与长文案 |
| G8 Runtime Verification | pass | 单测与真实 Safari 桌面/移动端登录复验都通过 | 运行态证据成立 |
| G9 Scope Control | pass | 只改登录分流、账户引导和提醒静默 | 无额外扩面 |

## 结论

本轮最小目标已经真实达成：

1. 默认凭据用户登录后不再先落回 `chat` 主界面。
2. 默认凭据治理入口已提前到首次登录后的第一落点。
3. 账户设置页内引导替代了重复浮层提醒。

本轮状态保持 `ui_partial`，因为：

1. 默认凭据治理问题本身仍未完成，用户还需要执行改密/改名动作。
2. 当前只是前端分流与引导闭环，不是后端强制改密闭环。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `credential_change_not_enforced_server_side`
- `governance_entry_completed_but_governance_action_still_pending`

## 下一步建议

1. 若继续推进，应把“修改密码成功后取消默认凭据风险提示”做成更明确的闭环验证。
2. 更强治理方案可考虑后端首次登录强制改密，但这将超出本轮最小前端范围。
3. 将“高风险账户状态优先分流到治理入口页”纳入项目群专业工作台类统一规范。
