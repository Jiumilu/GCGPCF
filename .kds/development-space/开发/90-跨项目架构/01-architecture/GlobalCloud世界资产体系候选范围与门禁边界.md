---
doc_id: GPCF-DOC-45A09FDDC2
title: GlobalCloud世界资产体系 WAE-WAES 与 SCaaS 关系门禁边界
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud世界资产体系候选范围与门禁边界.md
source_path: 01-architecture/GlobalCloud世界资产体系候选范围与门禁边界.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud世界资产体系 WAE-WAES 与 SCaaS 关系门禁边界

## 1. 定位与来源

本文件依据以下三份统一重构版 PDF 校准 WAS 在 GlobalCloud 项目群中的候选接入边界：

- `/Users/lujunxiang/Desktop/WAS总体规划V1.1_整体系统规划_统一重构版.pdf`
- `/Users/lujunxiang/Desktop/XWAIL可扩展世界资产信息建模语言规范V1.1_统一重构版.pdf`
- `/Users/lujunxiang/Desktop/资产即服务（AaaS）战略蓝图V1.1_XWAIL对齐统一重构版.pdf`

三份文件均采用 `WAS 统一语义基线 1.1.0`。本文件不是对 PDF 的全文复刻，而是把其中可执行的关系、边界、门禁和 GlobalCloud 接入要求沉淀为 GPCF 受控架构说明。

本轮最终确认命名基线：

```text
GlobalCloud 世界资产体系 = GlobalCloud 品牌下以 WAS 为产品体系总称的世界资产产品体系。
WAS = World Asset System。
AaaS = Assets as a Service。
SCaaS = Supply Chain as a Service。
```

其中 `GlobalCloud` 是品牌，`WAS` 是品牌下的产品体系总称，`XWAIL` 是 WAS 的主规范建模语言与机器契约，`AaaS` 是服务化交付模式与产品族，`SCaaS` 是 AaaS 在供应链行业的行业化架构。当前唯一切入口为 `GlobalCloud 绿色供应链体系`。

主项目归属固定为：

| 体系对象 | 主项目 | 说明 |
|---|---|---|
| WAS | WAS世界资产体系 | WAS 的主项目，承接世界资产体系理论、标准、总体规划和术语基线 |
| XWAIL | GlobalCloud XWAIL | XWAIL 的主项目，承接规范、Schema、Profile、Validator、模板、示例、迁移和一致性测试 |
| AaaS | GlobalCloud AaaS（本地目录：GlobalCloud AAAS） | AaaS 的主项目，承接服务包、订阅、商业交付、计量、SLA 和通用服务治理 |

本文件与以下新增文档共同构成本轮问答后的受控基线：

- `01-architecture/GlobalCloud世界资产体系正式命名与产品系统架构总纲.md`
- `01-architecture/XWAIL可扩展世界资产信息建模语言规范V1.2草案.md`

WAE 与 WAES 的正式定义：

| 名称 | 英文 | 中文 | 定位 |
|---|---|---|---|
| WAE | World Asset Engine | 世界资产引擎 | 世界资产体系的核心引擎、统一资产主账、XWAIL 注册、状态事件、关系图谱、策略、证据、计量和 AaaS 接入底座 |
| WAES | World Asset Explorer | 世界资产浏览器 | 基于 WAE 的业务实现，承载资产浏览、业务操作、场景应用、可视化、运营工作台、AaaS/SCaaS 治理平台和客户侧入口 |

WAE 是底层世界资产主账与引擎；WAES 是基于 WAE 的业务实现。历史文档中旧 `WAE = 浏览器/入口`、旧 `WAES = 主账/引擎` 的口径作废。历史文档中“接入 WAES”的表述，在新命名基线下应解释为：AaaS 及其子集接入 WAE 主账与引擎能力，并通过 WAES 形成业务可用入口、治理平台和场景实现。

一句话定位：

```text
WAS 定义资产世界，XWAIL 描述资产世界，AaaS 运营资产世界。
```

