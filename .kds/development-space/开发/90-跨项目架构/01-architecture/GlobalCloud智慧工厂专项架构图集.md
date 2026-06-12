---
doc_id: GPCF-DOC-3DBC8DC5C3
title: GlobalCloud 智慧工厂专项架构图集
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂专项架构图集.md
source_path: 01-architecture/GlobalCloud智慧工厂专项架构图集.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 智慧工厂专项架构图集

日期：2026-06-07
当前口径：本图集已纳入 **GlobalCloud 绿色供应链体系**，原“智慧工厂”仅指生产与执行层/工厂执行子域。主架构采用治理与监控层、运营与协同层、生产与执行层。
用途：补齐项目群总览图未展开的关键实施架构，包括统一数据与事件、GFIS-GPC-WAES 集成边界、OT/IT 安全与边缘采集、异常闭环与 AI 治理授权。

四流优化口径：本图集的所有图都必须按治理流、业务流、数据流、AI 服务流进行解释。连接器、SOP、AI 服务、数据治理、多厂协同和 Edge 安全的落地细节分别以专项模型文档为准。

当前阅读口径：

1. 绿色供应链平台业务主线看 `GPC`。
2. 治理、证据、状态和 AI 授权看 `WAES`。
3. 工厂执行和现场事实看 `GFIS + Edge`。
4. 宪法内容主要体现为边界、门禁、证据和授权纪律。

## 1. 统一数据与事件架构图

```mermaid
flowchart TB
  subgraph Source["业务事实源"]
    GFIS["GFIS<br/>工厂本地事实<br/>订单 / 工单 / 质检 / 库存 / 设备 / 发货"]
    GPC["GPC<br/>外部协同事实<br/>供应商 / 客户 / 运输 / 签收 / 回单"]
    Odoo["Odoo GPC 原型<br/>历史样本 / back-office connector 候选"]
    PVAOS["PVAOS<br/>生态协作上下文<br/>组织 / 项目 / 伙伴 / 门户"]
    Brain["Brain<br/>知识事实源<br/>SOP / 标准 / 案例 / 复盘"]
  end

  subgraph Integration["连接器与事件交换层"]
    Connector["Connector Registry<br/>系统连接器目录 / 权限 / 版本"]
    API["API Gateway<br/>认证 / 限流 / 路由 / 风险等级"]
    Outbox["Outbox / Inbox<br/>事件暂存 / 重试 / 幂等 / 补偿"]
    Bus["Event Bus<br/>订单 / 物料 / 质量 / 物流 / 异常 / AI建议"]
  end

  subgraph DataBase["工业数据底座"]
    MDM["主数据目录<br/>客户 / 供应商 / 物料 / 工厂 / 仓库 / 设备 / 人员"]
    TSDB["时序数据<br/>设备 / 能耗 / 环境 / 产线状态"]
    Metric["指标库<br/>OEE / 齐套率 / 准交率 / 一次合格率 / 物流准时率"]
    Evidence["证据台账<br/>命令输出 / 业务记录 / 业务审批引用 / 治理确认 / 截图 / 回执"]
    Lake["数据湖 / 历史归档<br/>事件快照 / 报表数据 / 训练样本"]
  end

  subgraph Consume["消费与决策层"]
    WAES["WAES 控制塔<br/>指标 / 风险 / 规则 / 证据 / Agent Desktop"]
    Agent["AI Agent 层<br/>Hermes / XGD（大象） / XiaoC<br/>查询 / 预警 / 建议 / 复盘"]
    Report["经营与运行报表<br/>日报 / 周报 / UAT / 验收报告"]
  end

  GFIS --> Connector
  GPC --> Connector
  Odoo -. "可选 back-office connector" .-> Connector
  PVAOS --> Connector
  Brain --> Connector
  Connector --> API --> Outbox --> Bus
  Bus --> MDM
  Bus --> TSDB
  Bus --> Metric
  Bus --> Evidence
  Bus --> Lake
  MDM --> WAES
  Metric --> WAES
  Evidence --> WAES
  TSDB --> WAES
  Brain --> Agent
  XiaoCRef["XiaoC Prompt / MCP"] --> Agent
  WAES --> Agent
  WAES --> Report
  Evidence --> Report

  classDef source fill:#e8f3ff,stroke:#2878c8,color:#0f2f4f;
  classDef integration fill:#fff4df,stroke:#c18424,color:#49300a;
  classDef data fill:#ecf8ef,stroke:#2f8f4e,color:#123d21;
  classDef consume fill:#f1edff,stroke:#7657c6,color:#28194c;
  class GFIS,GPC,Odoo,PVAOS,Brain source;
  class Connector,API,Outbox,Bus integration;
  class MDM,TSDB,Metric,Evidence,Lake data;
  class WAES,Agent,Report,XiaoCRef consume;
```

