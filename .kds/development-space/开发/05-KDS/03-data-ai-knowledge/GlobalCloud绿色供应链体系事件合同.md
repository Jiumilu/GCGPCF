---
doc_id: GPCF-DOC-9B55FCEA8F
title: GlobalCloud 绿色供应链体系事件合同
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系事件合同.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系事件合同.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系事件合同

日期：2026-06-10
版本：一期事件合同 v2（口径修正稿）
基线引用：[GlobalCloud绿色供应链体系总架构.md](/Users/lujunxiang/Projects/GlobalCloud%20GPCF/GlobalCloud绿色供应链体系总架构.md)
适用范围：GPC、GFIS、WAES、PVAOS、Brain、XiaoC、Hermes/XGD、Edge 与连接器/事件总线；连接器必须落在 [总架构] §4 定义的 5 个根连接器编号下。

## 0. 口径修正（与 [总架构] 一致）

1. **GPC** 是绿色供应链公共服务平台本体，事件中以 `gpc.` 域名承载平台公共服务事实。
2. **GFIS** 是工厂执行系统 / 工厂事实主账，事件中以 `gfis.` 域名承载工厂执行事实。
3. **WAES** 是治理、证据、状态门控、AI 越权控制系统，事件中以 `waes.` 域名承载治理事实；WAES 不发布平台业务事实事件，也不发布工厂执行事实事件。
4. **PVAOS** 是平台运营、租户、组织、伙伴、用户、门户底座，事件中以 `pvaos.` 域名承载生态入口事实。
5. **Edge** 是现场采集与边缘缓冲层，事件中以 `edge.` 域名承载现场信号；Edge 不得在自身落业务主账，事件先进入 GFIS，由 GFIS 规则确证后才形成业务事实事件。
6. **KDS** 是企业知识主存（唯一数据源），**Brain / LLM Wiki** 是知识编制与引擎候选，事件中以 `brain.` / `knowledge.` 域名承载。
7. **XiaoC / Hermes / XGD** 是 AI 与 Agent 编排层，事件中以 `ai.` / `agent.` / `xiaoc.` 域名承载；AI 不得发布业务完成事实。
8. 任何事件不得被解释为绕开主责系统主账的写入授权；事件是事实通知，不是远程命令。

## 1. 设计原则

1. **事件是事实通知，不是远程命令**：业务事实由主责系统生成事件；消费系统不得把收到事件当作自己可改写主账的授权。
2. **AI 建议不是业务事实事件**：AI 只能发布 `ai.suggestion.*`、`agent.task.*` 等建议或过程事件，不能发布质量放行、库存扣减、发货确认、客户签收等事实事件。
3. **主责系统唯一**：GFIS 负责工厂事实；GPC 负责平台公共服务事实；WAES 负责治理规则、证据、指标、状态审计和建议状态。
4. **WAES 不承办具体事务审批**：工单、质量、库存、发货、签收等事务审批在 GFIS 或 GPC 内完成；WAES 只记录引用、治理确认和证据确证。
5. **所有事件必须可追踪**：事件必须带 `traceId`、`correlationId`、`sourceSystem`、`sourceRecordId`、`idempotencyKey` 和证据引用。
6. **先小范围闭环**：一期只覆盖订单、齐套、工单、质量、库存、发货、运输、签收、异常、边缘采集、治理确认和 AI 建议。
7. **平台事件优先围绕 GPC**：绿色供应链公共服务平台事实事件默认由 `GPC` 主责发布，`WAES` 不发布平台业务事实事件。
8. **Edge 不得越级**：Edge 事件只承载现场信号与缓存补传，不得在事件层模拟业务完成事实；任何"现场信号直接进入平台事实流"的事件链在体系中不得成立。

## 2. 事件命名规范

```text
<domain>.<object>.<past_tense_action>
```

示例：

```text
gfis.work_order.released
gfis.quality_inspection.accepted
gpc.shipment.in_transit
gpc.pod.signed
waes.governance_approval.approved
ai.suggestion.submitted
```

命名规则：

1. domain 使用主责系统或领域：`gfis`、`gpc`、`pvaos`、`waes`、`edge`、`brain`、`xiaoc`、`agent`、`ai`。
2. object 使用下划线英文名。
3. action 使用过去式，表达已发生事实。
4. 建议、草案、治理审批请求不得命名为业务完成事实。

