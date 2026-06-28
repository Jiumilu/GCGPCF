---
doc_id: GPCF-DOC-6E7DCE4A91
title: LOOP 工程体系整体实施规范
project: WAES
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md
source_path: 02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP 工程体系整体实施规范

本文是 LOOP 工程体系的权威整体实施基线。它定义 LOOP 工程体系的目标、边界、文档层级、版本路线图、状态升级规则、证据链、门禁链和自我提升机制。

本文不替代 [Loop Control Board](./LOOP_CONTROL_BOARD.md)，不替代 [Loop Autonomy Policy](./LOOP_AUTONOMY_POLICY.md)，不替代 [LOOP 执行规则](./LOOP_EXECUTION_RULES.md)，也不替代 [Loop Engineering 五方向实施规范](./LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md)。本文负责定义整体基线；控制板负责记录当前事实；自治策略负责授权和停止；执行规则负责每轮动作；五方向规范负责运行、停止、验证、恢复、调试的操作模型。

当前真实执行治理入口必须以以下两份证据为准：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

当前接力事实保持：

```text
project_group_current_state_baseline_refresh_20260626 = controlled
development_queue_ready = true
dirty_repo_count = 7
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
```

## 1. 基线目标

LOOP 工程体系的基线目标是：把 GlobalCloud 项目群的需求、实施、证据、审查、验收准备、状态判断和自我修复纳入可审计、可回放、可门禁、可持续提升的工程闭环。

基线必须同时满足：

| 维度 | 基线要求 |
|---|---|
| 事实真实 | 业务完成只能来自真实 source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact 和人工确认 |
| 工程可执行 | 每轮必须形成输入、判断、动作、输出、检查、反馈和下一轮候选 |
| 证据可回放 | 每个关键结论必须能回指文档、validator 输出、evidence JSON/Markdown 或 Git diff |
| 状态可控 | 没有 evidence 时不得升级状态；文档债务存在时状态最高为 `partial` |
| 边界安全 | 默认不执行 production write、external API write、schema sync、bench migrate、deployment、permission change、commit、push |
| 自我提升 | 主体错位、弱证据误判、长序列风险、批量生成误计数和中文本地化债务必须进入治理 backlog |

## 1.1 开发完成与真实业务验证分离原则

LOOP v1.1 及后续版本必须遵守项目群最高裁决：

```text
真实业务输入是验收门，不是开发门。
```

LOOP 必须把 Delivery Loop 与 Governance Loop 的职责分开：

| Loop | 默认服务对象 | 可推进事项 | 不得释放 |
|---|---|---|---|
| Delivery Loop | `development_lane` | 本地开发、fixture E2E、controlled sample E2E、dry-run、contract validator、runtime intake development、review queue development、WAES review candidate development、verified artifact candidate development、`development_ready_for_real_business_validation` | 真实业务验证、accepted、integrated、production_ready、customer_accepted |
| Governance Loop | `real_business_validation_lane`、`acceptance_lane`、`production_lane` | 真实 source-of-record 验证、owner/WAES/客户验收裁决、生产就绪、交付和状态提升 | 未经人工确认的状态升级 |

P0/P1/P2/P3 门禁必须区分开发阻断与验证阻断。`real_source_records = 0` 可以阻断真实业务验证、生产动作、客户交付声明和状态提升；不得阻断本地开发、fixture E2E、dry-run、contract validator 或开发完成候选。

允许使用 fixture、mock、controlled sample、desensitized sample schema、synthetic-but-contract-valid data、dry-run 和 local validator 证明系统具备处理真实业务输入的开发能力；这些证据不得用于证明真实业务已经验证、客户已经确认、业务已经验收、系统已经集成或生产已经就绪。

GFIS 当前主线按以下方式解释：

```text
GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001
```

该主线目标是先完成可接收真实业务输入的 runtime SOP E2E 开发闭环，再等待真实业务 source-of-record 进入真实业务验证阶段。GFIS 的 `real_business_lane=repair_required` 不得被解释为 Delivery Loop 本地开发阻断。

## 2. 权威文档层级

