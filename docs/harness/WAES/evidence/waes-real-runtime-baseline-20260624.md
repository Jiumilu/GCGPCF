---
doc_id: GPCF-DOC-WAES-REAL-RUNTIME-BASELINE-20260624
title: WAES 真实运行基线证据 2026-06-24
project: WAES
related_projects: [WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md
source_path: docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAES 真实运行基线证据 2026-06-24

## 1. 证据定位

本文记录 WAES 在 `GlobalCloud 项目群实施方案` 下的首轮真实运行基线采集结果。

本文只证明本轮在本地仓库执行过指定命令，并记录结果边界；不声明 WAES 真实运行闭环已完成，不声明跨项目集成完成，不声明客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 执行日期 | 2026-06-24 |
| 执行仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES` |
| 当前分支 | `waes/integration-release` |
| 工作区状态 | dirty，存在未跟踪治理文档和 `tools/` 目录 |
| 依赖状态 | `node_modules_present` |
| 证据采集方式 | 本地命令执行 |

## 3. 执行命令与结果

| 命令 | 结果 | 说明 |
|---|---|---|
| `git branch --show-current` | pass | 输出 `waes/integration-release` |
| `git diff --check` | pass | 无输出 |
| `git ls-files -u` | pass | 无冲突文件 |
| `test -d node_modules && echo node_modules_present || echo node_modules_missing` | pass | 输出 `node_modules_present` |
| `npm run check` | fail | `typecheck` 执行后进入 `lint`，`lint` 因 2 个解析错误失败，后续链路被中断 |
| `npm run typecheck` | pass | `tsc --noEmit` 通过 |
| `npm run test` | pass | 33 个测试文件通过，135 个测试通过；输出包含 `Not implemented: navigation to another Document` 提示 |
| `npm run build` | pass | Vite 构建通过；输出包含 chunk 大小超过 500 kB 的警告 |
| `npm run check:wasm` | pass | WAE Rust+WASM 必需文件、可选文件和依赖检查通过 |

## 4. 失败点

`npm run check` 的失败点是 `npm run lint`：

```text
src/app/components/AppLazyImports.ts
  6:9  error  Parsing error: '>' expected

src/app/plugin/PluginManager.tsx
  14:0  error  Parsing error: Identifier expected
```

现场读取显示：

- `src/app/components/AppLazyImports.ts` 包含 JSX，但文件扩展名为 `.ts`，ESLint 解析时在 JSX 标签处失败；
- `src/app/plugin/PluginManager.tsx` 在第 12-14 行附近存在不完整的 `import type {` 结构。

## 5. 结论边界

本轮可以登记：

```text
waes_runtime_evidence = partial_verified
waes_repair_required = lint_parse_errors
```

本轮不得登记：

- 不登记 WAES 真实运行闭环完成；
- 不登记 WAES 与 XWAIL、AaaS、KDS、Brain 的真实集成完成；
- 不登记可交付版本已完成；
- 不登记客户验收通过。

## 6. 下一步

WAES 下一轮应在明确授权的实现分支或隔离 worktree 中修复 lint 解析错误，然后重新执行：

```bash
npm run check
```

修复前，WAES 在核心链路证据矩阵中的真实运行状态应保持 `repair_required`，真实研发状态可标记为 `partial_verified`。
