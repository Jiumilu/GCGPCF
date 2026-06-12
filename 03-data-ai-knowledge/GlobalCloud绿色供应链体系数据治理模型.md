# GlobalCloud 绿色供应链体系数据治理模型

日期：2026-06-07  
状态：四流优化专项模型 v1  
适用范围：API Gateway、Connector Registry、Outbox/Inbox、Event Bus、Evidence Ledger、Metric、Trace、Data Platform、Edge、知识主存层、LLM Wiki、Brain。

## 1. 模型定位

数据流是业务流、治理流和 AI 服务流之间的证据底座。数据治理模型不共享业务数据库，不改变事实归属，只保证跨系统事实、证据、指标、追踪和 AI 上下文可信、可追踪、可重放、可隔离。

当前架构升级口径：横向底座统一收口为 `AI 与数据层`，其内部包含：

1. 业务事实层。
2. 资源仓库域。
3. 结构化数据库域。
4. 企业级知识主存域。
5. 知识引擎域。
6. AI 服务域。
7. 技术运行底座。

## 2. 数据治理原则

1. 主责系统唯一：GFIS、GPC-Native、PVAOS、WAES、Brain、Edge 各自负责自己的事实。
2. 事件是事实通知，不是远程命令。
3. EvidenceRecord 是证据事实，不是业务主账事实。
4. DeviceSignal 是遥测事实，不是业务主账事实。
5. AI 建议只能引用数据，不能把推断写成事实。
6. 任何重放必须幂等，不得制造重复业务事实。
7. 宪法内容在数据治理中的落点是：`source_refs`、证据等级、状态纪律、连接器注册和默认 canonical-only 的可信数据准入。
8. `LLM Wiki` 与 `Brain` 当前只作为知识引擎层候选，不作为企业级知识真源。

## 3. 数据层分层结构

### 3.1 AI 与数据层内部结构

| 层 | 作用 | 主要组件 |
|---|---|---|
| 业务事实层 | 产生真实业务事实 | PVAOS / GPC-Native / GFIS / Edge |
| 资源仓库域 | 以资源仓库组织业务资源，当前已定义十一池，后续可继续新增其它池 | 订单池、运力池、产能池、资金池、政策池、装备池、数据池、能源池、原料池、人才池、场景池 |
| 结构化数据库域 | 承载结构化运行数据和治理数据 | 业务主账库、治理审计库、指标时序库、知识元数据库、读模型库 |
| 知识主存域 | 承载企业级原文档、版本、审批、归档 | 企业级知识库 |
| 知识引擎域 | 切片、索引、图谱、RAG、回指 | LLM Wiki / Brain |
| AI 服务域 | Prompt、模型、Agent、交互与后台任务 | XiaoC / Hermes / XGD |
| 技术运行底座 | API、事件、证据、指标、追踪、重放 | API Gateway / Connector Registry / Event Bus / Evidence Ledger / Metric / Trace |

## 4. 数据流架构

```text
Source System
-> Connector
-> API Gateway
-> Outbox
-> Event Bus
-> Inbox
-> Evidence / Metric / Trace / Lake
-> WAES / AI / Report
```

知识链路补充：

```text
Knowledge Source
-> Knowledge Release
-> Knowledge Ingest Job
-> LLM Wiki / Brain
-> AI / WAES / Report
```

## 5. Schema 版本治理

| 对象 | 说明 |
|---|---|
| SchemaVersion | API 或事件 schema 的版本、兼容性、字段约束 |
| SchemaCompatibilityCheck | 发布前兼容性检查 |
| ApiContract | OpenAPI 或接口合同 |
| DomainEvent | 领域事件 envelope 和 payload |

兼容性等级：

| 等级 | 含义 | 治理要求 |
|---|---|---|
| backward_compatible | 新消费者可读旧事件 | 普通发布门 |
| forward_compatible | 旧消费者可容忍新字段 | 普通发布门 |
| breaking | 删除、改名、语义变化 | 必须 GovernanceApproval |
| deprecated | 已废弃但仍可读 | 设置退役日期 |

## 6. 数据质量规则

| 规则 | 检查点 |
|---|---|
| completeness | 必填字段不为空 |
| uniqueness | eventId、idempotencyKey 唯一 |
| timeliness | publishedAt 与 occurredAt 延迟在阈值内 |
| consistency | sourceSystem、sourceRecordId、payload 语义一致 |
| referential_integrity | evidenceRefs、traceId、correlationId 可回指 |
| tenant_isolation | 租户、链、厂、角色边界不越界 |

## 7. 死信与重放

死信来源：

1. schema 不兼容。
2. 目标系统不可用。
3. 幂等冲突。
4. 权限不足。
5. 数据质量失败。
6. 租户隔离违规。