| 层级 | 文档 | 职责 | 是否权威 |
|---|---|---|---|
| L0 总纲 | 本文 | 定义整体实施基线、版本和路线图 | 是 |
| L1 当前事实 | `LOOP_CONTROL_BOARD.md` | 记录当前模式、状态、阶段、允许动作、阻塞和下一步 | 是 |
| L1 授权边界 | `LOOP_AUTONOMY_POLICY.md` | 定义 L3/L3.5/L4/L5 授权、停止条件和禁止动作 | 是 |
| L1 执行规则 | `LOOP_EXECUTION_RULES.md` | 定义每轮必读输入、完成定义和不可绕过规则 | 是 |
| L2 操作模型 | `LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md` | 定义运行、停止、验证、恢复、调试 | 是 |
| L2 自我纠错 | `LOOP_ENGINEERING_SELF_CORRECTION.md` | 定义主体错位、弱证据和失败优先的防复发规则 | 是 |
| L2 会话主线 | `LOOP_SESSION_MAINLINE_CONTROL_PACK.md` | 定义会话主线声明、跨会话 handoff、防偏离和启动/恢复前置门禁 | 是 |
| L2 治理视图 | `LOOP_GOVERNANCE_DASHBOARD.md` | 聚合质量、效率、自我纠错、边界和状态上限信号 | 是 |
| L2 专项实施链路 | `GlobalCloud 项目群实施方案.md`、`04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`、`04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md` | 定义项目群总实施主线与界面工程/UI/工作台专项实施链路 | 是 |
| L3 状态记录 | `docs/harness/loop-state.md` | 记录项目群轮次状态和最近事实 | 是 |
| L3 轮次证据 | `docs/harness/loops/loop-round-*.md` | 记录单轮输入、动作、输出、检查和反馈 | 是 |
| L3 机器证据 | `docs/harness/evidence/*.{json,md}` | 保存 validator 输出、审查结果和门禁证据 | 是 |

如上述文档冲突，优先级为：真实运行证据 > validator 输出 > `LOOP_CONTROL_BOARD.md` 当前事实 > 本文基线规则 > 历史轮次记录。历史轮次记录不得被批量改写来制造完成态。

## 3. 体系边界

| 组件 | 职责 | 不得替代 |
|---|---|---|
| LOOP | 编排微循环、中循环、大循环，管理状态上限和下一步 | 不替代业务事实、不替代人工确认 |
| KDS | 受控知识事实主存与镜像 | 不替代 GFIS 运行层事实 |
| WAES | 授权、风险、门禁、审查和最终裁决 | 不替代业务主账 |
| Harness | 执行、证据、回放、指标和验收准备 | 不替代原始凭证 |
| GFIS | 工厂运行层事实与 SOP E2E 主体 | 不被 Demo、fixture、KDS candidate 或 Loop 文档替代 |
| GPCF | 项目群总控、文档治理、状态矩阵和跨项目 evidence 汇聚 | 不直接创建业务完成事实 |

## 4. 运行模型

每轮 LOOP 必须采用可回放的六段式记录：

| 字段 | 含义 | 最低要求 |
|---|---|---|
| 输入 | 本轮读取的事实、文档、缺口、授权边界 | 必须包含控制板、自治策略、状态或相关 evidence |
| 判断 | 本轮取舍、风险、状态上限、是否可并行 | 必须说明为何可以或不能推进 |
| 动作 | 实际执行的文件改动、命令、工具和 no-write 边界 | 必须可复现 |
| 输出 | 文档、代码、evidence、validator 或报告 | 必须有路径或命令输出 |
| 检查 | validator、门禁、diff、污染、TOKEN 或等价检查 | 必须记录通过或失败 |
| 反馈 | 下一轮输入、阻塞项、授权需求、回滚方式 | 不得把建议写成完成 |

连续模式下还必须记录 `declared_rounds`、`substantive_rounds`、`generated_items`、`batch_generated`、`substance_gate` 和 `stop_type`。

## 5. 会话主线与跨会话防偏离控制

多会话并行、长时间连续运行或跨项目治理时，必须先声明当前会话主线。任何会话不得在未授权、未交接、未重新校验范围的情况下，转去执行其它会话、其它项目或其它工作流的任务。

| 控制项 | 规则 |
|---|---|
| 主线声明 | 每个会话开始或恢复时必须声明 `session_mainline`、目标、范围、允许动作和停止条件 |
| 任务所有权 | 每个任务包必须绑定 owner session、项目、文档或 evidence，不得被其它会话隐式接管 |
| 跨会话交接 | 只有存在 handoff note、source evidence、当前状态复核和用户确认时，才允许接续其它会话工作 |
| 偏离检测 | 若用户请求、当前路径、Git dirty、任务包、validator 或 evidence 指向不同主线，必须暂停并报告 `mainline_drift_detected` |
| 并行限制 | 多智能体并行开发必须拆成互不重叠的 scope；最终集成和状态裁决只能回到主会话执行 |
| 禁止动作 | 不得因另一个会话存在未完成任务而自动切换主线、改其它项目、同步其它仓库、更新其它任务状态或关闭其它会话结论 |
| 恢复动作 | 发现偏离后只能执行只读核对、生成建议、请求确认或回到当前主线；不得继续写入 |

