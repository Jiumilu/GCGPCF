---
doc_id: GPCF-DOC-05774FB8AD
title: GlobalCloud 绿色供应链体系 AI 服务模型
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, Studio]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系AI服务模型.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系AI服务模型.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系 AI 服务模型

日期：2026-06-07
状态：四流优化专项模型 v1
适用范围：KDS（知识主存）、Brain、XiaoC、Hermes/XGD、WAES、企业级知识主存层及各业务系统连接器。

## 1. 模型定位

AI 服务流消费数据流，受治理流约束，辅助业务流，但不替代业务流。AI 输出的建议、摘要、预警和复盘草案不是业务事实，不能直接写入 GFIS、GPC、PVAOS 或 Edge 的业务主账。

当前架构更新口径：AI 服务首先服务 `GPC + GFIS + WAES` 三条主线；宪法内容在 AI 模型中的具体体现，是证据分级、越权拦截、状态门禁和工具授权。知识架构上，AI 只能通过知识引擎层读取已发布知识，不应直接把 `LLM Wiki` 或 `Brain` 当成企业级知识真源。

## 2. 角色边界

| 组件 | 主责 | 不做什么 |
|---|---|---|
| Brain | SOP、知识、案例、复盘、RAG 可信源 | 不替代当前业务记录 |
| XiaoC | PromptTemplate、ModelConfig、MCP、Agent 模板和评估 | 不直接决定业务事实 |
| Hermes/XGD | AgentRun、工具编排、多端交互、后台任务 | 不绕过 WAES 授权和业务确认 |
| WAES | AI 授权、Agent 工具权限、越权拦截、建议结果评价 | 不审批具体业务事务 |
| 企业级知识主存层 | 知识版本、发布、归档和权限真源 | 不直接做 Agent 推理 |
| GFIS/GPC | 业务确认和业务事实 | 不接受未授权 AI 直接写主账 |

## 3. L1-L5 授权模型

| 等级 | 默认能力 | 授权对象 | 输出 | 禁止 |
|---|---|---|---|---|
| L1 查询/报表 | 自动执行 | 只读工具 | 摘要、日报草案 | 编造事实 |
| L2 预警 | 自动提醒 | 规则和指标工具 | 风险提醒 | 自动关闭异常 |
| L3 建议 | 需业务确认 | 建议和草案工具 | AISuggestion | 自动写业务事实 |
| L4 治理授权 | 需 GovernanceApproval | 工具授权、指标、状态、证据 | GovernanceApproval、AgentToolGrant | 当作业务批准 |
| L5 禁止接管 | 禁止 | 无 | 阻断记录 | 急停、安全联锁、设备保护、环保排放控制 |

## 4. 核心对象状态机

`AgentToolGrant`：

```text
draft -> submitted -> approved -> active -> suspended -> revoked -> expired
```

`AgentRun`：

```text
queued -> running -> waiting_governance -> waiting_business_reference -> completed
queued -> cancelled
running -> failed
waiting_governance -> rejected
waiting_business_reference -> rejected
```

`AISuggestion`：

```text
draft -> submitted -> needs_evidence -> governance_authorized -> business_action_referenced -> closed
submitted -> rejected -> closed
```

`PromptEvaluation` / `ModelEvaluation`：

```text
not_started -> running -> pass
not_started -> running -> fail
running -> blocked
pass -> superseded
```

`ModelAuthorizationGrant`：

```text
draft -> approved -> active -> suspended -> revoked -> expired
draft -> rejected
```

`ModelUsageRecord` / `ModelMeterSnapshot`：

```text
captured -> verified -> archived
captured -> disputed

calculated -> stale
calculated -> invalid
```

## 5. Agent 工具权限模型

| 字段 | 说明 |
|---|---|
| grantId | `ATG-*` |
| agentId | Hermes/XGD Agent 标识 |
| projectId | SupplyChainProject |
| toolId | MCP 或 connector tool |
| connectorId | 关联连接器 |
| allowedOperations | read / summarize / suggest / create_draft / request_governance |
| forbiddenOperations | write_business_fact / approve_transaction / close_exception / release_quality / confirm_pod |
| riskLevel | L1-L5 |
| evidenceRequired | 是否必须引用证据 |
| expiresAt | 到期时间 |
| governanceApprovalId | L4 授权引用 |

## 5.1 模型治理对象