三者不是并列产品，而是世界资产体系内部从顶层体系到技术标准，再到商业服务的纵向链路。

绿色供应链体系是世界资产体系基于 AaaS 的行业场景架构，对内架构名为：

```text
SCaaS = Supply Chain as a Service = 供应链即服务
```

对外名称统一为：

```text
GlobalCloud 绿色供应链体系
```

因此，后续提到“绿色供应链体系”时，应优先理解为 GlobalCloud WAS 在供应链行业的 AaaS 场景实现，而不是独立于世界资产体系之外的另一套顶层体系。

## 2. 世界资产体系内部关系

| 层级 | 定位 | 回答的问题 | 当前 GlobalCloud 边界 |
|---|---|---|---|
| WAS | 世界资产体系与顶层架构 | 什么是资产，资产如何分类、关联、流动、演化和治理 | 作为跨项目资产语义基线候选，不替代 GFIS/GPC/PVAOS 主账 |
| XWAIL | 规范性建模语言与机器契约 | 如何把 WAS 定义的资产变成机器可读、可验证、可交换的模型 | 作为 schema、validator、XAP、接口契约和 CI 门禁候选 |
| AaaS | 服务化交付与商业运营模式 | 如何把已建模、可运行的资产能力提供给客户，并计量、收费和持续运营 | 作为未来服务目录、计量模型和商业闭环候选，不声明已上线 |

传导关系：

```text
WAS
定义三层资产、八维、八流、七阶段生命周期和治理原则
  ↓
XWAIL
编码为模型、关系、事件、状态机、策略、快照、证据和接口契约
  ↓
WAE
注册、连接、同步、孪生、分析、验证、快照、审计、世界资产主账和服务接入控制
  ↓
WAES
基于 WAE 的浏览、操作、运营、场景应用和业务工作台
  ↓
AaaS
封装为可订阅、可调用、可组合、可计量、可运营的服务
  ↓
业务结果
降本、提效、风控、增收、合规和价值证明
```

反向反馈：

```text
AaaS 运营数据与客户需求
  ↓
行业 Profile 与场景资产包修订
  ↓
XWAIL 扩展与验证规则完善
  ↓
WAS 理论和治理体系演进
```

## 3. WAS：顶层语义与治理基线

WAS 是三者的最高语义和治理基线。它不是单一资产管理软件，而是把现实世界、组织世界、数字世界和商业世界中的对象统一转化为可识别、可描述、可连接、可运行、可验证、可度量和可服务化资产的体系。

WAS 的统一对象模型为：

```text
资产 = 身份 + 元数据 + 八维画像 + 静态关系 + 八流行为 + 生命周期 + 策略权限 + 快照证据 + 服务接口
```

### 3.1 三层资产

| 层级 | 英文 | 说明 | 主要产物 |
|---|---|---|---|
| 基础资产 | Base Asset | 用统一八维、关系、状态与身份描述跨行业公共语义 | 核心 Schema、词表、模板 |
| 行业资产模型 | Industry Asset Profile | 在基础资产上叠加行业词表、规则、模板和价值路径 | 行业 Profile、规则包 |
| 场景资产包 | Scenario Asset Package | 将资产、流程、规则、服务与 KPI 封装成可复用解决方案 | XAP 场景包、应用模板 |

行业资产模型不得复制或改写基础语义，应通过 Profile、命名空间、约束和模板进行特化。场景资产包不得绕过行业和基础模型，应显式声明依赖、版本、接口、策略和 KPI。

### 3.2 八维资产画像

| 规范标签 | 中文 | 说明 |
|---|---|---|
| `PhysicalDimension` | 物理维 | 实体形态、规格、容量、材料、性能与物理能力 |
| `RuleDimension` | 规则维 | 法律、合同、制度、约束、业务规则与操作规程 |
| `IntellectualDimension` | 智力维 | 知识、专利、算法、设计、标准、经验与方法 |
| `DataDimension` | 数据维 | 数据结构、数据集、接口、质量、频率、血缘与语义 |
| `EconomicDimension` | 经济维 | 成本、价格、估值、收益、折旧、权益与风险 |
| `EnergyDimension` | 能源维 | 能源来源、容量、消耗、效率、碳排放与转换 |
| `OrganizationDimension` | 组织维 | 所有者、运营者、责任人、角色、权限与协作主体 |
| `SpaceTimeDimension` | 时空维 | 位置、坐标系、时间窗口、轨迹、有效期与历史状态 |

