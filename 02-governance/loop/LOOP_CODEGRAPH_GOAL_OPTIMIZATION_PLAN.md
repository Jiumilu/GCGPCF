---
doc_id: GPCF-DOC-AB6DC46557
title: Loop CodeGraph Goal Optimization Plan
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, Brain, XiaoC, XGD, XiaoG, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md
source_path: 02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Goal Optimization Plan

## 1. 目标

本方案用于把 `colbymchenry/codegraph` 纳入 GlobalCloud Loop Engineering，形成“代码图谱感知 + 目标优化 + 成本度量 + 自我进化”的受控工程闭环。

目标不是引入一个新的业务系统，而是降低 Loop 在代码理解、影响分析、测试选择和复盘沉淀上的探索成本。

## 2. 定位

| 层级 | CodeGraph 角色 | 不得替代 |
|---|---|---|
| 感知层 | 本地代码结构索引、符号关系、调用链、路由和影响面查询 | 源码复核、测试、业务事实 |
| 计划层 | 帮助确定最小改动范围、相关测试和风险路径 | 人工授权、Loop 目标定义 |
| 执行层 | 为 Codex/Hermes/Cursor 等 agent 提供 MCP 查询能力 | 代码审查、质量门禁 |
| 复盘层 | 记录工具调用节省、误改减少、查询模板复用 | Harness/WAES 状态裁决 |

## 3. 实施原则

1. CodeGraph 只作为本地辅助索引；`.codegraph/` 是本机缓存，必须被 Git 忽略。
2. CodeGraph 查询结果不能直接证明业务完成、真实接口完成、UAT 完成、客户满意或 `accepted/integrated`。
3. 涉及真实 API、生产配置、部署、权限、密钥、KDS TOKEN、数据库迁移和外部写入时，仍按 Loop L3.5/L4/L5 授权边界执行。
4. 所有目标优化必须落回五段式微循环：输入、动作、输出、检查、反馈。
5. 每轮必须保留“CodeGraph 是否使用、查了什么、影响范围是否命中、是否减少探索成本”的 evidence。

## 4. 分阶段实施

| 阶段 | 模式 | 范围 | 动作 | 验收 |
|---|---|---|---|---|
| P0 准入设计 | L0/L1 | GPCF 总控 | 建立本方案、evidence、validator、`.gitignore` 缓存排除 | `validate_loop_codegraph_goal_optimization.py` pass |
| P1 本地试点 | L2 | GPCF + GFIS | 在本机安装 CLI、配置 agent MCP、对试点仓执行 `codegraph init` | 索引存在但不入库；试点轮次记录查询和影响面 |
| P2 对照度量 | L2/L3 | GFIS repair 任务 | 选择 5-10 个真实 Loop 任务记录使用前后探索成本 | 工具调用、读文件数、返工数趋势下降 |
| P3 模板固化 | L3/L4 | 多项目 | 把高频查询、影响分析模板和测试选择模板纳入 skill/checklist | 每轮复盘能生成下一轮约束 |
| P4 持续进化 | L4 授权后 | 项目群 | 自动把低风险查询模板更新为治理资产 | 不越权升级状态，不触达生产写入 |

## 5. 目标优化 Loop

每个开发或治理目标进入执行前，增加一个目标优化子循环：

```text
目标声明 -> 图谱预检 -> 影响面收敛 -> 最小动作计划 -> 验证选择 -> 执行 -> 结果度量 -> 规则沉淀
```

| 步骤 | 输入 | 输出 | 检查 |
|---|---|---|---|
| 目标声明 | 用户目标、Loop 队列、当前状态矩阵 | `target_id`、成功标准、禁止范围 | 是否可验证 |
| 图谱预检 | 目标关键词、模块名、函数名、路由名 | `codegraph_scope_query` | 是否命中真实仓库代码 |
| 影响面收敛 | 调用链、相关符号、入口文件 | `impacted_symbols`、`impacted_files` | 是否需要人工源码抽查 |
| 最小动作计划 | 影响面和风险 | `planned_change_set` | 是否超出目标 |
| 验证选择 | 相关测试、validator、文档门禁 | `required_validators` | 是否覆盖核心风险 |
| 执行 | 受控改动 | diff、evidence | 是否保护既有工作 |
| 结果度量 | 命令输出、工具调用、耗时 | cost/effectiveness 指标 | 是否真实降低探索成本 |
| 规则沉淀 | 本轮偏差和高价值查询 | skill/checklist/模板候选 | 是否形成下一轮约束 |

## 6. 每轮必填字段

