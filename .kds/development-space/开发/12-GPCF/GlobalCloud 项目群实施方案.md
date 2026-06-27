---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-IMPLEMENTATION-PLAN-20260624
title: GlobalCloud 项目群实施方案
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/GlobalCloud 项目群实施方案.md
source_path: GlobalCloud 项目群实施方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群实施方案

## 1. 实施方案定位

本文位于 GPCF 仓库根目录，是 GlobalCloud 项目群唯一主体实施方案，也是项目群当前唯一总实施主方案，承接 `WAS世界资产体系总体方案.md` 和 `GlobalCloud 项目群主方案控制台账`，用于控制项目群从方案一致性走向真实进度、真实研发、真实运行、真实集成、真实交付和真实客户验收。

本文不替代任何项目总体方案，不重新定义 WAS、Ontology、XWAIL、WAE、WAES、AaaS 或 SCaaS 的定位。本文只定义如何实施、如何验证、如何交付、如何验收和如何保留证据。

历史路径 `01-architecture/GlobalCloud项目群实施方案.md` 只保留兼容镜像职责，不再是主体文件。

## 2. 与项目群总体方案的继承关系

本方案继承：

```text
GPCF:01-architecture/GlobalCloud 项目群总体方案.md
```

本方案受以下文件控制：

- `01-architecture/GlobalCloud 项目群总体方案.md`
- `09-status/globalcloud-project-master-plan-control-register.md`
- `09-status/globalcloud-project-implementation-control-register.md`
- `09-status/globalcloud-core-chain-real-evidence-register.md`
- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`
- `02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md`
- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `templates/project-implementation-plan-template.md`
- `templates/real-evidence-record-template.md`
- `02-governance/project-implementation-plan-change-propagation-template.md`

主方案变化影响实施口径时，必须先更新项目群实施方案，再传导到相关项目实施方案。项目实施方案变化影响总体职责、接口、交付或验收口径时，必须回流项目群实施方案或 Change Proposal。

## 3. 实施范围与项目清单

本方案覆盖以下业务和治理项目：

1. WAS世界资产体系
2. GlobalCloud XWAIL
3. GlobalCloud AaaS / AAAS
4. GlobalCloud WAES
5. GlobalCloud GFIS
6. GlobalCloud GPC
7. GlobalCloud PVAOS
8. GlobalCloud KDS
9. GlobalCloud Brain
10. GlobalCloud Studio
11. GlobalCloud MMC
12. GlobalCloud PKC
13. GlobalCloud SOP
14. GlobalCloud XGD
15. GlobalCloud XiaoC
16. GlobalCloud XiaoG
17. GlobalCoud GPCF

`shared/python_utils` 是共享工具目录，不建立项目实施方案，但必须纳入依赖、导入可用性和回滚控制。

## 4. 实施状态机

| 状态 | 含义 | 升级要求 |
|---|---|---|
| `not_started` | 尚未建立实施动作 | 无 |
| `planned` | 已有实施方案或任务计划 | 有受控方案或任务 |
| `in_progress` | 正在实施 | 有真实任务或代码/配置变更 |
| `blocked` | 被依赖、权限、测试、环境或确认阻塞 | 有阻塞证据 |
| `candidate` | 有候选实现或候选交付物 | 有候选证据，不得声明完成 |
| `verified` | 内部验证通过 | 有测试、运行或接口证据 |
| `ready_for_review` | 可进入人工审查 | 证据包完整 |
| `ready_for_uat` | 可进入用户/客户验收 | 有交付包和验收清单 |
| `customer_review` | 用户/客户正在验收 | 有验收记录 |
| `customer_accepted` | 用户/客户确认通过 | 必须有人类确认 |
| `repair_required` | 验证或验收退回 | 有修复项 |
| `closed` | 完整闭环 | 有验收、交付和归档证据 |

Agent、脚本或自动化不得自动声明 `customer_accepted`、`accepted`、`integrated` 或 `production_ready`。

## 5. 真实进度管理

真实进度必须由任务、里程碑、阻塞项、证据和下一步组成。没有任务，不叫进度。

项目实施状态由 `09-status/globalcloud-project-implementation-control-register.md` 统一登记。每个项目实施方案必须列出当前真实状态、当前里程碑、阻塞项、证据索引和下一步动作。

项目群当前 live 基线与开发态入口口径由以下两份证据控制：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

当前必须保持：

```text
project_group_current_state_baseline_refresh_20260626 = controlled
development_queue_ready = true
dirty_repo_count = 7
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
```

若项目级实施方案、状态矩阵、真实执行治理总控板与上述两份证据冲突，以当前状态刷新证据、开发态任务队列和总控板为准，并触发回写。

## 6. 真实研发管理

真实研发必须有代码、配置、脚本、测试或工程证据。文档更新不能单独声明研发完成。

每个项目实施方案必须列出：

- 研发任务清单；
- 代码或配置变更位置；
- 测试命令；
- 构建命令；
- 失败记录；
- 回滚路径。

## 7. 真实运行管理

真实运行必须有环境、启动命令、健康检查、日志、依赖服务和最近一次运行证据。页面存在、README 存在或 mock 成功都不能替代真实运行。

每个项目实施方案必须列出运行环境、启动命令、健康检查方式、日志位置、依赖服务和运行失败处理。

运行、集成、交付和客户验收的当前前置控制统一以以下两份证据为准：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

当前必须保持：

```text
project_group_current_state_baseline_refresh_20260626 = controlled
development_queue_ready = true
dirty_repo_count = 7
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
```

在上述前置控制未变化前，不得把任何运行、集成、交付或客户验收候选直接解释为真实完成。

## 8. 真实集成管理

真实集成必须按调用方、被调用方、接口类型、数据对象、权限方式、契约版本、测试命令、最近验证时间和失败处理登记。

集成状态分级：

```text
declared -> contracted -> mocked -> tested -> verified -> accepted
```

`accepted` 必须有业务方或用户确认，不能由自动化脚本直接生成。

## 9. 真实交付管理

真实交付必须具备交付说明、部署说明、运行说明、配置说明、账号权限说明、测试报告、已知问题、回滚说明、培训材料和验收清单。

项目实施方案不得把代码合并、构建通过或文档完成直接声明为客户交付完成。

## 10. 客户验收管理

客户验收必须记录验收对象、验收场景、验收步骤、验收数据、验收人、验收结果、问题清单、修复记录和签收证据。

没有客户或授权人确认，不得声明 `customer_accepted`。

## 11. 项目间实施依赖矩阵

| 链路 | 主要项目 | 实施控制 |
|---|---|---|
| 模型契约链路 | WAS、Ontology、XWAIL、WAES | 模型、Profile、Validator、发布状态 |
| 服务运营链路 | XWAIL、WAES、AaaS、PVAOS | ServicePackage、计量、SLA、订阅状态 |
| 业务事实链路 | GFIS、GPC、PVAOS、KDS | 事实源、证据源、审计和回滚 |
| 知识智能链路 | KDS、Brain、XiaoC、PKC、XGD、XiaoG | 知识、提示、智能体输出和候选边界 |
| 工程治理链路 | GPCF、MMC、SOP、Studio | Harness、LOOP、SOP、模板、配置和证据 |
| 界面工程链路 | WAES、Studio、PKC、XGD、GPC、GFIS、GPCF | 统一体验骨架、设计令牌、工作台母框架、UI 工具链、UI gate 和页面/组件三方案机制 |

## 12. 版本、里程碑与发布节奏

| 对象 | 当前基线 |
|---|---|
| 项目群方案基线 | `GC-WAS-PG-BASELINE-0.1.0` |
| 项目群实施方案 | `v1.0` |
| 实施登记状态 | `implementation_plan_governance = phase_3_all_project_plans_controlled` |

实施方案版本不得高于其继承的项目总体方案版本控制边界。项目实施方案发生结构性变化时，必须更新实施控制台账。

## 13. 证据标准

| 证据类型 | 最低要求 |
|---|---|
| 进度证据 | 任务、里程碑、状态、阻塞、下一步 |
| 研发证据 | 代码/配置/脚本变更、测试、构建、回滚 |
| 运行证据 | 启动命令、健康检查、日志、依赖 |
| 集成证据 | 契约、接口测试、权限、数据对象 |
| 交付证据 | 交付包、部署说明、测试报告、已知问题 |
| 验收证据 | 验收场景、验收人、验收结果、签收或退回 |

核心链路真实证据由 `09-status/globalcloud-core-chain-real-evidence-register.md` 控制，单条证据记录使用 `templates/real-evidence-record-template.md`。历史 evidence、mock、dry-run 或专项样例不能自动升级为当前真实运行证据，必须经台账登记和验证脚本确认。

## 14. LOOP 接入

```yaml
loop_enabled: true
loop_owner: GPCF
required_gates:
  - document_gate
  - implementation_plan_gate
  - real_progress_gate
  - real_development_gate
  - runtime_gate
  - integration_gate
  - delivery_gate
  - customer_acceptance_gate
  - evidence_gate