关键补充：

1. 项目之间不直接共享业务数据库。
2. 业务事实必须从主责系统通过连接器、API、Outbox/Inbox 和事件总线进入数据底座。
3. WAES 读取指标和证据，不直接伪造 GFIS/GPC 事实。
4. AI Agent 只能消费数据和生成建议；具体业务写入必须进入 GFIS/GPC 主责系统确认，WAES 只做治理授权、证据确证和状态审计。

四流补充：

1. 数据事件架构必须增加 schema、数据质量、DLQ、重放、血缘和租户隔离。
2. 连接器上线、降级、恢复和下线必须进入 `ConnectorLifecycleRecord`。
3. AI 读取数据必须通过 `AgentToolGrant` 和 `EvidenceCitation` 约束。
4. Edge 设备信号是遥测事实，不是业务主账事实。

## 2. GFIS-GPC-WAES 集成边界图

```mermaid
flowchart LR
  subgraph GFIS["GFIS 单厂执行域"]
    GOrder["工厂订单确认"]
    WO["生产工单 / 报工"]
    QI["质量检验 / 放行 / 隔离"]
    INV["库存 / 批次 / 仓储"]
    LES["线边配送 / 厂内转运"]
    ShipOut["发货出库事实"]
  end

  subgraph GPC["GPC 外部协同域"]
    PlatformOrder["平台订单 / 客户协同"]
    ASN["供应商 ASN / 到货预约"]
    Carrier["承运商 / 车辆 / 月台"]
    Transit["在途跟踪"]
    POD["客户签收 / 回单"]
    PublicService["绿色供应链公共服务"]
  end

  subgraph WAES["WAES 控制塔域"]
    Dashboard["跨系统看板"]
    Risk["风险识别 / 预警"]
    Governance["治理规则 / 证据确证"]
    Evidence["证据台账"]
    AgentDesk["Agent Desktop"]
  end

  PlatformOrder -- "订单下发 / 需求同步" --> GOrder
  ASN -- "到货预约 / ASN" --> INV
  GOrder --> WO --> QI --> INV --> LES --> ShipOut
  ShipOut -- "发货事件 / 批次 / 数量 / 客户" --> Carrier
  Carrier --> Transit --> POD
  POD -- "签收回传 / 回单状态" --> ShipOut

  GOrder -- "只读事件" --> Dashboard
  WO -- "只读事件" --> Dashboard
  QI -- "质量风险" --> Risk
  INV -- "库存/齐套风险" --> Risk
  LES -- "物流超时风险" --> Risk
  POD -- "交付证据" --> Evidence

  Risk --> AgentDesk
  AgentDesk -- "建议草案" --> Governance
  Governance -. "治理规则 / 证据要求 / AI授权" .-> GFIS
  Governance -. "治理规则 / 证据要求 / AI授权" .-> GPC
  GFIS -- "执行回执" --> Evidence
  GPC -- "协同回执" --> Evidence

  classDef gfis fill:#e8f3ff,stroke:#2878c8,color:#0f2f4f;
  classDef gpc fill:#ecf8ef,stroke:#2f8f4e,color:#123d21;
  classDef waes fill:#fff4df,stroke:#c18424,color:#49300a;
  class GOrder,WO,QI,INV,LES,ShipOut gfis;
  class PlatformOrder,ASN,Carrier,Transit,POD,PublicService gpc;
  class Dashboard,Risk,Governance,Evidence,AgentDesk waes;
```

