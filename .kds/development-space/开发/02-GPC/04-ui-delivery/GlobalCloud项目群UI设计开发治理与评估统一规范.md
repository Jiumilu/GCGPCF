---
doc_id: GPCF-DOC-7C1E59A4D2
title: GlobalCloud项目群UI设计开发治理与评估统一规范
project: GPC
related_projects: [GPC, WAES, KDS, GPCF, Studio]
domain: ui-delivery
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md
source_path: 04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud项目群UI设计开发治理与评估统一规范

日期：2026-06-22  
状态：项目群 UI 统一主规范 v1

## 1. 目标与边界

本规范解决两件事：

1. 让 UI 质量在 Loop 中被实际执行、记录、校验，而不是只停留在技能定义。
2. 把项目群 UI 的设计、开发、治理、评估收口为一套统一主规范，避免各项目各做各的。

本规范不替代业务事实、Harness 验收、WAES 裁决或项目级交付状态。UI 证据最高只到 `ui_evidence_candidate`。

## 2. 单一主线

项目群 UI 工作统一遵守以下主线：

1. 先判定界面类型，再设计结构。
2. 先对齐体验骨架，再决定视觉细节。
3. 先复用统一令牌和组件，再写页面实现。
4. 先区分业务事实、治理状态、AI 建议，再决定展示方式。
5. 先做真实运行验证，再写完成结论。

## 3. 与现有规范的关系

本规范是总纲；以下文档继续作为分项权威：

1. `04-ui-delivery/GlobalCloud绿色供应链体系统一体验骨架规范.md`
2. `04-ui-delivery/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md`
3. `04-ui-delivery/GlobalCloud绿色供应链体系对话模式与操作模式规范.md`
4. `04-ui-delivery/GlobalCloud绿色供应链体系界面分阶段治理规则.md`
5. `04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md`

若分项文档与本规范冲突，以本规范的项目群治理边界为准，再回写分项文档。

## 4. 设计基线

### 4.1 默认使用产品界面寄存器

项目群 UI 默认为产品/运营寄存器，不是品牌海报寄存器：

1. 颜色克制，状态区分清楚。
2. 信息密度高但可读。
3. 页面结构稳定，可预测。
4. 关键状态、阻断和来源必须可见；详细治理证据必须可追溯，但不得默认主导产品界面。
5. 动效只服务于状态反馈、切换或定位，不做装饰性炫技。

只有品牌页、宣传页、展示页、演示页才允许切换到更高实验性的视觉寄存器。

### 4.2 统一界面类型

所有界面必须先归类为以下类型之一：

1. list
2. detail
3. edit-config
4. operation-workbench
5. exception-handling
6. evidence-audit
7. ai-chat
8. ai-sidebar
9. brand-marketing
10. mobile-desktop-shell

未完成归类的界面不得进入开发和验收。

### 4.3 统一视觉与文案原则

1. 相同语义必须使用相同颜色、标签、按钮优先级和反馈方式。
2. 业务完成态、治理完成态、AI 建议态不得混色。
3. 界面文案必须从用户可识别动作出发，不得使用系统内部术语冒充用户语言。
4. 空状态、错误态、阻断态必须指向下一步，而不是只做描述。

## 5. 开发基线

### 5.1 统一令牌与组件

所有项目必须优先复用统一令牌和组件，不允许先做页面、后补统一样式。

最小统一对象：

1. semantic color tokens
2. typography scale
3. spacing tokens
4. radius / border / shadow tokens
5. buttons
6. inputs
7. forms
8. tables
9. status tags
10. cards
11. modals / drawers
12. toasts
13. empty / loading / error / blocked states

### 5.2 真实工程约束

1. 只改请求范围内的界面和必要共享组件。
2. 不允许为一次性页面发明新设计系统。
3. 不允许无授权新增依赖、全局 hook、浏览器扩展或大型重构。
4. 交互、键盘路径、响应式和长文本鲁棒性属于必须项，不是加分项。

### 5.3 AI 与业务事实分离

1. AI 建议必须单独分区。
2. AI 建议必须能回指来源或 evidence。
3. AI 建议必须可驳回。
4. AI 建议不得伪装成最终业务确认、验收完成或治理放行。

## 6. Loop 接入

### 6.1 触发条件

Loop 轮次出现以下任一情况，必须执行 UI Quality Gate：

1. 新增或修改产品界面
2. 工作台、控制塔、详情页、证据页、异常页、配置页改造
3. AI 对话页或 AI 侧栏改造
4. 前端回归被用作本轮重要结论的一部分
5. 需要对“界面可用”“界面已完成”“交互已闭环”做结论

### 6.2 Loop 必填输出

涉及 UI 的 round 必须显式写出：

1. `UI scope = true`
2. `UI gate status`
3. `Tool route`
4. `Context package`
5. `Prompt profile`
6. `Design options`
7. `Selected option`
8. `WAES baseline reuse`
9. `Surface`
10. `Tools used`
11. `Verification`
12. `Status ceiling`
13. G1-G9 gate table
14. UI caveats，例如 `runtime_not_verified`、`mobile_not_verified`、`a11y_manual_only`、`figma_not_verified`

### 6.3 Loop 状态上限