### 3.3 八流协同

| 规范标签 | 中文 | 说明 |
|---|---|---|
| `LogisticsFlow` | 物流 | 物料、商品、设备或实体载荷的移动 |
| `InformationFlow` | 信息流 | 消息、数据、事件、文档和知识的传递 |
| `FinancialFlow` | 资金流 | 支付、结算、融资、分账与资金转移 |
| `EnergyFlow` | 能量流 | 电、热、燃料等能源的输送、转换与消耗 |
| `ServiceFlow` | 服务流 | 能力调用、服务履约、工单与服务结果交付 |
| `ControlFlow` | 控制流 | 指令、策略、审批、编排与自动控制信号 |
| `ValueFlow` | 价值流 | 价值创造、增值、分配、消耗与归因 |
| `CreditFlow` | 信用流 | 信用、评分、担保、信任与履约声誉变化 |

边界：八维表达资产是什么和处于什么状态；八流表达资产如何与其他对象发生作用。`EconomicDimension` 描述某一时点的经济属性，`FinancialFlow` 描述真实资金转移；`EnergyDimension` 描述能源状态，`EnergyFlow` 描述能源输送和转换；`RuleDimension` 描述资产受到哪些规则约束，治理策略描述平台如何强制执行这些约束。

### 3.4 七阶段生命周期

| 阶段 | 中文 | 关键输出 |
|---|---|---|
| `Plan` | 规划 | 需求、边界、责任与价值假设 |
| `Design` | 设计 | 模型、接口、策略与验证计划 |
| `Build` | 构建 | 资产模型、连接器与测试资产 |
| `Deploy` | 部署 | 发布包、基线快照和上线审批 |
| `Operate` | 运营 | 实时状态、事件、SLA 与审计 |
| `Optimize` | 优化 | 策略、模型和运营持续优化 |
| `Retire` | 退役 | 停用、归档、权利与证据处置 |

任何状态转换必须由事件、超时或补偿动作驱动，并携带可追溯事件、参与者、关联编号和证据引用。

## 4. XWAIL：WAS 的机器契约

XWAIL 是 WAS 的工程化表达层。它把 WAS 的三层资产、八维、八流、七阶段生命周期和治理机制转化为机器可读、可验证、可交换的模型。

| WAS 概念 | XWAIL 表达 |
|---|---|
| 资产及资产集合 | `Assets`、`AssetGroup`、`AssetUnit` |
| 八维资产画像 | `Dimensions` 与八个 `*Dimension` 元素 |
| 静态资产关系 | `Relations` |
| 八流动态协同 | `was:FlowRelations`、`TriggerFlow`、`SideEffect` |
| 生命周期 | `was:StateMachines`、`State`、`Transition` |
| 外部系统连接 | `Integrations` |
| 安全与治理 | `SecurityProfile`、`policy:Governance`、`PolicyRef` |
| 行业复用 | `Templates`、`UseTemplate`、Profile、XAP |
| 快照与证据 | `was:Snapshots`、`Evidence`、双时态记录 |

XWAIL 的核心价值是把架构语义变成约束和门禁：

| 能力 | 要求 |
|---|---|
| 标识 | `id` 文档内唯一，`AssetURI` 跨文档和跨系统稳定，版本使用 SemVer |
| 命名空间 | 核心结构、WAS 扩展、治理策略、行业扩展必须分离 |
| 结构验证 | XSD / JSON Schema 校验元素、属性、类型、必填项和引用 |
| 业务验证 | Policy as Code 校验嵌套、循环关系、安全绑定、维流映射、生命周期完整性 |
| 错误治理 | 关键错误码需进入 CI/CD 和发布门禁，例如循环关系、安全缺失、嵌套超限、维流映射缺失 |

