---
doc_id: GPCF-DOC-WAES-LINT-RUNTIME-REPAIR-AUTHORIZATION-20260625
title: WAES lint runtime 修复授权包 2026-06-25
project: WAES
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md
source_path: docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# WAES lint runtime 修复授权包 2026-06-25

## 1. 授权包定位

本文登记 `WAES-LINT-RUNTIME-001` 的真实执行前置状态、阻塞原因、授权范围和验证门禁。

本文不是修复结果，不声明 WAES 已通过 `npm run check`，不声明 WAES 真实运行闭环完成。

## 2. 当前真实检查结果

执行仓库：

```text
/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES
```

当前分支：

```text
waes/integration-release
```

工作区状态：

```text
dirty = true
untracked = GlobalCloud WAES 实施方案.md, GlobalCloud WAES 总体方案.md, tools/
```

预检结果：

| 命令 | 结果 |
|---|---|
| `git diff --check` | pass，无输出 |
| `git ls-files -u` | pass，无冲突文件 |
| `find .codex/locks -name '*.lock' -type f` | pass，无 lock 输出 |
| `npm run lint` | fail，2 个解析错误 |

lint 失败输出：

```text
src/app/components/AppLazyImports.ts
  6:9  error  Parsing error: '>' expected

src/app/plugin/PluginManager.tsx
  14:0  error  Parsing error: Identifier expected
```

## 3. 真实阻塞原因

当前阻塞不是测试失败，也不是构建失败，而是 lint 解析失败。

已定位到两个最小修复点：

| 文件 | 问题 | 预期修复 |
|---|---|---|
| `src/app/components/AppLazyImports.ts` | 文件内包含 JSX，但扩展名为 `.ts`，ESLint 按 TS 解析时在 JSX 标签处失败 | 将文件改为 `.tsx`，并更新引用路径 |
| `src/app/plugin/PluginManager.tsx` | 第 12-14 行附近存在不完整 `import type {` 结构 | 合并/修复 type import，使导入列表完整 |

## 4. 为什么需要授权

WAES 仓 `AGENTS.md` 明确规定：

```text
dirty workspace: allowed = inspect / classify / report
blocked = implement / dispatch / commit / stash / clean
Codex 只能实现包含任务元数据的任务
```

当前 WAES 工作区 dirty，且本轮不是 WAES 仓内已登记的 `.codex/tasks/**` 任务。因此本轮只能形成授权包，不能直接修改 WAES 源码。

## 5. 建议授权文本

如需执行修复，请用户明确确认：

```text
我确认执行 WAES-LINT-RUNTIME-001，允许在 /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES 的 waes/integration-release 分支上进行 local dev 范围内最小修复；允许修改 src/app/components/AppLazyImports.ts 或重命名为 AppLazyImports.tsx、更新其引用，以及修复 src/app/plugin/PluginManager.tsx 的 import type 解析错误；允许运行 npm run lint、npm run check、npm run typecheck、npm run test、npm run build、npm run check:wasm；不允许提交、推送、部署、权限变更、生产写入或删除无关文件。
```

## 6. 授权后允许范围

| allow | value |
|---|---|
| allowed_project | WAES |
| allowed_branch | `waes/integration-release` |
| allowed_environment | local dev only |
| allowed_touches | `src/app/components/AppLazyImports.ts`、`src/app/components/AppLazyImports.tsx`、引用该文件的 import、`src/app/plugin/PluginManager.tsx` |
| allowed_commands | `npm run lint`、`npm run check`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run check:wasm` |
| allowed_evidence | `docs/harness/WAES/evidence/waes-lint-runtime-repair-*.md` |

## 7. 禁止范围

| forbid | value |
|---|---|
| git_commit | true |
| git_push | true |
| deployment | true |
| permission_change | true |
| production_write | true |
| delete_unrelated_files | true |
| accepted_or_integrated_upgrade | true |
| customer_acceptance_claim | true |

## 8. 验证门禁

授权执行后，必须至少通过：

```bash
npm run lint
npm run check
```

若 `npm run check` 仍失败，必须记录失败命令、失败原因、剩余阻塞和回滚边界，不得声明 WAES 从 `repair_required` 升级。

若全部通过，GPCF 侧仍最多登记：

```text
waes_lint_runtime_repair = verified_with_local_dev_boundary
waes_status_candidate = ready_for_review
```

是否升级仍需 GPCF/Harness 后续裁决。

## 9. 当前结论

```text
waes_lint_runtime_repair_authorization = required
waes_lint_runtime_failure_reproduced = true
waes_dirty_workspace = true
waes_implementation_allowed_without_authorization = false
waes_status = repair_required
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```