```

每轮真实实施推进必须覆盖 `run -> stop -> verify -> recover -> debug`。

## 14.1 UI/LOOP 实施链路

项目群界面工程实施方案已正式纳入本主体实施方案，并作为 LOOP 工程体系中的受控专项实施链路。

受控入口：

- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `.codex/skills/globalcloud-ui-quality-gate/SKILL.md`
- `templates/LOOP_ROUND_TEMPLATE.md`
- `tools/kds-sync/validate_loop_ui_quality_baseline.py`
- `docs/harness/loops/loop-round-GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001.md`

最低推进规则：

| 阶段 | 目标 | 退出门禁 |
|---|---|---|
| 方案控制 | 确认项目群主体实施方案与界面工程专项方案一致 | `validate_project_group_implementation_plan.py` pass |
| 设计前置 | 对整体界面、页面类、关键组件类和结构性重设计形成 `@product-design` 三方案 | 未形成 `Selected option` 前不得直接实现 |
| 母框架复用 | 专业工作台类先映射 `WAES` 现有界面框架 | 未登记 `WAES baseline reuse` 时状态最高 `partial` |
| 运行验证 | 形成桌面/移动、键盘路径、截图或等价真实验证 | `validate_loop_ui_quality_baseline.py` pass |
| Loop 留证 | round 必须登记 `Tool route`、`Context package`、`Prompt profile`、`Design options`、`Selected option` 和 UI gate | 缺任一字段时状态最高 `partial` |

项目类型与界面规范总控映射：

| 项目类型 | 适用项目 | 主控 UI 规范 |
|---|---|---|
| 控制塔类 | GPCF、WAES 副类 | 状态总览、门禁、证据、阻断、下一步必须稳定可见 |
| 专业工作台类 | WAES、GPC、GFIS、PKC、XGD、Studio | 默认以 `WAES` 现有界面框架为母框架，先做外壳层、页面骨架层、核心高风险组件层复用映射，再做项目级优化 |
| 运营后台类 | MMC、PVAOS 副类 | 配置、发布、审计、模板和组织运营入口必须强调批量操作安全与回滚 |
| 分析决策类 | Brain、KDS、PKC 副类、XGD 副类、Studio 副类、WAS 副类 | 知识来源、推理链、证据引用和 AI 建议必须与业务事实分离 |
| 门户与展示类 | PVAOS、公开入口 | 可保留项目级表达，但不得突破统一令牌、状态语义、证据边界和 AI 边界 |
| 移动作业类 | XiaoG | 轻执行、轻查询、通知、只读入口优先，触控、弱网、长文本和阻断反馈必须验证 |
| 系统配置与治理类 | MMC、SOP、XiaoC、WAS、GPCF 副类 | 权限、危险操作、配置变更、审计链和治理状态必须显式呈现 |

页面类与组件类最低门禁：

| 对象 | 强制范围 | LOOP 要求 |
|---|---|---|
| 页面类 | 主列表页、详情页、编辑/配置页、操作工作台页、异常处理页、证据/审计页、AI 对话页、AI 侧栏/辅助页、门户/入口页、移动/轻执行页 | 必须声明 `Surface`，并按 G1-G9 输出 UI gate |
| 组件类 | 按钮、输入、选择、表单编排、表格与数据呈现、状态与标记、导航与定位、弹层与上下文操作、反馈与系统状态、审计与证据、AI 交互、复合工作台 | 高风险组件变更必须声明复用令牌、状态语义、可访问性、响应式和证据边界 |

工具链真实作用方式固定如下：

| 工具层 | 真实作用 | LOOP 留证字段 |
|---|---|---|
| `@product-design` | 总体界面、页面类、关键组件类和结构性重设计的设计前置层，必须产出 `get-context -> ideate -> select option` 和三方案 | `Design options`、`Selected option` |
| `WAES` 现有界面框架 | 专业工作台母框架复用层，当前是可复用基础框架而非最终标准件 | `WAES baseline reuse` |
| `ui-ux-pro-max` | 设计系统、组件词汇、令牌语义和页面类型约束来源 | `Tool route`、`Context package` |
| `Figma` / `Storybook` | 视觉真值源、组件映射源、组件/页面可见性回归源；不存在或未使用时必须说明 | `figma_not_verified` 或 Storybook 证据 |
| `impeccable` | 产品界面审计、硬化、润色和结构优化层 | `Tools used`、整改建议 |
| `Playwright/browser` | 真实运行、桌面/移动截图、键盘路径和交互验证层 | `Verification` |
| `axe-core` / `Lighthouse` | 无障碍、可读性和性能辅助验证层 | `a11y_manual_only` 或自动化证据 |
| `GPCF Loop UI Quality Gate` | 最终 UI 门禁层，只产出 `ui_evidence_candidate` | `UI gate status`、`Status ceiling` |

工具上下文包与提示词能力必须作为 UI 工程输入，而不是事后说明。上下文包至少包含项目与角色、页面类或组件类、用户目标与关键路径、视觉/代码/设计系统来源、`WAES` 复用层级、约束/非目标/禁改项、门禁/证据/交付要求。提示词能力至少覆盖 `functional-accuracy`、`visual-quality`、`usability-experience`、`governance-evidence`、`scope-control`，并明确功能准确、真实执行、美观界面、方便使用和优秀体验的验收口径。

三方案机制固定适用于项目总界面、高风险页面类、关键组件类和结构性重设计对象。三种方案必须共享统一框架、统一令牌和统一风格样式；未记录 `Selected option` 时不得进入实现；小型缺陷修复可写 `Selected option = existing`，但仍需说明复用的既有方向。

当前 UI/LOOP 状态固定为：

```text
ui_toolchain_governance = controlled
ui_toolchain_route = @product-design -> WAES -> ui-ux-pro-max -> Figma -> Storybook -> impeccable -> Playwright/browser -> axe-core/Lighthouse -> GPCF UI Gate
ui_scope_round_baseline = established
ui_evidence_status_ceiling = ui_evidence_candidate
```

界面工程专项不得把设计稿、截图、mock、前端构建通过、浏览器可见性或 UI gate 直接写成客户验收、业务完成、accepted、integrated 或 production_ready。

## 14.2 WAS/LOOP 实施链路

WAS/LOOP 实施链路是本实施方案体系的默认主链之一，用于把 WAS 顶层语义、Ontology 语义知识层、XWAIL 机器契约、WAES 审查门禁、KDS 证据引用、Brain 候选解释和 GPCF LOOP 运行控制闭环合并到同一实施路径。

受控入口：

- `02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md`
- `docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100.md`
- `docs/harness/evidence/was-real-source-record-monitor-100-20260623.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_100.py`
- `tools/kds-sync/validate_was_status_matrix_control_board_refresh.py`

WAS/LOOP 实施链路的最低推进规则：

| 阶段 | 目标 | 退出门禁 |
|---|---|---|
| 方案控制 | 确认 WAS 总体方案、项目群实施方案和专项全量实施方案一致 | `validate_project_group_implementation_plan.py` pass |
| Source Record 准备 | 定义并监控真实 P4 candidate 输入 | 无真实输入时 `hold_required=1` |
| 语义与契约 replay | 复跑 profile mapping、crosswalk、negative fixtures 和 WAS validator | 不提升真实业务计数 |
| WAES 审查前置 | 只有真实 source-record 和授权齐备后才允许进入 review/runtime | 缺输入时 `review_queue=0`、`runtime_intake=0`、`waes_review=0` |
| 证据与下一轮 | 形成 Loop round、Harness evidence、validator output 和下一轮输入 | 必须包含 `run -> stop -> verify -> recover -> debug` |

当前 WAS/LOOP 状态固定为：`latest_monitor_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100`，`next_monitor_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101`，`real_source_records=0`，`valid_source_records=0`，`runtime_primary_key_ready=0`，`review_queue=0`，`runtime_intake=0`，`waes_review=0`，`verified=0`，`accepted=false`，`integrated=false`，`production_ready=false`。

WAS/LOOP 实施链路不得把文档、模板、测试数据、mock、KDS 候选、用户口述、报价材料、合同审阅稿或治理 validator 写成真实 source-of-record、业务事实、客户验收或生产完成。

## 15. 变更传导机制

```text
Implementation Change Proposal
  -> Scope Review
  -> Affected Project Implementation Matrix
  -> Master Implementation Plan Decision
  -> Project Implementation Plan Patch List
  -> User Confirmation
  -> Document Control / KDS Mirror
  -> Gate Validation
  -> Evidence / Status Report