跨会话工作允许的最低条件：

- 当前用户明确确认接管或继续该会话任务。
- 已读取目标会话的最后一轮 `loop-round`、evidence、validator 输出和 Git 状态。
- 新会话记录 `handoff_source`、`handoff_time`、`scope_delta` 和 `authorization_delta`。
- 若涉及其它项目仓、真实 KDS API、外部 API、提交、推送、部署或状态升级，必须重新请求授权。
- 若没有完整交接证据，只能生成建议，不能执行写入。

该控制适用于 GPCF 总控仓、项目本地仓、KDS 镜像、能力注册表、CodeGraph、Agent-Reach、Ontology、Headroom、WAS、OKF/ODF、LCX、RAG/语义索引和多智能体并行开发全过程。

会话主线控制包见 [LOOP 会话主线控制包](./LOOP_SESSION_MAINLINE_CONTROL_PACK.md)。每轮 LOOP 启动、恢复或跨会话接续前，必须运行或等价检查：

```bash
python3 tools/kds-sync/validate_loop_session_mainline_control.py
```

## 6. 工程执行型 LOOP 决策基线

LOOP 工程体系的阶段性目标不是纯文档治理型 LOOP，而是工程执行型 LOOP：它必须能把项目群需求、任务包、工具能力、证据、状态和下一轮输入连接成可执行的工程主进程。

| 决策项 | 基线决定 |
|---|---|
| 最终目标 | 工程执行型 LOOP |
| 执行范围 | 项目群级执行，以 GPCF 总控和项目本地 LOOP 混合推进 |
| 优先级 | 业务闭环优先，治理只为提升工程质量、效率和自我提升 |
| 总体业务闭环 | 端到端绿色供应链闭环 |
| 第一落地点 | GFIS 运行层 SOP E2E |
| 输入分层 | `test_data_lane`、`candidate_lane`、`real_business_lane` |
| 候选转真实 | 业务 owner + WAES + Harness 组合放行 |
| 任务包完成定义 | 文档 + validator + evidence + 状态同步 + 运行层事实或明确阻塞 |
| 冲突裁决 | 分层优先：项目本地运行证据优先判运行事实，GPCF 判项目群状态，不一致则 `review_required` 或 `repair_required` |
| 代码权限 | 受控工程修改；不得默认触碰生产写入、外部 API 写入、schema、部署、权限、commit 或 push |
| Git 权限 | 按任务 Git 授权 |
| 会话主线 | 当前会话主线优先；跨会话接续必须有 handoff evidence 和用户确认 |
| 评分模型 | 治理成熟度、工程执行进度、业务闭环三层评分 |
| 自我提升 | v1/v2 以质量和效率为主，v3 以后才评估自治能力 |

## 7. 能力纳入与治理机制

LOOP 工程实施方案必须纳入技能、工具和方法。能力不再只作为临时执行手段，而必须进入受控能力池、接受风险分级、证据升级、降级停用和门禁检查。

权威能力清单见 [LOOP 能力注册表](./LOOP_CAPABILITY_REGISTRY.md)。本文只定义总体规则；注册表记录具体能力、状态、风险、适用范围、证据要求、validator 或门禁、回滚或停用方式。

| 机制 | 规则 |
|---|---|
| 能力分池 | 技能池、工具池、方法池 |
| 准入策略 | 快速准入：只要能力能提升效率，可以先以 `fast_admitted` 或 `candidate` 纳入能力池 |
| 默认启用 | `default_enabled` 必须按风险分级裁决，不因快速准入自动启用 |
| 状态升级 | `pilot` 以上状态变化必须有 evidence |
| 生命周期 | 支持 `downgraded`、`disabled`、`deprecated`、`superseded` |
| 门禁接入 | `validate_loop_capability_registry.py` 是 LOOP 文档门禁硬检查 |
| 非授权边界 | 能力登记不授权生产写入、外部 API 写入、schema sync、部署、权限变更、commit、push、accepted 或 integrated |

核心方法必须包含 CodeGraph、外部搜索/检索、RAG/语义索引、多智能体并行开发。上述方法采用子能力分级：只读、分析、检索、规划类子能力可进入 `controlled`；写入、自动执行、跨仓变更、外部 API 写入、生产或部署相关子能力只能进入 `pilot`、`candidate` 或显式授权范围。