1. 涉及 UI 但未执行 UI gate，本轮状态上限为 `partial`。
2. UI gate 为 `ui_blocked`，本轮状态上限为 `blocked`。
3. UI gate 为 `ui_rework_required`，本轮状态上限为 `rework_required`。
4. UI gate 为 `ui_partial`，本轮状态上限仍为 `partial`。
5. UI gate 为 `ui_ready` 也只代表 `ui_evidence_candidate`，不等于业务完成。

### 6.4 UI 产品优先控制

涉及 Studio、工作台、AI 会话工作区、KDS 对象工作区或其它产品界面的 LOOP 轮次，必须遵守 `LOOP_UI_PRODUCT_FIRST_CONTROL.md`。

最高规则：

```text
LOOP success must not reduce product usability.
UI evidence is not UI structure.
Governance evidence must be traceable, not dominant.
Debug details must not become default product copy.
A test-visible element is not automatically user-visible.
```

UI Quality Gate 需要额外判断：

| Gate | 要求 |
|---|---|
| `product_first_ui_gate` | 本轮是否推进用户可识别任务流 |
| `evidence_overexposure_gate` | 是否避免默认界面继续堆叠治理证据 |
| `debug_details_visibility` | 技术细节是否默认隐藏并进入调试或治理详情 |
| `task_flow_e2e_status` | E2E 是否验证用户任务流，而不是只验证治理条存在 |
| `audit_traceability_gate` | 审计、权限、回执、边界是否仍可追溯 |

任一核心 gate 失败时，UI gate 不得高于 `ui_rework_required`。

## 7. 评估基线

项目群 UI 统一采用 G1-G9 九门评估：

1. G1 Surface Structure
2. G2 Design Tokens
3. G3 Component Consistency
4. G4 Evidence And Governance
5. G5 AI Fact Separation
6. G6 Accessibility
7. G7 Responsive And Text Robustness
8. G8 Runtime Verification
9. G9 Scope Control

每个 gate 只能取：

1. pass
2. partial
3. fail
4. not_applicable

任何 `pass` 都必须有证据；任何 `partial` 或 `fail` 都必须有剩余工作。

## 8. 角色分工

1. 产品/业务负责人：确认目标任务、关键路径、业务事实边界。
2. 设计负责人：确认界面类型、体验骨架、页面结构、令牌与组件策略。
3. 前端/实现负责人：在既有技术栈内做最小实现并保留可验证证据。
4. Loop 编排负责人：判断本轮是否触发 UI gate，并确保 round 写入完整字段。
5. Harness / WAES：决定 broader project status，UI gate 不能越权替代。

## 9. 交付物最小集合

一个可审计的 UI 交付至少应包含：

1. 目标界面类型
2. 影响范围
3. 令牌/组件复用说明
4. G1-G9 gate table
5. desktop 与 mobile 至少各一条验证说明
6. keyboard / focus 或明确 `a11y_manual_only`
7. screenshot、browser、Playwright 或同等级运行证据
8. remaining work 和 status ceiling

## 10. 标准工具链

项目群 UI 统一采用以下工具链：

1. `@product-design`
2. `WAES` 现有界面框架
3. `ui-ux-pro-max`
4. `Figma`
5. `Storybook`
6. `impeccable`
7. `Playwright/browser`
8. `axe-core` / `Lighthouse`
9. `GPCF Loop UI Quality Gate`

执行规则：

1. 整体界面、页面类、关键组件类和结构性重设计，必须先走 `@product-design` 的 `get-context -> ideate -> 选择方案`。
2. 专业工作台类默认先对齐 `WAES` 现有界面框架，再做项目级优化。
3. 没有运行验证的工具输出，最高只算候选，不算完成。

## 11. 工具上下文包与提示词能力

### 11.1 工具上下文包

所有 UI 任务都必须具备统一 `工具上下文包`，至少包含：

1. 项目与业务角色
2. 页面类或组件类
3. 用户目标与关键路径
4. 视觉/代码/设计系统来源
5. `WAES` 复用层级
6. 约束、非目标和禁改项
7. 门禁、证据与交付要求

### 11.2 提示词能力

所有 UI 工具都必须使用可审计的 `提示词能力`，至少覆盖：

1. `functional-accuracy`
2. `visual-quality`
3. `usability-experience`
4. `governance-evidence`
5. `scope-control`

不允许只给模糊要求。最小提示词必须写出：

1. 要解决的对象
2. 要达成的结果
3. 禁止越权的边界
4. 输出格式
5. 验证要求

## 12. 三方案机制

以下对象必须至少给出 `3` 种界面设计方案：

1. 项目总界面
2. 高风险页面类
3. 关键组件类
4. 结构性重设计对象

规则如下：

1. 三方案必须保持统一框架、统一令牌和统一风格样式。
2. 三方案产出后必须明确 `Selected option`，未选定不得直接实现。
3. 小型缺陷修复可复用既有选定方向，但必须显式写 `Selected option = existing`。

## 13. 非声明事项

本规范不自动声明以下事项：

1. 业务完成
2. 真实用户验收完成
3. Harness 通过
4. WAES 放行
5. accepted
6. integrated
7. production_ready