```

未经用户确认的结构性实施变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 16. 第一阶段实施边界

第一阶段只建立项目群实施方案管控体系：

- 项目群实施主方案；
- 项目实施方案模板；
- 项目实施方案控制台账；
- 实施方案变更传导模板；
- 第一批实施方案治理验证脚本。

第一阶段不声明任何项目真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

第二阶段建立核心链路项目唯一实施方案：

- GPCF；
- WAS世界资产体系；
- GlobalCloud XWAIL；
- GlobalCloud AaaS / AAAS；
- GlobalCloud WAES；
- GlobalCloud GFIS；
- GlobalCloud GPC；
- GlobalCloud PVAOS；
- GlobalCloud KDS；
- GlobalCloud Brain。

第二阶段不声明上述项目真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

第三阶段建立全部剩余支撑与智能体项目唯一实施方案：

- GlobalCloud Studio；
- GlobalCloud MMC；
- GlobalCloud PKC；
- GlobalCloud SOP；
- GlobalCloud XGD；
- GlobalCloud XiaoC；
- GlobalCloud XiaoG。

第三阶段完成后，可以声明所有登记业务项目均已有唯一当前有效实施方案，但仍不得声明真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

## 17. 非声明边界

本文不声明：

- 不声明任何业务项目已经真实研发完成；
- 不声明任何业务项目已经真实运行完成；
- 不声明任何跨项目接口已经真实集成完成；
- 不声明任何项目已经客户交付完成；
- 不声明任何项目已经客户验收通过；
- 不声明 accepted、integrated 或 production_ready。
