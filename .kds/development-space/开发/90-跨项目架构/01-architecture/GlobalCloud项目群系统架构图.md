---
doc_id: GPCF-DOC-GROUP-SYSTEM-ARCHITECTURE-20261017
title: GlobalCloud 项目群系统架构图
project: GPCF
related_projects: [WAS, XWAIL, AAAS, WAME, WAE, GFIS, GPC, PVAOS, PQC, KDS, GCMEM, Brain, PKC, MMC, XiaoC, XiaoG, XGD, SOP, ICP, SpaceAI, SpaceAIStudio, World, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群系统架构图.md
source_path: 01-architecture/GlobalCloud项目群系统架构图.md
sync_direction: bidirectional
last_reviewed: 2026-10-17
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群系统架构图

日期：2026-10-17　状态：controlled v1.0（2026-10-17 老卢审阅确认转正）
口径：覆盖项目群当前纳入的 **23 个纳管项目**（加 GPCF 治理仓共 24 个仓库；2026-10-16 口径，含 2026-10-10 新增 PQC/SpaceAI/SpaceAIStudio、2026-10-12 新增 WAE、2026-10-16 新增 World 与 GCMEM；`GlobalCloud 项目群总体方案` 的 related_projects 与 §2 清单在 WAE/World 上存在口径差异，本图以 GPCF `projects/` 目录实况为准），继承 `GlobalCloud 项目群总体方案` 与 `GlobalCloud 项目群实施方案` 双总控，吸收 2026-10-12 WAS 命名修订（WAME 合并、WAE 移交）与 2026-10-16 第九流「场景流」裁定。

本文是 2026-06-07 版项目群架构图（`GlobalCloud智慧工厂项目群架构图.md`、`GlobalCloud绿色供应链体系最新架构图.md`）的**全量完成形态**：原图只覆盖 11 个项目，本文补入 WAS 语义契约体系、WAS 运行时链（WAME 引擎/World/CWME/WAE）、知识工程链（KDS/GCMEM/Brain/PKC）、产业控制平面（ICP）、包装业务（PQC）与安防桌面域（SpaceAI/SpaceAIStudio）。

## 1. 分层模型与横切面

| 层 | 名称 | 项目 | 一句话职责 |
|---|---|---|---|
| L0 | 品牌与宪法 | GlobalCloud 宪法（KDS 保管正本、ICP 主责产业领域、GPCF 传导、WAME/人工裁决） | 最高规范性权威 |
| L1 | 统一入口层 | WAE | 统一界面框架与统一入口，只统一界面层，不掌业务主账 |
| L2 | 治理与授权层 | WAME（平台面）、GPCF、MMC、SOP（流引擎中心）、ICP | 治理、证据、授权、状态裁决与项目群控制 |
| L3 | 平台协同层 | GPC、PVAOS、PQC、AaaS/SCaaS | 跨组织协同、生态入口、商业交付与包装运营 |
| L4 | 生产执行层 | GFIS、Edge/OT | 单厂事实源与现场接入 |
| L5 | 知识与数据层 | KDS、GCMEM、Brain、PKC、结构化 DB 域 | 知识主存、长期记忆、知识 UI 与结构化数据 |
| L6 | AI 能力层 | XiaoC（蚁后）、XGD（大象）、XiaoG（蚂蚁/Hermes） | AI 能力生产、编排路由与受权执行 |
| L7 | 工程研发底座 | Studio、Harness Engineering（规范仓 MMC） | 研发、治理、发布与验收纪律 |
| — | 横切面 A | WAS/Ontology/XWAIL | 语义契约体系：定义体系 → 定义语义 → 定义契约 |
| — | 横切面 B | WAME（引擎面）、World、CWME | WAS 运行时链：引擎 → 世界运行时 → 域实现 |
| — | 横切面 C | 四流（治理流/业务流/数据流/AI 服务流） | 跨层交互约束模型 |
| — | 旁挂域 | SpaceAI、SpaceAIStudio | 安防桌面域：统一重构工作区（BFF/桌面/插件）+ 空间智能工作台，独立纳管，partial |

## 2. 主图：项目群全景系统架构图

> 可视化形态：[GlobalCloud项目群架构图_20261017_v1.0.html](./GlobalCloud项目群架构图_20261017_v1.0.html)（蓝图风拍板图，结构对标 AaaS_项目群架构图_20261017_v1.0.html；本文件 mermaid 图为其规范源）。

```mermaid
flowchart TB
  CON["GlobalCloud 宪法<br/>产业模型总纲·最高规范性权威"]

  subgraph L1["L1 统一入口层"]
    WAE["WAE 世界资产浏览器<br/>统一界面框架·统一入口<br/>ui-tokens·ui-kit·app-shell·app-registry<br/>host-kit：写门禁·idp·装配态"]
  end

  subgraph L2["L2 治理与授权层"]
    GPCF["GPCF 项目群治理中枢<br/>双总控·Feature·LOOP<br/>Evidence Gate·状态传导"]
    WAMEG["WAME 治理平台面<br/>受理器·证据·策略·授权·发布<br/>运行视图·AaaS 治理入口"]
    MMC["MMC 治理中枢·控制面运行时<br/>规范模板·API/模型 Registry<br/>Adapter Gateway·统一 SDK"]
    SOP["SOP · 流引擎中心<br/>全流定义·规则装配·会话治理<br/>流规则包下发·规则候选晋升"]
    ICP["ICP 产业控制平面 candidate<br/>24字产业模型·十一池只读投影<br/>场景编排·决策候选"]
  end

  subgraph L3["L3 平台协同层"]
    GPC["GPC 绿色供应链公共服务平台<br/>订单池·七池·虚拟工厂<br/>流规则包消费·TMS/SRM/CRM 协同"]
    PVAOS["PVAOS 价值联盟门户<br/>租户·组织·伙伴·项目·工作流"]
    PQC["PQC 包装报价成本系统<br/>成本引擎·三级审批·回款"]
    AAAS["AaaS / SCaaS<br/>服务包·订阅·计量·SLA·证据"]
  end

  subgraph L4["L4 生产执行层"]
    GFIS["GFIS 单厂事实源<br/>ERP·MES·QMS·WMS·EAM<br/>经营台账"]
    EDGE["Edge / OT<br/>OPC UA·MQTT·工业网关<br/>PLC·DCS·AGV·仪表"]
  end

  subgraph L5["L5 知识与数据层"]
    KDS["KDS 知识主存 canonical<br/>OKF·四空间·十一池<br/>RAG 准入"]
    GCMEM["GCMEM 长期记忆<br/>append-only 账本·语义检索<br/>四端共用·夜间挖掘"]
    BRAIN["Brain 知识 UI WiIKI<br/>语义检索·知识图谱<br/>高级工作台"]
    PKC["PKC 个人知识工作台<br/>仪表盘·任务·通知"]
    DB["结构化 DB 域<br/>业务主账·治理审计·指标时序<br/>知识元数据·读模型"]
  end

  subgraph L6["L6 AI 能力层"]
    XIAOC["XiaoC 蚁后<br/>Prompt·MCP·模型路由<br/>任务拆解·汇总评估"]
    XGD["XGD 大象<br/>长程 Agent·重分析<br/>TICK·多端交互"]
    XIAOG["XiaoG 蚂蚁 Hermes<br/>live API·通知·审计<br/>跨系统操作执行"]
  end

  subgraph L7["L7 工程研发底座"]
    STUDIO["Studio 研发治理发布工作台<br/>Vue·Koa·Electron"]
    HARNESS["Harness Engineering<br/>Manifest·验收·状态纪律<br/>规范仓 MMC"]
  end

  subgraph WASX["横切 A：WAS 语义契约体系"]
    WASN["WAS 语义基座<br/>三层资产·八维·九流·生命周期"]
    ONT["Ontology 语义本体<br/>概念·关系·词表·约束·推理"]
    XWAIL["XWAIL 机器契约<br/>Schema·Profile·Validator·XAP"]
  end

  subgraph RT["横切 B：WAS 运行时链"]
    WAMEE["WAME 引擎面 not_implemented<br/>资产主账·模型注册·事件·关系<br/>策略·证据·计量·运行底座"]
    WORLD["World 世界运行时<br/>世界状态·投影·授权上下文<br/>模拟推演·Agent 实例"]
    CWME["CWME 域引擎实现<br/>城市/园区/空间域<br/>资产查找·视频巡检·警情处置"]
  end

  subgraph SIDE["旁挂域：安防桌面·独立纳管"]
    SPACEAI["SpaceAI 安防统一重构工作区<br/>BFF·桌面·插件·CWME 场景应用<br/>Vue3·Tauri2"]
    SAIST["SpaceAI Studio 空间智能工作台<br/>原 C# WinForms 宿主·Tauri 重构<br/>敏感文件仅本地"]
  end

  CON --> WASN
  WASN <--> ONT
  ONT <--> XWAIL
  XWAIL --> WAMEE
  WAMEE --> WAMEG
  WAMEE --> WORLD
  WORLD <--> CWME
  WORLD --> WAE

  WAE -. "界面承载各项目应用" .-> GPC
  WAE -. "界面承载" .-> PVAOS
  WAE -. "界面承载" .-> BRAIN
  WAE -. "界面承载" .-> WAMEG

  GPCF -. "双总控·门禁·LOOP 传导" .-> WAE
  GPCF -. "方案继承与回传" .-> GPC
  GPCF -. "方案继承与回传" .-> GFIS
  GPCF -. "方案继承与回传" .-> KDS
  GPCF -. "方案继承与回传" .-> WAMEG

  WAMEG -. "治理门禁·授权·证据" .-> GPC
  WAMEG -. "治理门禁·授权·证据" .-> GFIS
  WAMEG -. "治理门禁·授权·证据" .-> PVAOS
  WAMEG -. "治理门禁·授权·证据" .-> PQC

  GPC <--> GFIS
  EDGE --> GFIS
  GPC --> PVAOS
  PQC --> PVAOS
  GFIS -- "事实·事件·证据" --> WAMEG
  GPC -- "订单·签收·异常·证据" --> WAMEG
  PVAOS -- "运行证据" --> WAMEG

  XWAIL --> AAAS
  AAAS --> WAMEG
  MMC -. "可信身份·跨服务授权" .-> BRAIN
  PKC -. "经 MMC Gateway 写回" .-> KDS
  GFIS -. "回读建议·不覆盖" .-> KDS
  GPC -. "知识引用" .-> KDS
  KDS <--> GCMEM
  KDS --> BRAIN
  KDS -. "RAG 导出" .-> XIAOC
  BRAIN --> XIAOC
  XGD --> XIAOC
  XIAOC --> XIAOG
  XIAOG -. "受权 API 执行" .-> GFIS
  XIAOG -. "受权 API 执行" .-> GPC
  XIAOG -. "受权 API 执行" .-> PVAOS
  XIAOG -. "通知" .-> PKC
  XIAOC -. "建议·草案·仅候选" .-> WAMEG

  ICP -. "十一池只读投影" .-> KDS
  ICP -. "匹配建议·不写事实" .-> GPC
  ICP -. "决策候选" .-> WAMEG
  SOP -. "SOP 版本·证据要求" .-> GPC
  SOP -. "SOP 执行依据" .-> GFIS

  HARNESS -. "Manifest·验收·状态纪律" .-> GPC
  HARNESS -. "Manifest·验收·状态纪律" .-> GFIS
  HARNESS -. "Manifest·验收·状态纪律" .-> WAMEG
  STUDIO -. "研发·治理·发布" .-> WAE
  STUDIO -. "研发·治理·发布" .-> GPC

  SPACEAI -. "独立纳管边界" .-> WAE
  SPACEAI -. "CWME 应用与归档" .-> CWME
```

## 3. 图2：WAS 世界资产产品链与运行时链

```mermaid
flowchart LR
  BRAND["GlobalCloud 品牌"] --> WAS["WAS 世界资产体系<br/>三层资产：基础资产/行业资产模型/场景资产包<br/>八维画像·九流·七阶段生命周期"]
  WAS --> ONT["Ontology 语义本体"]
  WAS --> XWAIL["XWAIL 机器契约<br/>Schema·Profile·Validator·XAP 包"]
  ONT <--> XWAIL
  XWAIL --> ENG["WAME 引擎面<br/>资产主账·模型注册·事件·关系<br/>策略·证据·计量·运行底座"]
  ENG --> PLAT["WAME 治理平台面<br/>受理器 xap-intake·授权·发布<br/>治理注册·运行视图"]
  ENG --> WORLD["World 世界运行时<br/>世界状态·投影·授权上下文<br/>模拟推演实验室"]
  WORLD <--> CWME["CWME 域引擎实现<br/>城市/园区/空间域"]
  PLAT --> AAAS["AaaS / SCaaS<br/>服务包·订阅·计量·SLA<br/>商业交付模式"]
  XWAIL --> AAAS
  WORLD --> WAE["WAE 世界资产浏览器<br/>统一界面框架（不属 WAS 产品链）"]
  WAE -. "界面层承载" .-> PLAT
  WAE -. "界面层封装" .-> WORLD
```

WAS 产品链口径（`GlobalCloud世界资产体系正式命名与产品系统架构总纲`）：

```text
WAS 定义体系 → Ontology 定义语义 → XWAIL 定义契约
→ WAME 负责运行、治理、发布和业务入口 → AaaS/SCaaS 服务化运营资产世界
```

`WAE` 不属于 WAS 产品链，是项目群级统一界面框架。

## 4. 图3：供应链业务流与治理闭环

```mermaid
flowchart TB
  subgraph EDGE["现场接入"]
    OT["PLC / DCS / AGV / 仪表"]
    EG["Edge 网关<br/>OPC UA·MQTT·缓存·断网续传"]
  end

  subgraph FACTORY["工厂执行（单厂本地）"]
    GFIS["GFIS 事实源<br/>ERP 闭环·MES·QMS·WMS·EAM<br/>经营台账"]
  end

  subgraph PLATFORM["平台协同"]
    PVAOS["PVAOS 门户<br/>租户·组织·伙伴·入口"]
    GPC["GPC 平台主线<br/>订单池·七池·虚拟工厂<br/>流规则包·ASN·预约·TMS·POD·异常"]
    PQC["PQC 包装业务<br/>报价·成本·采购·回款"]
  end

  subgraph GOV["治理闭环"]
    WAME["WAME 治理平台<br/>受理器·证据·状态门·AI 授权门"]
    SOP["SOP 流引擎中心<br/>G0-G8 轻量闸门·周评分"]
    KDS["KDS 知识引用源<br/>客户·订单·合同·交付·回款"]
  end

  OT --> EG --> GFIS
  PVAOS --> GPC
  GPC <--> GFIS
  GFIS -- "发货·签收·质量·库存·产能" --> GPC
  GPC -- "平台订单·到货预约·SOP 段·调度建议" --> GFIS
  PQC -. "运营数据归属 PVA" .-> PVAOS
  GFIS -- "事实·单据·事件·证据" --> WAME
  GPC -- "签收·异常·周评分·证据" --> WAME
  SOP -. "SOP 版本·证据要求" .-> GPC
  SOP -. "SOP 执行依据" .-> GFIS
  WAME -. "治理规则·证据门·状态门·授权门" .-> GPC
  WAME -. "治理规则·证据门·状态门·授权门" .-> GFIS
  GPC -. "知识引用" .-> KDS
  GFIS -. "回读建议·不覆盖" .-> KDS
```

读图口径：GPC 负责平台协同、GFIS 负责工厂执行、WAME 负责治理约束、PVAOS 负责生态入口、Edge 负责现场接入；PQC 是 PVA 运营侧包装报价成本业务系统，不替代 KDS 主存、GFIS 工厂执行或 WAME 治理。

## 5. 图4：知识工程链 GKE-001

```mermaid
flowchart LR
  GPCF["GPCF 控制面<br/>模型定义·词表·兼容规则"] -->|"KnowledgeObject 正本"| KDS["KDS 知识事实主存<br/>OKF·四空间·十一池"]
  KDS <-->|"append-only 账本<br/>_meta/hermes-memory-log.md"| GCMEM["GCMEM 长期记忆<br/>四端共用·语义检索·夜挖"]
  KDS -->|"RAG 导出·证据检索"| BRAIN["Brain 受控分析与候选<br/>WiIKI 工作台"]
  MMC["MMC<br/>可信身份·跨服务授权"] --> BRAIN
  KDS --> PKC["PKC 个人工作台<br/>任务·通知·协同"]
  BRAIN -->|"候选结果"| STUDIO["Studio 用户任务·人工复核"]
  STUDIO -->|"确认后按授权写回"| KDS
  WAME["WAME / 人工<br/>授权与状态裁决"] -. "授权门" .-> BRAIN
  WAME -. "授权门" .-> STUDIO
  GFIS["GFIS / GPC / PVAOS<br/>业务权威主数据"] -. "知识输入·证据镜像" .-> KDS
```

GKE-001 单一责任链：GPCF 定义 → KDS 主存 → Brain 消费 → MMC 调用 → WAME/人工授权。任何系统不得建立平行资料、证据、审计或长期记忆主账；任何 AI 结果在确认前只能是 `candidate`。当前工程状态固定为 `active / partial / not_complete`。

## 6. 图5：AI 三层 Agent 体系与授权边界

```mermaid
flowchart TB
  XGD["XGD 大象<br/>长程 Agent·重分析·全局调度<br/>TICK 驱动·多端交互"]
  XIAOC["XiaoC 蚁后<br/>Prompt·MCP·模型路由<br/>任务拆解·分发·汇总评估"]
  XIAOG["XiaoG 蚂蚁 / Hermes<br/>本地执行·live API<br/>跨系统操作代理"]
  BRAIN["Brain 知识上下文<br/>SOP·案例·复盘"]
  SYS1["GFIS 工厂事实"]
  SYS2["GPC 平台协同"]
  SYS3["PVAOS 门户"]
  SYS4["PKC 个人面板"]
  WAME["WAME 治理<br/>AI 授权·越权拦截·审计"]

  BRAIN --> XIAOC
  XGD -->|"复杂任务分解"| XIAOC
  XIAOC -->|"子任务分发"| XIAOG
  XIAOG -->|"受权 API 调用"| SYS1
  XIAOG -->|"受权 API 调用"| SYS2
  XIAOG -->|"受权 API 调用"| SYS3
  XIAOG -->|"通知推送"| SYS4
  XIAOG -->|"运行记录·审计日志"| WAME
  XIAOC -. "建议/摘要/预警/复盘草案" .-> WAME
  WAME -. "工具授权范围" .-> XIAOG
```

```mermaid
flowchart LR
  L1["L1 查询/报表<br/>可自动执行"] --> L2["L2 预警/提醒<br/>可自动提醒"]
  L2 --> L3["L3 建议/草案<br/>人工确认"]
  L3 --> L4["L4 治理授权<br/>规则/AI 授权/证据/状态"]
  L4 --> L5["L5 安全关键控制<br/>AI 不得接管"]
  AI["Brain / XiaoC / XGD / XiaoG"] -. "默认只到 L1-L3" .-> L3
  WAME["WAME 治理与证据台账"] -. "承接 L4" .-> L4
  GFIS["GFIS / GPC 主责系统"] -. "承接具体事务确认" .-> L4
```

## 7. 图6：四流交互总图

```mermaid
flowchart TB
  subgraph GF["治理流"]
    G1["WAME 项目发起"]
    G2["模板启用/规则生效"]
    G3["指标口径/状态升级"]
    G4["证据确证/阶段验收"]
    G5["AI 授权/Agent 工具权限"]
    H["GPCF LOOP + Harness<br/>工程边界·Manifest·验收纪律"]
  end

  subgraph BF["业务流"]
    P["PVAOS 组织/项目/伙伴/门户"]
    C["GPC 订单/样品/转量产/ASN/预约/运输/POD/异常"]
    F["GFIS 配方/打样/工单/质量/库存/批次/LES/EAM/发货"]
    Q["PQC 报价/成本/采购/回款"]
    E["Edge 采集/转换/缓存/回执"]
  end

  subgraph DF["数据流"]
    API["API Gateway"]
    CR["Connector Registry"]
    OI["Outbox / Inbox"]
    BUS["Event Bus"]
    EV["Evidence Ledger"]
    MT["Metric / Trace / Schema / DLQ / Replay"]
  end

  subgraph AF["AI 服务流"]
    B["Brain 知识/SOP/复盘"]
    X["XiaoC 蚁后 Prompt/MCP/路由/拆解"]
    A["XGD 大象 + XiaoG/Hermes Agent/执行"]
    S["AI 建议/摘要/预警/复盘草案"]
  end

  G1 --> P
  G1 --> C
  G1 --> F
  G2 -. "治理规则约束" .-> C
  G2 -. "治理规则约束" .-> F
  G5 -. "AI 授权约束" .-> A
  H -. "工程边界和验收纪律" .-> G1

  P --> C
  C <--> F
  Q --> P
  E --> F
  C --> API
  F --> API
  P --> API
  E --> API
  API --> CR --> OI --> BUS --> EV
  BUS --> MT
  EV --> G4
  MT --> G3

  EV --> S
  MT --> S
  B --> X --> A --> S --> G5
  S -. "不能直接写业务事实" .-> C
  S -. "不能直接写业务事实" .-> F
```

四流口径：治理流约束业务流，不替代业务流；业务流产生事实和事件，不把 WAME 作为业务主账；数据流承载跨系统事实、证据、指标和追踪，不共享业务数据库；AI 服务流消费数据流、受治理流授权，输出建议草案，不写业务事实。

## 8. 项目-架构角色映射矩阵（23 纳管项目 + GPCF）

| # | 项目 | 架构层 | 主责 | 关键模块 | 对外数据流 | 就绪度（2026-10-17 口径） |
|---|---|---|---|---|---|---|
| 1 | WAS | 横切 A·语义基座 | 总体语义、架构与治理基线 | 三层资产·八维·九流·生命周期；OKF 契约层 + 11 validator | 读 KDS/GPCF；输出语义边界 → XWAIL/WAME/RAG | controlled，治理准入中；P0 落地，P1-P3 骨架 |
| 2 | XWAIL | 横切 A·契约 | 机器建模语言、契约、验证 | Schema·Profile·Validator·XAP 包·CLI 校核 | 读 WAS/Ontology；契约 → WAME 受理器/AAAS/Studio | draft/in_progress；V1.2 规则 PoC |
| 3 | AAAS | L3·商业交付 | 资产服务化、计量、SLA、证据要求 | ServicePackage·Metering·SLA/SLO·EvidenceRequirement·商业状态机 | 读 XWAIL/WAME 状态；服务包 → WAME 治理入口/SCaaS | baseline；服务包定义与样例 |
| 4 | WAME | L2 平台面 + 横切 B 引擎面 | 资产主账、运行引擎、治理执行、授权发布 | 受理器 xap-intake·主账·模型注册状态机·事件·关系·策略·证据·计量·Agent Desktop | 读 WAS/XWAIL/各业务只读；发布签名制品 → PVAOS | 引擎面 not_implemented；平台面 partial（受理器参考实现可用） |
| 5 | WAE | L1·统一入口 | 项目群统一界面框架与入口 | ui-tokens·ui-kit·app-registry·app-shell·host-kit 写门禁/idp/装配态 | 界面承载各项目；写门禁默认关闭 | in_progress；框架实施中 |
| 6 | GFIS | L4·工厂事实源 | 单厂生产/质量/仓储/设备/台账第一执行主体 | ERP 闭环·MES·QMS·WMS·EAM·云端 SaaS 汇总层 | → GPC 产能/库存/发货/签收；→ WAME 事实证据；→ KDS 回读建议 | ready_for_human_acceptance（96/100） |
| 7 | GPC | L3·平台主线 | 绿色供应链公共服务与协同 | 七池·虚拟工厂·流规则包消费·GPC 平台对象模型（PlatformOrder/Shipment/POD/ExceptionCase）·工厂适配器 | ↔ GFIS 订单/事件；→ PVAOS；→ WAME 事件证据 | ready_for_review；平台对象模型 Phase 0/1 |
| 8 | PVAOS | L3·生态入口 | 价值联盟门户与运营底座 | 门户·租户/组织/权限·伙伴·项目空间·工作流·PVAAI | ← GPC/GFIS/WAME 展示；→ AaaS 订阅计量 | ready_for_review；跨项目接口 implementation_pending |
| 9 | PQC | L3·包装运营 | 报价成本、采购、订单回款 | 统一口径表·成本引擎·参数审批·报价快照·三级审批·9 表 | ← KDS 案例只读；→ PVA 运营侧 | partial；工程验证通过，业务验收未确认 |
| 10 | KDS | L5·知识主存 | 知识事实主存与证据镜像（canonical） | OKF·四空间·十一池·SPACE_REGISTRY·可信治理内核 | ← GPCF 文档镜像；→ Brain/XiaoC RAG；← GCMEM 账本；← MMC Gateway（PKC/Brain 授权写回） | ready_for_human_acceptance（95/100） |
| 11 | GCMEM | L5·长期记忆 | 跨会话长期记忆（替代 mem0） | gcmem 核心库·MCP server·REST API 19090·管理台·夜挖 | ↔ KDS 唯一账本；四端（Hermes/Codex/Reasonix/DSH）共用 | active；v1.5.x |
| 12 | Brain | L5·知识 UI | 知识治理、语义检索、智能分析 UI | WiIKI 工作台·知识图谱·gbrain 检索（pgvector/Ollama）·面板契约 | ← KDS canonical；→ WAME/GPCF 门禁状态 | ready_for_review；authorization_boundary |
| 13 | PKC | L5·个人工作台 | 个人知识、任务与协同 | 仪表盘·任务·AgentRuns·Ask；SDK kds-client/mmc-llm | ← KDS personal 空间；写经 MMC Gateway 回 KDS | in_progress |
| 14 | MMC | L2·治理模板 + 控制面运行时 | 治理模板、模型管理与复用控制、API/模型注册 | 规范/模板/验收清单·openspec；控制面运行时 Gateway·API Registry·LLM Registry·PermissionGuard（FastAPI :8000）·统一 SDK | → 全项目下发规范/注册表/SDK；Brain/PKC 经 MMC Gateway 调 KDS | complete（Ph1，12/12 evidence） |
| 15 | XiaoC | L6·蚁后 | AI 能力生产、模型路由、任务拆解 | Prompt 工程·MCP·模型路由·Agent 模板·l4 编排 | ← Brain 知识；→ XiaoG 分发；→ WAME 草案 | partial（历史口径 78/100） |
| 16 | XGD | L6·大象 | 长程 Agent、重分析、多端交互 | TICK 主循环·双层思考·记忆系统（SQLite+向量）·焦点栈·Brain UI | → XiaoC 任务分解；→ WAME 建议草案 | not_started（2026-06-10 首轮纳入口径） |
| 17 | XiaoG | L6·蚂蚁 | 轻量执行、live API、通知、审计 | Hermes Studio：Vue3 控制台·Koa BFF·Electron·八平台渠道·Cron/语音 | 受权执行 → GFIS/GPC/PVAOS/PKC；→ WAME 审计 | ready_for_review |
| 18 | SOP | L2·流引擎中心 | 项目群唯一流引擎：全流（业务/开发）定义、规则装配、会话治理、流规则包下发 | schemas·sop/matrix·scripts 基线·会话收口·flow-registry（规划中） | ← KDS 唯一事实源；→ GPC/GFIS 下发流规则包；→ WAME/MMC/GPCF 证据 | P1 最小可运行基线，流引擎中心升级中（2026-10-17 裁定） |
| 19 | GPCF | L2·项目群治理 | 治理、文档、证据、门禁、LOOP 编排 | 双总控·features 体系·Evidence Gate·LOOP·09-status 台账 | → KDS 开发空间镜像；→ 各项目方案传导 | 活跃；F-001~F-024 |
| 20 | ICP | L2·产业控制 | 24 字产业模型、场景编排、决策候选 | IndustryModel·ResourcePoolProjection·ScenarioPackage·ControlDecisionCandidate·FastAPI | ← KDS 十一池只读；→ SOP/WAME/GPCF；→ GPC/GFIS/PVAOS 建议 | candidate / partial / human_required |
| 21 | SpaceAI | 旁挂域 | 安防监控平台统一重构 + CWME 场景运营应用 | apps/desktop（Tauri2+Vue3）·apps/server（Koa BFF·SSE）·packages/protocol（52 端点）·domain（32 模型）·plugin-sdk·plugins（设备/报警/巡更/门禁）·mobile-shell·apps/city-model | ↔ World（CWME 空间域）；BFF 注册 MMC 能力目录；契约归 XWAIL；ONVIF/RTSP/GB28181 设备接入 | partial/in_progress（BFF :39010 运行；业务验收未确认） |
| 22 | SpaceAIStudio | 旁挂域 | 空间智能工作台（与 Studio 平行，不合并） | 遗留 C# WinForms 宿主（12 模块）；重构 apps/desktop（Vue3+Tauri2+Cesium 三维 GIS） | 独立边界；与 SpaceAI/Studio 互不写入 | partial（registered；P0-P5 已交付，待人工验收） |
| 23 | World | 横切 B·世界运行时 | 世界状态、投影、授权上下文、模拟推演 | 世界模型投影·组织与 Agent·动态授权上下文·模拟实验室·统一工作台 | ← WAME 引擎能力；← KDS 事实；→ WAE 封装；↔ CWME | partial；中央文档门禁 rework_required |
| 24 | Studio | L7·工程研发底座 | 研发、治理和发布工作台（Hermes Web UI 形态） | Vue3 client（:8649）·Koa server（:8647）·Electron·features 管理·kds-sync LOOP 门禁 | 读 KDS（真实写需显式授权）；LOOP 证据经 WAME/GPCF 门禁；gcworld 模块 2026-10-17 已迁出至 World | LOOP 驱动，无静态状态 |

> 未纳入项目群 23 项目清单的仓：`GlobalCloud FireQuote`（消防定额测算平台，独立业务 MVP；GPCF `config/project-group-projects.yaml` 与 `projects/` 均无其条目，仅自管本地 Manifest）、`GlobalCloud SpaceAI Platform`（与 SpaceAI 同远端 GCSpaceAI 的统一重构主工作区，即 registry `spaceai` 条目承载地）、`GlobalCloud Studio-release0`（Studio 旧发行基线）、`_worktree-archive-20261012`（历史 worktree 归档），不进入本图主结构。

## 9. 读图口径与不越权声明

1. **一个总控体系**：项目群总体方案 + 项目群实施方案为双主控，所有项目方案必须继承并回传。
2. **WAS 语义契约体系是横切面**：不为任一业务层提供事实源；GFIS/KDS/十一池写回必须先过 WAS 语义与 WAME 门禁。
3. **WAME 是治理与授权平面**：不承办工单、质量、库存、发货、签收等具体事务审批；治理面（WAME）与运行面（PVAOS）共享契约不共享数据库。
4. **KDS 是唯一知识事实源**：Brain 是 UI，GCMEM 是记忆账本，均不建立第二主账；跨空间默认引用或脱敏投影。
5. **AI 只到 L1-L3**：AI 服务流只能生成建议、摘要、预警和复盘草案，不能直接写业务事实或正式知识版本；L4 治理授权归 WAME 与人工，L5 安全关键控制 AI 不得接管。
6. **ICP 固定 candidate/partial/human_required**：不拥有业务事实写入权、治理批准权或生产执行权。
7. **WAE 只统一界面层**：不接管任何项目的业务主账、治理裁决权或事实源；写门禁默认关闭。
8. **非声明边界**：本文不声明任一系统已实现、已集成、已交付或已验收；不声明 XWAIL/WAME/WAE 达到 `production_ready`；不声明真实业务闭环、客户验收或商业上线完成。未经人工确认，不得声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## 10. 承接关系与裁定记录

| 既有文档 | 关系 |
|---|---|
| `GlobalCloud智慧工厂项目群架构图.md`（2026-06-07，11 项目） | 已由本文承接，登记为历史基线（superseded；2026-10-17 老卢裁定） |
| `GlobalCloud绿色供应链体系最新架构图.md`（2026-06-07） | 已由本文承接，登记为历史基线（superseded；2026-10-17 老卢裁定） |
| `GlobalCloud世界资产体系正式命名与产品系统架构总纲.md`（2026-10-12） | 本文图2 为其完整展开 |
| `GlobalCloud体系最小闭环与三阶段激活深度总表.md` | 分层与激活深度口径来源 |

裁定记录（2026-10-17，老卢「全部同意」）：

1. 旧两版项目群架构图登记为历史基线、由本文承接——**已执行**：`09-status/document-deprecation-register.md` 登记，两份旧文档 frontmatter `status=archive`、`superseded_by` 指向本文，文档控制总台账与目录清单同步为 archive。
2. SpaceAI 中央台账——**核实已闭环**：`projects/spaceai/STATUS.md` v1.1（2026-10-16）已修正为「主项目 = SpaceAI Platform；本目录为 CWME 归档与本地应用区」，与本文图口径一致，无需再改；`/tmp/gcspaceai-backup` 疑似凭据脱敏事项由该 STATUS 台账继续跟踪。
3. 本文 status：draft v0.1 → **controlled v1.0**（2026-10-17 老卢确认）。
