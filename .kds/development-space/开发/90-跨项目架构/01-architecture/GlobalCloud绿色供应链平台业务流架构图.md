---
doc_id: GPCF-DOC-3DB47E5509
title: GlobalCloud 绿色供应链平台业务流架构图
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链平台业务流架构图.md
source_path: 01-architecture/GlobalCloud绿色供应链平台业务流架构图.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链平台业务流架构图

日期：2026-06-07
状态：平台业务流架构图 v1
口径：只看业务主链，不展开治理、AI 和数据治理细节。

## 1. 平台业务流总图

```mermaid
flowchart LR
  PVAOS["PVAOS<br/>租户 / 组织 / 伙伴 / 项目 / 门户入口"]
  GPC["GPC<br/>平台订单 / ASN / 预约 / 车辆 / 运输 / POD / 外部异常"]
  GFIS["GFIS<br/>工厂订单 / 工单 / 质量 / 库存 / 批次 / LES / 发货出库"]
  Edge["Edge<br/>现场采集 / 缓存 / 回执"]
  Customer["客户"]
  Supplier["供应商"]
  Carrier["承运商"]

  PVAOS --> GPC
  Supplier --> GPC
  Customer --> GPC
  Carrier --> GPC

  GPC -->|"平台订单 / ASN / 预约"| GFIS
  Edge --> GFIS
  GFIS -->|"发货出库事实"| GPC
  GPC -->|"运输 / 在途 / POD"| Customer
  GPC -->|"运输任务 / 回单 / 异常"| Carrier
  GPC -->|"到货协同 / ASN / 预约"| Supplier
```

## 2. 业务链路拆解

1. `PVAOS` 提供租户、组织、伙伴、项目和门户入口。
2. `GPC` 负责平台订单、ASN、预约、车辆、运输、POD 和外部异常。
3. `GFIS` 负责工厂订单确认、工单、质量、库存、批次、LES 和发货出库事实。
4. `Edge` 只负责现场接入，先进入 `GFIS`，不直接进入平台主账。

## 3. 边界重点

1. `GPC` 不做工单、质量放行、库存主账。
2. `GFIS` 不做厂外运输、POD 和外部协同主账。
3. `PVAOS` 不做生产执行。
4. `Edge` 不做业务审批和业务主账。
