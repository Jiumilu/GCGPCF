---
doc_id: GPCF-DOC-F036-REVIEW-20261022
title: F-036 正式接入评审准备（UI gate 六件套证据与评审建议，2026-10-22）
project: GPCF
related_projects: [WAE, PKC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/review-20261022/README.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/review-20261022/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-036 正式接入评审准备（UI gate 六件套，2026-10-22）

> 性质：**评审准备材料**，不是验收结论。不声明 PKC 已接入 / accepted / integrated / production_ready；不关闭 Feature；未 commit/push；未改 PKC 仓 / WAE 业务代码（新增内容全部在 F-036 证据目录）。
> 评审建议：**conditional（有条件进入正式接入评审）** —— 六门均有真实证据，但存在 2 项 shell 级无障碍风险、E2E 依赖 WAE 未提交修复、PKC 侧 P4/P5 与真实嵌入未完成。

## 0. 六门总览

| gate | 取值 | 证据 | 说明 |
|---|---|---|---|
| `functional_completeness` | pass | `evidence/summary.md` §2–§3；`review.spec.ts`（admin 侧栏入口可见/可进入）；`check:apps`/`build` | PKC 注册 + 页入口 + 菜单 + 入口页行为齐备 |
| `quality_baseline` | pass | `logs/wae-checks.log`；`e2e-20261022/logs/run3-raw-dev-pass/`；`ui_gate` C1/C9/C10 | WAE 五项门禁全过；ui_gate C10 有效 0 |
| `multi_user_usability` | **pass（本轮新增）** | 本目录 `screens/review-01/02*.png`、`logs/review-assertions.json` | A=system-admin 可见 `app-nav-pkc`；B=viewer `/me` menus=`[overview, feedback-center, scene, pqc-sop]`（无 pkc）、侧栏 `app-nav-pkc` 计数 0（服务端 403/菜单收敛不被 UI 掩盖） |
| `task_flow_e2e_status` | pass（复用 run3） | `e2e-20261022/README.md` §3、`logs/run3-raw-dev-pass/` | 原始 dev 无垫片 10 步全过；pageErrors=0 / externalRequests=0 |
| `accessibility_status` | **pass（R-A11Y-1/2 已修复）** | 本目录 `screens/review-03/04*.png`、`logs/review-assertions.json`（mainCount=1 / shellUnnamedCount=0 / trap=false） | pkc 页 h1/aria 正常、页内可交互元素可访问名缺失 0；键盘真实 Tab 到达 `app-nav-pkc` 且焦点可见；16 步 Tab：distinct=14、**无陷阱**；`<main>` landmark=1、shell 未命名控件=0（修复见 §3.1） |
| `evidence_overexposure_gate` | pass | `e2e-20261022/README.md` §3（机器字段 leaked=[]）；`ui_gate` C10 有效 0 | 人类入口不暴露 packageId/evidenceRefs/contentDigest 等 |

## 1. 方法与环境（隔离、可复现、可清理）

- **multi_user**：`run-review.sh` 起 WAE dev `:4301`（**4300 被其它会话占用，未终止他人实例**）+ 隔离临时 IdP `/tmp/f036-review-idp`；`POST /api/idp/bootstrap` 建 A=system-admin（首登强制改密）；A 通过 `POST /api/idp/users` 建 B=viewer（首登强制改密）；A/B 各自独立 browser context（不共享会话）。
- **accessibility**：A 进入 `pkc-intake` 页后做静态审计（landmark/aria/heading/lang/可访问名）+ 键盘焦点与 16 步 Tab 遍历（焦点可见性、重复/陷阱判定）。
- **凭据**：A/B 初始与新口令运行时随机生成，仅存 /tmp（600）与进程 env；**不写入证据**；运行后删除临时目录。
- 复现：`bash "…/evidence/review-20261022/run-review.sh"`。

## 2. multi_user_usability（真实结果）

| 断言 | 结果 |
|---|---|
| A=system-admin 登录成功（隔离 IdP，首登改密） | ✓ |
| A 在应用壳侧栏可见 `app-nav-pkc`（PKC 知识工作台） | ✓（截图 `screens/review-01-admin-sidebar-pkc-visible.png`） |
| A 通过 `POST /api/idp/users` 建 B=viewer（服务端 200/ok） | ✓ |
| B=viewer 登录成功，`/api/idp/me` role=viewer，menus=`["overview","feedback-center","scene","pqc-sop"]` | ✓（**不含 pkc**） |
| B 进入应用壳后侧栏 `app-nav-pkc` 计数 = 0（入口不可见） | ✓（截图 `screens/review-02-viewer-sidebar-no-pkc.png`） |
| 全程 pageErrors | 0（console error 仅登录前 `/me` 401 × 2，预期） |

## 3. accessibility_status（真实结果，R-A11Y-1/2 已修复）

### 3.1 修复（task-32，2026-10-22）

| 风险 | 根因 | 修复 | 文件 |
|---|---|---|---|
| R-A11Y-1 | AppsShell 内容区是 `<section>`，全页无 `<main>` landmark | 内容区 `<section className="flex min-w-0 flex-1 flex-col">` → `<main className="flex min-w-0 flex-1 flex-col">`（保留 class；闭合标签同步）；渲染态实测 `mainCount=1`（无重复 main） | `GlobalCloud WAE/apps/wame/src/app/apps/AppsShell.tsx` |
| R-A11Y-2 | 项目标签关闭按钮（`Button size=icon`，仅 hover 显示，`X` 图标无可访问名） | 补 `aria-label={`关闭项目标签：${project.title}`}` | `GlobalCloud WAE/apps/wame/src/app/components/TopTabs.tsx` |

修复后复跑（本目录同一 spec，`run-review.sh`）：`mainLandmark=true`、`mainCount=1`、`shellUnnamedCount=0`、`shellUnnamedList=[]`、`pageUnnamed=[]`、`keyboardReachedPkc=true`、`navFocusVisible=true`、`trap=false`、`distinct=14`、`pageErrors=0`（console error 仅登录前 `/me` 401 × 2，预期）。WAE `typecheck`/`test`(1379)/`build` 复跑全 pass（`logs/wae-checks.log` 末节）。

### 3.2 复跑明细（真实结果）

静态审计（`pkc-intake` 页）：`lang=zh-CN`；`h1` = 「PKC 知识工作台（候选接入）」；`aria-label` 8 处；可见标题 4 处；**页内可交互元素 0 个（只读候选页，无需操作）⇒ 页内可访问名缺失 0**。

键盘（真实 Tab，不靠程序化 focus）：
- 从页面起点按 Tab 最多 40 次**真实键盘到达** `app-nav-pkc`（`keyboardReachedPkc=true`）；聚焦态：`outline: oklab(0.439 0 0 / 0.5) auto 1px` + `box-shadow: …0px 0px 0px 1px…` ⇒ **焦点可见**（截图 `screens/review-04-keyboard-focus-visible.png`，与 03 的哈希不同，可验证焦点态差异）。
- 16 步 Tab 遍历：`distinct=14`、`maxSame=1`、**trap=false**（无键盘陷阱）。
- 截图：`screens/review-03-pkc-page-a11y.png`（页面静态审计视图）、`screens/review-04-keyboard-focus-visible.png`（PKC 入口键盘焦点态）。

## 4. task_flow_e2e_status（复用 run3，不重跑）

依据 `evidence/e2e-20261022/README.md` §3 与 `logs/run3-raw-dev-pass/taskflow-assertions.json`：原始 dev（无垫片）10 步全过，`pageErrors=0`、`externalRequests=0`、`consoleErrors=1`（登录前 `/me` 401 预期）。本轮未重跑（lead 指示复用）。

## 5. WAE 门禁复跑（本轮真实结果）

| 命令 | 结果 |
|---|---|
| `pnpm check:apps` | exit 0 —— 应用落位校验全部合规（sidebar 4 项，第 4 项 PKC；服务控制台 7 个二级） |
| `pnpm gen:apps --check` | exit 0 —— 生成物均最新（应用 5 / 条目 21） |
| `pnpm typecheck` | exit 0 |
| `pnpm test`（根） | exit 0 —— **132 files / 1379 tests passed** |
| `pnpm build` | exit 0 —— `✓ built`（仅 chunk>500kB 警告，非阻断） |

原始记录：`logs/wae-checks.log`。注：该轮 WAE 工作区含 F-036 已落仓改动 + WAE 属主**未提交**的 `CONSOLE_COLORS` import 修复。

## 6. 风险与豁免（评审需接受/整改）

| ID | 级别 | 内容 | 处置建议 |
|---|---|---|---|
| R-A11Y-1 | ~~P2~~ **已修复** | WAE AppsShell 无 `<main>` landmark（a11y 审计 `mainLandmark=false`） | 2026-10-22 修复：AppsShell 内容区改 `<main>`；复跑 `mainLandmark=true / mainCount=1`（证据 `logs/wae-checks.log` 末节、`logs/review-assertions.json`） |
| R-A11Y-2 | ~~P3~~ **已修复** | shell 层 1 个无名称可交互按钮（精确定位：`TopTabs.tsx` 项目标签关闭按钮 `<Button size="icon"><X/></Button>`，hover 才显示） | 2026-10-22 修复：补 `aria-label=关闭项目标签：<title>`；复跑 `shellUnnamedCount=0` |
| R-DEP-1 | P2 | `task_flow` 依赖 WAE **未提交**工作区修复（`useAppContent.ts` 补 `CONSOLE_COLORS` import）；若回退，task_flow 回退 fail（run1 可复现） | WAE 属主尽快提交该修复 |
| R-PKC-1 | P2 **部分完成（最小接入）** | PKC P4/P5 已最小接入：gc 令牌快照 + theme 颜色层映射（ui_gate C6 `--gc-*` **0→117**）、7 值状态字典 + StatusBadge（C5 **未发现→存在**）；PKC `typecheck` pass、`test` **27 files/143 tests**、`build` pass。残留：非真实包消费（快照过渡）、仅 TasksPage 状态迁移、C1=5/C4=1/C10=31 既有项、真实受控嵌入未联调 | 证据 `GlobalCloud PKC/docs/evidence/pkc-p4-p5-20261022.md`；下一步=令牌包发布/并入 workspace、状态语义全页铺开、嵌入联调单独立项 |
| R-SCOPE-1 | P3 | 本评审只看 WAE 侧候选入口；PKC 业务运行态、MMC/授权、正式登记号能力未覆盖 | 正式接入评审需 PKC/WAME 属主参与 |
| 豁免 | — | `multi_user` 未做并发/多租户隔离压测（只做角色可见性）；`accessibility` 未做屏幕阅读器实测（仅 DOM/键盘审计） | 记为评审已知边界，不声称全面无障碍合规 |

## 7. 评审建议

**conditional（有条件进入正式接入评审）**：

- 已满足：六门均有真实证据（DOM/浏览器真实运行，无 mock 会话/菜单）；WAE 五项门禁全过；viewer 侧栏不可见 PKC 入口；无键盘陷阱、焦点可见；task_flow 原始 dev 通过。
- 条件（评审通过前需完成或明确接受）：
  1. WAE 属主提交 `CONSOLE_COLORS` import 修复（R-DEP-1，防 gate 回退）；
  2. ~~WAE 属主修复 `<main>` landmark 与 shell 未命名控件~~ **已完成**（R-A11Y-1/2 于 2026-10-22 修复并复跑验证）；
  3. ~~PKC 侧 P4/P5（令牌/状态语义）给出排期与验收口径~~ **已最小接入（2026-10-22，R-PKC-1 部分完成）**；正式评审需接受"快照过渡态"并给出令牌包发布/并入 workspace 计划与状态语义全页铺开计划；
  4. 真实受控嵌入（`VITE_PKC_EMBED_URL`）联调与回滚演练单独立项（R-PKC-1 残留）。
- 不满足 / 不建议：直接宣称"PKC 已接入"或升级任何 `accepted/integrated/production_ready` 状态。

## 8. 证据清单

| 证据 | 路径 |
|---|---|
| PKC P4/P5 接入证据 | `GlobalCloud PKC/docs/evidence/pkc-p4-p5-20261022.md`（盘点/范围/验证/残留） |
| 评审断言 JSON（multi_user + a11y） | `logs/review-assertions.json` |
| 运行日志（Playwright/dev/meta） | `logs/playwright-run.log`、`logs/dev-server.log`、`logs/run-meta.json` |
| WAE 门禁记录 | `logs/wae-checks.log` |
| 截图 | `screens/review-01-admin-sidebar-pkc-visible.png`、`review-02-viewer-sidebar-no-pkc.png`、`review-03-pkc-page-a11y.png`、`review-04-keyboard-focus-visible.png` |
| 复现脚本/配置/spec | `run-review.sh`、`playwright.review.config.ts`、`review.spec.ts` |
| task_flow（复用） | `../e2e-20261022/README.md`、`../e2e-20261022/logs/run3-raw-dev-pass/` |
| 落仓与功能证据 | `../summary.md` §2–§3、`../e2e-20261022/` |

## 9. 清理确认

- WAE dev `:4301` 已停止（0 listener）；`:4300` 上他人实例未动（仍 1 listener）。
- 临时 IdP `/tmp/f036-review-idp` 已删除；Playwright `node_modules` 软链已删除。
- 证据无实际口令值；无凭据泄漏。未 commit/push。

## 10. 非声明

- 不声明 PKC 已接入 / 已集成 / accepted / integrated / production_ready / 客户验收。
- 本文件为评审准备材料，不是评审结论；最终结论由评审人/老卢给出。
- 未 commit / push；未关闭 Feature；未改 PKC 仓 / WAE 业务代码。

## 2026-10-23 更新：真实嵌入（本地 dev）

- R-PKC-1 的“真实受控嵌入未联调”部分更新：
  - 本地 dev bypass 验证通过（点击前 frame=0/按钮=1；点击后 frame=1、src=PKC :5174；iframe 内 PKC Home 渲染）。
  - 证据：`evidence/embed-20261023/`（截图 + assertions + run-embed.sh）。
- 仍未验证：生产构建、CSP/X-Frame-Options、SSO/403 对齐；不改变 conditional 结论，不声明 PKC 已接入。