界面工程/UI/工作台专项能力必须纳入 LOOP 能力池并受同等级门禁约束：

- `@product-design`
- `WAES` 母框架复用
- `ui-ux-pro-max`
- `Figma`
- `Storybook`
- `impeccable`
- `Playwright/browser`
- `axe-core` / `Lighthouse`
- `globalcloud-ui-quality-gate`

凡涉及整体界面、页面类、关键组件类、控制塔、工作台、证据页、异常页、AI 对话页、配置页、移动端或桌面端交互的 LOOP 轮次，必须显式写入：

- `Tool route`
- `Context package`
- `Prompt profile`
- `Design options`
- `Selected option`
- `WAES baseline reuse`
- `UI gate status`

## 8. 版本基线

| 版本 | 名称 | 目标 | 状态 |
|---|---|---|---|
| v0.1 | 文档化 Loop | 建立控制板、自治策略、执行规则、loop-state、round record | 已形成 |
| v0.2 | 证据化 Loop | 建立 evidence index、validator、文档门禁、污染检查和 KDS TOKEN 检查 | 已形成 |
| v0.3 | 自我纠错 Loop | 建立 GFIS 主体错位纠偏、弱证据拒收、状态降级和 repair_required 天花板 | 已形成 |
| v0.4 | 五方向 Loop Engineering | 建立运行、停止、验证、恢复、调试五方向操作模型 | 已形成 |
| v1.0 | 整体实施基线 | 建立本文、文档层级、能力注册表、版本路线图、状态升级规则和总纲 validator | 当前目标 |
| v1.1 | 中文治理与测试 lane | 清理核心治理文档中文本地化债务，稳定 `test_data_lane` 可回放链路 | 规划中 |
| v1.2 | 项目群任务队列 | 建立跨项目调度、任务包队列和 `candidate_lane` 可审查机制 | 规划中 |
| v2.0 | 工程执行型 LOOP | 形成工程执行主进程，GFIS 运行层 SOP E2E 进入真实业务 lane 候选 | 阻塞中 |
| v2.1 | 跨项目联动执行 | GPC、GFIS、KDS、WAES 形成可回放联动，candidate 到 real 的放行可验证 | 未启动 |
| v3.0 | 受控自治运行 | 具备可回滚、可审计、可授权的受控自治，端到端绿色供应链闭环进入候选 | 未启动 |
| v4.0 | 生产级准入评估 | 形成生产级准入评估材料，但不自动上线、不自动 accepted 或 integrated | 未启动 |

## 9. 路线图

### P0：基线立法

目标：把本文确立为 LOOP 工程体系整体实施规范，并接入机器校验。

完成条件：

- 本文存在且为 `controlled`。
- `LOOP_CAPABILITY_REGISTRY.md` 存在且为 `controlled`。
- `02-governance/loop/README.md` 登记本文。
- `02-governance/loop/README.md` 登记能力注册表。
- `02-governance/loop/README.md` 登记会话主线控制包。
- `tools/kds-sync/validate_loop_engineering_master_plan.py` 通过。
- `tools/kds-sync/validate_loop_capability_registry.py` 通过。
- `tools/kds-sync/validate_loop_session_mainline_control.py` 通过。
- `loop_document_gate.py` 接入该 validator。
- 不升级 `accepted`、`integrated` 或 `production_ready`。

### P1：治理债务收敛

目标：降低中文本地化债务、长序列风险和历史轮次记录债务。

完成条件：

- 核心治理文档中文门禁 findings 为 0。
- 当前 hard window 保持 `hard_missing_truth_fields=0` 和 `hard_missing_five_segment=0`。
- 长连续序列达到 checkpoint 时必须有 review disposition。
- 不批量改写历史 round record。

### P2：证据链一致性

目标：把控制板、loop-state、状态矩阵、evidence index 和 round record 的当前事实对齐。

完成条件：

- 同一当前轮次在五类控制面中一致。
- 机器 validator 能检查关键状态字段。
- `test_data_lane`、`candidate_lane`、`real_business_lane` 明确分层。
- 真实业务计数保持由 GFIS 运行层证据驱动。

### P3：项目群覆盖

目标：所有纳入项目具备最小 LOOP harness。

完成条件：

- 每个项目有 Manifest 或等价项目说明。
- 每个项目有 `loop-state`、evidence index、round record 和 validator。
- GPCF 控制板登记项目状态和阻塞。
- 技能、工具和方法进入能力注册表，且默认启用受风险分级约束。
- 未接入真实项目仓时必须标记为 GPCF 总控侧初始化，不得写成真实项目完成。

