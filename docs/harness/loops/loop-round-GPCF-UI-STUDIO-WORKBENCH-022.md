---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-022
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-022
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-022.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-022.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-022

## 输入

- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-021.md`
- `docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.md`
- 用户继续要求推进下一步

## run

1. 读取上一轮结论，确认整改态的入口、设置域和账户动作白名单都已收紧。
2. 复核整改完成态退出条件，发现服务端仍把 `requiresCredentialChange` 判成“默认用户名和默认密码同时存在才触发”。
3. 先补失败测试，把规则改成“任一默认值仍存在都必须继续整改”，再做真实运行复验。
4. 在干净临时 `appHome` 的生产态源码服务中，走完整链路：
   - 默认登录进入整改态；
   - 只改密码，仍留在整改态；
   - 再改用户名，退出整改态；
   - 补 completed mobile 复验。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 默认凭据整改完成态门禁已修正，并形成测试与真实运行证据 |

## verify

本轮执行并通过：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

真实运行新增结论：

1. password-only desktop `1440x900` 下，改完密码后仍停留在 `#/hermes/settings?tab=account&reason=default-credentials`。
2. completed desktop `1440x900` 下，再改用户名后 URL 变为 `#/hermes/settings?tab=account`，整改提示区消失，头像区和锁定 IP 管理区恢复出现。
3. completed mobile `390x844` 下，账户页同样保持无整改提示区，头像区和锁定 IP 管理区仍可见。

## recover

1. 默认凭据整改链路的退出条件现已闭合，后续无需继续围绕该链路扩散开发。
2. 若后续再次进入这条链路，只需要做回归验证，不需要再改规则。

## debug

当前未关闭的边界：

1. 本轮只修正默认凭据整改完成态门禁，不外推到其他权限或登录治理链路。
2. 本轮未引入 Figma 或 Impeccable，继续保留 `figma_not_verified`。

## 输出

- `docs/harness/evidence/studio-default-credential-completion-gate-verified-20260625.md`
- `docs/harness/evidence/studio-default-credential-completion-gate-verified-20260625.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-022.md`
- `docs/harness/evidence/assets/studio-default-credential-password-only-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-complete-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-complete-mobile-20260625.png`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/server/user-auth.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/account-settings-default-credential.test.ts`

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
| Surface | edit/config |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts` |
| Scope | 默认凭据整改完成态门禁修正，必须在用户名和密码都脱离默认值后才退出整改态 |
| Tools used | `vitest` / `system Chrome (Playwright)` / `curl` / `git diff --check` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 9 个测试文件 94 个测试通过 + password-only desktop + completed desktop/mobile 真实运行复验 + 三张截图 |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_ready
Surface: edit/config
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts
Scope: 默认凭据整改完成态门禁修正，必须在用户名和密码都脱离默认值后才退出整改态
Tools used: vitest, system Chrome (Playwright), curl, git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 9 个测试文件 94 个测试通过 + password-only desktop + completed desktop/mobile 真实运行复验 + 三张截图
Status ceiling: ui_evidence_candidate
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 整改态与完成态页面边界真实切换 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 继续沿用既有整改提示、账户页和完成态结构 | 无 |
| G4 Evidence And Governance | pass | 测试、运行态、截图和 round 均已留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | pass | 整改提示与完成态切换未破坏既有焦点语义 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 完成态均稳定 | 无 |
| G8 Runtime Verification | pass | password-only 与 completed 两阶段均已真实复验 | 无 |
| G9 Scope Control | pass | 仅改服务端整改判定和对应测试 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | pass |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 默认凭据整改链路到此可以收口，后续只保留回归验证
- 切回 Studio 主线，优先回到 release boundary 治理或更高优先级工作台任务
