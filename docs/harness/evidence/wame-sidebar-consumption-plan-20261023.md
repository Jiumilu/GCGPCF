---
doc_id: GPCF-DOC-WAME-SIDEBAR-CONSUMPTION-PLAN-20261023
title: WAME 侧栏消费共享契约方案（2026-10-23）
project: GPCF
related_projects: [GPCF, WAME, WAE]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/wame-sidebar-consumption-plan-20261023.md
source_path: docs/harness/evidence/wame-sidebar-consumption-plan-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# WAME 侧栏消费共享契约方案（2026-10-23）

> 背景：F-035 阻塞于 `@globalcloud/app-shell` 未发布且已被移出发布集；老卢选择 WAME 消费 ui-kit/app-registry 契约。
> 本文件是落地方案，**未改 WAME/WAE 代码**。

## 1. 事实核查

| 包 | 是否有侧栏契约 | 说明 |
|---|---|---|
| `app-shell` | 原应有，但**目录已被清空**、发布集移除 | 无法发布 |
| `app-registry` | **无** `SidebarItem` / `GlobalCloudSidebarProps` | 只有 platform/placement/nav 装配类型 |
| `ui-kit` | 无侧栏契约 | 只有基础组件/状态字典 |
| `ui-templates` / `idp-kit` / `module-kit` | 无 | — |

结论：**当前没有可发布包承载侧栏契约**；直接改 WAME import 无处可导。

## 2. 建议方案（最小、可回滚）

1. WAE `packages/app-registry` 新增纯类型文件 `src/sidebarContract.ts`：
   ```ts
   export interface SidebarItem { id: string; label: string; path: string; requires?: { roles?: string[] } }
   export interface SidebarContractProps { items?: SidebarItem[]; subject?: { role?: string } | null; rootPath?: string; getCurrentPath?: () => string }
   ```
   并在 `src/index.ts` 导出；不影响运行时。
2. 重新 `pnpm release:pack`，产出含该类型的 `app-registry` tgz。
3. WAME 在 `wame/architecture-contracts` 分支：
   - `package.json` 加 `file:` 依赖（六个 tgz 中至少 `app-registry`；如用令牌再逐包加）。
   - `GlobalCloudSidebar.tsx` 把本地 `SidebarItem` 定义改为 `import type { SidebarItem } from '@globalcloud/app-registry'`；保留本地组件实现与默认 4 项行为。
   - 跑 tsc/test/build；保留回滚脚本。
4. 证据：WAME 依赖 lock diff、tsc/test/build 输出、契约类型来源。

## 3. 风险

- `file:` 依赖跨仓相对路径，仅开发态；生产仍需私有 registry。
- `app-registry` 增加纯类型属 additive，不改变运行时，但需 repack/发布。
- WAME 当前 `wame/pm-governance` 分支禁改 package/lock，须换分支。

## 4. 回滚

- 移除 `package.json` 依赖与 lock 变更；恢复本地 `SidebarItem` 定义；`pnpm install`。
- 无运行时数据变更。

## 5. 非声明

- 不声明已发布/已消费；不声明 F-035 可关闭；不声明状态提升。

## 6. 执行进展（2026-10-23 04:00）

- 已完成步骤 1–2：WAE `packages/app-registry/src/sidebarContract.ts` 新增并导出；
  `pnpm typecheck` pass；`pnpm build:packages` + `pnpm release:pack` pass。
- 新 tgz：`globalcloud-app-registry-1.0.0.tgz` 13.1KB / sha256 `b7af0730…`，内含 `dist/sidebarContract.d.ts`。
- 未做：WAME 侧依赖与 import（需 WAME `wame/architecture-contracts` 分支）。

## 7. WAME 侧 patch 文件（2026-10-23 04:10）

- 已生成 `wame-sidebar-consumption.patch`（package.json 增加 file: 依赖；SidebarItem 改为 extends 共享契约 + icon）。
- 应用前提：WAME `wame/architecture-contracts` 分支（PM 分支禁改 package/lock）。
- 应用命令：
  ```bash
  cd "GlobalCloud WAME"
  git switch -c wame/architecture-contracts   # 或使用既有分支
  git apply <本 patch>
  pnpm install
  pnpm typecheck && pnpm test && pnpm build
  ```
- 回滚：`git checkout -- package.json src/app/layout/GlobalCloudSidebar.tsx pnpm-lock.yaml` + `pnpm install`。
- 未在 WAME 应用；未 commit/push。