| 字段 | 含义 | 示例 |
|---|---|---|
| `codegraph_enabled` | 本轮是否启用 CodeGraph | `true/false` |
| `codegraph_scope_query` | 本轮图谱查询目标 | `CustomerRequirementOrPlatformOrder runtime gate` |
| `impacted_symbols` | 命中的符号、函数、路由或模块 | `validate_gfis_runtime_sop_e2e` |
| `impacted_files` | 建议关注文件 | `scripts/validate_*.py` |
| `manual_source_check` | 是否抽查源码确认 | `required/pass/not_applicable` |
| `related_validators` | 本轮必须运行的测试或门禁 | `python3 scripts/...` |
| `exploration_tool_calls_before` | 对照基线工具调用数 | 数字或 `baseline_pending` |
| `exploration_tool_calls_after` | 本轮工具调用数 | 数字或 `pending` |
| `file_reads_before` | 对照基线读文件数 | 数字或 `baseline_pending` |
| `file_reads_after` | 本轮读文件数 | 数字或 `pending` |
| `scope_precision_result` | 影响面是否命中 | `pass/partial/fail` |
| `optimization_feedback` | 下一轮规则或模板建议 | 文本 |

## 7. 成本与效率指标

| 指标 | 目标 | 说明 |
|---|---|---|
| `exploration_tool_call_reduction_rate` | 趋势下降 | 与同类任务历史基线比较 |
| `file_read_reduction_rate` | 趋势下降 | 减少无目标读文件 |
| `round_duration_delta` | 趋势下降 | 不以牺牲质量为代价 |
| `validator_first_pass_rate` | 趋势提升 | 修改范围更准 |
| `wrong_scope_change_count` | 0 | 不改无关文件 |
| `impact_miss_count` | 0 或下降 | 图谱未发现但验证发现的影响 |
| `rework_count` | 趋势下降 | 减少因理解错误导致的返工 |

## 8. 工具接入边界

后续 P1 试点可使用以下命令，但本方案本轮不执行安装、不修改 MCP 配置：

```bash
# 安装 CLI，需用户明确授权
npm i -g @colbymchenry/codegraph

# 或使用上游安装脚本，需单独确认网络与脚本信任边界
# curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# 配置 agent MCP，需用户明确授权
codegraph install

# 在每个试点项目仓建立本地索引
codegraph init
```

`.codegraph/` 必须保持本地缓存，不进入 Git、KDS、本地镜像或 OKF 派生包。

## 9. 试点选择

| 优先级 | 项目 | 原因 | 成功标准 |
|---|---|---|---|
| P0 | GPCF | Loop 控制面、文档和 validator 集中 | 方案与 validator 受控 |
| P0 | GFIS | 当前 repair 主线复杂，影响分析成本最高 | GFIS repair 轮次可记录影响面和测试选择 |
| P1 | Brain/KDS | 知识和索引链路复杂 | KDS/Brain 依赖查询模板可复用 |
| P1 | XiaoC/XGD/XiaoG | agent 编排链路复杂 | 调用链和路由查询减少误读 |

## 10. Definition of Done

P0 完成条件：

1. 本方案存在并具备受控 front matter。
2. `.gitignore` 排除 `.codegraph/`。
3. evidence 文件记录本轮准入、边界、指标和非声明。
4. validator 能检查方案、evidence、loop 记录和 `.gitignore`。
5. loop round 记录五段式微循环。
6. 文档治理、污染、KDS TOKEN、Loop 文档门禁至少完成本轮范围验证或登记受限原因。

P1 完成条件：

1. 用户明确授权安装和 MCP 配置。
2. GPCF/GFIS 本地索引建立，且 `.codegraph/` 未进入 Git。
3. 至少 3 个真实任务记录 CodeGraph 查询、影响面、测试选择和结果。
4. 每轮仍以源码复核、测试和 Harness/WAES 门禁为准。

P2 完成条件：

1. 形成 5-10 轮对照样本。
2. 能量化探索工具调用、读文件数、轮次耗时、返工次数和影响遗漏。
3. 至少 3 个高频查询模板进入 skill/checklist 候选。

## 11. 风险与回滚

| 风险 | 控制 |
|---|---|
| 盲信图谱导致漏改 | 每轮必须保留 `manual_source_check` 和 validator |
| 本地索引误提交 | `.gitignore` 排除 `.codegraph/`，Git 门禁复核 |
| 工具安装改变 agent 行为 | P1 必须用户授权，保留 uninstall/rollback 记录 |
| 把效率提升写成业务完成 | 非声明和 validator 强制拦截 |
| 图谱过期 | 试点轮次记录 auto-sync 状态；疑似不一致时重新初始化或禁用 |

## 12. 非声明

- 本方案不证明 GFIS runtime SOP E2E 已通过。
- 本方案不创建 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact、UAT 签收、客户满意、`accepted` 或 `integrated`。
- 本方案不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、推送或合并。
- 本方案不把 CodeGraph 查询结果替代源码、测试、文档门禁、KDS TOKEN 门禁、Harness/WAES 判定或人工确认。