符合性等级：

| 等级 | 必须具备 | 适用场景 |
|---|---|---|
| Core | Metadata、Assets、唯一 ID、至少一个 Dimension、结构验证 | 目录、台账、静态建模 |
| Operational | Core + Relations + FlowRelations + StateMachine + Integration 安全绑定 | 数字孪生、流程协同、运营应用 |
| Trusted | Operational + Policy + Snapshot + Evidence + 签名/审计 + 双时态 | 跨组织协作、AaaS、合规与价值服务 |

## 5. AaaS：基于契约的服务化运营

AaaS 不是再创造一套资产模型，而是使用 WAS 与 XWAIL 统一后的资产对象，把资产模型、数据连接、数字孪生、智能分析、治理可信、价值度量和运营能力封装为可订阅、可调用、可组合、可计量的服务。

AaaS 的基本约束：

| 约束 | 要求 |
|---|---|
| 不另建模型 | 服务对象仍使用基础资产、行业资产模型和场景资产包三层结构 |
| 不替代客户系统 | 不替代 ERP、WMS、MES、SCADA 等系统，只建立统一资产语义和服务层 |
| 不跳过可信基础 | 身份、权利、事实源、证据、价值口径和审计链不完整时，不进入金融化或交易化叙事 |
| 不以大模型问答替代结构 | 结构化资产、事件、权限和证据仍是服务基础 |

### 5.1 AaaS 对象到 XWAIL 载体

| AaaS 对象 | XWAIL 载体 | 最低要求 |
|---|---|---|
| 服务资产 | `AssetGroup` / `AssetUnit` + `Dimensions` | 唯一身份、版本、责任、权利范围 |
| 服务流程 | `FlowRelations` + `StateMachine` | 事件、SLA、失败补偿和审计 |
| 服务包 | XAP | 依赖、策略、测试、签名、回滚 |
| 服务连接 | `Integration` + `SecurityProfile` | 契约、安全、重试、限流和可观测 |
| 服务价值 | `EconomicDimension` + `ValueFlow` + evidence | 口径、时间点、归因和证据 |
| 服务可信 | `Policy` + `Snapshot` + `Evidence` | 授权、快照、双时态、审计和保留 |

### 5.2 AaaS 服务目录

| 服务域 | 英文 | 主要能力 | 主要计量 |
|---|---|---|---|
| 资产模型服务 | Model as a Service | 资产建模、模板、行业 Profile、验证、版本与注册 | 模型数、资产数、验证次数 |
| 数字孪生服务 | Twin as a Service | 数据连接、状态同步、事件、仿真、快照与回放 | 活跃孪生数、实例时长、事件量 |
| 资产智能服务 | Intelligence as a Service | GraphRAG、异常、预测、根因、建议与智能体工具 | 推理量、任务量、模型等级 |
| 治理可信服务 | Governance as a Service | 身份、授权、策略、合规、审计、证据与签名 | 受管策略数、审计量、可信级别 |
| 数据价值服务 | Value as a Service | 数据质量、融合、标注、估值、价值流和报告 | 数据量、报告数、价值项目 |
| 资产运营服务 | Operations as a Service | 场景编排、SLA 运营、优化、服务目录与伙伴协作 | 受管场景、工单、结果或分成 |

### 5.3 控制平面

| 平面 | 核心职责 |
|---|---|
| 控制平面 | 租户、目录、订阅、计量、计费、SLA、版本、工单和发布 |
| 资产平面 | 身份、注册、模型、关系、权利和 XAP 包 |
| 运行平面 | 孪生、事件、状态机、工作流、快照和回放 |
| 智能平面 | 知识、检索、分析、预测、智能体和评估 |
| 信任平面 | 身份、授权、加密、策略、证据、审计和风险 |

### 5.4 统一计量字典