| 对象 | 主责 | 用途 |
|---|---|---|
| `ModelCapabilityProfile` | XiaoC / WAES | 定义模型能力、上下文窗口、结构化输出、工具调用、推理等级和风险等级 |
| `ModelAuthorizationPolicy` | WAES | 定义模型允许使用范围、角色、场景、租户、密级和证据要求 |
| `ModelAuthorizationGrant` | WAES | 定义具体项目、Agent、场景或用户范围内的模型治理授权 |
| `ModelRouteDecision` | XiaoC / WAES | 记录模型选择、降级、切换、回退和人工覆盖决策 |
| `ModelUsageRecord` | XiaoC / Hermes / WAES | 记录单次模型调用的 token、延迟、费用、证据引用和治理结果 |
| `ModelMeterSnapshot` | WAES / Data Platform | 汇总项目、租户、Agent、模型、时间窗的调用量、费用、阻断率和成功率 |
| `ModelOverreachBlocked` | WAES | 记录模型因授权、密级、预算、场景或输出约束被阻断的审计事实 |

## 6. AI 建议进入业务系统的路径

```text
AI 读取证据和指标
-> 读取已发布知识版本对应的知识引擎索引
-> 生成 AISuggestion
-> WAES 检查 AgentToolGrant、riskLevel、evidenceRefs
-> 需要治理授权时生成 GovernanceApproval
-> 需要业务动作时进入 GFIS/GPC 内部流程
-> 主责系统确认后生成 BusinessApprovalReference
-> WAES 记录 AISuggestionOutcome
```

禁止路径：

```text
AISuggestion -> 直接写 GFIS/GPC 主账
AISuggestion -> 绕过 WAES 授权并发布 GFIS 或 GPC 业务事实事件
Agent -> 直接调用安全联锁或设备保护控制
Agent -> 直接改写知识主存层正式知识版本
```

## 6.1 模型治理路径

```text
全局模型目录 / 能力标签
-> 项目模型引用与用户模型偏好
-> WAES 检查 ModelAuthorizationPolicy / ModelAuthorizationGrant
-> XiaoC 形成 ModelRouteDecision
-> Hermes 发起模型调用
-> 记录 ModelUsageRecord
-> WAES / Data Platform 汇总 ModelMeterSnapshot
-> 若越权、超预算、超密级或超场景，生成 ModelOverreachBlocked
```

## 7. 质量评价指标

| 指标 | 口径 |
|---|---|
| suggestion_adoption_rate | 被业务采纳并形成业务确认引用的建议数 / 建议总数 |
| suggestion_rejection_rate | 被驳回建议数 / 建议总数 |
| evidence_completeness_rate | 带完整 evidenceRefs 和 sourceRecordId 的建议数 / 建议总数 |
| overreach_block_count | 越权调用被拦截次数 |
| prompt_regression_pass_rate | Prompt 回归通过数 / 回归总数 |
| model_fallback_rate | 模型失败或降级次数 / 调用总数 |
| model_authorization_hit_rate | 命中有效模型授权的调用数 / 调用总数 |
| model_meter_completeness_rate | 已记录 token、延迟、费用和 trace 的调用数 / 调用总数 |
| model_overreach_block_rate | 被模型治理拦截的调用数 / 高风险调用总数 |
| model_cost_accuracy_rate | 计量快照与底层调用记录一致的窗口数 / 计量窗口总数 |
| business_fact_violation_count | AI 试图直接写业务事实次数，目标为 0 |

## 8. 事件要求

AI 服务流必须使用以下事件：

```text
ai.tool_grant.changed
ai.agent_run.started
ai.agent_run.completed
ai.agent_run.failed
ai.prompt_evaluation.completed
ai.model_evaluation.completed
ai.model_authorization_grant.changed
ai.model_route_decision.recorded
ai.model_usage.recorded
ai.model_meter.snapshot_calculated
ai.suggestion.submitted
ai.suggestion.governance_authorized
ai.suggestion.outcome_recorded
ai.overreach.blocked
ai.model_overreach.blocked
```

AI 不得发布：

```text
gfis.work_order.released
gfis.quality_inspection.accepted
gfis.inventory_transaction.posted
gfis.factory_shipment.released
gpc.pod.signed
gpc.external_exception.closed
waes.governance_approval.approved
waes.evidence.verified
```

## 9. 验收场景

| 场景 | 对应验收 |
|---|---|
| AI 生成日报草案且每个结论有证据 | A7 |
| AI 建议被治理规则驳回且不写业务事实 | A9 |
| Agent 工具越权被拦截 | A13 |
| Prompt 回归评估通过后发布 | A14 / AI 扩展 |
| AI 建议被采纳后形成业务确认引用 | A3 / A5 / A6 |
| 模型授权变更被正确执行 | A21 |
| 模型路由/降级记录完整 | A22 |
| 模型使用计量可回指 | A23 |
| 模型越权或超预算调用被拦截 | A24 |
