---
doc_id: GPCF-DOC-664403C419
title: GlobalCloud 绿色供应链体系 SOP 模板库
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, Studio]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系SOP模板库.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系SOP模板库.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系 SOP 模板库

日期：2026-06-07
状态：四流优化专项模板 v1
适用范围：供应链项目初始化、试运营、正式运营和持续治理监控。

## 1. 模板定位

SOP 在本体系中不是静态文档，而是可配置、可版本化、可执行、可留证、可复盘、可验收的运行对象。SOP 模板必须同时覆盖治理流、业务流、数据流和 AI 服务流。

基本边界：

1. SOP 可以定义业务确认点，但 WAES 只承办治理确认，不承办具体事务审批。
2. SOP 可以允许 AI 生成建议、摘要、预警和复盘草案，但不能允许 AI 直接写业务事实。
3. SOP 完成必须有执行记录、事件、证据、回执和必要的业务确认引用。
4. 配置完成不等于 SOP 完成；发布通过也不等于 SOP 完成。
5. 平台型 SOP 默认以 `GPC` 为主责系统；宪法要求通过证据要求、治理确认点和状态升级门进入 SOP 模板，而不是直接替代业务步骤。

## 2. 标准 SOPDefinition 字段

| 字段 | 说明 |
|---|---|
| sopId | `SOP-*` |
| sopName | SOP 名称 |
| domain | governance / collaboration / factory_execution / data / ai_service |
| applicableTemplate | 一链一厂 / 一链多厂 / 多链多厂 / 区域平台 |
| ownerSystem | GFIS / GPC / PVAOS / WAES / Edge / Brain / XiaoC / Hermes / XGD |
| ownerRole | 主责角色 |
| governanceOwner | WAES 或 Harness 治理负责人 |
| inputObjects | 输入对象 |
| outputObjects | 输出对象 |
| triggerEvents | 触发事件 |
| businessConfirmationPoints | 业务确认点，仅由主责业务系统承办 |
| governanceCheckpoints | WAES/Harness 治理确认点 |
| evidenceRequirements | 来源记录、事件、日志、截图、回执、BusinessApprovalReference |
| aiAllowedActions | 查询、摘要、预警、建议、复盘草案 |
| aiForbiddenActions | 写业务事实、审批事务、关闭异常、质量放行、库存调整、签收确认 |
| connectorRequirements | 依赖连接器和合同版本 |
| dataQualityRules | 数据质量要求 |
| rollbackPlan | 回滚和补偿策略 |
| acceptanceScenario | 对应 A1-A18 |

## 3. SOPVersion 状态机

```text
draft -> review -> governance_authorized -> published -> frozen -> retired
published -> rollback_pending -> published
published -> superseded -> retired
```

状态说明：

| 状态 | 含义 |
|---|---|
| draft | 草案，不可执行 |
| review | 业务和治理评审中 |
| governance_authorized | WAES/Harness 治理授权通过 |
| published | 可用于试运营或正式运营 |
| frozen | 暂停修改，用于审计或问题排查 |
| rollback_pending | 回滚待确认 |
| superseded | 已被新版本替代 |
| retired | 退役 |

## 4. SOPExecution 状态机

```text
not_started -> running -> waiting_business_confirmation -> waiting_governance_confirmation -> completed
running -> blocked
waiting_business_confirmation -> rejected
waiting_governance_confirmation -> rejected
completed -> reviewed -> closed
```

完成要求：

1. 每个关键步骤有来源系统和来源记录。
2. 每个业务确认点有 `BusinessApprovalReference`。
3. 每个治理确认点有 `GovernanceApproval` 或 `EvidenceVerification`。
4. 每个 AI 建议有 `AISuggestion` 和 `AISuggestionOutcome`。
5. 每个异常有 `ExceptionCase` 或 `ExternalException`。

## 5. P0 SOP 模板

### 5.1 订单到交付 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | GPC / GFIS |
| 触发事件 | `gpc.platform_order.received` |
| 输入对象 | PlatformOrder、Customer、Material、Factory、ConnectorBinding |
| 输出对象 | FactoryOrder、WorkOrder、QualityInspection、FactoryShipmentRelease、Shipment、ProofOfDelivery、EvidenceRecord |
| 业务确认点 | 工厂订单确认、质量放行、发货出库、客户签收 |
| WAES 治理点 | 证据链完整性、AI 授权、阶段验收 |
| AI 可做 | 交付风险摘要、缺料预警、日报草案 |
| AI 禁止 | 自动承诺交期、自动发货、自动签收 |
| 验收场景 | A1 |

