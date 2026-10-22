---
doc_id: GPCF-DOC-F034-EVIDENCE-20261022
title: F-034 WAE AppsShell 角色收敛证据摘要
project: GPCF
related_projects: [WAE, GPCF]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-034-wae-p0-shell-and-role-convergence/evidence/summary.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/summary.md
sync_direction: local_only
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-034 WAE AppsShell 角色收敛 —— 证据摘要（2026-10-22）

本文件记录本地可回放证据，仅用于关闭候选判断，不代表提交、推送、部署或项目状态提升。

## 1. 结论

- AppsShell 角色收敛缺陷已修复：服务控制台 7 个 entries 在 `placement.city.yaml` 声明 `requires`，`generated.ts` 已重新生成并带上 `requires`。
- viewer / 未认证场景下 7 个受限入口全部不可见；system-admin 全部可见；部分授权按菜单 id 精确收敛（DOM 测试 + 机器可读角色矩阵双重证据）。
- `check:apps`、`gen:apps --check`、`typecheck`、`test`（根仓 + apps/wame）、`build`、`check:modules` 全部真实复跑通过。
- 本轮（2026-10-22 收尾轮）已补齐 `scope.in` 的 **O1–O4 可回放证据**（`evidence/o1-*.md` ~ `o4-*.md`）与 **PKC 首批接入纸面演练**（`evidence/pkc-intake-protocol-20261022.md`）：O1 pass / O2 pass（附清单口径限制）/ O3 partial（现状可核、归并未完成）/ O4 pass；PKC 当前**未在 WAE 注册**，本轮为 dry-run，不声明已接入。未 close Feature，未声明状态提升。

## 2. 改动文件（WAE 仓，均在授权写范围内）

| 文件 | 改动 |
|---|---|
| `docs/assembly-spec/placement.city.yaml` | 服务控制台 7 个 entries 增加 `requires: <menu-id>`（gcas/mmc/gpcf/icp/aaas/feedback/idp-console，逐个取自 host-kit `MENU_CATALOG`，未猜测） |
| `apps/wame/src/app/apps/generated.ts` | `pnpm gen:apps` 重新生成，entries 带 `requires`（`generated.loaders.ts` 无变化） |
| `apps/wame/src/app/apps/AppsShell.dom.test.tsx` | 新增 4 例角色收敛 DOM 测试（viewer / system-admin / 部分授权 / 未认证），并对既有用例注入确定性菜单（默认全量菜单，不改生产代码分支） |

未改 `packages/app-registry/`（`requires?: string` 类型与生成器已支持，无需改类型/测试）；未改 `GlobalCloud WAE` 之外的其它项目仓。

## 3. 验收命令与真实结果（WAE 仓根）

| 命令 | 结果 | 摘要 |
|---|---|---|
| `pnpm gen:apps` | pass | 1 写入 / 1 无变化 |
| `pnpm gen:apps --check` | pass | 2 个生成物均最新 |
| `pnpm check:apps` | pass | P001–P010 全部通过；服务应用 7 个二级 |
| `pnpm typecheck` | pass | 无输出 |
| `pnpm --filter @globalcloud/wame typecheck` | pass | 无输出 |
| `pnpm test` | pass | 131 files / 1373 tests |
| `pnpm --filter @globalcloud/wame test` | pass | 13 files / 89 tests（AppsShell 15 例，含新增 4 例） |
| `pnpm build` | pass | 构建成功；仅 >500 kB chunk 体积警告（非阻断） |
| `pnpm check:modules` | pass | 19 个模块包合规/不适用 19，不合规 0 |
| `python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAE" --fail-on error` | pass（exit 0） | error 0 / warn 4 / info 1；4 条 warn 均为开工前既有（根 .md 上限、Manifest 六段、根目录布局、散落文件），非本轮引入 |

原始输出见 `evidence/role-convergence.txt`。

## 4. 角色收敛验证

菜单目录来源：`packages/host-kit/src/host/menus.ts`（`/me.menus` 的 id 来源）。七个 menu id 均真实存在：

```text
catalog_menu_ids = overview,gcas,mmc,gpcf,icp,aaas,feedback-center,feedback,scene,pqc,pqc-calc,pqc-orders,pqc-sop,idp-console,alarm-action,message-dispatch
```

