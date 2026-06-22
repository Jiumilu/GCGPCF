---
doc_id: GPCF-DOC-475051A08A
title: GlobalCloud 绿色供应链体系项目群架构图
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD, XiaoG, GPCF, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂项目群架构图.md
source_path: 01-architecture/GlobalCloud智慧工厂项目群架构图.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系项目群架构图

日期：2026-06-07
口径：基于当前项目群定位，表达三层主架构、数据/事件流、AI 辅助边界和工程治理关系。原“智慧工厂”归入生产与执行层/工厂执行子域。

当前阅读口径：

1. 平台主线系统看 `GPC`。
2. `WAES` 是治理平面，不是业务主账。
3. `GFIS` 是工厂事实平面。
4. 宪法内容以治理门禁方式进入图中，不单独形成业务平台。

专项实施架构见：[GlobalCloud智慧工厂专项架构图集.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智慧工厂专项架构图集.md)

```mermaid
flowchart TB
  subgraph GOV["治理与监控层"]
    Harness["GlobalCloud 开发控制台<br/>Harness Engineering<br/>项目注册 / Manifest / 验收 / 状态纪律"]
    WAES["GlobalCloud WAES<br/>跨系统控制塔 / Agent Desktop<br/>规则 / 证据 / 状态治理<br/>指标 / 风险 / 异常 / 复盘"]
    Brain["GlobalCloud Brain<br/>长期知识库 / SOP / RAG<br/>案例 / 标准 / 质量与物流知识"]
    XiaoC["GlobalCloud XiaoC（蚁后）<br/>Prompt / MCP / 模型路由<br/>Agent 模板 / 任务拆解 / 汇总评估"]
    Hermes["GlobalCloud XiaoG Agent<br/>Hermes WebUI<br/>轻量执行入口 / 后台任务 / 会话工具"]
    XGD["GlobalCloud XGD（大象）<br/>长程 Agent / 重分析<br/>桌面 / 语音 / 社交 / Brain UI"]
  end

  subgraph OPS["运营与协同层"]
    GPC["GlobalCloud GPC<br/>轻量绿色供应链协同平台<br/>TMS / SRM协同 / CRM协同 / 外部协同<br/>预约 / 车辆 / 在途 / 签收 / 回单"]
    Odoo["Odoo GPC 原型<br/>历史样本 / 可选 back-office connector<br/>不再作为主架构底座"]
    PVAOS["GlobalCloud PVAOS<br/>价值联盟门户<br/>组织 / 项目 / 伙伴 / 客户接入"]
  end

  subgraph EXEC["生产与执行层"]
    Field["现场设备与作业资源<br/>PLC / DCS / CNC / 传感器 / 仪表<br/>AGV / 叉车 / 产线 / 月台"]
    Edge["边缘采集层<br/>OPC UA / MQTT / 工业网关<br/>边缘缓存 / 断网续传"]
    GFIS["GlobalCloud GFIS<br/>单厂本地第一执行系统<br/>MES / QMS / WMS / LES / EAM<br/>工单 / 质量 / 库存 / 发货事实"]
    LocalOps["本地运行控制台<br/>生产 / 质量 / 仓储 / 设备 / 物流"]
  end

  Field --> Edge
  Edge --> GFIS
  GFIS --> LocalOps

  GFIS -- "确认事件<br/>订单 / 工单 / 质检 / 库存 / 发货" --> WAES
  GFIS -- "发货出库 / 产能 / 库存 / 质量状态" --> GPC
  GPC -- "订单协同 / 到货预约 / 运输 / 签收回单" --> GFIS
  Odoo -. "可选 back-office 集成" .-> GPC
  PVAOS -- "组织 / 项目 / 伙伴 / 客户入口" --> GPC
  PVAOS -- "生态协作状态" --> WAES

  WAES -- "只读看板 / 风险 / 治理 / 证据" --> Hermes
  WAES -- "治理待办 / 预警 / 证据结果" --> XGD
  Brain -- "SOP / 规则 / 案例 / 知识上下文" --> XiaoC
  XiaoC -- "Agent Prompt / MCP / 模型路由 / 任务拆解" --> Hermes
  Hermes -- "日报 / 异常摘要 / 建议草案" --> WAES
  XGD -- "长程分析 / 语音查询 / 异常上报 / 现场提醒" --> Hermes

  Harness -. "工程边界 / 命令入口 / 验收证据" .-> GFIS
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> GPC
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> PVAOS
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> WAES
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> Brain
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> XiaoC
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> Hermes
  Harness -. "工程边界 / 命令入口 / 验收证据" .-> XGD

  classDef execution fill:#e8f3ff,stroke:#2878c8,stroke-width:1px,color:#0f2f4f;
  classDef platform fill:#ecf8ef,stroke:#2f8f4e,stroke-width:1px,color:#123d21;
  classDef tower fill:#fff4df,stroke:#c18424,stroke-width:1px,color:#49300a;
  classDef ai fill:#f1edff,stroke:#7657c6,stroke-width:1px,color:#28194c;
  classDef gov fill:#f5f5f5,stroke:#555,stroke-width:1px,color:#222;

  class Field,Edge,GFIS,LocalOps execution;
  class GPC,PVAOS,Odoo platform;
  class WAES tower;
  class Brain,XiaoC,Hermes,XGD ai;
  class Harness gov;
```

## 读图口径

1. **GFIS 是单厂执行事实源**：生产、质量、库存、设备、发货等最终业务事实归 GFIS。
2. **GPC 是跨企业协同平台**：供应商、客户、运输、签收、公共服务和绿色供应链协同归 GPC；Odoo GPC 仅保留为历史原型或可选 back-office connector。
3. **WAES 是治理与监控中枢和证据平面**：聚合指标、风险、治理规则、证据，不审批具体事务，不直接改写生产主账。
4. **Brain/XiaoC（蚁后）/Hermes/XGD（大象） 是 AI 支撑层**：Brain 提供知识，XiaoC 负责能力生产、模型路由、任务拆解和汇总，Hermes/XGD 承载长程 Agent、重分析和多端交互。
5. **Harness 是工程治理底座**：约束所有项目的边界、命令、验证、人工确认和状态纪律。
6. **四流是横向校验口径**：治理流约束业务流，业务流产生数据流，数据流支撑治理流，AI 服务流消费数据流并受治理流约束。
7. **连接器、SOP、AI、数据治理、多厂协同和 Edge 安全已有专项合同/模型**：项目群图只表达关系，落地细节以专项文档为准。

## 授权边界

```mermaid
flowchart LR
  L1["L1 查询 / 报表<br/>可自动执行"] --> L2["L2 预警 / 提醒<br/>可自动提醒"]
  L2 --> L3["L3 建议 / 草案<br/>人工确认"]
  L3 --> L4["L4 治理授权<br/>规则 / AI授权 / 证据 / 状态"]
  L4 --> L5["L5 安全关键控制<br/>AI 不得接管"]

  AI["Brain / XiaoC / Hermes / XGD（大象）"] -. "只能到 L1-L3 默认能力" .-> L3
  WAES["WAES 治理与证据台账"] -. "承接 L4 治理授权" .-> L4
  GFIS["GFIS / GPC 主责系统"] -. "承接具体事务确认" .-> L4
```