## 3. 事件 Envelope

```json
{
  "eventId": "EVT-20260610-000001",
  "eventType": "gfis.factory_shipment.released",
  "eventVersion": "1.0",
  "sourceSystem": "GFIS",
  "sourceRecordId": "FSR-20260610-0001",
  "occurredAt": "2026-06-10T09:00:00+08:00",
  "publishedAt": "2026-06-10T09:00:03+08:00",
  "actorType": "human",
  "actorId": "USER-001",
  "riskLevel": "L2",
  "traceId": "TRC-20260610-0001",
  "correlationId": "PO-20260610-0001",
  "idempotencyKey": "GFIS:FSR-20260610-0001:released:v1",
  "connectorId": "CON-GPC-GFIS-001",
  "payload": {},
  "evidenceRefs": [
    "EVD-20260610-0001"
  ]
}
```

字段说明：

| 字段 | 必填 | 说明 |
|---|---|---|
| `eventId` | 是 | 全局唯一事件 ID |
| `eventType` | 是 | 事件类型 |
| `eventVersion` | 是 | 事件版本 |
| `sourceSystem` | 是 | 事件生产系统 |
| `sourceRecordId` | 是 | 来源记录 ID |
| `occurredAt` | 是 | 业务发生时间 |
| `publishedAt` | 是 | 发布时间 |
| `actorType` | 是 | human / system / agent / integration |
| `actorId` | 是 | 操作者或系统 ID |
| `riskLevel` | 是 | L1 / L2 / L3 / L4 / L5 |
| `traceId` | 是 | 端到端追踪 ID |
| `correlationId` | 是 | 关联业务链路 ID |
| `idempotencyKey` | 是 | 幂等键 |
| `connectorId` | 是 | 事件承载连接器编号（必须属于 [总架构] §4 的 5 个根连接器之一） |
| `payload` | 是 | 事件载荷 |
| `evidenceRefs` | 是 | 证据引用 |

## 4. GFIS 工厂执行事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `gfis.factory_order.accepted` | FactoryOrder | L2 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 工厂订单确认 |
| `gfis.work_order.released` | WorkOrder | L2 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 工单释放 |
| `gfis.kitting_check.completed` | KittingCheck | L2 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 齐套检查完成 |
| `gfis.kitting_check.shortage_detected` | KittingCheck | L2 | GFIS | WAES / Agent | CON-GFIS-WAES-001 | 否 | 缺料风险 |
| `gfis.logistics_task.created` | LogisticsTask | L2 | GFIS | WAES / XGD | CON-GFIS-WAES-001 | 否 | 厂内物流任务创建 |
| `gfis.logistics_task.completed` | LogisticsTask | L2 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 厂内物流任务完成 |
| `gfis.production.reported` | JobCard / WorkOrder | L2 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 生产报工 |
| `gfis.quality_inspection.accepted` | QualityInspection | L3 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 质量合格 |
| `gfis.quality_inspection.rejected` | QualityInspection | L3 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 质量不合格 |
| `gfis.inventory_transaction.posted` | InventoryTransaction | L3 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 库存事务入账 |
| `gfis.lot.status_changed` | MaterialLot | L3 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 批次质量/可用状态变化 |
| `gfis.factory_shipment.released` | FactoryShipmentRelease | L3 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 工厂发货出库 |
| `gfis.equipment.down` | Equipment | L2 | GFIS | WAES / Agent | CON-GFIS-WAES-001 | 否 | 设备停机 |
| `gfis.maintenance_order.closed` | MaintenanceOrder | L3 | GFIS | WAES | CON-GFIS-WAES-001 | 否 | 维修关闭 |

### 示例：发货出库事件 payload

```json
{
  "factoryShipmentReleaseId": "FSR-20260610-0001",
  "factoryOrderId": "FO-20260610-0001",
  "platformOrderId": "PO-20260610-0001",
  "customerId": "CUS-0001",
  "warehouseId": "WH-FINISHED-01",
  "items": [
    {
      "materialId": "MAT-BOX-001",
      "lotId": "LOT-20260610-A",
      "quantity": 15000,
      "uom": "pcs",
      "qualityStatus": "qualified"
    }
  ],
  "releasedBy": "USER-WH-001",
  "releasedAt": "2026-06-10T09:00:00+08:00"
}
```

