---
doc_id: GPCF-DOC-F035-EVIDENCE-20261022
title: F-035 WAME 侧栏归并 —— 证据摘要
project: GPCF
related_projects: [WAME, WAE, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-035-wame-sidebar-unification/evidence/summary.md
source_path: features/done/F-035-wame-sidebar-unification/evidence/summary.md
sync_direction: local_only
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-035 WAME 三套侧栏归并 —— 证据摘要（2026-10-22）

> 性质：**导航侧栏收口（最小改动、保留行为）**；不声明 `accepted` / `integrated` / `production_ready`；未 commit/push。
> 依据：F-035 feature.yaml 目标、F-034 `o3-sidebar-unification.md`（框架侧唯一侧栏已成立、WAME 侧未归并）、`@globalcloud/app-shell` v1.0.0 契约。

## 1. 盘点（改造前，WAME 仓 `wame/pm-governance`）

| 侧栏/面板 | 文件 | 行数 | 调用方 | 性质 |
|---|---|---|---|---|
| ① 导航侧栏 | `src/app/layout/GlobalCloudSidebar.tsx` | 49 | `layout/GlobalCloudShell.tsx` | **在用导航**（硬编码 4 项） |
| ② 旧侧栏 | `src/app/components/Sidebar.tsx` | 114 | **无任何 import**（grep 全仓为空） | 死代码（第二套实现） |
| ③ 功能面板 | `src/app/components/FunctionPanel.tsx` | 1557 | `components/MainContent.tsx` | **内容区功能面板**（资产/文档/分区/主题/用户菜单），不是导航侧栏 |

跨仓约束：`@globalcloud/app-shell` 是 WAE 私有 workspace 包（`private: true`、exports 指向 `src/index.ts`、依赖 `workspace:*`），**未发布 npm**；WAME 仓无法直接 import ⇒ 本次按**同一契约**在 WAME 侧收口为唯一实现（contract mirror）。

## 2. 改动（WAME 仓；工作区改动，未 commit/push）

| 文件 | 类型 | 改动 |
|---|---|---|
| `src/app/layout/GlobalCloudSidebar.tsx` | 改 | 唯一导航侧栏：导出与 `@globalcloud/app-shell` 同形的 `SidebarItem`/`GlobalCloudSidebarProps`（`items`/`subject`/`rootPath`/`getCurrentPath`/`title`/`description`）；默认项 = 原 4 项（顺序/图标/路径不变）；无 props 渲染与改造前等价；受限项按 `subject.role` 做 L1 呈现收敛 |
| `src/app/layout/GlobalCloudShell.tsx` | 改 | 壳层显式注入 `items={DEFAULT_SIDEBAR_ITEMS}`（导航配置从侧栏组件移到壳层注入） |
| `src/app/components/Sidebar.tsx` | 改 | 114 行独立实现 → **兼容 re-export**（`@deprecated`），`Sidebar` 别名等同统一侧栏；不再保留第二套实现 |
| `src/app/components/FunctionPanel.tsx` | 改（仅头注释） | 标注"内容区功能面板，非导航侧栏；不并入侧栏（产品重构另立项）"；实现零改动 |
| `tests/global-cloud-sidebar.test.tsx` | 新增 | 5 例：默认 4 项等价 / items 注入 / subject 角色收敛 / 激活判定 / 旧 Sidebar 是同一实现别名 |

> 未改 WAE 仓（`@globalcloud/app-shell` 未发布，跨仓直接消费需发布或并入同一 workspace，属授权/发布动作）。
> 环境说明：WAME 仓原本**无 node_modules**（typecheck/test/build 因缺依赖无法运行）；为完成验证执行 `npm ci --no-audit --no-fund`（按 lockfile 安装，未改 lockfile，node_modules 为忽略产物）。基线差量：typecheck 由"缺依赖失败"→ 通过；测试 38 files/184 tests → **39 files/189 tests**。

## 3. 验证命令与真实结果（WAME 仓；基线 = 改造前）

| # | 命令 | 改造前 | 改造后 |
|---|---|---|---|
| 1 | `npx tsc --noEmit` | 缺依赖失败（npm ci 前） | **pass（exit 0）** |
| 2 | `npx vitest run tests/global-cloud-sidebar.test.tsx` | — | **1 file / 5 tests passed** |
| 3 | `npx vitest run`（全量） | 38 files / 184 tests passed（npm ci 后基线） | **39 files / 189 tests passed**（+1 file/+5 tests） |
| 4 | `npx vite build` | pass（chunk >500kB 警告） | **pass**（同警告，非阻断） |
| 5 | `npx eslint`（仅改动文件） | — | pass（exit 0） |
| 6 | `git diff --check`（仅改动文件） | — | pass（exit 0） |
| 7 | `python3 _governance/drafts/ui-spec/tools/ui_gate.py "GlobalCloud WAME"` | — | C10 治理字段暴露 **原始 0 / 有效 0**；C1 有效 47（5 个文件）与 C4 1 **均为既有文件**（useAppContent/WassetCanvas/WaeEditor/project-templates/AIWorkspace，非本次改动） |
| 8 | `python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAME" --fail-on error` | — | **exit 0（error 0）**；R14-dirty-worktree info（9 条未提交，含本任务 5 条） |

> ui_gate `--strict` 在 WAME 的失败为**既有** C1/C4（同上文件），非本次 diff 引入；如实记录，不粉饰。

## 4. 阻塞 / 未完成（真实登记）

1. **未能直接 import `@globalcloud/app-shell`**：该包为 WAE 私有 workspace 包、未发布 npm（`private: true`、exports 指向 TS 源码、依赖 `workspace:*`）；跨仓消费需 ①发布包 或 ②两仓并入同一 workspace，均属发布/架构动作，需老卢或 WAE 属主授权。本次以**契约镜像**（同 props 同行为）落地。
2. **FunctionPanel 未并入导航侧栏**：1557 行是主内容区功能面板（资产/文档/分区/DnD/主题/用户菜单），并入侧栏属**信息架构产品重构**，超出"最小改动、保留行为"，需产品设计 + 验收授权后另行立项。
3. **无视觉回归证据**：本轮以 DOM 测试 + 契约测试守护行为等价，未做截图比对（screenshots=waived）；未做多用户/无障碍实测（waived）与任务流 E2E（pending）。
4. WAME 仓 `wame/pm-governance` 为 PM 综合管理分支，按仓内 AGENTS 规则业务代码应由对应任务分支承接；本轮为跨仓授权实施，未 commit/push、未切分支。

## 5. 回滚（WAME 仓）

```bash
git -C "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAME" restore -- \
  src/app/layout/GlobalCloudSidebar.tsx \
  src/app/layout/GlobalCloudShell.tsx \
  src/app/components/Sidebar.tsx \
  src/app/components/FunctionPanel.tsx
rm -f "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAME/tests/global-cloud-sidebar.test.tsx"
```

无数据迁移、无外部写入、无部署；FunctionPanel 实现未改动，回滚零产品风险。
