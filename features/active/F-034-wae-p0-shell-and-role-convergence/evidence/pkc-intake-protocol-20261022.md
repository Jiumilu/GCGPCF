---
doc_id: GPCF-DOC-CD9F4B31B1
title: PKC 首批接入协议 + 检查表 + 演练记录（WAE AppsShell，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/pkc-intake-protocol-20261022.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/pkc-intake-protocol-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# PKC 首批接入协议 + 检查表 + 演练记录（WAE AppsShell，2026-10-22）

> **性质：纸面演练 / dry-run。** 本轮**不修改 PKC 仓、不修改 WAE 仓**，不产生任何注册代码；不声明 PKC「已接入 / 已集成 / 生产就绪 / 已验收」。
>
> 依据：`GlobalCloud WAE/docs/assembly-spec/装配模板与评审检查单_v0.1.md`（模板 A/B/C、检查单 D）、`docs/assembly-spec/framework-readiness.md`（R1–R10）、F-034 的 `ui_product_first_control` gates 与 `tools/ui_gate.py`（C1–C9）。

## 0. 一句话结论

**PKC 当前未在 WAE 注册**（`placement.city.yaml` 无 pkc app/entry，`docs/assembly-spec/manifests/` 无 pkc manifest；`appSwitcher.test.ts` 中的 `pkcs` 仅是"新应用泛化"示例，不构成注册）。本轮给出可执行的接入协议、检查表与纸面演练步骤；**按协议接入后 PKC 才具备 WAE 侧入口**。

## 1. WAE 侧 PKC 注册现状（只读核对）

| 核对项 | 命令/路径 | 结果 |
|---|---|---|
| 落位 apps | `docs/assembly-spec/placement.city.yaml` 的 `apps[]` | `feedback` / `spaceai` / `pqc` / `service` —— **无 pkc** |
| 落位 entries | 同上 `entries[]` | 20 条，**无 pkc 条目** |
| 模块清单 | `docs/assembly-spec/manifests/` | 16 个 manifest（aaas/ai-assistant/gbrain/gpcf/icp/identity/message/mmc/observability/pqc×4/spaceai×3），**无 pkc** |
| 平台注册类型 | `packages/app-registry/src/platform.ts` | `PlatformId` 为**开放类型**（已泛化）：新项目以任意 id 接入**不改公共契约** |
| 泛化示例 | `packages/app-shell/src/appSwitcher.test.ts` | `id: 'pkcs'`、`name: 'PKC 包装知识中心'` 仅作"新应用不改契约即可纳入"的测试样例，**不是注册** |
| 鉴权/菜单 | `packages/host-kit/src/host/menus.ts` | 目录中**无 pkc 菜单项**（需接入时新增 `pkc` menu id 并给 `requires`） |

> `host-kit` 中出现的 "PKCE" 是 OAuth 授权码流程术语（`pkceChallenge`），与 PKC 项目无关，不作为注册证据。

## 2. PKC 侧现状（只读，未改）

| 项 | 观测值 | 说明 |
|---|---|---|
| 技术栈 | React `18.3.1` / ReactDOM `18.3.1` / Vite `6.3.5` | 与 WAE 母本同代，适配成本低 |
| 可用脚本 | `build` / `dev` / `test` / `typecheck` / `lint`(=tsc) / `smoke:routes` / `smoke:runtime` / `verify:pkc` | 具备接入前自检与回滚验证入口 |
| 令牌消费 | `ui_gate.py GlobalCloud PKC`：`--gc-*` **0 次** / 任意 CSS 变量 67 次 | **未消费** WAE 单一来源令牌；存在副本偏离（已知 4 处值偏离，见 F-034 O2 证据） |
| 状态语义 | 同上：C5「统一状态字典：**未发现**」 | 未采用 7 值字典 / StatusBadge |
| UI 门禁基线 | 同上：C1 裸色值 5 处（`src/app/components/ui/chart.tsx`）、C2 0、C3 0、C4 1 处（`src/app/components/theme-provider.tsx`）、C9 0 | C4 属主题唯一入口白名单候选，需接入评审确认 |