## 5. GPC 平台公共服务事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `gpc.platform_order.received` | PlatformOrder | L2 | GPC | WAES | CON-GPC-WAES-001 | 否 | 平台订单接收 |
| `gpc.platform_order.dispatched_to_factory` | OrderMapping | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 订单分发到工厂 |
| `gpc.asn.created` | ASN | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 供应商 ASN |
| `gpc.appointment.confirmed` | Appointment | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 预约确认 |
| `gpc.vehicle.arrived` | Appointment / Vehicle | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 车辆到达 |
| `gpc.shipment.created` | Shipment | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 发运单创建 |
| `gpc.shipment.loaded` | Shipment | L3 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 装车完成 |
| `gpc.shipment.in_transit` | Shipment | L2 | GPC | WAES | CON-GPC-WAES-001 | 否 | 在途 |
| `gpc.shipment.delayed` | Shipment | L2 | GPC | WAES / Agent | CON-GPC-WAES-001 | 否 | 运输延迟 |
| `gpc.pod.signed` | ProofOfDelivery | L3 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 客户签收 |
| `gpc.pod.disputed` | ProofOfDelivery | L3 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 签收争议 |
| `gpc.external_exception.raised` | ExternalException | L2 | GPC | WAES / Agent | CON-GPC-WAES-001 | 可生成草案，不自动确证 | 外部协同异常 |
| `gpc.external_exception.closed` | ExternalException | L3 | GPC | WAES | CON-GPC-WAES-001 | 否 | 外部异常关闭 |

### 示例：POD 签收事件 payload

```json
{
  "podId": "POD-20260610-0001",
  "shipmentId": "SHIP-20260610-0001",
  "factoryShipmentReleaseId": "FSR-20260610-0001",
  "customerId": "CUS-0001",
  "signedBy": "customer-contact-001",
  "signedAt": "2026-06-10T16:30:00+08:00",
  "items": [
    {
      "materialId": "MAT-BOX-001",
      "lotId": "LOT-20260610-A",
      "deliveredQuantity": 15000,
      "acceptedQuantity": 15000,
      "rejectedQuantity": 0
    }
  ],
  "attachments": [
    "EVD-POD-PHOTO-0001",
    "EVD-POD-SIGNATURE-0001"
  ],
  "disputeReason": null
}
```

## 6. WAES 控制塔、治理与证据事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `waes.evidence.captured` | EvidenceRecord | L1 | WAES | Harness / 各系统 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 / CON-EDGE-WAES-001 | 可提交候选 | 证据捕获 |
| `waes.evidence.verified` | EvidenceRecord | L2 | WAES | Harness / Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 证据确证 |
| `waes.governance_approval.requested` | GovernanceApproval | L3/L4 | WAES | Harness / Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 可生成草案，不自动提交关键治理审批 | 治理审批请求 |
| `waes.governance_approval.approved` | GovernanceApproval | L4 | WAES | Harness / 各系统 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 治理规则、AI 授权、指标口径、状态升级等审批通过 |
| `waes.governance_approval.rejected` | GovernanceApproval | L3/L4 | WAES | Agent / 请求系统 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 治理审批拒绝 |
| `waes.business_approval.referenced` | BusinessApprovalReference | L2/L3 | GFIS / GPC | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 引用业务系统内部事务审批结果，WAES 不承办该审批 |
| `waes.metric.calculated` | MetricSnapshot | L1 | WAES | ControlTower | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 指标计算 |
| `waes.exception.linked` | ExceptionCase | L2 | WAES | GFIS / GPC / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 异常关联 |

## 7. Edge 现场与边缘事件

Edge 事件是现场信号进入 GFIS/WAES 的事实通知，不是工单、质量、库存、发货或签收主账。

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `edge.node.online` | EdgeNode | L1 | Edge | GFIS / WAES | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 边缘节点上线 |
| `edge.node.offline` | EdgeNode | L2 | Edge | GFIS / WAES / Agent | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 边缘节点离线 |
| `edge.device_signal.received` | DeviceSignal | L1 | Edge | GFIS | CON-EDGE-GFIS-001 | 否 | 现场信号接收 |
| `edge.device_alarm.raised` | DeviceSignal / Equipment | L2/L3 | Edge | GFIS / WAES / Agent | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 设备或现场报警 |
| `edge.buffer.replayed` | EdgeNode | L1 | Edge | GFIS / WAES | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 断网缓存补传 |

