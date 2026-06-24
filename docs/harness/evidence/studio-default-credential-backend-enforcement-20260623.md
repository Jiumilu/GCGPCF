---
doc_id: GPCF-DOC-8C4A16F2DE
title: Studio 默认凭据后端强制门禁落地证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.md
source_path: docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据后端强制门禁落地证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-BACKEND-ENFORCEMENT-20260623`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-016` 的新增事实：Studio 默认凭据治理已从“前端登录后提示并跳转”收口到“后端真实阻断受保护接口，只保留整改最小通道”。

本轮新增事实如下：

1. 后端 `requireUserJwt` 现在会识别“默认用户名 + 默认密码”用户，并对受保护接口执行强制整改门禁。
2. 默认凭据用户仅保留 3 条整改所需通路：`GET /api/auth/me`、`POST /api/auth/change-password`、`POST /api/auth/change-username`。
3. 其他受保护本地 BFF 接口会返回 `403`，并显式附带 `requiresCredentialChange: true`。
4. 前端 `request()` 已识别该 `403`，不会清理现有登录态，而是把用户重定向到 `#/hermes/settings?tab=account&reason=default-credentials`。
5. `currentUser` 已不再按 `HERMES_DESKTOP === true` 关闭整改标记，桌面/网页端语义回到一致。

## Required Summary

```text
UI gate status: ui_partial
Surface: mobile-desktop-shell
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts
Scope: 默认凭据用户的后端强制整改门禁、前端 remediation 403 跳转与最小回归测试
Tools used: vitest, git diff --check
Tools unavailable: runtime_not_verified, mobile_not_verified, impeccable_not_invoked, figma_not_verified
Verification: 后端鉴权测试通过 + 客户端 API 跳转测试通过 + 登录页/账户页既有治理测试通过 + diff check 通过
Status ceiling: ui_evidence_candidate
```

## 代码落点

| 类型 | 路径 | 变更 |
|---|---|---|
| 后端门禁 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts` | 新增默认凭据判定与整改 allowlist |
| 后端语义 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/controllers/auth.ts` | `currentUser` 统一复用后端整改判定 |
| 前端跳转 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/api/client.ts` | 识别 remediation 403 并跳转账户页 |
| 前端提示 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/AuthEventListener.vue` | 新增整改提示消息 |
| 回归测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/server/user-auth.test.ts` | 新增默认凭据阻断与 allowlist 用例 |
| 回归测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/api.test.ts` | 新增 remediation 403 跳转用例 |

## 验证结果

### 测试命令

```bash
npm test -- tests/server/user-auth.test.ts tests/client/api.test.ts tests/client/login-view.test.ts tests/client/account-settings-default-credential.test.ts tests/client/default-credential-prompt.test.ts
git diff --check -- packages/server/src/middleware/user-auth.ts packages/server/src/controllers/auth.ts packages/client/src/api/client.ts packages/client/src/components/auth/AuthEventListener.vue tests/server/user-auth.test.ts tests/client/api.test.ts
```

### 测试结论

1. `5` 个测试文件全部通过。
2. 总计 `76` 个测试全部通过。
3. 新增后端门禁用例已证明：默认凭据用户访问 `/api/hermes/sessions` 会被 `403` 阻断。
4. 新增 allowlist 用例已证明：默认凭据用户仍可访问 `me/change-password/change-username` 三条整改通路。
5. 新增客户端用例已证明：收到 `requiresCredentialChange: true` 的 `403` 时，前端会保留 token 与 profile，并跳到账户设置页。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 聊天主入口与账户整改入口已由后端门禁串成固定治理路径 | 后续可再补路由级前置守卫 |
| G2 Design Tokens | pass | 本轮未改视觉令牌，只补治理行为 | 无 |
| G3 Component Consistency | pass | 登录分流、账户整改、403 跳转仍复用现有 WAES/Studio 框架 | 无 |
| G4 Evidence And Governance | pass | 默认凭据整改已从提示升级为真实后端阻断，且证据与状态边界清晰 | 后续补运行态截图或录屏 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议展示 | 无 |
| G6 Accessibility | partial | 未新增键盘/读屏验证 | 后续补 a11y 证据 |
| G7 Responsive And Text Robustness | partial | 本轮未重跑移动端/桌面端真实运行视口 | 后续补运行复验 |
| G8 Runtime Verification | partial | 本轮以自动化测试为主，未重新拉起隔离运行时 | 后续补真实运行复验 |
| G9 Scope Control | pass | 仅修改鉴权、客户端 403 处理与最小测试 | 无 |

## 结论

默认凭据治理现在具备新的真实约束层：

1. 登录成功不再代表可继续使用聊天与其他受保护能力。
2. 只要仍使用默认凭据，后端会把用户限制在整改通道内。
3. 前端会把该限制转译成明确的账户页治理入口，而不是登出或无意义报错。

这关闭了“手工改地址或直接打接口即可绕过治理”的缺口，但本轮仍保持 `ui_partial`，因为尚未补充这次后端门禁的真实运行态复验。

## UI Caveats

- `runtime_not_verified`
- `mobile_not_verified`
- `a11y_manual_only`
- `impeccable_not_invoked`
- `figma_not_verified`

## 下一步建议

1. 用隔离运行时补一次“默认凭据登录后直接进 chat 被后端阻断并跳到账户页”的真实复验。
2. 视需要再补客户端路由级前置守卫，把页面壳层也收得更严。