## 3. 接入协议（WAE AppsShell，步骤化）

> 原则：**登记侧驱动、工程零改造优先**（framework-readiness R1/R2）；**先统一语义、后统一装饰**；**页面可见性（L1）与服务端授权分离**。

| 步 | 动作 | 落点（示例，接入时才改） | 完成判据 |
|---|---|---|---|
| P0 | 立项与清单：确认项目在注册表 28 项目内、产出 PKC manifest（模板 A） | `GlobalCloud WAE/docs/assembly-spec/manifests/pkc.yaml`（待建） | manifest 四字段（id/name/entry.route/data_contract）齐备 |
| P1 | 平台注册：`PlatformModule` 条目（开放 `PlatformId`，不改契约） | `packages/app-registry/src/platform.ts` 消费侧 registry（按 R1 清单驱动） | 组件无需硬编码 PKC 映射即可渲染 |
| P2 | 落位：`placement.city.yaml` 增加 `pkc` app + `pkc-*` entries；**服务控制台类**必须收进 `service` hub，不自占一级 | `docs/assembly-spec/placement.city.yaml` | `pnpm gen:apps && pnpm check:apps` 通过（P001–P010） |
| P3 | 角色收敛：给每个受限 entry 标 `requires: <menu-id>`；`menus.ts` 新增 `pkc` 目录项与其 `requires` | `placement.city.yaml` + `packages/host-kit/src/host/menus.ts` | viewer 不可见、system-admin 可见（同 F-034 角色收敛判据） |
| P4 | 令牌消费：PKC 只做**薄壳消费** `@globalcloud/ui-tokens`（不得再复制实体）；既有 4 处值偏离按 R4「记录而非抹平」裁定 | `GlobalCloud PKC/src/styles/theme.css`（属主执行） | `sync_tokens.py --check` 通过；`ui_gate C6` 出现 `--gc-*` 消费 |
| P5 | 状态语义：状态区改用 `statusDictionary` / `StatusBadge`；未映射词走 S1 显式标注，门禁词走 S2 | `GlobalCloud PKC` 页面状态区 | `ui_gate C5` = 存在；无「accepted 折算为 complete」 |
| P6 | 身份/权限：接入 host SSO（`/me` → role/actions/menus）；前端只用 `filterMenu`/`canDo` 做呈现层收敛，授权判据留在服务端 | `packages/host-kit/src/host/sso.ts` / `menus.ts` | 页面与接口一致：受限页 403 不被 UI 掩盖 |
| P7 | 验证与回滚：执行第 4 节检查表 + PKC 自带 `test/typecheck/build/verify:pkc` | 两仓均只读执行 | 检查表全绿方可申请「已接入」评审（本轮不做） |

## 4. 检查表（接入评审用，UI gate 六件套 + 四项横切）

### A. UI gate 六件套（F-034 `ui_product_first_control.gates`）

| # | 检查项 | 方法 | 期望 | dry-run 当前观测（PKC） |
|---|---|---|---|---|
| A1 | `functional_completeness` | PKC 核心任务可完成 + WAE 入口可进入 | pass | 未接入（无 WAE 入口）→ **未评** |
| A2 | `quality_baseline` | `ui_gate.py` C1–C4/C9 无未豁免有效违规 | pass | C1 有效 5（1 文件）、C4 1 处、C2/C3/C9 为 0 → **需先处理或白名单登记** |
| A3 | `multi_user_usability` | 首次/低频、高频、治理审计三类用户任务实测 | pass 或 waived（附理由） | 无实测证据 → **pending** |
| A4 | `task_flow_e2e_status` | 端到端任务流（含错误恢复）浏览器 E2E | pass | 无 E2E 证据 → **pending** |
| A5 | `accessibility_status` | 键盘/焦点/读屏等无障碍实测 | pass 或 waived（附理由） | 无实测证据 → **pending** |
| A6 | `evidence_overexposure_gate` | 人类入口不暴露机器字段/evidence 结构 | pass | 无界面审查证据 → **pending** |

### B. 四项横切检查

