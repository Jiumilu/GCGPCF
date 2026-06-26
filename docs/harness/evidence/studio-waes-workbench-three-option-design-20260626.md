---
doc_id: GPCF-EVIDENCE-STUDIO-WAES-WORKBENCH-THREE-OPTION-DESIGN-20260626
title: Studio WAES Workbench Three Option Design Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, PKC, XGD, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.md
source_path: docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Studio WAES Workbench Three Option Design Evidence

## 1. Scope

本 evidence 用于 `GPCF-UI-STUDIO-WORKBENCH-023`，目标是在不改动 Studio / WAES 业务代码的前提下，把 `WAES -> Studio` 专业工作台主线推进到可审计的三方案设计候选。

本轮不声明 Studio 页面已改造完成，不声明 WAES 母框架已成为最终标准件，不声明 `accepted`、`integrated` 或 `production_ready`。

## 2. Context Package

| 项 | 内容 |
|---|---|
| Project | GlobalCloud Studio / Hermes Web UI |
| Parent frame | GlobalCloud WAES professional workbench baseline |
| Surface | operation workbench |
| Page class | AI chat + Kanban + governance side context |
| Key components | app shell, sidebar, chat panel, kanban board, session context bar, session object panel, prompt bar |
| User goal | 个人/团队在知识系统中完成 AI 协作、任务编排、证据回指和治理约束下的工作推进 |
| Runtime boundary | Studio 和 WAES 仓均存在 dirty 状态，本轮不进入项目仓改代码或启动生产写入 |
| Non-goals | 不改默认凭据整改链路，不改 release workflow，不提交、不推送、不部署 |
| Evidence boundary | 本轮只输出 UI design evidence candidate |

## 3. Tool Route

| Tool | Result |
|---|---|
| `@product-design` | 可调用工具未在本轮暴露；按项目群强制协议产出 `get-context -> ideate -> select option` 结构，并登记为 `product_design_tool_not_exposed` |
| `WAES` baseline | 读取 `PM_WORKBENCH.md` 和 `GLOBALCLOUD_CONTROL_TOWER.md`，采用 shell first、page skeleton second、core high-risk components third |
| `ui-ux-pro-max` | 已运行设计系统搜索；输出偏品牌/强动效，本轮按产品界面规则降噪，不采用其黑底强动效为默认 |
| `impeccable` | 已运行 context 探测；返回 `NO_PRODUCT_MD`，本轮不初始化 Studio `PRODUCT.md`，避免越界 |
| Figma | 未提供 Figma URL，标记 `figma_not_verified` |
| Playwright/browser | 本轮未启动 runtime，标记 `runtime_not_verified`、`mobile_not_verified` |

## 4. Prompt Profile

```text
functional-accuracy:
  Studio 工作台必须让 chat、kanban、session context、evidence/pending 对象边界清楚，不能只做装饰性 UI。
visual-quality:
  采用项目群产品界面寄存器，克制、稳定、高密度但可读；不采用品牌页强动效和纯黑沉浸叙事。
usability-experience:
  用户应能从当前对话进入任务编排、证据查看和下一步动作，且移动端有降级路径。
governance-evidence:
  AI 建议、业务事实、治理阻断、证据回指和 pending action 必须分区展示。
scope-control:
  本轮只形成设计候选和 UI gate evidence，不修改 Studio / WAES 仓，不升级项目状态。
```

## 5. Product Design Protocol

### 5.1 get-context

已确认的真实代码与文档上下文：

1. Studio `App.vue` 使用 app shell、全局 sidebar、page-sidebar 分流和 mobile menu。
2. Studio `AppSidebar.vue` 已含 `hermes.kanban`、jobs、skills、plugins、mcp、memory、models 等工作台入口。
3. Studio `ChatView.vue` 已含 `StudioDrawer`、`PromptBar`、`SessionContextBar`、`SessionObjectPanel`，具备知识/证据绑定基础。
4. Studio `KanbanView.vue` 已含 board selector、状态列、任务抽屉、dispatch 和归档动作。
5. WAES `PM_WORKBENCH.md` 提供控制塔、验收闸口、任务状态、风险、成本、验证基线和下一步动作口径。

### 5.2 ideate

Option 1 = WAES Shell-first Workbench
Option 2 = Studio Knowledge Cockpit
Option 3 = Chat-Kanban Split Focus