## 8. PVAOS 生态入口与平台运营事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `pvaos.tenant.created` | Tenant | L2 | PVAOS | WAES / GPC | CON-GPC-WAES-001 | 否 | 租户创建 |
| `pvaos.organization.onboarded` | Organization | L2 | PVAOS | GPC / WAES | CON-GPC-WAES-001 | 否 | 组织接入 |
| `pvaos.partner.onboarded` | Partner | L2 | PVAOS | GPC / WAES | CON-GPC-WAES-001 | 否 | 伙伴接入 |
| `pvaos.role_grant.changed` | RoleGrant | L3 | PVAOS | WAES / GPC | CON-GPC-WAES-001 | 否 | 角色授权变化 |

## 9. Brain / XiaoC / Agent 事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `brain.knowledge_entry.proposed` | KnowledgeEntry | L1 | Brain / Agent | WAES / XiaoC | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | 知识候选 |
| `brain.knowledge_entry.verified` | KnowledgeEntry | L2 | Brain | WAES / XiaoC | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 知识确证 |
| `xiaoc.prompt_template.published` | PromptTemplate | L2 | XiaoC | Hermes / WAES | CON-GPC-WAES-001 | 否 | Prompt 模板发布 |
| `agent.task.completed` | AgentTask | L1 | Hermes / XGD | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | Agent 任务完成 |
| `ai.suggestion.submitted` | AISuggestion | L3 | WAES / Hermes / XGD | WAES / Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | AI 建议提交 |
| `ai.suggestion.rejected` | AISuggestion | L3/L4 | WAES | Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | AI 建议被治理规则或人工确认驳回 |
| `ai.suggestion.governance_authorized` | AISuggestion | L3/L4 | WAES | GFIS / GPC | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | AI 建议通过治理授权；具体业务执行仍由 GFIS/GPC 内部流程确认，不表示业务批准 |
| `ai.suggestion.closed` | AISuggestion | L2 | WAES | Brain / Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 建议关闭和复盘 |

## 10. 禁止 AI 直接发布的事件

AI 不得直接发布：

```text
gfis.factory_order.accepted
gfis.work_order.released
gfis.kitting_check.completed
gfis.production.reported
gfis.quality_inspection.accepted
gfis.quality_inspection.rejected
gfis.inventory_transaction.posted
gfis.lot.status_changed
gfis.factory_shipment.released
gfis.maintenance_order.closed
gpc.platform_order.dispatched_to_factory
gpc.appointment.confirmed
gpc.shipment.loaded
gpc.pod.signed
gpc.external_exception.closed
waes.governance_approval.approved
waes.evidence.verified
edge.device_alarm.raised
pvaos.role_grant.changed
```

AI 可以生成：

```text
ai.suggestion.submitted
agent.task.completed
brain.knowledge_entry.proposed
```

但这些事件不能作为业务完成证据。

## 11. 四流优化新增事件

本节根据四流综合架构补充事件合同，优先服务治理规则生命周期、连接器治理、数据治理、AI 服务审计和多厂协同。以下事件均不得被解释为 GFIS/GPC 具体事务审批。

### 11.1 治理流事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `waes.governance_rule.created` | GovernanceRule | L2 | WAES | Harness / Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 治理规则创建 |
| `waes.governance_rule.activated` | GovernanceRuleVersion | L4 | WAES | GFIS / GPC / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 治理规则版本生效 |
| `waes.governance_rule.retired` | GovernanceRuleVersion | L4 | WAES | GFIS / GPC / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 治理规则版本废止 |
| `waes.policy_assignment.changed` | PolicyAssignment | L3 | WAES | Connector / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 规则绑定范围变化 |
| `waes.status_transition.requested` | StatusTransitionRequest | L3 | WAES / Harness | Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 可生成草案，不自动提交关键状态升级 | 状态流转请求 |
| `waes.status_transition.approved` | StatusTransitionRequest | L4 | WAES / Harness | Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 状态流转通过 |
| `waes.status_transition.rejected` | StatusTransitionRequest | L3 | WAES / Harness | Report / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 状态流转驳回 |
| `waes.release_gate.passed` | ReleaseGate | L3 | WAES / Harness | Project | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 发布或阶段验收门通过 |
| `waes.release_gate.failed` | ReleaseGate | L3 | WAES / Harness | Project / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 发布或阶段验收门失败 |
| `waes.connector_lifecycle.changed` | ConnectorLifecycleRecord | L3 | WAES / Connector Registry | 各系统 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 连接器上线、降级、恢复或下线 |
| `waes.evidence.rework_requested` | EvidenceReworkRequest | L2 | WAES / Harness | SourceSystem / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 可生成草案，不自动确证 | 证据被驳回后的补证请求 |