### 5.2 批次追溯 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | GFIS |
| 触发事件 | `gfis.lot.status_changed` |
| 输入对象 | ASN、MaterialLot、QualityInspection、WorkOrder、FactoryShipmentRelease、ProofOfDelivery |
| 输出对象 | QualityTraceScope、TraceSegment、EvidenceRecord |
| 业务确认点 | 来料检验、成品质检、批次隔离或放行 |
| WAES 治理点 | 追溯证据确证、断点补证 |
| AI 可做 | 追溯路径摘要、异常归因草案 |
| AI 禁止 | 自动改变批次质量状态 |
| 验收场景 | A2 |

### 5.3 缺料异常 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | GFIS |
| 触发事件 | `gfis.kitting_check.shortage_detected` |
| 输入对象 | WorkOrder、BOM、InventoryTransaction、LineSideStock |
| 输出对象 | AISuggestion、BusinessApprovalReference、LogisticsTask、EvidenceRecord |
| 业务确认点 | 补料任务创建、配送确认 |
| WAES 治理点 | AI 建议未越权、证据完整 |
| AI 可做 | 补料建议、替代方案、影响分析 |
| AI 禁止 | 自动创建或关闭补料任务 |
| 验收场景 | A3 |

### 5.4 质量异常 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | GFIS |
| 触发事件 | `gfis.quality_inspection.rejected` |
| 输入对象 | QualityInspection、MaterialLot、WorkOrder、Equipment |
| 输出对象 | ExceptionCase、CAPA 草案、KnowledgeEntry、EvidenceRecord |
| 业务确认点 | 隔离、返工、报废、放行、CAPA 关闭 |
| WAES 治理点 | 复盘证据、AI 越权检查 |
| AI 可做 | CAPA 草案、原因分析、相似案例 |
| AI 禁止 | 自动质量放行、自动报废 |
| 验收场景 | A5 |

### 5.5 运输签收异常 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | GPC |
| 触发事件 | `gpc.pod.disputed` 或 `gpc.shipment.delayed` |
| 输入对象 | Shipment、TransitCheckpoint、ProofOfDelivery、ExternalException |
| 输出对象 | BusinessApprovalReference、EvidenceRecord、AISuggestionOutcome |
| 业务确认点 | 签收争议处理、数量差异确认、交期承诺变更 |
| WAES 治理点 | 证据完整性、客户承诺风险监控 |
| AI 可做 | 异常原因摘要、处理建议、客户沟通草案 |
| AI 禁止 | 自动签收、自动承诺交期 |
| 验收场景 | A6 |

### 5.6 AI 越权拦截 SOP

| 项 | 内容 |
|---|---|
| 主责系统 | WAES |
| 触发事件 | Agent 工具调用请求 |
| 输入对象 | AgentToolGrant、AgentRun、AgentToolPolicy |
| 输出对象 | AIOverreachBlocked、EvidenceRecord |
| 业务确认点 | 无，业务主账不得变化 |
| WAES 治理点 | 越权判定、工具权限冻结或调整 |
| AI 可做 | 报告失败原因、请求补证 |
| AI 禁止 | 继续重试禁止动作 |
| 验收场景 | A13 |

## 6. P1 SOP 模板

| SOP | 主责系统 | 重点 |
|---|---|---|
| 线边配送 SOP | GFIS | LineSideDelivery、LogisticsTask、线边确认 |
| 设备异常 SOP | GFIS | Equipment、MaintenanceOrder、停机影响复盘 |
| 连接器降级恢复 SOP | WAES / Connector Registry | ConnectorLifecycleRecord、DLQ、Replay |
| SOP 版本回滚 SOP | WAES / Brain | SOPVersion、ReleaseGate、影响范围 |
| 一链多厂分单 SOP | GPC / GFIS | FactoryAllocation、CapacityCommitment |
| 指标口径变更 SOP | WAES | MetricDefinition、LineageRecord、重算 |

## 7. P2 SOP 模板

| SOP | 主责系统 | 重点 |
|---|---|---|
| 能源异常 SOP | GFIS / WAES | 能耗采集、指标、异常复盘 |
| 安环隐患 SOP | GFIS / WAES | HSE 事件、作业票、AI 禁止接管 |
| 多链多厂协同 SOP | GPC / WAES | 跨链隔离、经营分析 |
| 区域平台监管披露 SOP | PVAOS / WAES | 对外披露证据和指标口径 |

## 8. SOP 验收口径

| 状态 | 判定 |
|---|---|
| `not_started` | 只有模板名，没有对象、事件和责任人 |
| `in_progress` | 已配置但未发布或未验证 |
| `partial` | 有局部执行证据，但关键确认点缺失 |
| `blocked` | 连接器、数据、权限或证据缺失 |
| `ready_for_human_acceptance` | 最小闭环通过，待人工验收 |
| `accepted` | 人工确认通过 |
| `complete` | 真实运行证据、业务确认、治理确认和复盘全部归档 |