| Option | Name | Structure | Strength | Risk |
|---|---|---|---|---|
| 1 | WAES Shell-first Workbench | 保留 Studio app shell；左侧按 WAES 工作台分组；主区 chat；右侧固定 context/evidence/pending；Kanban 作为任务 lane 可见入口 | WAES baseline reuse 最强，最小改动，适合专业工作台扩散 | 视觉新意较低，需要后续补强 page skeleton |
| 2 | Studio Knowledge Cockpit | 顶部项目/知识对象上下文，中心为知识任务 cockpit，chat 与 kanban 作为并列面板 | 知识系统表达更强，适合个人/团队知识工作台 | 与 WAES shell 差异较大，可能需要例外审批 |
| 3 | Chat-Kanban Split Focus | Chat 与 Kanban 双主区，右侧 evidence drawer，面向执行流 | 任务推进清晰，适合短周期执行 | 高信息密度，移动端和键盘路径风险更高 |

### 5.3 select option

`Selected option = 1`

选择理由：

1. 与 `WAES` 母框架复用边界一致：shell first、page skeleton second、core high-risk components third。
2. 对 Studio 现有代码侵入最小，能复用 `App.vue`、`AppSidebar.vue`、`ChatView.vue`、`KanbanView.vue`。
3. 能把 chat、kanban、session context、evidence/pending 从“功能存在”推进到“工作台结构可治理”。
4. 更适合作为项目群专业工作台类首个可扩散样板，再向 PKC、XGD、GPC、GFIS 扩散。

## 6. WAES Baseline Reuse

| Layer | Reuse decision | Evidence |
|---|---|---|
| Shell | reuse | Studio app shell 和 sidebar 可承接 WAES 工作台分组；不需要整套重写 |
| Page skeleton | partial | Chat 主区、context bar、object panel、kanban board 已有基础，但缺统一“任务/风险/证据/AI 建议”可见层级 |
| Core components | partial | 状态列、任务卡、提示条、侧栏、抽屉可复用；证据状态、治理阻断和 AI 建议标签仍需统一语义 |
| Exception | not_required | 当前不需要申请整套例外 |

## 7. UI Gate Report

UI gate status: ui_partial
Surface: operation workbench
Repository/path: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/ChatView.vue`
Scope: `WAES -> Studio` 专业工作台三方案设计候选，不改代码
Tools used: `ui-ux-pro-max` / local code inspection / WAES baseline docs / GlobalCloud UI Quality Gate
Tools unavailable: `product_design_tool_not_exposed` / `impeccable_blocked_by_NO_PRODUCT_MD` / `figma_not_verified`
Verification: design_evidence_only; runtime_not_verified; mobile_not_verified; a11y_manual_only
Status ceiling: ui_evidence_candidate

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | Surface 已定为 operation workbench，三方案均覆盖 chat、kanban、context/evidence/pending | 后续实现时补页面区块截图 |
| G2 Design Tokens | partial | 已引用项目群令牌规则和 Studio 现有 Naive UI/theme 结构 | 未做代码级 token diff |
| G3 Component Consistency | partial | 已识别 app shell、sidebar、chat panel、kanban、drawer、prompt bar | 未验证组件交互一致性 |
| G4 Evidence And Governance | pass | 方案强制 evidence/pending/context 分区，状态上限写明 | 后续需运行态截图证明 |
| G5 AI Fact Separation | pass | prompt profile 明确 AI 建议不得等同业务事实 | 后续需在 UI 文案与标签中实现 |
| G6 Accessibility | partial | 已列为 prompt profile 和 gate 要求 | 未跑键盘路径和 contrast |
| G7 Responsive And Text Robustness | partial | 已保留移动降级要求 | mobile_not_verified |
| G8 Runtime Verification | partial | 本轮只做文档候选，未启动 runtime | runtime_not_verified |
| G9 Scope Control | pass | 未改 Studio / WAES 业务代码；仅产 GPCF evidence candidate | 无 |

## 8. Decision

本轮设计候选可以作为下一轮 Studio 工作台实际改造或运行态验证输入。下一轮若继续推进，应优先在 Studio dirty 边界被确认后，选择 `Selected option = 1` 做最小 UI patch 或只读 browser screenshot 验证。