| 计量单位 | 定义 | 防争议要求 |
|---|---|---|
| `RegisteredAsset` | 已注册且处于有效状态的唯一资产 | 排除重复、测试和已退役资产 |
| `ActiveTwinHour` | 孪生实例处于可运行状态的一小时 | 明确休眠、故障和边缘离线规则 |
| `ProcessedEvent` | 通过平台接收并完成校验/路由的事件 | 明确重试、重复和死信是否计量 |
| `SnapshotGBMonth` | 快照和证据存储容量乘以月 | 明确压缩、归档和保留级别 |
| `APICall` | 成功或按契约处理的接口调用 | 明确错误、重试和批量调用口径 |
| `AIWorkUnit` | 按模型等级、输入输出或任务复杂度定义 | 明确模型、版本、缓存和失败不重复计费 |
| `ManagedScenario` | 持续受 SLA 和运营管理的场景资产包 | 明确边界、环境、版本和服务时间 |

## 6. GlobalCloud 项目群接入边界

WAS-XWAIL-AaaS 可作为 GlobalCloud 项目群的跨域资产语义层候选，但必须遵守现有主账、治理和证据边界。

| 项目 | 关系 | 禁止替代 |
|---|---|---|
| GFIS | 工厂执行事实、运行层对象、source-of-record 来源 | 不替代工厂事实主账，不凭模型生成真实运行层主键 |
| GPC | 公共服务平台业务入口和协作对象来源 | 不替代 GPC 业务入口和客户/协作事实 |
| PVAOS | 平台运营、门户、租户和运营对象来源 | 不替代租户、门户和运营控制边界 |
| WAE | 世界资产主账、统一资产引擎、AaaS 接入底座、治理控制与运行时 | 不替代 GFIS/GPC/PVAOS 的领域事实源，但要承接其资产化后的统一主账视图 |
| WAES | 基于 WAE 的 World Asset Explorer 业务实现、浏览器、运营工作台和场景入口 | 不写成 WAE 的同义词，不承担底层引擎定义；其门禁和视图必须回到 WAE 主账与治理链 |
| KDS | 受控知识主存、文档、来源和引用路径 | 不把 KDS 候选或摘要写成 accepted fact |
| Brain | 知识编制、分析和界面层 | 不把分析输出直接写成主账事实 |
| GPCF | 编排、文档治理、Loop 记录和状态框架 | 不自动改状态矩阵，不升级 accepted/integrated |

## 7. SCaaS：绿色供应链体系的行业场景定位

绿色供应链体系在新的命名基线下不再作为与世界资产体系并列的顶层体系表达，而是：

```text
世界资产体系
  -> AaaS 服务化交付模式
  -> SCaaS 供应链即服务行业场景架构
  -> GlobalCloud 绿色供应链体系具体实现与运营闭环
```

SCaaS 的定义：

| 项 | 定义 |
|---|---|
| 中文名 | 供应链即服务 |
| 英文名 | Supply Chain as a Service |
| 缩写 | SCaaS |
| 上位体系 | 世界资产体系 |
| 服务化模式 | AaaS |
| 行业场景 | 绿色供应链、工厂执行、订单协同、物流交付、证据治理、价值计量 |
| 语义与契约 | WAS / XWAIL |
| 世界资产主账 | WAE |
| 业务实现入口 | WAES |
| 治理与门禁 | WAE / WAES / Harness |
| 领域事实源 | GFIS、GPC、PVAOS 等业务系统按边界承担 |

SCaaS 不重新定义 WAS 的三层资产、八维、八流或生命周期。SCaaS 应通过行业 Profile、场景资产包、服务目录、计量字典和 no-write / writeback 门禁，把世界资产体系落到供应链行业。

SCaaS 的最低候选对象：

| 对象 | WAS/XWAIL 表达 | GlobalCloud 来源 |
|---|---|---|
| 供应链参与方 | OrganizationDimension / OrganizationAsset | GPC、PVAOS、GFIS |
| 工厂与产线 | PhysicalDimension / AssetGroup | GFIS |
| 订单、合同、采购与交付 | RuleDimension、EconomicDimension、FlowRelations | GPC、GFIS |
| 库存、批次、工单、POD | AssetUnit、StateMachine、LogisticsFlow | GFIS |
| 质量、审计、证据与状态裁决 | Policy、Snapshot、Evidence | WAE、WAES、Harness |
| 知识、SOP、行业模板 | Templates、Profile、KDS refs | KDS、Brain |
| 价值计量与服务履约 | ValueFlow、ServiceFlow、AaaS metering | GPCF 编排后进入受控验证 |

