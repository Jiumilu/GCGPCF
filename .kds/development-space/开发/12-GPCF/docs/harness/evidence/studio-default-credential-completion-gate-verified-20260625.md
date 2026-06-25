---
doc_id: GPCF-EVIDENCE-6C4D2A91F8
title: Studio 默认凭据整改完成态门禁复验
project: GPCF
related_projects: [GPCF, WAES, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-completion-gate-verified-20260625.md
source_path: docs/harness/evidence/studio-default-credential-completion-gate-verified-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Studio 默认凭据整改完成态门禁复验

## 结论

- 服务端 `requiresCredentialChange` 已从“默认用户名和默认密码同时存在才触发”修正为“任一默认值仍存在就继续触发”。
- 真实链路证明：只改密码后，用户仍被留在 `#/hermes/settings?tab=account&reason=default-credentials`；再改用户名后，整改态才退出。
- 退出整改态后，账户页恢复头像区和锁定 IP 管理区，整改提示区消失。

## 代码范围

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/server/src/middleware/user-auth.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/server/user-auth.test.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/account-settings-default-credential.test.ts`

## 验证

### 自动化测试

执行命令：

```bash
npm test -- tests/client/account-settings-default-credential.test.ts tests/client/settings-view-default-credential.test.ts tests/client/profile-selector-default-credential.test.ts tests/client/app-default-credential-remediation.test.ts tests/client/default-credential-prompt.test.ts tests/client/router-default-credential-guard.test.ts tests/client/login-view.test.ts tests/client/api.test.ts tests/server/user-auth.test.ts
```

结果：

- `9` 个测试文件通过
- `94` 个测试通过

新增约束点：

- 默认用户名或默认密码任一仍存在时，`requiresCredentialChange` 必须保持 `true`
- 只改密码后，账户整改提示必须继续保留
- 两项都完成后，才允许清除 `reason=default-credentials` 并退出整改态

### 真实运行态

运行环境：

- backend: `http://127.0.0.1:8667`
- frontend: `http://127.0.0.1:8669`
- 服务端模式：`NODE_ENV=production` + 临时 `appHome`
- 浏览器：system Chrome (Playwright)

实测路径：

1. 用默认账户 `admin / 123456` 进入 chat，确认被强制导向整改页。
2. 先执行“修改密码”，将密码改为 `stronger-password`。
3. 验证仍停留在整改态。
4. 再执行“修改用户名”，将用户名改为 `owner`。
5. 验证整改态退出。
6. 在完成态下补移动视口验证。

实测结果：

- password-only desktop `1440x900`：
  - `hash` 真实为 `#/hermes/settings?tab=account&reason=default-credentials`
  - 整改提示区仍存在
  - 关闭按钮数量为 `0`
  - 头像区仍未出现
- completed desktop `1440x900`：
  - `hash` 真实为 `#/hermes/settings?tab=account`
  - 整改提示区已消失
  - 头像区与锁定 IP 管理区已出现
- completed mobile `390x844`：
  - `hash` 真实为 `#/hermes/settings?tab=account`
  - 整改提示区已消失
  - 头像区与锁定 IP 管理区已出现

截图：

- `docs/harness/evidence/assets/studio-default-credential-password-only-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-complete-desktop-20260625.png`
- `docs/harness/evidence/assets/studio-default-credential-complete-mobile-20260625.png`

## UI 质量门禁

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

## 状态边界

- 本证据只证明 `ui_evidence_candidate`
- 不提升 `accepted`
- 不提升 `integrated`
- 不提升 `production_ready`
