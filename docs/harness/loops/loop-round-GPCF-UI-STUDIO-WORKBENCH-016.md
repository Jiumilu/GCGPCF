---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-016
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-016
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-016.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-016.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-016

## 输入

- `docs/harness/evidence/studio-default-credential-mobile-runtime-verified-20260623.md`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-015.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/api/client.ts`
- 用户要求继续下一轮，最小目标是把默认凭据治理从前端提示收口到后端真实强制门禁

## run

1. 审计 Studio 当前默认凭据治理边界，确认后端此前只回传 `requiresCredentialChange`，并未阻断受保护接口。
2. 在后端鉴权中间件中新增默认凭据整改 allowlist，只保留 `me/change-password/change-username` 三条最小通路。
3. 在前端 API 客户端中识别 remediation `403`，保留当前 token 与 profile，统一跳转到账户页治理入口。
4. 补齐后端与前端最小回归测试，覆盖阻断、allowlist 和跳转语义。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 后端强制门禁与最小客户端跳转已落地，自动化证据已形成；真实运行复验留给下一轮 |

## verify

本轮执行并通过：

```bash
npm test -- tests/server/user-auth.test.ts tests/client/api.test.ts tests/client/login-view.test.ts tests/client/account-settings-default-credential.test.ts tests/client/default-credential-prompt.test.ts
git diff --check -- packages/server/src/middleware/user-auth.ts packages/server/src/controllers/auth.ts packages/client/src/api/client.ts packages/client/src/components/auth/AuthEventListener.vue tests/server/user-auth.test.ts tests/client/api.test.ts
```

验证事实：

1. `5` 个测试文件、`76` 个测试全部通过。
2. 默认凭据用户访问 `/api/hermes/sessions` 已会被后端 `403` 阻断。
3. 默认凭据用户仍可访问 `GET /api/auth/me`、`POST /api/auth/change-password`、`POST /api/auth/change-username`。
4. 客户端在 remediation `403` 下不会清理登录态，而会重定向到 `hermes.settings?tab=account&reason=default-credentials`。

## recover

1. 若后续真实运行复验发现还有路由级绕行，可在不改后端门禁前提下补客户端前置守卫。
2. 若账户页需要更多自助能力，可再讨论是否扩展 allowlist，但默认不放开 `avatar/locked-ips` 等非必要接口。

## debug

当前剩余缺口：

1. 本轮没有重新拉起隔离运行时，因此仍缺“默认凭据登录后直接进 chat 被后端阻断”的真实运行证据。
2. 本轮未新增键盘路径、读屏或移动端再回归验证，因此 UI 状态上限仍保持 `ui_partial`。

## 输出

- `docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.md`
- `docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-016.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/controllers/auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/api/client.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/AuthEventListener.vue`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 7.1 UI 质量门禁

| 字段 | 值 |
|---|---|
| UI scope | true |
| Surface | mobile-desktop-shell |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts` |
| Scope | 默认凭据用户的后端强制整改门禁、remediation 403 跳转与最小测试闭环 |
| Tools used | `vitest` / `git diff --check` |
| Tools unavailable | `runtime_not_verified` / `mobile_not_verified` / `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 后端鉴权测试通过 + 客户端 API 跳转测试通过 + 登录页/账户页既有治理测试通过 + diff check 通过 |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_partial
Surface: mobile-desktop-shell
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts
Scope: 默认凭据用户的后端强制整改门禁、remediation 403 跳转与最小测试闭环
Tools used: vitest, git diff --check
Tools unavailable: runtime_not_verified, mobile_not_verified, impeccable_not_invoked, figma_not_verified
Verification: 后端鉴权测试通过 + 客户端 API 跳转测试通过 + 登录页/账户页既有治理测试通过 + diff check 通过
Status ceiling: ui_evidence_candidate
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 后端门禁把聊天入口与账户整改入口串成固定路径 | 后续可补路由级守卫 |
| G2 Design Tokens | pass | 本轮未改视觉层 | 无 |
| G3 Component Consistency | pass | 沿用 WAES/Studio 现有框架和账户页治理入口 | 无 |
| G4 Evidence And Governance | pass | 已从提示升级到后端真实阻断，且证据边界清楚 | 后续补运行态证据 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议展示 | 无 |
| G6 Accessibility | partial | 未新增完整 a11y 验证 | 后续补充 |
| G7 Responsive And Text Robustness | partial | 未重跑视口级真实验证 | 后续补充 |
| G8 Runtime Verification | partial | 本轮以自动化为主，未补隔离运行时复验 | 下一轮补真实运行 |
| G9 Scope Control | pass | 只改鉴权、客户端 403 与测试 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | partial |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 进入隔离运行时，复验“默认凭据登录后直接进 chat 被后端阻断并跳到账户页”
- 若希望页面壳层也立即拦截，再补客户端路由级前置守卫
