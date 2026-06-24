---
doc_id: GPCF-DOC-0A2D9C6B81
title: LOOP Multi-Agent Execution Policy
project: WAES
related_projects: [GFIS, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_MULTI_AGENT_EXECUTION_POLICY.md
source_path: 02-governance/loop/LOOP_MULTI_AGENT_EXECUTION_POLICY.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Multi-Agent Execution Policy

本文件登记当前 Codex 与 GlobalCloud LOOP 工程体系中的默认多智能体/团队执行方案。它只定义执行面选择、边界和证据要求，不替代 `LOOP_CONTROL_BOARD.md`、`LOOP_AUTONOMY_POLICY.md`、OpsX Full Cycle、Harness Governance、WAES 裁决或 KDS TOKEN 安全边界。

## 默认分层

| 层级 | 默认能力 | 状态 | 作用 |
| --- | --- | --- | --- |
| 控制面 | `globalcloud-loop-orchestrator` | controlled | 读取状态、选择技能、执行门禁、生成下一轮 LOOP 输入 |
| 团队规则 | `globalcloud-collaborative-dev` | controlled | 定义 agent-fe / agent-be / agent-qa / agent-data / agent-security，限制并行度和文件边界 |
| 执行面 | Codex 内置 `multi_agent_v1` | controlled | 派发 explorer / worker 子智能体，执行受控并行分析或小范围实现 |
| 专家审计 | `gstack` | pilot | 作为 review / QA / security / design / release 专家组，不作为主调度层 |
| 候选增强 | OMX | candidate | 仅允许 L2/L3 隔离试点；不得直接进入 L4/L5 或替代 LOOP 控制面 |
| 长期平台 | OpenAI Agents SDK + Codex MCP | candidate | 作为未来正式编排平台候选，需单独设计 adapter、evidence 和 validator |

## 派发规则

- 默认由主 Codex 会话担任 LOOP Orchestrator，负责 `run`、`stop`、`verify`、`recover`、`debug` 的状态闭环。
- 只在任务能拆成互不冲突的独立子任务时启用并行子智能体。
- `explorer` 只做代码、文档、门禁、风险、依赖的只读调查。
- `worker` 只在写入范围清晰时使用，必须声明负责文件或模块，不得与其他 worker 共享写入边界。
- 同轮默认最多 3 个并行 agent；单 agent 最多 12 个文件、30 分钟、1 次重试。
- 跨项目、跨仓库、真实外部 API、生产配置、KDS/WAES/GFIS 真实写入、部署、推送、状态提升必须另行授权。

## 证据要求

每个并行 agent 的输出必须至少包含：

- 任务范围与允许路径。
- 结论类型：`verified`、`inferred` 或 `unconfirmed`。
- 变更文件清单；无变更时说明只读。
- 执行命令与结果摘要。
- 阻塞项、风险、回滚建议。
- 可纳入 LOOP round 的 evidence candidate。

主会话必须在收口前完成：

- 合并或拒收 agent 输出。
- 运行相关 validator、测试或等价门禁。
- 标注本轮 `substantive_round` 是否成立。
- 明确是否满足 Definition of Done。
- 明确不得自动升级 `accepted`、`integrated`、`production_ready`。

## 工具边界

| 工具 | 允许用途 | 禁止用途 |
| --- | --- | --- |
| Codex `multi_agent_v1` | 默认并行执行面；只读调查、受控小范围实现、并行验证 | 绕过 LOOP 门禁、跨边界写入、替代 Harness 裁决 |
| `globalcloud-collaborative-dev` | 团队角色与并行约束 | 不经 OpsX/Harness 直接宣告完成 |
| `gstack` | 专家评审、QA、安全、设计、发布前审查 | 作为主执行 runtime 或状态裁决层 |
| OMX | 隔离 L2/L3 smoke、hook 行为审计、CLI worker runtime 候选 | 默认 `--madmax`、直接写主仓、进入 L4/L5、生产写入 |
| Agents SDK + Codex MCP | 后续 supervisor/worker 平台化试点 | 未建 adapter 与 validator 前接管 LOOP 主线 |

## LOOP 映射

| LOOP 方向 | 多智能体执行要求 |
| --- | --- |
| `run` | 主会话生成任务包，最多 3 个并行 agent 执行独立子任务 |
| `stop` | 任一 agent 触发权限、生产写入、密钥、跨仓冲突、测试不可局部修复时暂停 |
| `verify` | 主会话复核 agent 结论并运行本地 validator / test / gate |
| `recover` | 保留成功 agent 输出；失败 agent 降级串行或重派一次 |
| `debug` | 输出阻塞原因、下一轮候选输入和需要人工确认的边界 |

## 当前判定

当前默认组合为：

```text
LOOP 主控：globalcloud-loop-orchestrator
团队规则：globalcloud-collaborative-dev
实际并行：Codex multi_agent_v1
专家审计：gstack
候选试点：OMX
长期平台：Agents SDK + Codex MCP
```

该组合为 `controlled + pilot + candidate` 混合状态。只有 Codex 内置子智能体与 GlobalCloud 协同开发规则可作为当前默认执行面；OMX 和 Agents SDK 仍需隔离试点与 evidence 后再评估升级。
