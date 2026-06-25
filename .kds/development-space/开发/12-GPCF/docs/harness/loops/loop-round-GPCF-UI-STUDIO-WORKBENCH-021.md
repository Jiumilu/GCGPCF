---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-021
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-021
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-021.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-021.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-021

## 输入

- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-020.md`
- `docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.md`
- 用户继续要求推进下一步

## run

1. 复读上一轮结论，确认默认凭据整改态的设置面白名单已显式化。
2. 继续收敛账户页内部动作白名单：
   - 强制整改中的 `hermes.settings` 访问缺少 `reason` 时自动补回 `reason=default-credentials`；
   - mandatory 整改提示区不再允许手动关闭。
3. 先补失败测试，再最小修改路由守卫和账户页提示动作，再做真实运行复验。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 默认凭据整改态账户页内部动作白名单已收紧，并形成测试与真实运行证据 |

## verify

本轮执行并通过：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

真实运行新增结论：

1. desktop `1440x900` 下，直接进入 `#/hermes/settings?tab=account` 会真实补回 `#/hermes/settings?tab=account&reason=default-credentials`。
2. mobile `390x844` 下，同一路径也会真实补回整改 reason。
3. desktop/mobile 下 mandatory 提示区的关闭按钮数量均为 `0`。
4. 焦点仍真实落在 `.credential-guidance`，页面文本中不出现 `Display`、`Voice` 等其他设置 tab。

## recover

1. 若后续还要继续收紧默认凭据整改链路，只能围绕账户页内的提交路径与完成态切换，不再扩展到其他页面。
2. 当前整改态的入口、设置域、账户页提示动作三层白名单已闭合，无需继续在 UI 面扩散。

## debug

当前未关闭的边界：

1. 本轮只约束默认凭据整改链路，不外推到其他工作台页面。
2. 本轮未引入 Figma 或 Impeccable，继续保留 `figma_not_verified`。

## 输出

- `docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.md`
- `docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-021.md`
- `docs/harness/evidence/assets/studio-default-credential-account-whitelist-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-account-whitelist-mobile-20260625.png`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/router-default-credential-guard.test.ts`
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
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue` |
| Scope | 默认凭据整改态账户页内部动作白名单收紧，mandatory 提示不可关闭且缺失 reason 的账户设置访问会自动归一 |
| Tools used | `vitest` / `system Chrome (Playwright)` / `curl` / `git diff --check` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 9 个测试文件 93 个测试通过 + desktop/mobile 真实运行态 URL/界面复验 + 双视口截图 |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_ready
Surface: edit/config
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue
Scope: 默认凭据整改态账户页内部动作白名单收紧，mandatory 提示不可关闭且缺失 reason 的账户设置访问会自动归一
Tools used: vitest, system Chrome (Playwright), curl, git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 9 个测试文件 93 个测试通过 + desktop/mobile 真实运行态 URL/界面复验 + 双视口截图
Status ceiling: ui_evidence_candidate
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 账户整改页在 mandatory 状态下保持单一路径与单一提示入口 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 沿用既有设置页和整改提示组件，仅移除越权关闭动作 | 无 |
| G4 Evidence And Governance | pass | 测试、浏览器复验、截图和 round 均已留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | pass | 提示区焦点语义保持有效，且无额外隐藏动作破坏键盘路径 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口均只保留整改入口 | 无 |
| G8 Runtime Verification | pass | clean isolated runtime 下 desktop/mobile 均已复验 | 无 |
| G9 Scope Control | pass | 仅改路由守卫、提示关闭动作和对应测试 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | pass |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 若继续沿默认凭据整改链路推进，只保留整改完成态切换与提交路径复验，不再扩展新的 UI 面
- 若切回 Studio 主线，优先回到 release boundary 治理或更高优先级工作台改造
