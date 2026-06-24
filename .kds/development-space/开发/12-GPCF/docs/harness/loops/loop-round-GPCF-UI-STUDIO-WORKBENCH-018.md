---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-018
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-018
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-018.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-018.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-018

## 输入

- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-017.md`
- `docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/App.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/ProfileSelector.vue`
- 用户继续要求推进默认凭据整改链路的下一步

## run

1. 复读上一轮零星 `403` 噪声结论，先做最小定位，不扩散修改范围。
2. 通过真实浏览器链路确认剩余受保护请求固定为 `GET /api/hermes/profiles`。
3. 定位触发源为全局侧边栏 `ProfileSelector` 的 `onMounted -> fetchProfiles()`。
4. 最小新增三处前端收敛：
   - `App.vue` 整改态暂停全局模型与健康轮询预加载；
   - `DefaultCredentialPrompt.vue` 统一补齐默认凭据整改 reason；
   - `ProfileSelector.vue` 整改态下跳过 profiles 预加载，离开整改态后恢复正常加载。
5. 补齐壳层与侧边栏对应测试，并在干净隔离 production runtime 中重跑桌面/移动双视口复验。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 默认凭据整改链路已完成桌面与移动零 403 运行复验，当前剩余缺口转为 a11y 证据 |

## verify

本轮执行并通过：

```bash
npm test -- tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/settings-view-default-credential.test.ts tests/client/account-settings-default-credential.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
git diff --check -- packages/client/src/App.vue packages/client/src/components/auth/DefaultCredentialPrompt.vue packages/client/src/components/layout/ProfileSelector.vue tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/profile-selector-default-credential.test.ts
```

真实运行新增结论：

1. 剩余最后 1 条 `403` 已被定位为 `ProfileSelector` 的 `profiles` 预加载。
2. 修补后，在干净 isolated production runtime 中，desktop `1440x900` 与 mobile `390x844` 直进 chat 都会稳定落到账户整改页。
3. 修补后，desktop 与 mobile 的控制台错误数与 `403` 响应数均为 `0`。

## recover

1. 后续若继续做默认凭据治理，优先转到键盘路径、焦点顺序与读屏语义，不再继续扩展功能面。
2. 若未来需要在整改态保留更多壳层组件，应继续按“整改态 defer、离开整改态恢复”的方式做局部白名单，而不是放开受保护接口。

## debug

当前未关闭的边界：

1. 仍缺完整 a11y 证据。
2. Vite 终端保留过中途旧日志，最终判断必须以修补后重新跑出的结构化浏览器结果为准。

## 输出

- `docs/harness/evidence/studio-default-credential-zero-noise-remediation-20260624.md`
- `docs/harness/evidence/studio-default-credential-zero-noise-remediation-20260624.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-018.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/App.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/ProfileSelector.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/app-default-credential-remediation.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/profile-selector-default-credential.test.ts`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 9 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 7.1 UI 质量门禁

| 字段 | 值 |
|---|---|
| UI scope | true |
| Surface | mobile-desktop-shell |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/ProfileSelector.vue` |
| Scope | 默认凭据整改态全局壳层预加载收敛、侧边栏 profile 预加载抑制、零噪声运行复验 |
| Tools used | `vitest` / `system Chrome (Playwright)` / `curl` / `git diff --check` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 9 个测试文件 87 个测试通过 + clean isolated runtime desktop/mobile 双视口零 403 复验 |
| Status ceiling | `ui_evidence_candidate` |

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

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | chat 直入仍稳定进入整改页，且壳层不再抢跑受保护请求 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 默认凭据整改语义已在登录页、提醒入口、壳层与整改页保持一致 | 无 |
| G4 Evidence And Governance | pass | 自动化 + 真实浏览器零噪声结果已分离留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | partial | 键盘路径、焦点、读屏证据未补 | 后续补 a11y |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口保持无横向溢出 | 可补 tablet |
| G8 Runtime Verification | pass | clean isolated runtime 下 desktop/mobile 双视口零 403 | 可补录屏 |
| G9 Scope Control | pass | 只围绕壳层预加载与统一整改入口做最小修补 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | partial |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 进入默认凭据整改链路的键盘路径、焦点顺序与读屏验证
- 如继续治理，可把整改态允许访问的账户功能显式整理为受控白名单
