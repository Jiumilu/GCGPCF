---
doc_id: GPCF-EVIDENCE-79B4D3F1A6
title: Studio 默认凭据整改态账户动作白名单复验
project: GPCF
related_projects: [GPCF, WAES, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.md
source_path: docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Studio 默认凭据整改态账户动作白名单复验

## 结论

- 强制整改仍成立时，`/hermes/settings?tab=account` 会自动补回 `reason=default-credentials`。
- mandatory 整改提示区不再允许手动关闭，账户页内部动作收敛为整改所需动作。
- desktop/mobile 真实运行下仍只保留 `account` 整改页，焦点保持在整改提示区。

## 代码范围

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/router-default-credential-guard.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/account-settings-default-credential.test.ts`

## 验证

### 自动化测试

执行命令：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

结果：

- `9` 个测试文件通过
- `93` 个测试通过

新增约束点：

- 当默认凭据整改仍必需时，访问 `hermes.settings` 但缺少 `reason` 也必须归一到 `tab=account&reason=default-credentials`
- mandatory 整改提示区不再渲染关闭按钮

### 真实运行态

运行环境：

- backend: `http://127.0.0.1:8667`
- frontend: `http://127.0.0.1:8669`
- 浏览器：system Chrome (Playwright)

实测路径：

1. 使用默认账号 `admin / 123456` 登录。
2. 手工进入 `#/hermes/settings?tab=account`。
3. 观察是否自动补回 `reason=default-credentials`。
4. 观察 mandatory 提示区是否还有关闭按钮。

实测结果：

- desktop `1440x900`：
  - `hash` 真实为 `#/hermes/settings?tab=account&reason=default-credentials`
  - `.credential-guidance__dismiss` 数量为 `0`
  - 焦点仍落在 `.credential-guidance`
  - 页面文本中不出现 `Display`、`Voice` 等其他设置 tab
- mobile `390x844`：
  - `hash` 真实为 `#/hermes/settings?tab=account&reason=default-credentials`
  - `.credential-guidance__dismiss` 数量为 `0`
  - 焦点仍落在 `.credential-guidance`
  - 页面文本中不出现 `Display`、`Voice` 等其他设置 tab

截图：

- `docs/harness/evidence/assets/studio-default-credential-account-whitelist-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-account-whitelist-mobile-20260625.png`

## UI 质量门禁

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
| G4 Evidence And Governance | pass | 测试、运行态、截图和 round 均已留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | pass | 提示区焦点语义保持有效，且无额外隐藏动作破坏键盘路径 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口均只保留整改入口 | 无 |
| G8 Runtime Verification | pass | clean isolated runtime 下 desktop/mobile 均已复验 | 无 |
| G9 Scope Control | pass | 仅改路由守卫、提示关闭动作与对应测试 | 无 |

## 状态边界

- 本证据只证明 `ui_evidence_candidate`
- 不提升 `accepted`
- 不提升 `integrated`
- 不提升 `production_ready`