### 11.2 业务流扩展事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `gpc.factory_allocation.proposed` | FactoryAllocation | L2 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 多厂分单建议结果 |
| `gpc.factory_allocation.confirmed` | FactoryAllocation | L3 | GPC | GFIS / WAES | CON-GPC-GFIS-001 / CON-GPC-WAES-001 | 否 | 分单确认；GFIS 仍需内部接单确认 |
| `gpc.cross_factory_exception.raised` | CrossFactoryException | L2 | GPC | WAES / GFIS | CON-GPC-WAES-001 | 可生成草案，不自动确证 | 跨厂协同异常 |
| `gpc.cross_factory_exception.closed` | CrossFactoryException | L3 | GPC | WAES / GFIS | CON-GPC-WAES-001 | 否 | 跨厂协同异常关闭 |
| `gfis.capacity_commitment.published` | CapacityCommitment | L2 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 工厂产能承诺发布 |
| `gfis.capacity_snapshot.published` | CapacitySnapshot | L1 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 工厂产能快照发布 |
| `gfis.inventory_visibility.snapshot_published` | InventoryVisibilitySnapshot | L2 | GFIS | GPC / WAES | CON-GPC-GFIS-001 / CON-GFIS-WAES-001 | 否 | 多厂库存可见性快照 |
| `gfis.quality_trace_scope.created` | QualityTraceScope | L2 | GFIS / WAES | GPC / Report | CON-GFIS-WAES-001 | 否 | 跨厂或跨链质量追溯范围建立 |

### 11.3 数据流事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `data.schema_version.published` | SchemaVersion | L3 | Connector Registry | WAES / 各系统 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | API 或事件 schema 版本发布 |
| `data.schema_compatibility.checked` | SchemaCompatibilityCheck | L2 | Connector Registry | WAES / Harness | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | Schema 兼容性检查完成 |
| `data.dead_letter.created` | DeadLetterRecord | L2 | Event Bus | WAES / SourceSystem | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 死信记录创建 |
| `data.replay.requested` | ReplayRequest | L3 | WAES / Event Bus | Harness / Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 可生成草案，不自动执行高风险重放 | 事件重放请求 |
| `data.replay.completed` | ReplayRun | L2 | Event Bus | WAES / SourceSystem | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 事件重放完成 |
| `data.quality_issue.detected` | DataQualityIssue | L2 | WAES / Data Platform | SourceSystem / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 数据质量问题发现 |
| `data.quality_issue.resolved` | DataQualityIssue | L2 | SourceSystem / WAES | Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 数据质量问题关闭 |
| `data.lineage_record.created` | LineageRecord | L1 | WAES / Data Platform | Report / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 数据血缘记录创建 |
| `data.retention_policy.changed` | RetentionPolicy | L3 | WAES | Data Platform / Harness | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 数据保留策略变更 |
| `edge.buffer_policy.changed` | EdgeBufferPolicy | L3 | Edge / WAES | GFIS / Harness | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 边缘缓存策略变更 |
| `edge.replay_run.completed` | ReplayRun | L2 | Edge | GFIS / WAES | CON-EDGE-GFIS-001 / CON-EDGE-WAES-001 | 否 | 边缘缓存补传完成 |

