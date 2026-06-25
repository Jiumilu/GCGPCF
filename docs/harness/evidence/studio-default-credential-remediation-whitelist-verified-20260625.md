---
doc_id: GPCF-EVIDENCE-8E2F18C4D1
title: Studio 默认凭据整改态白名单复验
project: GPCF
related_projects: [GPCF, WAES, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.md
source_path: docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Studio 默认凭据整改态白名单复验

## 结论

- 默认凭据整改态现在显式收敛为 `account` 单一设置 tab。
- 当用户或系统直接进入 `#/hermes/settings?tab=voice&reason=default-credentials` 时，前端路由会真实归一到 `#/hermes/settings?tab=account&reason=default-credentials`。
- 整改态界面上不再显示 `display`、`voice` 等其他设置 tab，页面只保留当前账户整改入口。

## 代码范围

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/settings-view-default-credential.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/router-default-credential-guard.test.ts`

## 验证

### 自动化测试

执行命令：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

结果：

- `9` 个测试文件通过
- `91` 个测试通过

新增约束点：

- 整改态访问其他设置 tab 时，路由守卫必须重定向回 `account`
- 整改态设置页只渲染 `account` tab，并把 URL 归一到 `tab=account`

### 真实运行态

运行环境：

- backend: `http://127.0.0.1:8667`
- frontend: `http://127.0.0.1:8669`
- 浏览器：system Chrome (Playwright)

实测路径：

1. 使用默认账号 `admin / 123456` 登录。
2. 进入 `#/hermes/settings?tab=voice&reason=default-credentials`。
3. 观察路由是否自动归一、界面是否只保留账户整改页。

实测结果：

- desktop `1440x900`：
  - `hash` 真实为 `#/hermes/settings?tab=account&reason=default-credentials`
  - 页面文本中不再出现 `Display`、`Voice` 等其他设置 tab
  - 焦点仍落在整改提示区 `.credential-guidance`
- mobile `390x844`：
  - `hash` 真实为 `#/hermes/settings?tab=account&reason=default-credentials`
  - 页面文本中不再出现 `Display`、`Voice` 等其他设置 tab
  - 焦点仍落在整改提示区 `.credential-guidance`

截图：

- `docs/harness/evidence/assets/studio-default-credential-whitelist-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-whitelist-mobile-20260625.png`

## UI 质量门禁

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
| G3 Component Consistency | pass | 继续沿用 WAES/Studio 既有设置页与账户整改组件 | 无 |
| G4 Evidence And Governance | pass | 测试、运行态、截图和 round 均已留证 | 无 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 展示 | 无 |
| G6 Accessibility | pass | 上轮焦点/读屏语义保持有效，本轮实测焦点仍在整改提示区 | 无 |
| G7 Responsive And Text Robustness | pass | desktop/mobile 双视口均只展示账户整改页 | 无 |
| G8 Runtime Verification | pass | clean isolated runtime 下 desktop/mobile 均已复验 | 无 |
| G9 Scope Control | pass | 仅改路由守卫、设置页 tab 白名单和对应测试 | 无 |

## 状态边界

- 本证据只证明 `ui_evidence_candidate`
- 不提升 `accepted`
- 不提升 `integrated`
- 不提升 `production_ready`