## 8. 最低闭环

PDF 基线的最低成功闭环不是同时完成所有模块，而是：

```text
一个现实资产
  -> 被 XWAIL 准确描述
  -> 在 WAE 或等效入口中可浏览和操作
  -> 通过事件驱动孪生状态变化
  -> 经规则与安全验证
  -> 形成可审计快照
  -> 产生可量化业务价值
```

映射到 GlobalCloud，最低闭环应收敛为 SCaaS 供应链即服务的第一个灯塔场景，例如仓储发运协同：

| 层 | 最小交付 |
|---|---|
| WAS | 仓库、货架、车辆、订单、发运、POD、责任方、规则、价值口径的三层/八维/八流定义 |
| XWAIL | 一个 Core 到 Operational 的 XWAIL 模型、状态机、事件、接口、安全绑定和验证器 |
| WAE | 本地 registry、世界资产主账、事件样本、状态变化、快照证据、审计日志、服务接入控制 |
| WAES | 基于 WAE 的浏览器/工作台/业务入口，可查看资产画像、关系、状态、证据和服务履约 |
| AaaS | 服务说明、SLA、计量字典、计费口径、退出条款和可复算价值报告 |
| SCaaS | 供应链行业 Profile、场景资产包、服务目录、履约指标和供应链价值证明 |
| WAE/WAES/Harness | WAE 主账与接入控制、WAES 业务实现入口、Harness evidence 和 no-write / writeback 门禁 |

## 9. Hard-stop

以下情况不得进入 AaaS 商业化、Trusted 级、跨组织交易或状态升级：

| 条件 | 结果 |
|---|---|
| 缺事实源、来源引用或业务 owner | `blocked` / `human_required` |
| 缺 evidence、快照、审计或价值口径 | `repair_required` |
| 只有 AI 摘要、用户口述、测试数据、mock、fixture 或 Demo | `metadata_only` |
| ACL、租户、权利束、隐私或敏感原文边界不清 | `blocked` |
| 未绑定 `SecurityProfile` 或等效安全策略 | `blocked` |
| 维度、流、生命周期或状态机映射不完整 | `repair_required` |
| 企图绕过 WAE/WAES/Harness 状态裁决 | `blocked` |
| 用 AaaS/RWA 叙事替代基础建模、运行、治理、证据和计量 | `blocked` |
| 把 SCaaS 写成脱离世界资产体系的独立顶层体系 | `repair_required` |
| 把绿色供应链体系写成已经完成商业化服务上线 | `blocked` |
| 把 WAES 写成 WAE 的同义词或底层引擎 | `repair_required` |
| 把 WAE 写成只读浏览器或普通前端入口 | `repair_required` |

## 10. 下一轮输入

建议下一轮进入 L1/L2 之间的 no-write 建模验证，不触达生产：

```text
输入：以 SCaaS 供应链即服务为第一个世界资产体系行业场景架构候选，以仓储发运协同为首个灯塔场景。
动作：建立一个最小 XWAIL Core/Operational 模型、负例样本和 no-write validator。
输出：SCaaS industry profile、warehouse-shipping XWAIL fixture、schema checks、policy checks、WAE registry draft、WAES explorer draft、AaaS/SCaaS service contract draft。
检查：document pollution、KDS token、loop document gate、XWAIL no-write assertions、WAE main-ledger boundary、WAES explorer implementation boundary。
反馈：若 validator 通过，再评估是否进入 WAE registry 与 WAES Explorer 本地 dry-run；若缺事实源或业务 owner，保持 repair_required。
```

本文件本身不构成实施完成、业务完成或状态升级依据。
