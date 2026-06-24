---
doc_id: GPCF-DOC-5A7D23B8E1
title: Studio 默认凭据整改零噪声复验证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-zero-noise-remediation-20260624.md
source_path: docs/harness/evidence/studio-default-credential-zero-noise-remediation-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据整改零噪声复验证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-ZERO-NOISE-REMEDIATION-20260624`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-018` 的新增事实：上一轮残留的最后 1 条默认凭据整改链路 `403` 噪声已被定位为全局侧边栏 `ProfileSelector` 的 `profiles` 预加载，并在最小修补后完成桌面与移动端真实零噪声复验。

本轮关键事实如下：

1. `App.vue` 已在默认凭据整改态暂停全局 `loadModels()` 与 `health polling`。
2. `DefaultCredentialPrompt.vue` 跳转账户整改页时已统一补齐 `reason=default-credentials`。
3. `ProfileSelector.vue` 已在整改态下跳过 `fetchProfiles()`，并在离开整改态后恢复正常预加载。
4. 在干净隔离 production runtime 中，默认凭据 token 直进 `#/hermes/chat` 后，桌面与移动端都稳定跳转到 `#/hermes/settings?tab=account&reason=default-credentials`，且不再出现任何 `403` 响应或控制台错误。

## Required Summary

```text
UI gate status: ui_partial
Surface: mobile-desktop-shell
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/ProfileSelector.vue
Scope: 默认凭据整改态全局壳层预加载收敛、侧边栏 profile 预加载抑制、零噪声运行复验
Tools used: vitest, system Chrome (Playwright), curl, git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 9 个测试文件 87 个测试通过 + clean isolated runtime desktop/mobile 双视口零 403 复验
Status ceiling: ui_evidence_candidate
```

## 运行时事实

### 隔离环境

| 项 | 值 |
|---|---|
| backend | `http://127.0.0.1:8667` |
| frontend | `http://127.0.0.1:8669` |
| runtime mode | `NODE_ENV=production` |
| isolated web ui home | `/tmp/gc-studio-default-credential-enforce-home-round18` |

### 最终剩余噪声定位

上一轮残留噪声的最终来源为：

```text
GET /api/hermes/profiles
source = packages/client/src/components/layout/ProfileSelector.vue
trigger = onMounted() global sidebar preload
```

这说明 Chat 主界面与账户整改页主体已经收敛，最后的受保护请求来自全局侧边栏，而不是主流程页面本身。

### 零噪声浏览器复验

本轮使用干净隔离 production backend 登录 `admin / 123456`，再把 JWT 注入浏览器 `localStorage.hermes_api_key`，直接访问：

```text
http://127.0.0.1:8669/#/hermes/chat
```

桌面与移动端复验结果如下：

| 视口 | URL | guidance | avatar section | locked ip section | remediation flag | console errors | 403 responses |
|---|---|---|---|---|---|---|---|
| desktop `1440x900` | `#/hermes/settings?tab=account&reason=default-credentials` | visible | hidden | hidden | `1` | `0` | `0` |
| mobile `390x844` | `#/hermes/settings?tab=account&reason=default-credentials` | visible | hidden | hidden | `1` | `0` | `0` |

补充说明：

1. Vite 终端在本轮中途保留过旧的历史 403 输出，但 HMR 后重新执行的结构化浏览器结果为最终权威证据。
2. 本轮未新增截图，运行态结论基于原始浏览器结构化输出。

## 自动化验证

### 命令

```bash
npm test -- tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
git diff --check -- packages/client/src/App.vue packages/client/src/components/auth/DefaultCredentialPrompt.vue packages/client/src/components/layout/ProfileSelector.vue tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/profile-selector-default-credential.test.ts
```

### 结论

1. `9` 个测试文件、`87` 个测试全部通过。
2. 新增 `profile-selector-default-credential` 已证明整改态不会触发侧边栏 profile 预加载。
3. 新增 `app-default-credential-remediation` 已证明整改态不会触发全局 model/health 预加载。
4. 更新后的 `default-credential-prompt` 已统一整改入口语义。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | chat 直入稳定送到账户整改页，且全局壳层不再干扰主流程 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 登录页、提醒入口、侧边栏、账户整改页的默认凭据语义已统一 | 无 |
| G4 Evidence And Governance | pass | 自动化测试 + 干净 production runtime 真实浏览器结果已形成双层证据 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议展示 | 无 |
| G6 Accessibility | partial | 仍未补完整键盘路径、焦点顺序、读屏语义证据 | 后续补 a11y |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口均无横向溢出，整改页聚焦保持成立 | 可补 tablet |
| G8 Runtime Verification | pass | clean isolated runtime 下已实现桌面/移动双视口零 403 复验 | 可补录屏 |
| G9 Scope Control | pass | 仅对壳层预加载与统一整改入口做最小修补 | 无 |

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`

## 状态边界

本轮仍不声明：

1. `accepted`
2. `integrated`
3. `production_ready`
4. 完整 a11y 验收完成

## 下一步建议

1. 进入默认凭据整改链路的键盘路径、焦点顺序和读屏验证。
2. 若要进一步收紧治理，可把整改态可访问的账户功能列表显式固化为前端受控清单。