| 主体 | 可见服务控制台 menu id | 结论 |
|---|---|---|
| viewer | 无（viewer_menus = overview/feedback-center/scene/pqc-sop） | 7 个受限入口全部不可见 |
| 未认证 | 无（与 viewer 同：仅公开项） | 不放开受限项 |
| system-admin | 全部 7 个（gcas/mmc/gpcf/icp/aaas/feedback/idp-console） | 全部可见 |
| 部分授权（仅 gcas/mmc） | 仅 gcas、mmc | 其余 5 项不可见 |

DOM 组件测试（jsdom）补充界面侧断言：viewer 时「服务控制台」一级项整体不渲染（服务应用 0 个可见二级 ⇒ 被收敛），深链 `/global-cloud-workbench/service/icp-console` 回落到公开应用；system-admin 时 7 个控制台二级按钮全部渲染。

> 口径：`requires` 只作用于 **L1 呈现层**（`packages/app-registry/src/placement.ts` 明确「不做授权判定」）；授权事实仍由服务端决定（R-20），本证据不声明授权绕过或权限提升。

## 5. gates

| gate | 取值 | 理由 |
|---|---|---|
| `functional_completeness` | pass | 角色收敛功能已实现并经 DOM 测试 + 机器矩阵验证；O1–O4 已补可回放证据（O1 pass / O2 pass / O3 partial / O4 pass，见第 9 节）；命令全绿 |
| `quality_baseline` | pass | check:apps / gen:apps --check / typecheck / test / build / check:modules / ui_gate / gc_standard 真实通过 |
| `multi_user_usability` | waived（保持） | 本轮为壳层收敛，未做多用户任务实测；不声明可用性通过 |
| `task_flow_e2e_status` | pending（保持） | 未跑浏览器端到端任务流；DOM 测试不等于 E2E，不加假证据 |
| `accessibility_status` | waived（保持） | 本轮未做无障碍实测；不声明无障碍通过 |
| `evidence_overexposure_gate` | pending（保持） | 未做人类入口证据展示审查；保持 pending |

`status_ceiling` 保持 `partial`。

## 6. 未覆盖范围（本轮不做 / 非声明）

- O1–O4 已有可回放证据（第 9 节），但 **O3 的归并动作未执行**（WAME 三套侧栏仍独立，跨仓改动属 WAME 属主）；O2 的 PKC/Brain 令牌偏离只登记未改写。
- 首批接入为**纸面演练（dry-run）**：PKC 未注册、未改 PKC/WAE 仓；UI gate 六件套中的 `multi_user_usability` / `task_flow_e2e_status` / `accessibility_status` / `evidence_overexposure_gate` 仍无运行时证据（gates 保持 waived/pending）。
- 未做真实身份服务/浏览器 E2E；角色收敛以本地 DOM 测试与菜单目录矩阵验证，不代表线上 403 链路已验证。
- 本证据**不构成 F-034 整体关闭依据**（O3 归并、PKC 真实接入、四项 UI gate 尚未闭环）。
- 未 commit / push / deploy；未声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；未 close Feature。

## 7. 基线 / 脏树说明（WAE 仓）

- 分支 `refactor/ui-spec-wae`。开工时 HEAD 为 `dab8667 ci: add project-group standards workflow`，工作区含其它会话的已暂存改动；工作期间该会话提交了 `18111a3 chore(wae): 补齐治理四件套（AGENTS.md + .gitignore 覆盖）` 与 `c8113ed fix(wae): P6a 焦点可见性（outline:none 2→0）`（**均非本任务提交**），本任务未 commit/push。
- 本任务收尾时工作区未提交项：本任务的 3 个文件（第 2 节）+ `docs/.DS_Store` 与 2 个未跟踪 docs 方案文件（开工前既有，本任务未触碰、未清理、未 stash）。
- 本任务在 WAE 仓的实际改动仅第 2 节列出的 3 个文件。

## 8. 回滚

```bash
# WAE 仓：恢复三处产品/测试文件，再按配置重新生成（生成物应与恢复后的 yaml 一致）
git -C "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAE" restore -- \
  docs/assembly-spec/placement.city.yaml \
  apps/wame/src/app/apps/generated.ts \
  apps/wame/src/app/apps/AppsShell.dom.test.tsx
```