边界规则：

1. GFIS 主责工厂本地事实：工单、质量、库存、厂内物流、发货出库。
2. GPC 主责外部协同事实：预约、车辆、在途、签收、回单、公共服务；Odoo GPC 仅作为历史原型或可选 back-office connector。
3. WAES 主责风险、治理规则、证据和控制塔，不成为业务主账，不承办具体事务审批。
4. 具体事务处理必须回到 GFIS/GPC，由主责系统生成业务确认和执行回执；WAES 只引用这些结果。

## 3. OT/IT 安全与边缘采集架构图

```mermaid
flowchart TB
  subgraph OT["OT 现场控制区"]
    PLC["PLC / DCS / CNC"]
    Safety["安全联锁 / 急停 / 设备保护"]
    SCADA["SCADA / HMI / 报警 / 趋势"]
    Machine["机器人 / AGV / 仪表 / 传感器"]
  end

  subgraph DMZ["工业 DMZ / 边缘区"]
    Gateway["工业网关<br/>OPC UA / Modbus / MQTT"]
    Buffer["边缘缓存<br/>断网续传 / 数据清洗"]
    EdgeRules["边缘规则<br/>只读采集 / 白名单 / 限流"]
    Historian["本地时序缓存<br/>设备 / 能耗 / 环境"]
  end

  subgraph IT["IT 业务区"]
    GFIS["GFIS<br/>生产 / 质量 / 仓储 / 设备"]
    WAES["WAES<br/>控制塔 / 告警 / 指标 / 证据"]
    GPC["GPC<br/>供应链 / 运输 / 客户协同"]
  end

  subgraph AI["AI 辅助区"]
    Agent["AI Agent<br/>预测 / 识别 / 建议 / 复盘"]
    Brain["Brain / XiaoC<br/>知识 / Prompt / 规则"]
  end

  PLC --> SCADA
  Machine --> SCADA
  PLC -- "只读采集" --> Gateway
  Machine -- "只读采集" --> Gateway
  Gateway --> Buffer --> EdgeRules --> Historian
  Historian --> GFIS
  Historian --> WAES
  GFIS --> WAES
  GFIS --> GPC
  WAES --> Agent
  Brain --> Agent
  Agent -- "L1-L3 建议" --> WAES
  WAES -. "治理规则 / 证据要求" .-> GFIS

  Safety -. "L5 禁止 AI 接管" .-> Agent
  Safety -. "只能由确定性控制系统和授权人员处理" .-> SCADA
  Agent -. "不得直接反控 PLC / DCS / 安全联锁" .-> PLC

  classDef ot fill:#ffe8e8,stroke:#c43d3d,color:#4a1111;
  classDef dmz fill:#fff4df,stroke:#c18424,color:#49300a;
  classDef it fill:#e8f3ff,stroke:#2878c8,color:#0f2f4f;
  classDef ai fill:#f1edff,stroke:#7657c6,color:#28194c;
  class PLC,Safety,SCADA,Machine ot;
  class Gateway,Buffer,EdgeRules,Historian dmz;
  class GFIS,WAES,GPC it;
  class Agent,Brain ai;
```

安全规则：

1. AI 不直接接管 PLC、DCS、急停、安全联锁、设备保护和环保排放控制。
2. OT 到 IT 默认只读采集，必须通过工业网关、DMZ、缓存和白名单。
3. GFIS 可以接收设备状态和能耗数据，但控制指令必须遵守现场控制系统和授权人员边界。
4. 断网时 GFIS 本地优先运行；恢复后由边缘缓存补传，不让云端不可用影响现场连续生产。

