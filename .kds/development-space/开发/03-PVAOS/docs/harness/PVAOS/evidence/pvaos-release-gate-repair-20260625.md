---
doc_id: GPCF-DOC-PVAOS-RELEASE-GATE-REPAIR-20260625
title: PVAOS Release Gate 修复与本地发布准入证据 2026-06-25
project: PVAOS
related_projects: [GFIS, GPC, PVAOS, WAES]
domain: docs
status: controlled
version: v1.0
owner: PVAOS
kds_space: 开发
kds_path: 开发/03-PVAOS/docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md
source_path: docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# PVAOS Release Gate 修复与本地发布准入证据 2026-06-25

## 1. 证据定位

本文登记 `PVAOS-RELEASE-GATE-001` 的本地真实执行结果。

本文只证明 PVAOS 仓在 `pvaos/D4-release-readiness-governance` 分支完成本地 release gate 修复并通过本地发布准入门禁。本文不声明远程 CI、PR、merge、生产发布、客户验收、AaaS 运营闭环或 `accepted` / `integrated` / `production_ready` 完成。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| PVAOS 仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS` |
| 当前分支 | `pvaos/D4-release-readiness-governance` |
| 执行日期 | 2026-06-25 |
| 初始失败目录 | `/tmp/pvaos-npm-test-20260625-092313`、`/tmp/pvaos-release-gate-after-20260625-092932` |
| 通过复跑目录 | `/tmp/pvaos-npm-test-after-20260625-092912`、`/tmp/pvaos-e2e-after-browser-20260625-093410`、`/tmp/pvaos-release-gate-pass-20260625-093517` |
| 本轮修改边界 | `vitest.config.ts`、`package.json`、`package-lock.json` |

## 3. 初始失败

`npm run test` 首次失败：

```text
Test Files  8 failed | 72 passed (80)
Tests  96 failed | 451 passed (547)
TypeError: Cannot read properties of undefined (reading 'clear')
localStorage.clear()
```

根因：根 `vitest.config.ts` 使用 `jsdom`，但未加载已有 `src/app/tests/setup.ts`，导致全局 `localStorage` mock 未注入。

`npm run release:gate:local` 首次失败：

```text
[release:gate:local] FAIL L3 verify chain
```

修复 test 后，release gate 又停在 audit 与 browser smoke：

```text
npm audit --audit-level=moderate ... 8 vulnerabilities
browserType.launch: Executable doesn't exist ... chromium_headless_shell-1217
```

## 4. 修复内容

| 类型 | 文件 | 说明 |
|---|---|---|
| Vitest setup | `vitest.config.ts` | 增加 `setupFiles: ['./src/app/tests/setup.ts']`，加载已有 localStorage、matchMedia、IntersectionObserver、ResizeObserver mocks |
| 依赖安全 | `package.json` | 将 npm/pnpm `dompurify` override 从 `3.4.2` 提升到 `3.4.11` |
| 依赖安全 | `package-lock.json` | 执行 `npm audit fix --registry=https://registry.npmjs.org` 与 `npm install --registry=https://registry.npmjs.org` 后刷新 lock |
| Browser smoke 环境 | Playwright cache | 执行 `npx playwright install chromium` 安装本地 Chromium/headless shell |

## 5. 通过命令与结果

| 命令 | 结果 |
|---|---|
| `npm run lint` | pass |
| `npm run validate:modules` | pass，`50 menu ids, 50 configured modules` |
| `npm run typecheck` | pass |
| `npm run test` | pass，`Test Files 80 passed (80)`，`Tests 547 passed (547)` |
| `npm run build` | pass |
| `npm audit --audit-level=moderate --registry=https://registry.npmjs.org` | pass，`found 0 vulnerabilities` |
| `npm run test:e2e` | pass，`50 passed`，`4 skipped` |
| `npm run check:production-domain` | pass，PVAOS production domain and CORS probes healthy |
| `npm run release:gate:local` | pass，`PASS all local release readiness checks` |

最终 release gate 输出摘要：

```text
Test Files  80 passed (80)
Tests  547 passed (547)
found 0 vulnerabilities
50 passed
4 skipped
[release:gate:local] PASS Production domain and CORS
[release:gate:local] PASS all local release readiness checks.
```

## 6. 状态建议

```text
pvaos_release_gate = verified_with_local_release_gate_boundary
pvaos_test_gate = pass
pvaos_e2e_gate = pass
pvaos_audit_gate = pass
pvaos_release_gate_local = pass
pvaos_status_candidate = ready_for_review
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 7. 保留边界

| 边界 | 说明 |
|---|---|
| local release gate only | 本轮只证明 PVAOS 本地 release gate 通过 |
| live auth skipped | Playwright 中 4 个 live auth smoke 因缺真实 live auth 环境跳过，不作为真实认证验收 |
| no remote CI | 未运行远程 CI |
| no PR/merge | 未创建 PR、未 merge、未推送 |
| no production release | 未执行生产发布、部署或客户通知 |
| no customer acceptance | 没有客户验收人、验收场景或签收证据 |

## 8. 下一步

1. 将 PVAOS 状态推进为 `ready_for_review / local_release_gate_boundary`。
2. 后续需要 PR/remote CI/merge/同步证据，才能进入更高阶段。
3. GFIS/GPC/PVAOS -> SCaaS 链路仍需 GFIS 真实 source-of-record 与 GPC evidence/browser 修复。