### P4：真实业务闭环候选

目标：在 GFIS 运行层真实业务链路具备 evidence 后，进入候选闭环评估。

完成条件：

- valid source records > 0。
- runtime primary key ready > 0。
- review queue > 0。
- runtime intake > 0。
- WAES review > 0。
- verified artifact > 0。
- 人工确认和回放证据存在。

### P5：受控自治准入

目标：在安全、回滚、权限、客户满意和依赖门禁全部满足后，评估 L4/L5 自治。

完成条件：

- 有明确授权。
- 有回滚方案和恢复检查点。
- 有客户满意或未收集原因。
- 无生产写入、外部 API、权限、部署、schema 或密钥风险。
- Harness Governance 明确裁决。

## 10. 状态升级规则

| 目标状态 | 最低条件 | 禁止误判 |
|---|---|---|
| `partial` | 文档、证据或 validator 局部完成，但仍有债务 | 不得写成业务完成 |
| `repair_required` | 真实链路或主体证据失败 | 不得被 demo/test pass 覆盖 |
| `evidence_ready` | 本轮 evidence 完整但未完成验收 | 不得等同 accepted |
| `ready_for_review` | 审查材料齐备 | 不得等同 integrated |
| `accepted` | 人工或授权裁决明确接受 | 不得由 agent 自动标记 |
| `integrated` | 真实系统集成证据、回放、验收和授权完整 | 不得由单个文档或 validator 自动标记 |
| `production_ready` | 生产、安全、回滚、客户、依赖和运行证据齐备 | 不得由 dry-run 或 fixture 自动标记 |

## 11. 门禁链

每轮至少按以下顺序检查：

1. 授权边界：是否允许改文件、运行真实接口、写入、提交、推送或部署。
2. 会话主线边界：是否存在 `session_mainline`、任务 owner、handoff evidence、scope delta、用户确认和 `validate_loop_session_mainline_control.py` 前置门禁。
3. Git 边界：是否存在用户工作、敏感文件、未提交冲突。
4. 文档边界：front matter、README、KDS 镜像、文档门禁。
5. 污染边界：旧项目名、旧架构口径、弱证据、Demo 替代、状态膨胀。
6. TOKEN 边界：KDS TOKEN 不得写入 Git、文档、evidence 或日志。
7. 质量边界：专项 validator、测试、diff check。
8. 证据边界：evidence JSON/Markdown、round record、loop-state、control board 对齐。
9. 状态边界：不得越过当前 status ceiling。
10. 能力边界：技能、工具、方法必须符合 `LOOP_CAPABILITY_REGISTRY.md`，且 `pilot` 以上状态变化必须有 evidence。

## 12. 自我提升机制

以下事件必须进入自我提升或治理 backlog：

- 主体错位：例如把 GFIS Demo 当成 GFIS 运行层。
- 弱证据误判：例如把 KDS candidate、fixture、测试数据、口述或 request package 当成 live proof。
- 状态膨胀：例如把 partial、repair_required、evidence_ready 写成 accepted/integrated。
- 连续轮次失真：例如批量生成 round record 却计为多个 substantive rounds。
- 文档债务：例如中文本地化债务、front matter 缺失、README 缺失、镜像不一致。
- validator 漂移：例如 evidence schema 变化导致校验器误报或漏报。
- 能力漂移：例如工具快速准入后缺少风险分级、证据、回滚、降级或停用路径。
- 会话主线漂移：例如一个会话偏离当前主线，转去执行其它会话、其它项目或其它任务包的工作。

## 13. 非声明边界

- 本文不创建 source-of-record。
- 本文不创建 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本文不证明 UAT、生产、客户满意、财务、accepted 或 integrated 完成。
- 本文不授权 production write、external API write、schema sync、bench migrate、deployment、permission change、commit 或 push。
- 本文不因登记技能、工具或方法而授权写入、上线、外部 API 调用、自动提交、自动推送或自动验收。
- 本文不替代 Harness Governance 的最终验收判定。

## 13. 当前基线结论

截至 `2026-06-22`，LOOP 工程体系进入 `v1.0 整体实施基线` 建立阶段。当前最权威整体实施规范为本文；当前能力清单以 `LOOP_CAPABILITY_REGISTRY.md` 为准；当前事实仍以 `LOOP_CONTROL_BOARD.md` 和 `docs/harness/loop-state.md` 为准；当前真实业务 lane 仍不得越过 GFIS 运行层 `repair_required` 状态天花板。