### 11.4 AI 服务流事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `ai.tool_grant.changed` | AgentToolGrant | L4 | WAES | Agent / Harness | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | Agent 工具授权变化 |
| `ai.agent_run.started` | AgentRun | L1 | Hermes / XGD | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | Agent 运行开始 |
| `ai.agent_run.completed` | AgentRun | L1 | Hermes / XGD | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | Agent 运行完成，不表示业务事实完成 |
| `ai.agent_run.failed` | AgentRun | L1 | Hermes / XGD | WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 是 | Agent 运行失败 |
| `ai.prompt_evaluation.completed` | PromptEvaluation | L2 | XiaoC | WAES / Hermes | CON-GPC-WAES-001 | 否 | Prompt 评估完成 |
| `ai.model_evaluation.completed` | ModelEvaluation | L2 | XiaoC | WAES / Hermes | CON-GPC-WAES-001 | 否 | 模型评估完成 |
| `ai.model_authorization_grant.changed` | ModelAuthorizationGrant | L4 | WAES | XiaoC / Hermes / Agent | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 模型治理授权变化 |
| `ai.model_route_decision.recorded` | ModelRouteDecision | L2 | XiaoC / WAES | Hermes / WAES | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 模型选择、降级、切换和回退决策记录 |
| `ai.model_usage.recorded` | ModelUsageRecord | L2 | XiaoC / Hermes | WAES / Data Platform | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 单次模型调用计量、延迟、费用和治理结果记录 |
| `ai.model_meter.snapshot_calculated` | ModelMeterSnapshot | L2 | WAES / Data Platform | Report / XiaoC / Hermes | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 模型 token、费用、成功率、阻断率等计量快照 |
| `ai.suggestion.outcome_recorded` | AISuggestionOutcome | L2 | WAES | Brain / Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 建议采纳、驳回或业务确认引用结果记录 |
| `ai.overreach.blocked` | AIOverreachBlocked | L4 | WAES | Harness / Agent / Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | AI 越权动作被阻断 |
| `ai.model_overreach.blocked` | ModelOverreachBlocked | L4 | WAES | Harness / XiaoC / Hermes / Human | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 模型调用因授权、密级、预算、场景或输出约束被阻断 |

### 11.5 知识主存域与结构化数据库域事件

| 事件 | 来源对象 | 风险等级 | 生产者 | 消费者 | 承载连接器 | AI 可发布 | 说明 |
|---|---|---|---|---|---|---|---|
| `knowledge.document.created` | KnowledgeDocument | L2 | 知识主存服务 | WAES / LLM Wiki / Brain | CON-GPC-WAES-001 | 否 | 正式知识文档创建 |
| `knowledge.version.approved` | KnowledgeVersion | L3 | 知识主存服务 / WAES | LLM Wiki / Brain / Report | CON-GPC-WAES-001 | 否 | 知识版本审批通过 |
| `knowledge.release.effective` | KnowledgeRelease | L4 | 知识主存服务 / WAES | LLM Wiki / Brain / WAES | CON-GPC-WAES-001 | 否 | 知识发布正式生效，先进入编制视图和主知识引擎，不直接把 Brain 当正式发布消费者 |
| `knowledge.release.rolled_back` | KnowledgeRelease | L4 | 知识主存服务 / WAES | LLM Wiki / Brain / WAES | CON-GPC-WAES-001 | 否 | 知识发布回滚，要求编制视图和引擎同步回滚 |
| `knowledge.access_policy.changed` | KnowledgeAccessPolicy | L4 | WAES / 知识主存服务 | LLM Wiki / Brain / Agent | CON-GPC-WAES-001 | 否 | 知识访问与 AI 可见范围变更 |
| `knowledge.compile_view.published` | KnowledgeCompileView | L2 | LLM Wiki | Brain / WAES | CON-GPC-WAES-001 | 否 | 知识编制视图发布或更新；用于人工可维护视图，不代表正式真源变更 |
| `knowledge.engine_index.refreshed` | KnowledgeEngineIndex | L2 | Brain | Brain / WAES / Report | CON-GPC-WAES-001 | 否 | 主知识引擎索引刷新完成，供 Brain 消费和 WAES 审计 |
| `knowledge.service.catalog.published` | KnowledgeServiceCatalog | L2 | Brain | XiaoC / Hermes / XGD / WAES | CON-GPC-WAES-001 | 否 | Brain 知识服务目录发布，面向 AI 与业务消费，不代表正式知识发布 |
| `knowledge.ingest.completed` | KnowledgeIngestJob | L2 | Brain | WAES / Brain / Report | CON-GPC-WAES-001 | 否 | 知识 ingest 完成，Brain 只能消费引擎结果 |
| `knowledge.ingest.failed` | KnowledgeIngestJob | L2 | Brain | WAES / Brain / Agent | CON-GPC-WAES-001 | 否 | 知识 ingest 失败 |
| `knowledge.audit_recorded` | KnowledgeAuditLog | L1 | 知识主存服务 | WAES | CON-GPC-WAES-001 | 否 | 知识查看、引用、导出审计记录 |
| `data.database_access_policy.changed` | DatabaseAccessPolicy | L3 | WAES / Data Platform | Query Service / SourceSystem | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 数据库访问策略变化 |
| `data.read_model_projection.published` | ReadModelProjection | L2 | Data Platform | WAES / 知识引擎 | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 读模型投影发布 |
| `waes.connector_decision.published` | ConnectorDecision | L4 | WAES / Connector Registry | GFIS / GPC / Harness | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 连接器治理结论发布 |
| `waes.status_requirement.changed` | StatusRequirement | L3 | WAES / Harness | Project / Report | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 状态门要求变化 |
| `waes.ai_authorization_grant.changed` | AIAuthorizationGrant | L4 | WAES | Agent / XiaoC / Hermes | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | AI 授权结论变化 |
| `waes.acceptance_conclusion.published` | AcceptanceConclusion | L4 | WAES / Harness | Report / Project | CON-GPC-WAES-001 / CON-GFIS-WAES-001 | 否 | 阶段验收或整体验收结论发布 |

