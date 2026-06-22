---
doc_id: GPCF-DOC-4DF13CF33D
title: GlobalCloud 绿色供应链体系最新架构图
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系最新架构图.md
source_path: 01-architecture/GlobalCloud绿色供应链体系最新架构图.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系最新架构图

日期：2026-06-07
状态：最新统一架构图 v1
口径：以 `GPC` 为绿色供应链平台主线，以 `WAES` 为治理与监控平面，以 `GFIS + Edge` 为生产与执行平面，横向统一为 `AI 与数据层`；其内部包含资源仓库、结构化数据库、企业级知识主存、知识引擎、AI 服务和技术运行底座。

## 1. 最新总架构图

```mermaid
flowchart TB
  subgraph GOV["治理与监控层"]
    WAES["WAES<br/>规则 / 治理 / 证据 / 状态 / 指标 / AI授权 / 发布验证"]
    Harness["Harness<br/>Manifest / 项目边界 / 验收 / 状态纪律"]
    Brain["Brain<br/>知识服务 / SOP / 案例 / 复盘 / RAG可信源"]
    XiaoC["XiaoC（蚁后）<br/>Prompt / MCP / 模型路由 / Agent模板 / 任务拆解"]
    Hermes["Hermes / XGD（大象）<br/>Agent运行 / 长程上下文 / 重分析 / 后台任务"]
  end

  subgraph OPS["运营与协同层"]
    PVAOS["PVAOS<br/>租户 / 组织 / 伙伴 / 项目 / 门户入口"]
    GPC["GPC<br/>平台订单 / 样品申请 / 客户签样 / 转量产 / ASN / 预约 / 运输 / POD / 外部异常 / 多厂协同"]
    Odoo["Odoo GPC 原型<br/>历史样本 / 可选 back-office connector"]
  end

  subgraph EXEC["生产与执行层"]
    GFIS["GFIS<br/>配方研发 / 样品打样 / 工厂订单 / 工单 / 质量 / 库存 / 批次 / LES / EAM / 发货出库"]
    Edge["Edge<br/>采集 / 协议转换 / 缓存 / 补传 / 去重 / 回执"]
    OT["PLC / SCADA / DCS / AGV / 仪表 / 工位终端"]
  end

  subgraph DATA["AI 与数据层"]
    POOLS["资源仓库<br/>当前已定义：订单 / 运力 / 产能 / 资金 / 政策 / 装备 / 数据 / 能源 / 原料 / 人才 / 场景"]
    DB["结构化数据库域<br/>业务主账库 / 治理审计库 / 指标时序库 / 知识元数据库 / 读模型库"]
    KMS["企业级知识主存层<br/>文档 / 版本 / 发布 / 权限 / 归档 / 审计"]
    KE["知识引擎层<br/>KDS（主存）→ Brain（UI平台）"]
    AI["AI服务域<br/>XiaoC / Hermes / XGD（大象）"]
    APIGW["API Gateway"]
    CR["Connector Registry"]
    OI["Outbox / Inbox"]
    BUS["Event Bus"]
    EVD["Evidence Ledger"]
    MT["Metric / Trace / Schema / DLQ / Replay"]
  end

  PVAOS --> GPC
  Odoo -. "历史原型 / 可选接入" .-> GPC

  GPC <--> GFIS
  OT --> Edge --> GFIS

  GPC --> POOLS
  GFIS --> POOLS
  PVAOS --> POOLS
  WAES --> POOLS

  PVAOS --> DB
  GPC --> DB
  GFIS --> DB
  WAES --> DB

  KMS --> KE
  KE --> Brain
  Brain --> AI

  GFIS --> APIGW
  GPC --> APIGW
  PVAOS --> APIGW
  Edge --> APIGW
  KE --> APIGW
  AI --> APIGW

  APIGW --> CR --> OI --> BUS
  BUS --> EVD
  BUS --> MT

  POOLS --> MT
  DB --> MT
  KMS --> WAES
  KE --> WAES
  EVD --> WAES
  MT --> WAES
  Harness --> WAES
  AI --> WAES

  WAES -. "治理规则 / 证据门 / 状态门 / AI授权门" .-> GPC
  WAES -. "治理规则 / 证据门 / 状态门 / AI授权门" .-> GFIS
  WAES -. "数据权限 / 审计 / AI可见范围" .-> DB
  WAES -. "知识准入 / 发布验证 / 引用审计 / AI可见范围" .-> KMS
  WAES -. "知识引擎授权 / RAG准入 / 失效拦截" .-> KE
  WAES -. "连接器治理 / 发布验证" .-> CR

  classDef gov fill:#e8f1ff,stroke:#3b82f6,color:#0f172a
  classDef ops fill:#eafaf1,stroke:#22c55e,color:#0f172a
  classDef exec fill:#fff7e8,stroke:#f59e0b,color:#0f172a
  classDef data fill:#f3f4f6,stroke:#6b7280,color:#111827

  class WAES,Harness,Brain,XiaoC,Hermes gov
  class PVAOS,GPC,Odoo ops
  class GFIS,Edge,OT exec
  class POOLS,DB,KMS,KE,AI,APIGW,CR,OI,BUS,EVD,MT data
```

## 2. 读图重点

1. `GPC` 是绿色供应链平台主线，不再把 Odoo 原型当成主线。
2. `WAES` 是治理与监控平面，不承办工单、质量、库存、发货、签收等具体事务审批。
3. `GFIS` 是工厂事实主账，`Edge` 是现场接入层，不是业务主账。
4. 横向底座已经统一收口为 `AI 与数据层`，其中包含资源仓库、结构化数据库、企业级知识主存、知识引擎、AI 服务和技术运行底座。
5. KDS 为企业级知识主存（canonical source），Brain 为知识 UI 平台；LLM Wiki 为知识编制工具，不直接等于企业级知识真源。
6. 结构化数据库已显式纳入主架构，用于承载业务主账、治理审计、指标时序、知识元数据和查询读模型。
7. 宪法内容不单独形成业务平台，而是通过规则门、证据门、状态门、授权门、知识准入门和连接器治理进入总架构。
8. AI 服务流只能生成建议、摘要、预警和复盘草案，不能直接写业务事实，也不能直接改写正式知识版本。

## 3. 一句话口径

最新统一架构不是“一个大平台统管全部”，而是：

`GPC 负责平台协同，GFIS 负责工厂执行，WAES 负责治理约束，PVAOS 负责生态入口，Edge 负责现场接入。`
