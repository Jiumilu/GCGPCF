---
doc_id: GPCF-DOC-E4DDF33CF8
title: GlobalCloud 绿色供应链体系连接器合同
project: KDS
related_projects: [KDS, GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系连接器合同.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系连接器合同.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系连接器合同

日期：2026-06-10
版本：连接器合同 v2（口径修正稿）
基线引用：[GlobalCloud绿色供应链体系总架构.md](/Users/lujunxiang/Projects/GlobalCloud%20GPCF/GlobalCloud绿色供应链体系总架构.md)
适用范围：GPC、GFIS、WAES、PVAOS、Edge、Brain、XiaoC、Hermes/XGD、Odoo back-office connector 候选。

## 0. 口径修正（与 [总架构] 一致）

1. 体系只承认 **5 个根连接器**：`CON-GPC-GFIS-001` / `CON-GPC-WAES-001` / `CON-GFIS-WAES-001` / `CON-EDGE-GFIS-001` / `CON-EDGE-WAES-001`，其他连接器必须挂接到这 5 个根连接器下。
2. **`CON-GFIS-WAES-001` 不废弃**，作为 GFIS ↔ WAES 工厂治理 / 异常 / 审计 / 证据直连连接器保留。
3. 连接器合同是数据流进入治理流、业务流和 AI 服务流的边界文件，不定义业务主账，不承办具体事务审批。
4. 连接器不得改变主责系统事实归属；不得绕过 GFIS / GPC / PVAOS 的业务确认流程；不得绕过 WAES 改写治理状态。
5. WAES 可以治理连接器上线、降级、恢复、下线和回滚，但不通过连接器审批具体业务事务。
6. AI Agent 只能使用 WAES 授权的连接器工具，且必须受 `AgentToolGrant` 和 `AgentToolPolicy` 约束。
7. 连接器失败不得被解释为业务完成；必须进入 retry、dead letter、replay 或 blocked 状态。
8. Edge 不得在自身数据库落地业务主账事实；任何"绕过 GFIS 写业务主账"的连接器在体系中不得成立。

## 1. 合同定位

连接器合同是数据流进入治理流、业务流和 AI 服务流的边界文件。它不定义业务主账，不承办具体事务审批，只定义系统之间如何安全、可靠、可审计地交换 API、事件、证据和业务确认引用。

核心原则：

1. 连接器只连接主责系统，不改变主责系统事实归属。
2. 连接器不能绕过 GFIS / GPC / PVAOS 的业务确认流程。
3. WAES 可以治理连接器上线、降级、恢复、下线和回滚，但不通过连接器审批具体业务事务。
4. AI Agent 只能使用 WAES 授权的连接器工具，且必须受 `AgentToolGrant` 和 `AgentToolPolicy` 约束。
5. 连接器失败不得被解释为业务完成；必须进入 retry、dead letter、replay 或 blocked 状态。
6. 绿色供应链公共服务平台主线连接器优先围绕 `GPC` 展开，治理内容在连接器层表现为注册、权限、证据、版本、状态和治理门禁。

## 2. 体系只承认的 5 个根连接器

| 编号 | 名称 | 两端 | 默认等级 | 主责 | 默认写权限 | 备注 |
|---|---|---|---|---|---|---|
| CON-GPC-GFIS-001 | GPC 与 GFIS 的业务协同连接器 | GPC ↔ GFIS | C1/C2 | GPC / GFIS | 业务主账前置接口；不绕过业务确认 | 平台订单分发、ASN/预约、运输回传、发货回执、工厂事实回流 |
| CON-GPC-WAES-001 | GPC 与 WAES 的平台证据 / 治理状态连接器 | GPC ↔ WAES | C1/C4 | GPC / WAES | 仅证据与治理引用，不写业务主账 | 平台事实证据、跨厂异常、状态升级请求、阶段验收引用 |
| CON-GFIS-WAES-001 | GFIS 与 WAES 的工厂治理 / 异常 / 审计 / 证据直连连接器 | GFIS ↔ WAES | C1/C4 | GFIS / WAES | 仅证据与治理引用，不写业务主账 | 工厂执行证据、工厂异常、审计追踪、证据确证；不废弃 |
| CON-EDGE-GFIS-001 | Edge 与 GFIS 的现场采集连接器 | Edge → GFIS | C1 | Edge / GFIS | Edge 不在自身数据库落地业务主账 | 设备信号、报警、缓存补传、回执；优先服务 GFIS |
| CON-EDGE-WAES-001 | Edge 与 WAES 的异常 / 安全 / 审计证据连接器 | Edge → WAES | C1/C4 | Edge / WAES | 可选；不替代 CON-EDGE-GFIS-001 | 边缘异常、节点安全、审计证据；存在时不得绕过 GFIS 写业务主账 |

任何其他跨系统连接器（如 `PVAOS -> GPC` 的运营上下文同步、`Brain -> WAES` 的知识准入等）必须挂接到这 5 个根连接器下，或在新版本基线中通过 [总架构] 补充新根连接器编号。

## 3. 连接器分级

| 等级 | 类型 | 说明 | 默认写权限 |
|---|---|---|---|
| C0 | 只读证据连接器 | 拉取状态、记录、截图、日志、回执和证据 | 无 |
| C1 | 事件发布连接器 | 从主责系统发布事实事件 | 仅主责系统 outbox |
| C2 | 业务草案连接器 | 允许创建建议、草案或待确认记录 | 需业务系统内部确认 |
| C3 | 业务写入连接器 | 允许写入业务系统主账前置接口 | 默认禁用，需专项治理 |
| C4 | 治理写入连接器 | 写 WAES 治理对象、证据和状态 | 需 `GovernanceApproval` |
| C5 | 禁止连接器 | 涉及安全联锁、急停、设备保护、环保排放控制 | 禁止 AI 使用 |

一期默认只允许 C0、C1、C2、C4。C3 必须逐接口审批，C5 禁止。

## 4. 标准合同字段

| 字段 | 必填 | 说明 |
|---|---|---|
| connectorId | 是 | `CON-*`；根连接器使用 5 个保留编号之一 |
| connectorName | 是 | 连接器名称 |
| rootConnectorId | 是 | 所属根连接器编号（CON-GPC-GFIS-001 / CON-GPC-WAES-001 / CON-GFIS-WAES-001 / CON-EDGE-GFIS-001 / CON-EDGE-WAES-001） |
| sourceSystem | 是 | PVAOS / GPC / GFIS / Edge / WAES / Brain / XiaoC / Hermes / XGD |
| targetSystem | 是 | 目标系统 |
| owner | 是 | 业务负责人和技术负责人 |
| environment | 是 | dev / test / demo / staging / production |
| connectorLevel | 是 | C0-C5 |
| allowedObjects | 是 | 允许访问对象；只能属于本根连接器下声明的允许对象域 |
| forbiddenObjects | 是 | 禁止访问对象；任何"非主账系统可写主账"对象都应进入 forbiddenObjects |
| allowedOperations | 是 | read / publish_event / create_draft / request_action / write_governance |
| authType | 是 | api_key / oauth / mTLS / service_account / local_token |
| secretRef | 是 | 密钥引用，不写明文 |
| schemaVersions | 是 | API 和事件 schema 版本 |
| eventTypes | 是 | 发布或订阅事件 |
| idempotencyPolicy | 是 | 幂等键规则 |
| retryPolicy | 是 | 重试次数、退避、超时 |
| deadLetterPolicy | 是 | 死信生成、责任人、处理 SLA |
| replayPolicy | 是 | 重放窗口、审批要求、幂等检查 |
| evidencePolicy | 是 | sourceRecordId、traceId、evidenceRefs 要求 |
| dataQualityRules | 是 | 完整性、唯一性、时效性、一致性规则 |
| retentionPolicy | 是 | 日志、事件、证据保留 |
| tenantBoundary | 是 | 租户、链、厂、角色隔离 |
| healthCheck | 是 | ping、schema、事件延迟、错误率 |
| lifecycleState | 是 | draft / active / degraded / disabled / retired |

## 5. 标准状态机

```text
draft -> validation_pending -> active -> degraded -> recovered -> active
draft -> validation_failed -> blocked
active -> disabled -> retired
active -> rollback_pending -> active
```

状态含义：

| 状态 | 含义 | 是否允许承载生产事实 |
|---|---|---|
| draft | 已定义，未验证 | 否 |
| validation_pending | 正在验证连接性、schema、权限和证据回指 | 否 |
| active | 验证通过并生效 | 是 |
| degraded | 可用性、延迟、错误率或 schema 异常 | 受限 |
| recovered | 从 degraded 恢复，等待证据确认 | 受限 |
| disabled | 人工或治理停用 | 否 |
| retired | 退役，不再使用 | 否 |
| blocked | 验证失败或存在安全风险 | 否 |

## 6. 治理确认边界

| 动作 | 是否需要 GovernanceApproval | 说明 |
|---|---:|---|
| 连接器首次上线 | 是 | 必须有验证证据 |
| schema 破坏性变更 | 是 | 必须有兼容性检查和回滚计划 |
| C2 草案写入启用 | 是 | 只能写草案，不写业务主账 |
| C3 业务写入启用 | 是，且默认 P0 风险 | 需专项确认和业务系统内部审批链 |
| 连接器降级 | 是 | 记录影响范围和临时策略 |
| 连接器恢复 | 是 | 需要补偿、重放或证据恢复记录 |
| 死信重放 | 是 | 防止重复业务事实 |
| 密钥轮换 | 是 | 不记录明文密钥 |
| 连接器退役 | 是 | 需要替代路径和历史证据保留 |

不需要 WAES 审批的事项：

1. GFIS 内部工单审批。
2. GFIS 内部质量放行。
3. GFIS 内部库存调整。
4. GFIS 发货出库确认。
5. GPC 客户签收和 POD 争议处理。
6. GPC 客户交付承诺变更。

这些事项只能通过 `BusinessApprovalReference` 引用。

## 7. 5 个根连接器模板

### 7.1 CON-GPC-GFIS-001（GPC ↔ GFIS 业务协同连接器）

```yaml
connectorId: CON-GPC-GFIS-001
connectorName: GPC to GFIS Business Collaboration Connector
rootConnectorId: CON-GPC-GFIS-001
sourceSystem: GPC
targetSystem: GFIS
owner:
  business: platform_collaboration
  technical: integration_team
environment: demo
connectorLevel: C1/C2
allowedObjects:
  - PlatformOrder
  - OrderMapping
  - ASN
  - Appointment
  - Shipment
  - ProofOfDelivery
  - FactoryOrder
  - QualityInspection
  - MaterialLot
  - FactoryShipmentRelease
  - CapacityCommitment
  - CapacitySnapshot
  - InventoryVisibilitySnapshot
forbiddenObjects:
  - payroll
  - finance_payment
  - safety_interlock_control
allowedOperations:
  - read
  - publish_event
  - create_draft
authType: service_account
secretRef: secret://connector/gpc-gfis/demo
schemaVersions:
  api: API-GPC-GFIS-v1
  events: EVT-GPC-v1
eventTypes:
  publish:
    - gpc.platform_order.dispatched_to_factory
    - gpc.asn.created
    - gpc.appointment.confirmed
    - gpc.shipment.created
    - gpc.shipment.loaded
    - gpc.pod.signed
  subscribe:
    - gfis.factory_order.accepted
    - gfis.quality_inspection.accepted
    - gfis.quality_inspection.rejected
    - gfis.lot.status_changed
    - gfis.factory_shipment.released
idempotencyPolicy: sourceSystem:sourceRecordId:eventType:eventVersion
retryPolicy:
  maxAttempts: 5
  backoff: exponential
  timeoutSeconds: 30
deadLetterPolicy:
  enabled: true
  owner: integration_team
  slaHours: 4
replayPolicy:
  replayWindowDays: 7
  requiresGovernanceApproval: true
evidencePolicy:
  requiresSourceRecordId: true
  requiresTraceId: true
  requiresEvidenceRefs: true
dataQualityRules:
  - sourceRecordId_not_null
  - traceId_not_null
  - occurredAt_before_publishedAt
retentionPolicy: RET-EVENT-365D
tenantBoundary: TDB-DEMO-001
healthCheck:
  pingSeconds: 60
  maxErrorRate: 0.01
  maxEventDelaySeconds: 120
lifecycleState: draft
```

### 7.2 CON-GPC-WAES-001（GPC ↔ WAES 平台证据 / 治理状态连接器）

```yaml
connectorId: CON-GPC-WAES-001
connectorName: GPC to WAES Platform Evidence and Governance State Connector
rootConnectorId: CON-GPC-WAES-001
sourceSystem: GPC
targetSystem: WAES
owner:
  business: platform_governance
  technical: integration_team
environment: demo
connectorLevel: C1/C4
allowedObjects:
  - PlatformOrder
  - OrderMapping
  - ASN
  - Appointment
  - Shipment
  - ProofOfDelivery
  - ExternalException
  - CrossFactoryException
  - EvidenceRecord
  - GovernanceApproval
  - GovernanceRule
  - StatusTransitionRequest
forbiddenObjects:
  - WorkOrder
  - QualityInspection
  - InventoryTransaction
  - FactoryShipmentRelease
allowedOperations:
  - read
  - publish_event
  - write_governance
authType: service_account
secretRef: secret://connector/gpc-waes/demo
schemaVersions:
  api: API-GPC-WAES-v1
  events: EVT-WAES-v1
eventTypes:
  publish:
    - gpc.platform_order.received
    - gpc.shipment.in_transit
    - gpc.shipment.delayed
    - gpc.pod.disputed
    - gpc.external_exception.raised
    - gpc.external_exception.closed
    - gpc.cross_factory_exception.raised
    - gpc.cross_factory_exception.closed
  subscribe:
    - waes.governance_rule.activated
    - waes.governance_rule.retired
    - waes.policy_assignment.changed
    - waes.evidence.verified
    - waes.release_gate.passed
    - waes.release_gate.failed
idempotencyPolicy: sourceSystem:sourceRecordId:eventType:eventVersion
retryPolicy:
  maxAttempts: 5
  backoff: exponential
  timeoutSeconds: 30
deadLetterPolicy:
  enabled: true
  owner: integration_team
  slaHours: 4
replayPolicy:
  replayWindowDays: 7
  requiresGovernanceApproval: true
evidencePolicy:
  requiresSourceRecordId: true
  requiresTraceId: true
  requiresEvidenceRefs: true
dataQualityRules:
  - sourceRecordId_not_null
  - traceId_not_null
  - occurredAt_before_publishedAt
retentionPolicy: RET-EVENT-365D
tenantBoundary: TDB-DEMO-001
healthCheck:
  pingSeconds: 60
  maxErrorRate: 0.01
  maxEventDelaySeconds: 120
lifecycleState: draft
```

### 7.3 CON-GFIS-WAES-001（GFIS ↔ WAES 工厂治理 / 异常 / 审计 / 证据直连连接器，不废弃）

```yaml
connectorId: CON-GFIS-WAES-001
connectorName: GFIS to WAES Factory Governance / Exception / Audit / Evidence Direct Connector
rootConnectorId: CON-GFIS-WAES-001
sourceSystem: GFIS
targetSystem: WAES
owner:
  business: factory_operations
  technical: integration_team
environment: demo
connectorLevel: C1/C4
allowedObjects:
  - FactoryOrder
  - WorkOrder
  - QualityInspection
  - InventoryTransaction
  - MaterialLot
  - FactoryShipmentRelease
  - KittingCheck
  - LogisticsTask
  - LineSideDelivery
  - MaintenanceOrder
  - Equipment
  - CapacityCommitment
  - CapacitySnapshot
  - QualityTraceScope
  - EvidenceRecord
  - GovernanceApproval
  - GovernanceRule
  - StatusTransitionRequest
forbiddenObjects:
  - payroll
  - finance_payment
  - safety_interlock_control
  - PlatformOrder
  - ProofOfDelivery
allowedOperations:
  - read
  - publish_event
  - write_governance
authType: service_account
secretRef: secret://connector/gfis-waes/demo
schemaVersions:
  api: API-GFIS-WAES-v1
  events: EVT-GFIS-v1
eventTypes:
  publish:
    - gfis.factory_order.accepted
    - gfis.work_order.released
    - gfis.kitting_check.completed
    - gfis.kitting_check.shortage_detected
    - gfis.logistics_task.created
    - gfis.logistics_task.completed
    - gfis.production.reported
    - gfis.quality_inspection.accepted
    - gfis.quality_inspection.rejected
    - gfis.inventory_transaction.posted
    - gfis.lot.status_changed
    - gfis.factory_shipment.released
    - gfis.equipment.down
    - gfis.maintenance_order.closed
    - gfis.capacity_commitment.published
    - gfis.capacity_snapshot.published
    - gfis.inventory_visibility.snapshot_published
    - gfis.quality_trace_scope.created
  subscribe:
    - waes.governance_rule.activated
    - waes.governance_rule.retired
    - waes.policy_assignment.changed
    - waes.evidence.verified
    - waes.release_gate.passed
    - waes.release_gate.failed
idempotencyPolicy: sourceSystem:sourceRecordId:eventType:eventVersion
retryPolicy:
  maxAttempts: 5
  backoff: exponential
  timeoutSeconds: 30
deadLetterPolicy:
  enabled: true
  owner: integration_team
  slaHours: 4
replayPolicy:
  replayWindowDays: 7
  requiresGovernanceApproval: true
evidencePolicy:
  requiresSourceRecordId: true
  requiresTraceId: true
  requiresEvidenceRefs: true
dataQualityRules:
  - sourceRecordId_not_null
  - traceId_not_null
  - occurredAt_before_publishedAt
retentionPolicy: RET-EVENT-365D
tenantBoundary: TDB-DEMO-001
healthCheck:
  pingSeconds: 60
  maxErrorRate: 0.01
  maxEventDelaySeconds: 120
lifecycleState: draft
```

### 7.4 CON-EDGE-GFIS-001（Edge → GFIS 现场采集连接器）

```yaml
connectorId: CON-EDGE-GFIS-001
connectorName: Edge to GFIS Field Collection Connector
rootConnectorId: CON-EDGE-GFIS-001
sourceSystem: Edge
targetSystem: GFIS
owner:
  business: factory_operations
  technical: integration_team
environment: demo
connectorLevel: C1
allowedObjects:
  - EdgeNode
  - DeviceSignal
  - Equipment
forbiddenObjects:
  - WorkOrder
  - QualityInspection
  - InventoryTransaction
  - FactoryShipmentRelease
  - PlatformOrder
  - ProofOfDelivery
allowedOperations:
  - read
  - publish_event
authType: service_account
secretRef: secret://connector/edge-gfis/demo
schemaVersions:
  api: API-EDGE-GFIS-v1
  events: EVT-EDGE-v1
eventTypes:
  publish:
    - edge.node.online
    - edge.node.offline
    - edge.device_signal.received
    - edge.buffer.replayed
  subscribe:
    - edge.buffer_policy.changed
idempotencyPolicy: sourceSystem:sourceRecordId:eventType:eventVersion
retryPolicy:
  maxAttempts: 5
  backoff: exponential
  timeoutSeconds: 30
deadLetterPolicy:
  enabled: true
  owner: integration_team
  slaHours: 4
replayPolicy:
  replayWindowDays: 7
  requiresGovernanceApproval: true
evidencePolicy:
  requiresSourceRecordId: true
  requiresTraceId: true
  requiresEvidenceRefs: true
dataQualityRules:
  - sourceRecordId_not_null
  - traceId_not_null
  - occurredAt_before_publishedAt
retentionPolicy: RET-EVENT-365D
tenantBoundary: TDB-DEMO-001
healthCheck:
  pingSeconds: 60
  maxErrorRate: 0.01
  maxEventDelaySeconds: 120
lifecycleState: draft
```

### 7.5 CON-EDGE-WAES-001（Edge → WAES 异常 / 安全 / 审计证据连接器，可选）

```yaml
connectorId: CON-EDGE-WAES-001
connectorName: Edge to WAES Exception / Security / Audit Evidence Connector
rootConnectorId: CON-EDGE-WAES-001
sourceSystem: Edge
targetSystem: WAES
owner:
  business: edge_governance
  technical: integration_team
environment: demo
connectorLevel: C1/C4
allowedObjects:
  - EdgeNode
  - DeviceSignal
  - EvidenceRecord
  - GovernanceRule
forbiddenObjects:
  - WorkOrder
  - QualityInspection
  - InventoryTransaction
  - FactoryShipmentRelease
  - PlatformOrder
  - ProofOfDelivery
allowedOperations:
  - read
  - publish_event
  - write_governance
authType: service_account
secretRef: secret://connector/edge-waes/demo
schemaVersions:
  api: API-EDGE-WAES-v1
  events: EVT-EDGE-WAES-v1
eventTypes:
  publish:
    - edge.node.offline
    - edge.device_alarm.raised
    - edge.buffer.replayed
  subscribe:
    - waes.governance_rule.activated
    - waes.policy_assignment.changed
    - waes.evidence.verified
idempotencyPolicy: sourceSystem:sourceRecordId:eventType:eventVersion
retryPolicy:
  maxAttempts: 5
  backoff: exponential
  timeoutSeconds: 30
deadLetterPolicy:
  enabled: true
  owner: integration_team
  slaHours: 4
replayPolicy:
  replayWindowDays: 7
  requiresGovernanceApproval: true
evidencePolicy:
  requiresSourceRecordId: true
  requiresTraceId: true
  requiresEvidenceRefs: true
dataQualityRules:
  - sourceRecordId_not_null
  - traceId_not_null
  - occurredAt_before_publishedAt
retentionPolicy: RET-EVENT-365D
tenantBoundary: TDB-DEMO-001
healthCheck:
  pingSeconds: 60
  maxErrorRate: 0.01
  maxEventDelaySeconds: 120
lifecycleState: draft
```

## 8. 标准连接器清单

| 连接器 | 等级 | 主责 | 根连接器 | 一期目标 |
|---|---|---|---|---|
| PVAOS -> GPC 上下文同步 | C1/C2 | PVAOS / GPC | CON-GPC-WAES-001（治理引用）或挂接到 CON-GPC-GFIS-001 治理上下文 | 组织、项目、伙伴、门户事件 |
| GPC -> WAES | C1/C4 | GPC | CON-GPC-WAES-001 | 订单、运输、POD、外部异常、跨厂异常证据 |
| GPC -> GFIS | C1/C2 | GPC / GFIS | CON-GPC-GFIS-001 | 订单分发、预约、运输回传、发货回执、工厂事实回流 |
| GFIS -> WAES | C1/C4 | GFIS | CON-GFIS-WAES-001 | 工厂执行事实、工厂异常、审计、证据确证 |
| GFIS -> GPC | C1 | GFIS | CON-GPC-GFIS-001 | 发货、质量、库存、产能事件 |
| Edge -> GFIS | C1 | Edge / GFIS | CON-EDGE-GFIS-001 | 设备信号、缓存补传、回执 |
| Edge -> WAES（可选） | C1/C4 | Edge / WAES | CON-EDGE-WAES-001 | 边缘异常、节点安全、审计证据 |
| Brain -> WAES | C0/C1 | Brain | 挂接到 CON-GPC-WAES-001 或 CON-GFIS-WAES-001（按发布范围） | SOP、知识、复盘可信源 |
| XiaoC -> Hermes/XGD | C0/C2 | XiaoC | 挂接到 CON-GPC-WAES-001（治理引用） | Prompt、模型和工具配置 |
| Hermes/XGD -> WAES | C0/C2 | Hermes / XGD | 挂接到 CON-GPC-WAES-001 / CON-GFIS-WAES-001 | AgentRun、AISuggestion、工具调用审计 |
| Odoo -> GPC | C0/C1 | GPC | 挂接到 CON-GPC-WAES-001（治理引用） | 历史原型或 back-office 数据引用 |

## 9. 验收要求

连接器不能只看页面或配置是否存在，必须至少完成：

1. 连接性验证。
2. 鉴权验证。
3. schema 兼容性验证。
4. 幂等键验证。
5. 事件发布或订阅回执。
6. 证据回指来源记录。
7. 死信生成和处理演练。
8. 重放演练。
9. 降级和恢复演练。
10. AI 工具权限拦截演练。
11. 越权写主账拦截演练（验证连接器不得在对方主账上模拟写入）。
12. 根连接器归属校验（验证本连接器属于 5 个根连接器之一）。

完成状态：

| 状态 | 判定 |
|---|---|
| `partial` | 连接器字段完整但未验证 |
| `ready_for_human_acceptance` | 验证全部通过，待人工确认 |
| `complete` | 完成真实运行态联调、业务证据和人工验收 |

## 10. 模型接入连接器合同

模型 provider、本地模型和自定义模型都属于 AI 与数据层的受控连接器，不得绕过 WAES 模型授权、计量和越权拦截边界。

### 10.1 模型连接器分型

| 类型 | 说明 | 默认等级 | 关键治理要求 |
|---|---|---|---|
| Provider 模型连接器 | 连接外部模型服务商 API | C0/C2 | 走统一密钥引用、授权、计量、降级和审计 |
| 本地模型连接器 | 连接本机、内网或自建推理服务 | C0/C2 | 不因"本地"而豁免授权、计量和审计 |
| 自定义模型连接器 | 用户自带 endpoint / key / routing | C0/C2 | 必须先准入，再允许项目引用 |

### 10.2 模型连接器扩展字段

| 字段 | 必填 | 说明 |
|---|---|---|
| modelConnectorType | 是 | provider / local_model / custom_model |
| modelCatalogId | 否 | 对应统一模型目录中的模型标识 |
| capabilityProfileId | 是 | `ModelCapabilityProfile` 引用 |
| authorizationPolicyId | 是 | `ModelAuthorizationPolicy` 引用 |
| authorizationGrantRequired | 是 | 是否必须存在 `ModelAuthorizationGrant` |
| routeDecisionRequired | 是 | 是否必须形成 `ModelRouteDecision` |
| meterRequired | 是 | 是否必须记录 `ModelUsageRecord` 与 `ModelMeterSnapshot` |
| budgetPolicy | 否 | 调用预算、token 上限、费用上限 |
| classificationPolicy | 否 | 密级、租户边界、数据出境与脱敏要求 |
| fallbackPolicy | 是 | 降级、切换、回退策略 |
| overreachBlockPolicy | 是 | 越权、超预算、超密级、超场景阻断策略 |

### 10.3 模型连接器治理确认边界

| 动作 | 是否需要 GovernanceApproval | 说明 |
|---|---:|---|
| 新模型连接器首次准入 | 是 | 包括 provider、本地模型、自定义模型 |
| 自定义模型启用 | 是 | 必须完成准入、密钥治理、能力画像和风险确认 |
| 本地模型启用 | 是 | 必须完成能力画像、授权、计量和越权阻断配置 |
| 模型 fallback 策略变更 | 是 | 影响路由、成本或输出风险 |
| 模型预算策略变更 | 是 | 影响计量和阻断阈值 |
| 模型密级策略变更 | 是 | 影响租户、项目和知识可见范围 |

### 10.4 模型连接器模板

```yaml
connectorId: CON-XIAOC-MODEL-001
connectorName: XiaoC to Unified Model Gateway Connector
rootConnectorId: CON-GPC-WAES-001
sourceSystem: XiaoC
targetSystem: WAES / Hermes
owner:
  business: ai_governance
  technical: model_platform
environment: test
connectorLevel: C2
modelConnectorType: provider
modelCatalogId: MODEL-GC-001
capabilityProfileId: MCP-001
authorizationPolicyId: MAP-001
authorizationGrantRequired: true
routeDecisionRequired: true
meterRequired: true
allowedObjects:
  - ModelAuthorizationGrant
  - ModelRouteDecision
  - ModelUsageRecord
  - ModelMeterSnapshot
forbiddenObjects:
  - WorkOrder
  - QualityInspection
  - InventoryTransaction
  - ProofOfDelivery
  - FactoryShipmentRelease
allowedOperations:
  - read
  - create_draft
  - request_action
authType: api_key
secretRef: secret://model/provider/unified-gateway
schemaVersions:
  api: API-MODEL-GW-v1
  events: EVT-AI-MODEL-v1
eventTypes:
  publish:
    - ai.model_authorization_grant.changed
    - ai.model_route_decision.recorded
    - ai.model_usage.recorded
    - ai.model_meter.snapshot_calculated
    - ai.model_overreach.blocked
  subscribe: []
fallbackPolicy:
  enabled: true
  orderedModels:
    - MODEL-GC-001
    - MODEL-GC-002
overreachBlockPolicy:
  blockUnauthorizedModel: true
  blockOverBudget: true
  blockCrossTenant: true
lifecycleState: draft
```

### 10.5 模型标准连接器清单

| 连接器 | 等级 | 主责 | 根连接器 | 一期目标 |
|---|---|---|---|---|
| WAES -> 统一模型治理目录 | C0/C4 | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 模型授权、计量、阻断策略读取与治理写入 |
| XiaoC -> 统一模型网关 | C2/C4 | XiaoC / WAES | CON-GPC-WAES-001 | 模型路由、能力画像、计量上报 |
| Hermes/XGD -> XiaoC | C0/C2 | Hermes / XGD | CON-GPC-WAES-001 | 模型调用请求、Agent 运行上下文、建议结果回传 |
| 自定义模型 -> WAES 准入网关 | C0/C4 | WAES | CON-GPC-WAES-001 | 自定义模型准入、风险评估、授权生效 |
| 本地模型 -> XiaoC/Hermes | C0/C2 | XiaoC / Hermes | CON-GPC-WAES-001 | 本地模型调用、计量记录、越权拦截 |