| # | 检查项 | 方法/命令 | 期望 | dry-run 当前观测 |
|---|---|---|---|---|
| B1 | 令牌单一来源 | `python3 tools/verify-token-sources.py` + `sync_tokens.py --check` | 复制件逐字节一致；PKC 4 处偏离登记 | PKC `theme.css` 4 处值偏离（既有，属主裁定） |
| B2 | 状态语义 | `ui_gate.py ... PKC` 的 C5 | C5 = 存在 | **未发现** → 需接入 P5 |
| B3 | 角色收敛（L1） | `placement` 的 `requires` + `menus.ts` 目录 + `AppsShell.dom.test.tsx` 同款断言 | viewer 不可见受限项；system-admin 可见 | PKC 无菜单项、未接入 → **未评** |
| B4 | 回滚 | 见 §6 回滚清单，逐条可执行 | 无数据迁移/无外部写入 | 协议已给出；**纸面核对通过** |

### C. 装配评审检查单 D（既有，摘录必过项）

- [ ] 术语层级：应用模块＝Route 级 / 平台＝PlatformModule 对位确认
- [ ] `entry.route` 三字段（`path`/`module_id`/`component_key`）逐一核对
- [ ] status 双义区分（治理态 ≠ 展示态）；治理态不得冒充展示态
- [ ] `data_contract`（引用键/世界层/geo）与 WAS/XWAIL 衔接确认
- [ ] 装饰字段归工程注册表，manifest 不承载

## 5. 纸面演练记录（dry-run，2026-10-22）

演练目标：验证"若今天接入 PKC，需要动哪些文件、会卡在哪些检查"，**不实际改任何仓**。

| 步 | 演练内容 | 结论 |
|---|---|---|
| D1 | 读 PKC 技术栈/脚本/UI 基线 | React 18.3.1 + Vite 6.3.5 与 WAE 同代；脚本齐备（test/typecheck/build/verify:pkc） |
| D2 | 查 WAE 是否已有 PKC 注册 | **未注册**（placement 无 pkc、manifests 无 pkc、menus 无 pkc） |
| D3 | 模拟 manifest + PlatformModule + placement 条目 | 可复用开放 `PlatformId`，**无需改公共契约**；需新增 1 app + N entries（N = PKC 一级页面数） |
| D4 | 模拟角色收敛 | 每个受限 entry 需 1 个 menu id（`menus.ts` 新增 `pkc` 与其子项），并标 `requires` |
| D5 | 模拟令牌/状态接入 | PKC 需改薄壳消费 + 状态区接入字典；**PKC 4 处令牌偏离需属主先裁定** |
| D6 | 回滚演练 | 删除 placement/manifest/registry 新增项 + 恢复 PKC 样式即回滚；无数据迁移 |

**dry-run 结论**：接入路径清晰、无契约阻塞；**真实阻塞点**是 PKC 侧令牌偏离裁定与状态字典接入（属主执行），以及 UI gate 六件套中的多用户/任务流/无障碍/证据展示四项尚无证据（保持 pending）。

## 6. 回滚清单（接入实施时执行，本轮不执行）

1. `placement.city.yaml` 删除 pkc app/entries（或 `git restore` 该文件）→ `pnpm gen:apps`。
2. 删除 `docs/assembly-spec/manifests/pkc.yaml`。
3. `menus.ts` 删除 `pkc` 目录项。
4. registry 删除 PKC `PlatformModule` 条目。
5. PKC 仓恢复样式/状态改动（属主执行，按 PKC 自身回滚路径）。
6. 复跑：`pnpm gen:apps --check`、`pnpm check:apps`、`pnpm test`、`pnpm typecheck`、`pnpm build`。

## 7. 非声明

- 本轮为**纸面演练（dry-run）**：未注册 PKC、未修改 PKC/WAE 任何仓、未运行跨仓联调。
- 不声明 PKC「已接入 / 已集成 / accepted / integrated / production_ready / customer_accepted」。
- 检查表中 A3–A6 保持 `pending`（无运行时证据），不得因本协议存在而视为通过。
- 未 commit/push。
