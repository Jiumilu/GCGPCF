---
doc_id: GPCF-DOC-B7351DDCF8
title: GlobalCloud 绿色供应链体系多厂协同模型
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, Brain]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系多厂协同模型.md
source_path: 01-architecture/GlobalCloud绿色供应链体系多厂协同模型.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系多厂协同模型

日期：2026-06-07
状态：四流优化专项模型 v1
适用范围：一链多厂、多链多厂、区域供应链平台。

## 1. 模型定位

多厂协同模型解决订单分发、产能协同、库存可见性、质量追溯和跨厂异常闭环问题。它不把 GPC 写成工厂执行主账，也不把 WAES 写成多厂调度审批中心。

当前架构更新口径：多厂协同默认由 `GPC` 作为平台主线组织，`GFIS` 作为各厂事实源确认，`WAES` 作为治理和风险监控平面。

## 2. 主责边界

| 事项 | 主责系统 | 边界 |
|---|---|---|
| 平台订单和分发规则 | GPC | 负责协同和分配，不确认工厂执行事实 |
| 工厂接单、产能、质量、库存、发货 | GFIS | 每个工厂独立主账 |
| 组织、伙伴、门户 | PVAOS | 提供生态入口 |
| 治理规则、证据、状态、AI 授权 | WAES | 监控和治理，不做具体事务审批 |
| 现场信号 | Edge / GFIS | 先进入本厂 GFIS |

## 3. 核心对象

| 对象 | 主责 | 用途 |
|---|---|---|
| SupplyChainNetwork | WAES / GPC | 多链多厂网络 |
| ChainSegment | GPC | 产业链或业务链段 |
| FactoryCapability | GFIS / GPC | 工厂能力、品类、工艺、资质 |
| FactoryAllocationRule | GPC / WAES | 分单规则 |
| FactoryAllocation | GPC | 分单结果 |
| CapacityCommitment | GFIS | 工厂承诺产能 |
| CapacitySnapshot | GFIS | 工厂实时或周期产能 |
| InventoryVisibilitySnapshot | GFIS / GPC | 多厂可见库存快照 |
| QualityTraceScope | GFIS / WAES | 跨厂质量追溯范围 |
| CrossFactoryException | GPC / WAES | 跨厂异常闭环 |

## 4. 分单流程

```text
PlatformOrder
-> FactoryAllocationRule
-> FactoryAllocation proposed
-> GFIS capacity and capability check
-> CapacityCommitment
-> FactoryAllocation confirmed
-> GFIS factory_order.accepted
-> WAES evidence and status tracking
```

关键规则：

1. GPC 可以提出分单和协同方案。
2. GFIS 必须确认本厂工厂订单和产能承诺。
3. WAES 只校验规则、证据和风险，不替代工厂接单。
4. AI 可以建议分单方案，但不能直接确认分单或工厂接单。

## 5. 库存可见性

库存可见性快照不是库存主账。

| 层级 | 数据 | 主责 |
|---|---|---|
| 本厂库存主账 | InventoryTransaction、MaterialLot、LineSideStock | GFIS |
| 多厂可见库存 | InventoryVisibilitySnapshot | GFIS 发布，GPC 汇总 |
| 治理指标 | 库存可用率、缺料风险、周转天数 | WAES |
| AI 建议 | 调拨建议、替代物料建议 | Agent，经 WAES 授权 |

## 6. 质量追溯

跨厂追溯必须使用 `traceId`、`correlationId` 和 `TraceSegment` 串联：

```text
Supplier / ASN
-> Receiving Lot
-> QualityInspection
-> WorkOrder
-> Finished Lot
-> FactoryShipmentRelease
-> Shipment
-> POD
```

多厂追溯断点必须进入：

1. `QualityTraceScope.incomplete`。
2. `TraceSegment.missing`。
3. `EvidenceReworkRequest`。
4. WAES 证据补证流程。

## 7. 跨厂异常

跨厂异常来源：

1. 工厂产能承诺失效。
2. 关键物料短缺。
3. 质量批次隔离。
4. 发货延迟。
5. 运输异常影响其他工厂。
6. 客户交付窗口变化。

处理路径：

```text
CrossFactoryException raised
-> GPC 分派责任方
-> GFIS/GPC 内部业务确认
-> WAES 监控证据和风险
-> Brain 沉淀复盘候选
```

## 8. 验收要求

| 场景 | 判定 |
|---|---|
| 一链多厂分单 | FactoryAllocation、CapacityCommitment、GFIS 接单确认完整 |
| 多厂库存可见 | 快照可回指 GFIS 来源记录，不替代库存主账 |
| 跨厂质量追溯 | TraceSegment 无断点，断点有补证流程 |
| 跨厂异常闭环 | CrossFactoryException 有责任方、处理记录、证据和复盘 |
