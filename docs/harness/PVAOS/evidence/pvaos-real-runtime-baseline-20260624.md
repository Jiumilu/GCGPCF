---
doc_id: GPCF-DOC-PVAOS-REAL-RUNTIME-BASELINE-20260624
title: PVAOS 真实运行基线证据 2026-06-24
project: PVAOS
related_projects: [GFIS, GPC, PVAOS, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: PVAOS
kds_space: 开发
kds_path: 开发/03-PVAOS/docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md
source_path: docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# PVAOS 真实运行基线证据 2026-06-24

## 1. 证据定位

本文记录 PVAOS 在 `GlobalCloud 项目群实施方案` 下的首轮真实运行、发布准入、生产域名、测试结果和阻塞状态。

本文不声明 PVAOS 发布完成，不声明客户验收通过，不声明 AaaS 运营闭环完成。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 执行日期 | 2026-06-24 |
| 执行仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS` |
| 当前分支 | `pvaos/D4-release-readiness-governance` |
| 工作区状态 | dirty，存在未跟踪总体/实施方案文档和 `tools/` 目录 |
| 仓库类型 | Vite + React + TypeScript + Vitest + Playwright 运营平台仓库 |
| 证据采集方式 | 本地命令执行 |

## 3. 已执行命令与结果

| 命令 | 结果 | 说明 |
|---|---|---|
| `npm run lint` | pass | ESLint 通过 |
| `npm run validate:modules` | pass | 50 个菜单 ID 和 50 个模块配置通过 |
| `npm run typecheck` | pass | `tsc -p tsconfig.typecheck.json --noEmit` 通过 |
| `npm run test` | fail | 80 个测试文件中 72 个通过、8 个失败；547 个测试中 451 个通过、96 个失败 |
| `npm run release:gate:local` | fail | L0 diff whitespace 通过；L3 verify chain 因 `npm test` 失败而失败 |
| `npm run check:production-domain` | pass | 生产域名页面、CORS、Vercel alias 检查通过 |
| `npm run build` | pass | Vite production build 通过 |

## 4. 已通过的关键证据

### 4.1 模块与类型

```text
Platform module validation passed: 50 menu ids, 50 configured modules.
```

### 4.2 生产域名与 CORS

```text
PVAOS production domain probe report
pvaos.csydsc.com | page:PASS(200) | server:Vercel | cache:HIT | cors:PASS(204) | allow-origin:https://pvaos.csydsc.com
PASS: all domain and CORS probes are healthy.
```

### 4.3 构建

```text
vite v6.4.2 building for production...
4091 modules transformed.
built in 4.09s
```

## 5. 失败点

### 5.1 单元测试失败

`npm run test` 失败摘要：

```text
Test Files  8 failed | 72 passed (80)
Tests       96 failed | 451 passed (547)
```

主要失败原因：

```text
ExperimentalWarning: localStorage is not available because --localstorage-file was not provided.
TypeError: Cannot read properties of undefined (reading 'clear')
TypeError: Cannot read properties of undefined (reading 'getItem')
TypeError: Cannot read properties of undefined (reading 'setItem')
```

受影响测试范围包括 extension registry、extension marketplace、theme SDK、PVAAI API contract、tenant service 和 tenant logging。

### 5.2 发布准入失败

`npm run release:gate:local` 失败于：

```text
[release:gate:local] PASS L0 diff whitespace
[release:gate:local] FAIL L3 verify chain
```

原因是 `npm run verify` 内部执行到 `npm test` 时失败。

## 6. 结论边界

本轮可以登记：

```text
pvaos_build_evidence = verified
pvaos_domain_evidence = verified
pvaos_runtime_evidence = partial_verified
pvaos_repair_required = localstorage_test_environment_release_gate
```

本轮不得登记：

- 不登记 PVAOS 发布完成；
- 不登记 PVAOS 客户验收通过；
- 不登记 PVAOS AaaS 运营闭环完成；
- 不登记 PVAOS production_ready；
- 不登记 PVAOS release gate 完成。

## 7. 下一步

PVAOS 下一轮修复优先级：

1. 修复 Vitest localStorage 测试环境或配置，重跑 `npm run test`。
2. 在测试通过后重跑 `npm run release:gate:local`。
3. 继续补充与 GPC/GFIS/AaaS 的运营、结算和服务化接口证据。