## 12. 幂等、重试与补偿

### 12.1 幂等键

格式：

```text
<sourceSystem>:<sourceRecordId>:<eventType>:<eventVersion>
```

示例：

```text
GFIS:FSR-20260610-0001:gfis.factory_shipment.released:1.0
```

### 12.2 重试规则

| 场景 | 处理 |
|---|---|
| 消费系统短暂不可用 | 指数退避重试 |
| 幂等键重复 | 标记 duplicate，不重复执行业务动作 |
| payload schema 不匹配 | 进入 dead letter |
| 主数据映射缺失 | 进入 pending_mapping，并触发 WAES 异常 |
| L4 治理授权缺失 | 阻断跨系统执行请求，只保留建议或治理草案 |

### 12.3 补偿规则

| 失败场景 | 补偿 |
|---|---|
| GFIS 发货事件已发布但 GPC 未创建 Shipment | 通过 `CON-GPC-GFIS-001` 重放 `gfis.factory_shipment.released` |
| GPC POD 已签收但 GFIS 未收到回传 | 通过 `CON-GPC-GFIS-001` 重放 `gpc.pod.signed` |
| Edge 信号未及时进入 GFIS | 通过 `CON-EDGE-GFIS-001` 重放 `edge.device_signal.received` |
| 主数据映射错误 | 生成 `ExceptionCase`，人工修正映射后重放 |
| AI 建议被误提交 | 撤回 `AISuggestion` 或治理草案；不得撤销业务事实事件，事务修正必须进入 GFIS/GPC 内部流程 |

## 13. 一期端到端事件链

```text
pvaos.organization.onboarded
-> gpc.platform_order.received
-> gpc.platform_order.dispatched_to_factory
-> gfis.factory_order.accepted
-> gfis.kitting_check.completed
-> gfis.work_order.released
-> gfis.logistics_task.created
-> gfis.logistics_task.completed
-> gfis.production.reported
-> gfis.quality_inspection.accepted
-> gfis.inventory_transaction.posted
-> gfis.factory_shipment.released
-> gpc.shipment.created
-> gpc.shipment.loaded
-> gpc.shipment.in_transit
-> gpc.pod.signed
-> waes.evidence.captured
-> waes.evidence.verified
-> waes.metric.calculated
```

异常链：

```text
gfis.kitting_check.shortage_detected
-> ai.suggestion.submitted
-> waes.governance_approval.requested
-> waes.governance_approval.approved
-> waes.business_approval.referenced
-> gfis.logistics_task.created
-> gfis.logistics_task.completed
-> ai.suggestion.closed
```

链路约束：

1. `pvaos.*` 只能由 PVAOS 发起，承载于 `CON-GPC-WAES-001` 或 `CON-GFIS-WAES-001` 的引用上下文。
2. `gpc.*` 只能由 GPC 发起；平台公共服务事实不允许由 WAES 或 GFIS 替代发布。
3. `gfis.*` 只能由 GFIS 发起；工厂执行事实不允许由 GPC、WAES 或 Edge 替代发布。
4. `edge.*` 只能由 Edge 发起；Edge 事件不直接进入 GPC 公共服务事实流。
5. `waes.*` 只能由 WAES 发起治理事实；不得发布业务主账事实。
6. `ai.*` / `agent.*` 只能由 XiaoC / Hermes / XGD 发起建议和 Agent 运行事件；不得发布业务主账事实。
