---
doc_id: GPCF-DOC-A13F6D7B4E
title: Studio 默认凭据整改链路可访问性复验证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-a11y-verified-20260624.md
source_path: docs/harness/evidence/studio-default-credential-a11y-verified-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据整改链路可访问性复验证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-A11Y-VERIFIED-20260624`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-019` 的新增事实：默认凭据整改链路在完成零噪声收敛后，已进一步补齐键盘路径、焦点顺序、读屏语义和移动端触控目标的真实验证。

本轮关键事实如下：

1. 账户整改提示区已新增 `role="region"`、`aria-labelledby`、`aria-describedby` 和初始程序化焦点。
2. “修改密码 / 修改用户名” 两个弹层已补齐首焦点逻辑；打开弹层后，焦点会直接落到第一个输入框。
3. 弹层关闭后，在整改态下焦点会回到账户整改提示区，保持当前受限上下文。
4. 移动端关闭按钮触控目标已从 `28x28` 收敛到 `44x44`。
5. 在干净隔离 runtime 中，桌面键盘链路和移动端尺寸验证均已成立。

## Required Summary

```text
UI gate status: ui_ready
Surface: mobile-desktop-shell
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue
Scope: 默认凭据整改链路的键盘路径、焦点顺序、读屏语义与移动触控目标验证
Tools used: vitest, system Chrome (Playwright), curl, git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 9 个测试文件 89 个测试通过 + clean isolated runtime desktop/mobile a11y 复验 + desktop/mobile screenshots
Status ceiling: ui_evidence_candidate
```

## 运行时事实

### 隔离环境

| 项 | 值 |
|---|---|
| backend | `http://127.0.0.1:8667` |
| frontend | `http://127.0.0.1:8669` |
| runtime mode | `NODE_ENV=production` |
| isolated web ui home | `/tmp/gc-studio-default-credential-enforce-home-round19` |

### 桌面键盘链路

使用默认凭据 token 直进 `#/hermes/chat` 后，真实浏览器自动落地到：

```text
http://127.0.0.1:8669/#/hermes/settings?tab=account&reason=default-credentials
```

桌面 `1440x900` 视口下的真实焦点序列如下：

1. 初始焦点落在 `.credential-guidance` 提示区。
2. 第 1 次 `Tab` 落到关闭按钮，`aria-label="关闭"`。
3. 第 2 次 `Tab` 落到 “修改密码”。
4. 第 3 次 `Tab` 落到 “修改用户名”。
5. 在 “修改密码” 上触发打开后，首焦点落到 placeholder 为 “当前密码” 的输入框。

同时，整改提示区真实包含：

```text
role="region"
aria-labelledby="default-credential-guidance-title"
aria-describedby="default-credential-guidance-message"
```

### 移动端触控目标

移动 `390x844` 视口下，整改提示区关闭按钮的真实尺寸为：

```text
width = 44
height = 44
```

这满足最小触控目标要求。

## 截图

| 类型 | 路径 |
|---|---|
| desktop a11y remediation view | `docs/harness/evidence/assets/studio-default-credential-a11y-desktop-20260624.png` |
| mobile a11y remediation view | `docs/harness/evidence/assets/studio-default-credential-a11y-mobile-20260624.png` |

## 自动化验证

### 命令

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
git diff --check -- packages/client/src/components/hermes/settings/AccountSettings.vue tests/client/account-settings-default-credential.test.ts
```

### 结论

1. `9` 个测试文件、`89` 个测试全部通过。
2. `account-settings-default-credential` 已覆盖：
   - 整改提示区初始焦点；
   - 改密弹层首焦点与关闭后返回焦点；
   - 改名弹层首焦点。
3. 真实浏览器复验已覆盖桌面键盘路径和移动端触控目标。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 整改态仍稳定落到账户页，提示区和操作区结构可预测 | 无 |
| G2 Design Tokens | pass | 本轮仅补焦点和尺寸，不改统一语义 | 无 |
| G3 Component Consistency | pass | 提示区、按钮、弹层、输入框行为一致 | 无 |
| G4 Evidence And Governance | pass | 组件测试、真实键盘路径、真实尺寸与截图已分层留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议展示 | 无 |
| G6 Accessibility | pass | 初始焦点、Tab 顺序、弹层首焦点、读屏语义、44px 触控目标均已验证 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口保持稳定，无横向溢出 | 无 |
| G8 Runtime Verification | pass | clean isolated runtime 下完成 desktop/mobile a11y 复验 | 无 |
| G9 Scope Control | pass | 只改整改提示区和两个整改弹层的可访问性细节 | 无 |

## UI Caveats

- `figma_not_verified`

## 状态边界

本轮仍不声明：

1. `accepted`
2. `integrated`
3. `production_ready`

## 下一步建议

1. 若继续沿默认凭据链路推进，可把整改态允许访问的账户操作白名单显式固化为前端受控规范。
2. 本轮 G6 已闭合，后续可切回更高优先级的业务或工作台改造事项。
