---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-017
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-017
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-017.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-017.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-017

## 输入

- `docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.md`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-016.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/dist/server/index.js`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- 用户继续要求推进默认凭据治理的下一步真实性闭环

## run

1. 在隔离 production backend + Vite frontend 组合中，复验“默认凭据 token 直进 chat 是否被后端真实拦回账户整改页”。
2. 运行中发现旧 `dist/server/index.js` 未包含 2026-06-23 新源码，于是最小执行 `node scripts/build-server.mjs`，只重编译 server dist。
3. 重启隔离后端后，用 `curl` 直接验证 `/api/hermes/sessions` 已返回 `403 + requiresCredentialChange=true`。
4. 用 system Chrome headless 在桌面 `1440x900` 与移动 `390x844` 下复验 chat 直入链路。
5. 运行中发现整改页仍有无关预加载噪声，于是最小新增：
   - `SettingsView` 整改态跳过 profiles/settings 预加载；
   - `AccountSettings` 整改态跳过头像与锁定 IP 加载并隐藏对应区块；
   - `router` 默认凭据预检，优先把默认用户名 token 送到账户整改页。
6. 补齐对应前端测试并再次复验运行时。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 真实运行复验已成立，且整改页无关 403 噪声已从多条收敛到单条初始噪声 |

## verify

本轮执行并通过：

```bash
node scripts/build-server.mjs
npm test -- tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/api.test.ts tests/client/login-view.test.ts tests/client/default-credential-prompt.test.ts tests/server/user-auth.test.ts
git diff --check -- packages/client/src/api/client.ts packages/client/src/api/auth.ts packages/client/src/router/index.ts packages/client/src/views/hermes/SettingsView.vue packages/client/src/components/hermes/settings/AccountSettings.vue tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

真实运行新增结论：

1. 旧 dist 未重建前，真实 production backend 不能体现新门禁，这一缺口已被识别并修正。
2. 重建后，默认凭据用户访问 `/api/hermes/sessions` 已会被真实 `403` 阻断。
3. 桌面与移动视口下，默认凭据 token 直进 chat 都会被送到账户整改页。
4. 整改页的头像区块和锁定 IP 区块在整改未完成前已不再显示。
5. 运行期控制台 `403` 噪声已从多条收敛到单条初始噪声。

## recover

1. 若后续要继续收敛噪声，可继续追最后 1 条初始 `403` 的来源，不必回退当前后端门禁。
2. 若未来需要给默认凭据整改态增加更多账户自助能力，应优先通过前端裁剪或明确定义 allowlist，而不是直接放宽全局受保护接口。

## debug

当前仍未关闭的边界：

1. 仍缺完整键盘路径 / 焦点顺序 / 读屏证据。
2. 桌面与移动端各仍残留 1 条初始 `403` 控制台噪声，说明首跳阶段还有一个非关键请求未被完全前置拦截。

## 输出

- `docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.md`
- `docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-017.md`
- `docs/harness/evidence/assets/studio-default-credential-backend-enforcement-desktop-20260624.png`
- `docs/harness/evidence/assets/studio-default-credential-backend-enforcement-mobile-20260624.png`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/api/client.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/api/auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 10 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 7.1 UI 质量门禁

| 字段 | 值 |
|---|---|
| UI scope | true |
| Surface | mobile-desktop-shell |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts` |
| Scope | 默认凭据 token 直进 chat 的后端门禁真实复验、整改页无关预加载收敛、路由级预检补强 |
| Tools used | `curl` / `vitest` / `system Chrome (Playwright)` / `git diff --check` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 原始 403 接口证据 + 桌面/移动双视口真实重定向 + 83 tests 通过 + diff check 通过 |
| Status ceiling | `ui_evidence_candidate` |

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

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 默认凭据 token 直进 chat 已稳定跳到账户整改页 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 登录、路由预检、整改页结构与后端门禁语义一致 | 无 |
| G4 Evidence And Governance | pass | 原始接口 + 浏览器运行 + 自动化测试已形成三层证据 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议展示 | 无 |
| G6 Accessibility | partial | 未补完整键盘/读屏证据 | 后续补 a11y |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口无横向溢出，整改页聚焦更强 | 可补更窄视口 |
| G8 Runtime Verification | pass | 默认凭据 chat 直入链路已真实复验 | 可补录屏 |
| G9 Scope Control | pass | 只围绕默认凭据门禁、预加载和预检做最小改动 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | partial |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 继续追最后 1 条初始 `403` 的来源，把默认凭据整改链路收敛到更干净的零噪声态
- 补默认凭据整改链路的键盘路径与焦点顺序验证
