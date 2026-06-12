---
doc_id: GPCF-DOC-5BF9469733
title: GlobalCloud 绿色供应链体系真实层次架构图
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系真实层次架构图.md
source_path: 01-architecture/GlobalCloud绿色供应链体系真实层次架构图.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系真实层次架构图

日期：2026-06-07
状态：体系级主架构图 v1
口径：只表达真实主责分层、横向底座和治理边界，不展开实现细节。横向底座统一收口为 `AI 与数据层`，内部包含资源仓库、结构化数据库、知识主存、知识引擎、AI 服务和事件证据底座。

## 1. 真实层次架构图

```mermaid
flowchart TB
  subgraph L1["治理与监控层"]
    WAES["WAES
项目发起 / 配置编排 / 发布验证
规则治理 / 指标口径 / 证据 / 状态
连接器治理 / AI授权 / 阶段验收"]
  end

  subgraph L2["运营与协同层"]
    PVAOS["PVAOS
组织 / 伙伴 / 项目 / 门户入口"]
    GPC["GPC
供应链平台 / 订单协同 / ASN / 预约
运输 / POD / 外部异常 / 多厂协同"]
  end

  subgraph L3["生产与执行层"]
    GFIS["GFIS
工厂订单 / 工单 / 质量 / 库存
批次 / LES / EAM / 发货出库"]
    EDGE["Edge
采集 / 协议转换 / 缓存 / 补传 / 回执"]
    OT["现场设备与终端
PLC / SCADA / DCS / AGV / 仪表 / 工位终端"]
  end

  subgraph L4["AI 与数据层"]
    POOLS["资源仓库
当前已定义十一池，可继续扩展新增池"]
    DB["结构化数据库域
业务主账库 / 治理审计库 / 指标时序库
资源仓库库 / 知识元数据库 / 查询读模型库"]
    KMS["企业级知识主存域"]
    KE["知识引擎域
KDS（主存）→ Brain（UI平台）"]
    AI["AI 服务域
XiaoC / Hermes / XGD（大象）"]
    DATA["事件 / 证据 / 指标 / 追踪底座"]
  end

  PVAOS --> GPC
  GPC <--> GFIS
  OT --> EDGE --> GFIS

  PVAOS --> POOLS
  GPC --> POOLS
  GFIS --> POOLS
  WAES --> POOLS

  PVAOS --> DB
  GPC --> DB
  GFIS --> DB
  WAES --> DB

  KMS --> KE
  KE --> AI

  PVAOS --> DATA
  GPC --> DATA
  GFIS --> DATA
  EDGE --> DATA
  KE --> DATA

  DATA --> WAES
  DATA --> KE
  DB --> WAES
  DB --> KE

  WAES -. 治理约束 .-> GPC
  WAES -. 治理约束 .-> GFIS
  WAES -. 知识准入 / AI授权 .-> KE
  WAES -. 发布验证 / 状态门 / 证据门 .-> DATA
  WAES -. 数据权限 / AI可见范围 / 治理审计 .-> DB
```

## 2. 一句话解释

这张图表达的是：

1. `WAES` 在最上层，负责治理与监控，不负责具体事务审批。
2. `PVAOS + GPC` 组成运营与协同层，其中 `GPC` 是平台主线。
3. `GFIS + Edge + OT` 组成生产与执行层，其中 `GFIS` 是工厂事实主线。
4. `AI 与数据层` 统一承载资源仓库、结构化数据库、企业级知识主存、知识引擎、AI 服务和事件证据底座。
5. 结构化数据库必须显式纳入架构，分别承载业务主账、治理审计、指标时序、知识元数据和查询读模型。
6. `XiaoC + Hermes/XGD（大象）` 作为 AI 服务域，只消费知识和数据，不直接写业务主账。

## 3. 这张图刻意不表达的内容

为了保持真实和清晰，这张图不展开：

1. 具体对象目录。
2. 具体事件合同。
3. 连接器明细。
4. WAES 内部子模块。
5. 知识对象明细。
6. AI 授权等级细则。

这些内容应留在专项图和专项文档中。

## 4. 主责边界

| 层 | 主责 | 不做什么 |
|---|---|---|
| 治理与监控层 | 治理、证据、状态、发布验证、AI 授权 | 不做工单、质量、库存、发货、签收审批 |
| 运营与协同层 | 链侧协同、平台订单、运输与外部异常 | 不做工厂主账 |
| 生产与执行层 | 工厂执行、质量、库存、批次、设备执行事实 | 不做区域协同治理 |
| AI 与数据层 | 资源仓库、结构化数据库、知识真源、知识引擎、AI 服务、事件证据支撑 | 不替代业务系统，不直接改变业务事实归属 |
