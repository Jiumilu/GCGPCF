---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-023
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-023
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-023.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-023.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-023

## 输入

- `GlobalCloud 项目群实施方案.md`
- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-022.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/App.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/AppSidebar.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/ChatView.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES/docs/current/PM_WORKBENCH.md`

## run

1. 复核上一轮 `GPCF-UI-STUDIO-WORKBENCH-022`，确认默认凭据整改链路已经收口，不再继续围绕该链路扩散。
2. 切回 `WAES -> Studio` 专业工作台主线，读取 Studio app shell、sidebar、chat、kanban 和 WAES PM 工作台文档。
3. 真实运行 `ui-ux-pro-max` 设计系统搜索，记录其输出偏品牌/强动效，不直接采用为控制塔/工作台默认视觉。
4. 运行 Impeccable context 探测，记录 `NO_PRODUCT_MD`，不越权初始化 Studio `PRODUCT.md`。
5. 查找 `@product-design` 可调用接口，未发现可用工具；按项目群强制协议形成 `get-context -> ideate -> select option` 三方案设计 evidence。
6. 选择 `Option 1: WAES Shell-first Workbench` 作为下一轮候选方向。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | Studio 操作工作台已形成 WAES 母框架三方案设计候选和 UI gate evidence，未触碰 Studio / WAES dirty 工作区 |

## verify

本轮执行并通过或取得结果：

```bash
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "GlobalCloud Studio WAES professional workbench governance evidence AI chat kanban" --design-system -p "GlobalCloud Studio WAES Workbench" -f markdown
node .agents/skills/impeccable/scripts/context.mjs
rg / sed 读取 Studio app shell、sidebar、chat、kanban 与 WAES PM_WORKBENCH
```

验证结论：

1. `ui-ux-pro-max` 已真实运行，但输出更接近品牌/沉浸式设计，已按 GlobalCloud 产品界面寄存器降噪处理。
2. Impeccable 已真实探测，结果为 `NO_PRODUCT_MD`；本轮不初始化 Studio 产品上下文，避免越过当前最小目标。
3. `@product-design` 未暴露可调用工具接口；本轮只记录强制三方案协议产物，不伪装成插件已执行。
4. Studio / WAES 仓均存在 dirty 状态；本轮不改项目仓代码。

## recover

1. 后续若 Studio dirty 边界被确认，可从 `Selected option = 1` 进入最小 UI patch。
2. 若需要更强设计产出，应先补 Studio `PRODUCT.md` 或取得 `@product-design` 可调用入口，再重新执行设计前置层。
3. 若只需验证现状，可用浏览器/Playwright 对 `#/hermes/chat` 与 `#/hermes/kanban` 做只读截图和键盘路径检查。

## debug

当前未关闭的边界：

1. `product_design_tool_not_exposed`：本轮没有真实调用 `@product-design` 插件。
2. `runtime_not_verified`：本轮没有启动 Studio runtime。
3. `mobile_not_verified`：本轮没有移动端截图。
4. `figma_not_verified`：本轮没有 Figma URL。
5. `impeccable_blocked_by_NO_PRODUCT_MD`：本轮未初始化 PRODUCT.md。

## 输出

- `docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.md`
- `docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.json`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-023.md`
- `tools/kds-sync/validate_studio_waes_workbench_three_option_design_20260626.py`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 4 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 7.1 UI 质量门禁（涉及 UI 时必填）

| 字段 | 值 |
|---|---|
| UI scope | true |
| Tool route | `@product-design -> WAES -> ui-ux-pro-max -> Figma -> Storybook -> impeccable -> Playwright/browser -> axe-core/Lighthouse -> GPCF UI Gate` |
| Context package | completed |
| Prompt profile | functional-accuracy / visual-quality / usability-experience / governance-evidence / scope-control |
| Design options | 3 |
| Selected option | 1 |
| WAES baseline reuse | shell / page-skeleton / core-components |
| Surface | operation workbench |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/ChatView.vue` |
| Scope | `WAES -> Studio` 专业工作台三方案设计候选，不改代码 |
| Tools used | `ui-ux-pro-max` / local code inspection / WAES baseline docs / GPCF UI Quality Gate |
| Tools unavailable | `product_design_tool_not_exposed` / `impeccable_blocked_by_NO_PRODUCT_MD` / `figma_not_verified` / `runtime_not_verified` |
| Verification | design_evidence_only; validator pending |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_partial
Surface: operation workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/ChatView.vue
Scope: WAES -> Studio 专业工作台三方案设计候选，不改代码
Tools used: ui-ux-pro-max, local code inspection, WAES baseline docs, GPCF UI Quality Gate
Tools unavailable: product_design_tool_not_exposed, impeccable_blocked_by_NO_PRODUCT_MD, figma_not_verified, runtime_not_verified
Verification: design_evidence_only; runtime_not_verified; mobile_not_verified; a11y_manual_only
Status ceiling: ui_evidence_candidate
```

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

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | ui_partial |
| 门禁结果 | evidence_candidate_ready |
| 是否需要人工确认 | yes, before implementation |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 若用户授权进入 Studio 项目仓，按 `Selected option = 1` 做最小 UI patch 或只读运行态截图验证。
- 若继续强化工具链，先补 Studio `PRODUCT.md` 或接入真实 `@product-design` 可调用工具。
