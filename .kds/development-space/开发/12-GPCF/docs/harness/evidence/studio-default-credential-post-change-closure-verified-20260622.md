---
doc_id: GPCF-DOC-1D4C8A73E2
title: Studio 默认凭据治理动作后收口验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-post-change-closure-verified-20260622.md
source_path: docs/harness/evidence/studio-default-credential-post-change-closure-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Studio 默认凭据治理动作后收口验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-POST-CHANGE-CLOSURE-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-013` 的真实结果：默认凭据治理入口已不仅能把用户导到正确页面，还能在用户完成改密/改名后自动收口页内引导，并清除残留的 `reason=default-credentials` 路由参数。

本轮关键事实如下：

1. `AccountSettings` 新增了从服务端重新同步 `requiresCredentialChange` 的收口逻辑。
2. 若服务端已经返回 `requiresCredentialChange=false`，账户页会自动关闭治理引导卡片，并清掉 URL 中的 `reason=default-credentials`。
3. 用户在账户页成功执行改密或改名后，也会立即重新读取当前用户状态，再决定是否关闭治理引导。
4. 后端现有自动化测试已明确证明：默认 `admin / 123456` 用户在改密或改名后，`requiresCredentialChange` 会变成 `false`。
5. 本轮没有对本机真实登录凭据做运行态改写，因此“治理动作后收口”证据来源于前端单测 + 后端单测，而不是对真实账号做破坏性验证。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue
Scope: 用户完成默认凭据治理动作后，页内引导自动收口并清理 default-credentials 路由原因
Tools used: manual, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified, runtime_mutation_skipped
Verification: 前端账户页单测通过 + 登录/提醒回归通过 + 后端 requiresCredentialChange 语义测试通过
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | 账户页新增 `syncCredentialGuidanceFromServer()`，改密/改名成功后重新同步用户状态 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue` |
| 代码修改 | 当 `requiresCredentialChange=false` 时清理 `reason=default-credentials` 路由参数 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue` |
| 前端测试 | 新增账户页治理引导收口测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/account-settings-default-credential.test.ts` |
| 前端测试 | 登录分流与提醒静默回归 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/login-view.test.ts` / `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts` |
| 后端测试 | `requiresCredentialChange` 在改密或改名后会变为 `false` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/server/user-auth.test.ts` |
| 测试命令 | `npm test -- tests/client/account-settings-default-credential.test.ts tests/client/login-view.test.ts tests/client/default-credential-prompt.test.ts` | 结果：`3 passed / 11 tests passed` |
| 测试命令 | `npm test -- tests/server/user-auth.test.ts -- --testNamePattern=\"marks only admin with password 123456 as requiring a credential change\"` | 结果：目标语义断言通过 |

## 验证说明

### 前端收口逻辑

前端单测已验证：

1. 当账户页带有 `reason=default-credentials`，但服务端已返回 `requiresCredentialChange=false` 时：
   - 治理引导卡片不会继续显示
   - 路由会被改写为移除 `reason`
2. 当用户在账户页成功执行修改密码后：
   - 前端会重新获取当前用户状态
   - 若风险已解除，治理引导卡片会隐藏
   - 路由中的 `reason=default-credentials` 会被清理

### 后端语义

后端测试已验证：

1. 默认 `admin / 123456` 用户会被标记为 `requiresCredentialChange=true`
2. 改密后该标志变为 `false`
3. 改用户名后该标志也变为 `false`

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 治理入口现在具备“进入后再收口”的完整页面状态转换 | 后续可继续补更强的一步式改密流 |
| G2 Design Tokens | pass | 本轮不新增视觉系统，只补状态收口逻辑 | 无 |
| G3 Component Consistency | pass | 登录分流、页内引导、治理动作、动作后收口已连成同一链路 | 后续可继续沉淀系统级治理模式 |
| G4 Evidence And Governance | pass | 明确区分“已补前端收口逻辑”和“未做真实账号破坏性验证” | 后续可在授权下补真实动作验证 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 事实边界 | 无 |
| G6 Accessibility | partial | 状态收口逻辑已补，但未新增更多焦点流转证据 | 后续补键盘和模态关闭焦点验证 |
| G7 Responsive And Text Robustness | pass | 本轮逻辑对桌面/移动账户页共用 | 后续补更细视口验证 |
| G8 Runtime Verification | partial | 采用前后端自动化测试闭环，但未对真实本机账号做变更验证 | 如获授权可补真实运行验证 |
| G9 Scope Control | pass | 仅修改账户页状态收口逻辑和对应测试 | 无额外扩面 |

## 结论

本轮最小目标已经达成：

1. 默认凭据治理入口不再只是“把用户带过去”。
2. 用户完成治理动作后，账户页能根据最新用户状态自动收口。
3. 残留的 `reason=default-credentials` 不会继续挂在 URL 上误导后续状态。

本轮状态保持 `ui_partial`，原因是：

1. 未对本机真实登录凭据做运行态改写验证。
2. 后端仍未强制首次登录改密，这仍属于下一阶段治理能力。

## UI Caveats

- `runtime_not_verified`
- `a11y_manual_only`
- `figma_not_verified`
- `credential_change_not_enforced_server_side`

## 下一步建议

1. 如果你允许改动本机当前测试账号，可补一轮真实“改密后重新登录”验证。
2. 若继续推进工程闭环，应考虑后端首次登录强制改密。
3. 将“治理入口 + 治理动作后自动收口”写入项目群统一规范。