死信处理状态：

```text
created -> triaged -> rework_requested -> replay_requested -> replayed -> closed
created -> discarded -> closed
```

重放要求：

1. 高风险事件重放必须有 `ReplayRequest` 和治理确认。
2. 重放必须使用原 `idempotencyKey` 或重放专用幂等键。
3. 重放结果必须写入 `ReplayRun`。
4. 重放不得直接生成业务审批结论。

## 8. 指标与血缘

`MetricDefinition` 必须绑定：

1. 指标口径。
2. 生效版本。
3. 来源对象和事件。
4. 计算窗口。
5. 租户和链厂边界。
6. 重算策略。
7. `LineageRecord`。

指标快照状态：

```text
calculated -> valid
calculated -> stale
calculated -> invalid
invalid -> recalculated
```

## 9. 证据治理

EvidenceRecord 必须包含：

| 字段 | 说明 |
|---|---|
| evidenceId | `EVD-*` |
| evidenceType | business_record / event / log / screenshot / receipt / business_approval_reference / governance_approval |
| sourceSystem | 来源系统 |
| sourceRecordId | 来源记录 |
| traceId | 追踪链 |
| correlationId | 业务链路 |
| capturedAt | 捕获时间 |
| verificationStatus | captured / verified / rejected / archived |
| retentionPolicy | 保留策略 |

证据确证只说明证据可用，不说明业务事务由 WAES 审批通过。

## 10. 结构化数据库域治理

### 10.1 数据库分工

建议至少分为：

1. 业务主账库：由 `PVAOS / GPC-Native / GFIS` 各自独立维护。
2. 治理审计库：由 `WAES` 维护规则、证据、状态、授权和验收数据。
3. 指标时序库：用于指标快照、时序数据、风险与趋势分析。
4. 资源仓库库：用于资源对象索引、映射和聚合关系。
5. 知识元数据库：用于文档、版本、发布、权限、引用元数据。
6. 读模型库：用于查询、控制塔视图和跨系统读优化。

### 10.2 原则

1. 不共享业务主账表。
2. 通过事件、API、证据引用和读模型协同。
3. 跨域查询必须保留权限和审计记录。

## 11. 知识主存层与知识引擎层治理

### 11.1 知识主存层要求

必须支持：

1. `KnowledgeDocument`
2. `KnowledgeVersion`
3. `KnowledgeRelease`
4. `KnowledgeAccessPolicy`
5. `KnowledgeRetentionPolicy`
6. `KnowledgeAuditLog`

### 11.2 知识引擎层要求

必须支持：

1. ingest 来源绑定。
2. 文档版本绑定。
3. 切片回指。
4. 引用结果带 `source_refs`。
5. 失效知识拦截。
6. 项目、空间、密级隔离。

### 11.3 禁止事项

1. 禁止知识引擎直接修改主存层正式版本。
2. 禁止 Agent 自动把摘要、复盘或建议写回为正式知识。
3. 禁止未发布文档默认进入全量 RAG。

## 12. 租户、多链、多厂隔离

隔离维度：

1. tenantId。
2. supplyChainProjectId。
3. chainId。
4. factoryId。
5. organizationId。
6. roleId。
7. connectorId。
8. agentId。

任何跨边界查询必须记录：

1. 调用者。
2. 授权来源。
3. 查询目的。
4. 返回字段范围。
5. evidenceRefs。
6. 是否被脱敏。

## 13. 数据保留策略

| 数据类型 | 建议保留 | 说明 |
|---|---:|---|
| 业务事实事件 | 3 年以上 | 按项目和合规要求调整 |
| EvidenceRecord | 3-7 年 | 验收、审计和争议处理依据 |
| AgentRun 日志 | 180-365 天 | 可脱敏归档 |
| PromptEvaluation | 1 年以上 | 用于回归和治理 |
| Edge 原始遥测 | 7-90 天 | 高频数据可聚合后归档 |
| MetricSnapshot | 1-3 年 | 经营分析和趋势 |
| DeadLetterRecord | 至少 1 年 | 审计和问题复盘 |
| KnowledgeAuditLog | 1-3 年 | 知识发布、引用、导出和 AI 消费审计 |

## 14. 验收要求

| 验收 | 对应场景 |
|---|---|
| schema 版本发布和兼容性检查 | A10 / A11 |
| DLQ 生成、处理和重放 | A12 |
| 指标口径变更和重算 | A17 |
| 多租户数据隔离 | A18 |
| Edge 缓存补传和去重 | A16 |
| 知识发布与 ingest 验证 | 知识底座扩展 A19 |
| 知识引用回指和权限隔离 | 知识底座扩展 A20 |