## 8. patch 校验（2026-10-23 04:20）

- 用 `diff -u` 由真实文件生成 `wame-sidebar-consumption.patch`（避免手写 hunk 计数错误）。
- `git apply --check` 在 WAME 当前工作区 **exit 0**（上下文匹配，可应用）。
- 仍未应用；应用需切换 `wame/architecture-contracts` 分支。

## 9. 隔离 worktree 应用尝试（2026-10-23 04:30）

- 使用既有 `wame/architecture-contracts` worktree（`~/.codex/worktrees/waes-architecture-contracts-pilot-scope`）。
- `git apply` 失败：该分支版本较旧，`GlobalCloudSidebar.tsx` 尚无 `SidebarItem` 接口（F-035 改动不在该分支）。
- 因此 patch 只对当前 `wame/pm-governance` 工作区上下文有效；跨分支应用需 WAME 属主先同步 F-035 改动或重新生成 patch。
- 已清理尝试过程中生成的 `pnpm-lock.yaml`/`pnpm-workspace.yaml`；未改该 worktree 跟踪文件。

## 10. tgz 消费编译验证（2026-10-23 04:50）

- 临时目录 `/tmp/app-registry-contract-test`：`npm install` app-registry tgz（6 packages，install exit 0）。
- `consume.ts` 导入 `SidebarItem` / `SidebarContractProps` 并构造示例。
- `tsc --noEmit --skipLibCheck --moduleResolution bundler` → **exit 0**。
- 结论：app-registry tgz 可作为跨仓类型契约被消费；WAME 仍需在 architecture-contracts 分支落依赖与 import。

## 11. worktree 端到端类型验证（2026-10-23 06:10）

- 在 `wame/architecture-contracts` worktree 中：
  1. 复制当前 F-035 `GlobalCloudSidebar.tsx`；
  2. `package.json` 增加 app-registry tgz 依赖（worktree 路径解析不同，测试用绝对路径）；
  3. `pnpm install --ignore-scripts`（exit 0，pnpm 忽略 build scripts 告警）；
  4. `pnpm typecheck` → **exit 0**。
- 证明：F-035 侧栏实现 + 共享契约类型可在 WAME 分支类型检查通过。
- 已恢复 worktree 跟踪文件并清理生成的 lock/workspace；未 commit。
- 真实 WAME patch 使用仓库根相对路径（`../GlobalCloud WAE/...`），与 worktree 测试的绝对路径等价。

## 12. 分支应用（2026-10-23 09:00）

- 老卢授权：在 `wame/architecture-contracts` worktree 应用 patch（不 commit），决策值 0.782。
- 执行：
  1. 复制当前 F-035 `GlobalCloudSidebar.tsx` 到 worktree；
  2. `git apply` patch（package.json 依赖 + import/interface）；
  3. 临时软链 `~/.codex/worktrees/GlobalCloud WAE` 使相对 file: 依赖可解析；
  4. `pnpm install --ignore-scripts` exit 0；`pnpm typecheck` exit 0；
  5. 移除临时软链与生成的 pnpm-lock。
- 当前 worktree 状态（未提交）：`package.json`、`src/app/layout/GlobalCloudSidebar.tsx` 修改。
- 回滚：`git restore package.json src/app/layout/GlobalCloudSidebar.tsx` + `pnpm install`。
- 注意：该 worktree 可能被其他会话共用，属主提交前需确认。

## 13. 本地提交（2026-10-23 09:10）

- 老卢授权：在 architecture-contracts worktree 本地 commit（不 push），决策值 0.409。
- 提交 `b233438 feat(wame): consume app-registry sidebar contract`（2 files，+78/-16）。
- 门禁：WAME pre-commit pass。
- 未 push；推送留给 WAME 属主。

## 14. 侧栏测试验证（2026-10-23 09:20）

- 在 architecture-contracts worktree 用临时 vitest 配置运行 `tests/global-cloud-sidebar.test.tsx`。
- 初次：4 passed / 1 failed（`components/Sidebar` 别名仍指旧实现）。
- 同步 F-035 `components/Sidebar.tsx` 后：**5/5 passed**。
- 追加本地提交 `ea8f321 fix(wame): keep Sidebar compatibility alias`（不 push）。
- 临时测试文件与 vitest 配置已移除；worktree clean。
- 说明：测试文件未提交（该分支 vitest include 仅 `*.test.ts`，需另调配置）。
