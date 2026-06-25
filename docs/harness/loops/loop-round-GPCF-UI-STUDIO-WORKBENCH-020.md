---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-020
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-020
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-020.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-020.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-020

## 输入

- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-019.md`
- `docs/harness/evidence/studio-default-credential-a11y-verified-20260624.md`
- 用户继续要求推进下一步

## run

1. 读取上一轮结论，确认默认凭据整改链路的可访问性已闭合，本轮不再扩展 a11y 面。
2. 将整改态允许访问的设置范围显式收敛为白名单：
   - 路由守卫拦截带 `reason=default-credentials` 的非 `account` 设置 tab；
   - 设置页在整改态只渲染 `account` tab；
   - URL 自动归一到 `tab=account`。
3. 先补测试，再最小修改实现，再做真实运行态复验。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 默认凭据整改态白名单已显式化，并形成测试与真实运行证据 |

## verify

本轮执行并通过：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

真实运行新增结论：

1. desktop `1440x900` 下，直接进入 `#/hermes/settings?tab=voice&reason=default-credentials` 会真实归一到 `#/hermes/settings?tab=account&reason=default-credentials`。
2. mobile `390x844` 下，同一路径也会真实归一到 `account`。
3. desktop/mobile 页面文本中均不再出现 `Display`、`Voice` 等非白名单设置 tab。
4. 整改提示区焦点行为保持不变，焦点仍落在 `.credential-guidance`。

## recover

1. 若后续继续收紧整改态，只能围绕账户页内部动作白名单，不再回放其他设置域。
2. 当前默认凭据整改链路的入口和设置面边界已经显式化，无需继续在 tab 层扩散。

## debug

当前未关闭的边界：

1. 本轮只约束 `hermes.settings` 整改态白名单，不外推到其他业务工作台。
2. 本轮未引入 Figma 或 Impeccable，继续保留 `figma_not_verified`。

## 输出

- `docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.md`
- `docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-020.md`
- `docs/harness/evidence/assets/studio-default-credential-whitelist-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-whitelist-mobile-20260625.png`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/settings-view-default-credential.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/router-default-credential-guard.test.ts`

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
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue` |
| Scope | 默认凭据整改态白名单显式化，仅允许 account tab 并归一 URL |
| Tools used | `vitest` / `system Chrome (Playwright)` / `curl` / `git diff --check` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 9 个测试文件 91 个测试通过 + desktop/mobile 真实运行态 URL/界面复验 + 双视口截图 |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_ready
Surface: edit/config
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue
Scope: 默认凭据整改态白名单显式化，仅允许 account tab 并归一 URL
Tools used: vitest, system Chrome (Playwright), curl, git diff --check
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 9 个测试文件 91 个测试通过 + desktop/mobile 真实运行态 URL/界面复验 + 双视口截图
Status ceiling: ui_evidence_candidate
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 整改态只保留 `account` tab，非白名单 tab 自动归一 | 无 |
| G2 Design Tokens | pass | 本轮不改视觉令牌 | 无 |
| G3 Component Consistency | pass | 继续沿用既有设置页与账户整改组件 | 无 |
| G4 Evidence And Governance | pass | 测试、浏览器复验、截图和 round 均已留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | pass | 上轮焦点/读屏语义保持有效，本轮实测焦点仍在整改提示区 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口均只展示账户整改页 | 无 |
| G8 Runtime Verification | pass | clean isolated runtime 下 desktop/mobile 均已复验 | 无 |
| G9 Scope Control | pass | 仅改路由守卫、设置页 tab 白名单和对应测试 | 无 |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | pass |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 若继续沿默认凭据整改链路推进，只收敛账户页内部动作白名单，不再扩展到其他设置域
- 若切回 Studio 主线，优先回到更高优先级的工作台或发布边界治理项
