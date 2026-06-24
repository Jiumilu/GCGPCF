---
doc_id: GPCF-DOC-F1A4B89C2D
title: Studio 默认凭据后端门禁真实运行复验证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.md
source_path: docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据后端门禁真实运行复验证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-BACKEND-RUNTIME-VERIFIED-20260624`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-017` 的新增事实：默认凭据治理不仅已经写入 Studio 源码和自动化测试，而且已在隔离运行时中被真实验证为“带默认凭据 token 直接进 chat，也会被拦回账户整改页”。

本轮关键事实如下：

1. 重新编译 `dist/server/index.js` 之前，隔离 production 后端仍停留在 2026-06-22 的旧构建，导致真实运行没有体现 2026-06-23 的源码门禁。
2. 重编译后，原始接口 `GET /api/hermes/sessions` 已对默认凭据用户返回 `403`，并附带 `requiresCredentialChange: true`。
3. 浏览器在桌面 `1440x900` 与移动 `390x844` 视口下，带默认凭据 token 直进 `#/hermes/chat`，都会被重定向到 `#/hermes/settings?tab=account&reason=default-credentials`。
4. 为避免整改页再触发与整改无关的受保护请求，本轮新增两层最小前端硬化：
   - `SettingsView` 在默认凭据整改态下不再预加载 profiles/settings。
   - `AccountSettings` 在整改未完成前不再加载或展示头像与锁定 IP 区块。
5. 为避免 `ChatView` 在页面挂载前打出多条受保护请求，本轮新增路由级默认凭据预检。当前桌面和移动端复验后，都只剩 1 条初始 `403` 控制台噪声，较整改前显著收敛。

## Required Summary

```text
UI gate status: ui_partial
Surface: mobile-desktop-shell
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts
Scope: 默认凭据 token 直进 chat 的后端门禁真实复验、整改页无关预加载收敛、路由级预检补强
Tools used: curl, vitest, system Chrome (Playwright), git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 原始 403 接口证据 + 桌面/移动双视口真实重定向 + 83 tests 通过 + diff check 通过
Status ceiling: ui_evidence_candidate
```

## 运行时事实

### 隔离环境

| 项 | 值 |
|---|---|
| backend | `http://127.0.0.1:8667` |
| frontend | `http://127.0.0.1:8669` |
| isolated home | `/tmp/gc-studio-default-credential-enforce-home` |
| backend mode | `NODE_ENV=production` |
| extra guards | `HERMES_WEB_UI_DISABLE_GATEWAY_AUTOSTART=1` `HERMES_WEB_UI_DISABLE_MCP_AUTOINJECT=1` `HERMES_LAN_DISCOVERY_ENABLED=false` |

### 原始接口证据

本轮用 `admin / 123456` 登录后，直接调用：

```text
GET /api/hermes/sessions
Authorization: Bearer <default-credential-jwt>
```

返回：

```text
HTTP/1.1 403 Forbidden
{"error":"Default credentials must be changed before continuing","requiresCredentialChange":true}
```

这证明后端真实运行已包含默认凭据门禁，而不只是测试态中间件。

### 浏览器重定向证据

桌面和移动端都采用同一方式验证：

1. 先通过后端登录接口获取默认凭据 JWT。
2. 在浏览器 `localStorage` 直接注入 `hermes_api_key`。
3. 直接访问 `http://127.0.0.1:8669/#/hermes/chat`。
4. 观察是否会在真实运行中跳回 `hermes.settings?tab=account&reason=default-credentials`。

结果如下：

| 视口 | URL | token 保留 | remediation flag | 账户整改提示 | 横向溢出 | 头像区块 | 锁定 IP 区块 |
|---|---|---|---|---|---|---|---|
| desktop `1440x900` | `#/hermes/settings?tab=account&reason=default-credentials` | true | `1` | true | false | false | false |
| mobile `390x844` | `#/hermes/settings?tab=account&reason=default-credentials` | true | `1` | true | false | false | false |

### 截图

| 类型 | 路径 |
|---|---|
| desktop redirected account view | `docs/harness/evidence/assets/studio-default-credential-backend-enforcement-desktop-20260624.png` |
| mobile redirected account view | `docs/harness/evidence/assets/studio-default-credential-backend-enforcement-mobile-20260624.png` |

## 自动化验证

### 命令

```bash
node scripts/build-server.mjs
npm test -- tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/api.test.ts tests/client/login-view.test.ts tests/client/default-credential-prompt.test.ts tests/server/user-auth.test.ts
git diff --check -- packages/client/src/api/client.ts packages/client/src/api/auth.ts packages/client/src/router/index.ts packages/client/src/views/hermes/SettingsView.vue packages/client/src/components/hermes/settings/AccountSettings.vue tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

### 结论

1. `7` 个测试文件、`83` 个测试全部通过。
2. 新增 `router-default-credential-guard` 已证明默认用户名 token 会在路由层触发整改预检。
3. 新增 `settings-view-default-credential` 已证明整改态不会预加载 profiles/settings。
4. 更新后的 `account-settings-default-credential` 已证明整改态不会加载头像和锁定 IP。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 默认凭据 token 直进 chat 会被稳定送到账户整改页 | 无 |
| G2 Design Tokens | pass | 本轮不改令牌，只收紧整改态结构 | 无 |
| G3 Component Consistency | pass | 登录、路由、账户整改页、后端门禁语义保持一致 | 无 |
| G4 Evidence And Governance | pass | 原始 403、真实重定向、测试与截图已分离取证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议显示 | 无 |
| G6 Accessibility | partial | 仍未补完整键盘/读屏链路 | 后续补 a11y 证据 |
| G7 Responsive And Text Robustness | pass | desktop 与 mobile 两个视口均无水平溢出 | 可继续扩展更窄视口 |
| G8 Runtime Verification | pass | 原始接口与双视口真实重定向均已复验 | 可继续补录屏 |
| G9 Scope Control | pass | 只围绕默认凭据门禁、预加载和路由预检做最小修改 | 无 |

## 仍保留的现实边界

本轮虽然把默认凭据治理的真实性补强到了“源码 + 自动化 + 真实运行”三层，但仍不声明：

1. `accepted`
2. `integrated`
3. `production_ready`
4. 完整 a11y 闭环完成

此外，本轮仍观察到桌面与移动端各有 1 条初始 `403` 控制台噪声。当前判断是：

1. 主体整改路径已可真实使用。
2. 无关预加载噪声已显著收敛。
3. 如果要进一步做到“控制台近乎零噪声”，下一步应再检查首个被拦截的非关键请求来源。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `single_initial_navigation_403_observed`

## 下一步建议

1. 继续追最后 1 条初始 `403` 的来源，把默认凭据整改路径收敛到更干净的零噪声态。
2. 补默认凭据整改链路的键盘路径与焦点顺序验证。