## 4. 异常闭环与 AI 治理授权图

```mermaid
flowchart TB
  subgraph Detect["异常识别"]
    Rule["规则引擎<br/>阈值 / SLA / 质量状态 / 库存状态"]
    Event["业务事件<br/>缺料 / 超时 / 不合格 / 停机 / 发货延迟"]
    AIWarn["AI 预警<br/>趋势 / 归因 / 风险预测"]
  end

  subgraph Case["异常工单闭环"]
    EXC["ExceptionCase<br/>异常编号 / 来源系统 / 影响范围"]
    Grade["自动分级<br/>P0 / P1 / P2 / P3"]
    Owner["责任归属<br/>生产 / 质量 / 仓储 / 设备 / 物流 / 经营"]
    Task["处理工单<br/>派发 / 升级 / 协同"]
    Resolve["处理记录<br/>措施 / 附件 / 回执"]
    Review["复盘改进<br/>原因 / CAPA / SOP 更新"]
    Close["关闭验收<br/>证据 / 指标恢复 / 人工确认"]
  end

  subgraph Approval["AI 建议与治理授权"]
    Suggest["AI 建议<br/>证据引用 / 置信度 / 风险等级"]
    L3["L3 业务确认引用<br/>补料 / 维修 / 质检建议"]
    L4["L4 治理授权<br/>AI授权 / 指标口径 / 证据确证 / 状态升级"]
    Reject["驳回 / 退回补证"]
  end

  subgraph Execute["主责系统执行"]
    GFIS["GFIS 执行<br/>生产 / 质量 / 库存 / 设备 / 厂内物流"]
    GPC["GPC 协同<br/>运输 / 签收 / 客户 / 供应商"]
    Evidence["WAES 证据台账<br/>治理确认 / 业务审批引用 / 执行回执 / 截图 / 日志"]
    Brain["Brain 知识沉淀<br/>SOP / 复盘 / 案例"]
  end

  Rule --> EXC
  Event --> EXC
  AIWarn --> Suggest
  Suggest --> L3
  Suggest --> L4
  L3 --> EXC
  L4 --> EXC
  L3 --> Reject
  L4 --> Reject
  EXC --> Grade --> Owner --> Task --> Resolve --> Review --> Close
  Task -- "业务系统内部确认后执行" --> GFIS
  Task -- "业务系统内部确认后协同" --> GPC
  GFIS -- "执行回执" --> Evidence
  GPC -- "协同回执" --> Evidence
  Evidence --> Close
  Review --> Brain
  Brain -- "更新后的 SOP / 规则上下文" --> Rule

  classDef detect fill:#fff4df,stroke:#c18424,color:#49300a;
  classDef casec fill:#e8f3ff,stroke:#2878c8,color:#0f2f4f;
  classDef approve fill:#f1edff,stroke:#7657c6,color:#28194c;
  classDef execute fill:#ecf8ef,stroke:#2f8f4e,color:#123d21;
  class Rule,Event,AIWarn detect;
  class EXC,Grade,Owner,Task,Resolve,Review,Close casec;
  class Suggest,L3,L4,Reject approve;
  class GFIS,GPC,Evidence,Brain execute;
```

闭环要求：

1. 每个异常必须有来源系统和来源记录，不能只有口头描述。
2. AI 建议必须带证据引用、风险等级和置信度。
3. L3 建议需要 GFIS/GPC 业务确认引用，L4 治理事项需要 WAES/Harness 治理授权。
4. 执行结果必须由 GFIS/GPC 主责系统返回回执。
5. 关闭异常必须有证据台账和复盘结论。
6. 复盘结论进入 Brain 后，才能成为后续 SOP 或 RAG 上下文候选。