- `placement.city.yaml` 回滚后若需同步生成物：`pnpm -C "GlobalCloud WAE" gen:apps`（或直接 restore 两文件）。
- `F-034` feature.yaml 为未跟踪新文件（创建于 2026-10-22 18:02），本轮（含收尾轮）改动点：`evidence` 5 个值、`verification.tests` 追加命令（角色收敛轮 3 条 + 收尾轮 3 条：O1–O4 聚焦测试 / token 源校验 / 令牌同步检查）、`verification.waivers.screenshots`、`gates.functional_completeness/quality_baseline`、`updated_at`；按上述字段恢复原值即回滚。
- 本目录新增 evidence 文件（`summary.md`、`role-convergence.txt`、`o1-shell-decoupling.md`、`o2-token-consolidation.md`、`o3-sidebar-unification.md`、`o4-status-semantics.md`、`pkc-intake-protocol-20261022.md`）删除即回滚，不影响任何产品代码。
- 收尾轮为只读：WAE 仓无新增改动（仅复用前一轮的 3 个未提交文件）。
- 无数据迁移、无外部写入、无部署、无权限变更，回滚无数据风险。

## 9. O1–O4 证据与 PKC 接入演练（2026-10-22 收尾轮，WAE 只读）

本轮对 WAE 仓只做只读检查（未改 WAE 代码）；证据文件与结论：

| 编号 | 证据文件 | 结论 |
|---|---|---|
| O1 外壳解耦 | `evidence/o1-shell-decoupling.md` | **pass**：能力默认全关（唯一例外 `errorBoundary` 安全网）+ slots 显式注入；`shellCapabilities.test.ts` 9 tests、`shell.dom.test.tsx` 8 tests 通过 |
| O2 令牌收口 | `evidence/o2-token-consolidation.md` | **pass（附清单口径限制）**：单源 `tokens.css` 76 令牌（sha `54729cdf…`）；`sync_tokens.py --check` 通过；`verify-token-sources.py` 清单 3/4 路径因项目改名失效，静态 sha256 补核得**可解析复制件 3 份逐字节一致**；PKC 4 处 / Brain 30+5 偏离只登记；PVA 新发现 1 处偏离 |
| O3 侧栏统一 | `evidence/o3-sidebar-unification.md` | **partial**：框架侧唯一侧栏成立（85 行，items/subject 注入）；WAME 三套（layout/GlobalCloudSidebar 49、components/Sidebar 114、FunctionPanel 1557）未归并，WAME 对 `@globalcloud/app-shell` 0 引用；跨仓不改 |
| O4 状态语义层 | `evidence/o4-status-semantics.md` | **pass**：7 值字典 + S1/S2 代码级判定 + StatusBadge + 14 个 `--status-*` 语义令牌；`statusDictionary.test.ts` 12 tests、`templateRegions.test.ts` 5 tests 通过；WAE `ui_gate C5=存在`，WAME/PKC `C5=未发现`（登记待接入） |
| PKC 首批接入 | `evidence/pkc-intake-protocol-20261022.md` | **dry-run**：PKC **当前未在 WAE 注册**（placement/manifests/menus 均无 pkc；`appSwitcher.test` 的 `pkcs` 仅泛化示例）；协议 + 检查表 + 纸面演练 + 回滚清单已产出；不改 PKC/WAE 仓、不声明已接入 |

聚焦验证命令（真实执行，exit 0）：

```bash
cd "GlobalCloud WAE"
pnpm exec vitest run \
  packages/app-shell/src/shellCapabilities.test.ts \
  packages/app-shell/src/shell.dom.test.tsx \
  packages/ui-kit/src/statusDictionary.test.ts \
  packages/ui-templates/src/templateRegions.test.ts
# Test Files  4 passed (4) / Tests  34 passed (34)
```

Evidence Gate 复核（`--check-only`，非 full run：不写 evidence、不 close、不改队列）：

```text
$ python3 scripts/gpcf_check_evidence.py --check-only F-034
gpcf_feature_evidence_check feature=F-034 close_candidate=true reasons=none
exit=0
```

> 口径：`close_candidate=true` 仅表示**证据门结构项无缺口**，**不**表示 F-034 可关闭 —— O3 归并、PKC 真实接入、四项 UI gate（多用户/任务流/无障碍/证据展示）仍未闭环（见第 6 节），故按要求**未 close**。
