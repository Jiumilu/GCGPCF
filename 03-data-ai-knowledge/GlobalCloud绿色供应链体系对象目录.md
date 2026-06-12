# GlobalCloud 绿色供应链体系对象目录

日期：2026-06-10  
版本：体系级对象目录 v2（口径修正稿）  
基线引用：[GlobalCloud绿色供应链体系总架构.md](/Users/lujunxiang/Projects/GlobalCloud%20GPCF/GlobalCloud绿色供应链体系总架构.md)  
适用范围：GlobalCloud GPCF 公共服务与治理体系全部对象、L0-L5 内部实施映射、对象主责、AI 写入边界。

## 0. 口径修正（与 [总架构] 一致）

本文自 v2 起统一按以下口径执行：

1. **GPC-Native** 是绿色供应链公共服务平台本体，平台主线与公共服务平台本体，不是"协同中台"，不是"新增中间层"。
2. **PVAOS** 是平台运营、租户、组织、伙伴、用户、权限、门户、项目和应用入口底座，不是平台订单主账。
3. **GFIS** 是工厂执行系统 / 工厂事实主账。当前仓库中的 gcfis_custom、ERPNext 相关代码只能称为 GFIS 历史实现资产、适配器资产或 legacy reference，不作为 GFIS 主线定义来源。
4. **WAES** 是治理、证据确证、状态门控、合规、风险、审计和 AI 越权控制系统，不是平台订单主账，也不是工厂执行主账。
5. **Edge** 是现场采集与边缘缓冲层，优先服务 GFIS 的工厂执行事实确认，不得绕过 GFIS 先进入 GPC 数据池。
6. **KDS** 是企业知识主存（唯一数据源）；**Brain / LLM Wiki** 是知识编制与引擎候选。
7. **XiaoC / Hermes / XGD** 是 AI 与 Agent 编排层，不能直接写业务事实。
8. GPC-Native 的内部流程引擎统一命名为"平台服务流程编排引擎 / 绿色供应链协同流程运行时 / 供应链公共服务流程引擎"，不再称为"虚拟工厂运行时"。
9. 任何系统不得越权写入其他系统的主账事实；跨系统只能通过对象主责、事件合同、连接器合同和证据链路协同。

## 1. 设计原则

1. **对象先于接口**：没有对象目录，不定义 API、事件、权限和验收。
2. **事实必须有主责系统**：每个业务事实只能有一个主责系统，协同系统只能引用或订阅。
3. **AI 建议不是业务事实**：AI 可以生成 `AISuggestion`，不能直接生成工单完成、质量放行、库存扣减、签收确认等事实。
4. **不共享业务数据库**：GFIS、GPC-Native、WAES、PVAOS、Brain 等系统通过 API、事件和证据引用协同，不直接共享主账表。
5. **GFIS 历史实现资产归一**：仓库中 gcfis_custom、ERPNext 相关代码仅作为 GFIS 历史实现资产、适配器资产或 legacy reference；GFIS 主线定义以本对象目录、事件合同、连接器合同、厂行专项和 [总架构] 为准。
6. **Odoo GPC 不是主线**：现有 Odoo GPC 仅作为历史原型、流程样本和可选 back-office connector。
7. **WAES 不审批具体事务**：WAES 只审批治理规则、指标口径、AI 授权、证据确证和状态升级；工单、质量、库存、发货、签收等事务审批留在 GFIS 或 GPC-Native。
8. **平台主架构优先**：当前绿链平台主线系统是 `GPC-Native`；平台侧对象优先围绕 `GPC-Native` 建模，不再回到 Odoo 式大平台建模。
9. **GPC-Native 引擎命名**：GPC-Native 内部流程引擎不得再以"虚拟工厂运行时"命名。
10. **不通过对象越权**：任何系统都不得越权写入其他系统的主账对象；跨系统只能通过连接器、事件或证据引用访问。

## 2. 三层主架构对象总览

| 主层级 | 主责 | 主责系统 | 典型对象 |
|---|---|---|---|
| 治理与监控层 | 规则、监控、治理、证据、状态、AI 授权、复盘 | WAES / Harness / Brain / XiaoC / Hermes / XGD | GovernancePolicy、MetricDefinition、EvidenceRecord、EvidenceVerification、GovernanceApproval、AISuggestion、AgentTask |
| 运营与协同层 | 平台协同、平台订单、需求池、供应商协作、产能协同、工厂分配、ASN、预约、运输、POD、异常协同、绿色绩效、合规证据包、服务开放、生态接入 | GPC-Native | PlatformOrder、Supplier、Customer、Carrier、Vehicle、ASN、Appointment、Shipment、ProofOfDelivery、ExternalException、CrossFactoryException、FactoryAllocation、CapacityCommitment |
| 生态入口与平台运营层 | 租户、组织、伙伴、用户、角色、权限、门户、项目、应用入口、平台运营配置 | PVAOS | Tenant、Organization、ProgramProject、Partner、PortalAccount、RoleGrant |
| 生产与执行层 | 工厂订单、工单、生产报工、质量、质量放行、库存、批次、设备维护、发货出库、工厂执行证据 | GFIS / Edge | FactoryOrder、WorkOrder、QualityInspection、InventoryTransaction、MaterialLot、LineSideDelivery、Equipment、FactoryShipmentRelease、EdgeNode、DeviceSignal |

## 3. L0-L5 内部对象映射

| 层级 | 子域 | 主责系统 | 对象类型 |
|---|---|---|---|
| L0 | 战略与治理层 | Harness 控制台 / WAES | Manifest、验收、证据、状态、治理规则 |
| L1 | 生态入口与平台运营层 | PVAOS | 租户、组织、项目、伙伴、用户、门户账号、角色授权 |
| L2 | 供应链公共服务层 | GPC-Native | 平台订单、需求池、供应商协作、产能协同、工厂分配、ASN、预约、车辆、运输、签收、POD、外部异常、绿色绩效、合规证据包、服务开放 |
| L3 | 工厂执行层 | GFIS | 工厂订单、BOM、工单、质量、库存、批次、厂内物流、设备、发货出库 |
| L4 | 数据与事件层 | Connector / WAES | 事件、连接器、主数据映射、指标、追踪、Outbox/Inbox |
| L5 | 控制塔与 AI 编排层 | WAES / Brain / XiaoC / Hermes / XGD | 控制塔视图、AI 建议、治理审批、知识条目、Prompt 模板、Agent 任务 |

## 4. 对象目录

### 4.1 L0 战略与治理对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 项目群 Manifest | ProgramManifest | `MAN-*` | Harness 控制台 | WAES | 否 | 否 | 否 | draft / active / superseded | 记录体系级目标、边界、命令、禁止项和完成定义 |
| 项目边界 | ProjectBoundary | `BDY-*` | Harness 控制台 | 各项目 | 否 | 否 | 否 | active / blocked / retired | 定义每个项目可读写范围和人工确认门 |
| 验收矩阵 | AcceptanceMatrix | `ACC-*` | WAES / Harness | GFIS / GPC-Native | 否 | 否 | 否 | draft / ready / accepted / blocked | 阶段验收清单 |
| 验收场景 | AcceptanceScenario | `ACS-*` | WAES / Harness | GFIS / GPC-Native | 否 | 否 | 否 | not_started / running / pass / fail / blocked | 单个验收用例 |
| 状态审计 | StatusAudit | `AUD-*` | Harness 控制台 | 各项目 | 否 | 否 | 否 | partial / blocked / ready / complete | 当前状态证据 |
| 人工确认 | HumanConfirmation | `HC-*` | WAES / Harness | 各系统 | 否 | 是 | 否 | requested / confirmed / rejected / expired | 治理、证据、状态和完成结论的人类确认，不替代业务事务审批 |
| 治理策略 | GovernancePolicy | `GOV-*` | WAES / Harness | 各系统 | 是 | 否 | 否 | draft / active / retired | 规则、指标、AI 授权和状态治理策略 |

### 4.2 L1 生态入口与平台运营对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 租户 | Tenant | `TEN-*` | PVAOS | WAES / GPC-Native | 是 | 否 | 否 | active / suspended / archived | 体系内组织租户 |
| 组织 | Organization | `ORG-*` | PVAOS | GPC-Native / WAES | 是 | 否 | 否 | active / inactive | 客户、供应商、承运商、园区、监管等组织实体 |
| 项目 | ProgramProject | `PRJ-*` | PVAOS | WAES / Brain | 是 | 否 | 否 | planning / active / paused / closed | 绿色供应链体系内项目 |
| 伙伴 | Partner | `PAR-*` | PVAOS | GPC-Native | 是 | 否 | 否 | prospect / onboarded / suspended | 合作伙伴关系 |
| 门户账号 | PortalAccount | `PA-*` | PVAOS / GPC-Native | WAES | 是 | 否 | 否 | invited / active / locked / revoked | 外部用户账号 |
| 角色授权 | RoleGrant | `RG-*` | PVAOS / WAES | GPC-Native / GFIS | 否 | 否 | 否 | active / expired / revoked | 跨系统角色授权 |

### 4.3 L2 供应链公共服务对象（GPC-Native 主账）

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 平台订单 | PlatformOrder | `PO-*` | GPC-Native | PVAOS / GFIS / WAES | 否 | 是 | 否 | draft / confirmed / dispatched / fulfilled / cancelled | 公共服务平台订单 |
| 工厂订单映射 | OrderMapping | `OM-*` | GPC-Native | GFIS | 否 | 是 | 否 | pending / linked / mismatch / closed | GPC-Native 订单与 GFIS 订单关系 |
| 供应商 | Supplier | `SUP-*` | GPC-Native | GFIS / PVAOS | 是 | 否 | 否 | onboarding / active / suspended / blacklisted | 外部供应商主数据 |
| 客户 | Customer | `CUS-*` | GPC-Native | GFIS / PVAOS | 是 | 否 | 否 | prospect / active / suspended | 外部客户主数据 |
| 承运商 | Carrier | `CAR-*` | GPC-Native | PVAOS | 是 | 否 | 否 | active / suspended / expired | 承运商主数据 |
| 车辆 | Vehicle | `VEH-*` | GPC-Native | GFIS | 是 | 否 | 否 | active / unavailable / expired | 车辆档案 |
| 供应商到货通知 | ASN | `ASN-*` | GPC-Native | GFIS | 否 | 是 | 否 | created / confirmed / arrived / received / cancelled | 供应商发货预告 |
| 预约 | Appointment | `APT-*` | GPC-Native | GFIS | 否 | 是 | 否 | requested / confirmed / checked_in / completed / no_show / cancelled | 到货或发货预约 |
| 月台时段 | DockSlot | `DS-*` | GPC-Native | GFIS | 是 | 否 | 否 | open / reserved / occupied / closed | 月台资源 |
| 发运单 | Shipment | `SHIP-*` | GPC-Native | GFIS / WAES | 否 | 是 | 否 | planned / released / loaded / in_transit / delivered / exception / closed | 厂外发运与运输主对象 |
| 在途节点 | TransitCheckpoint | `TCP-*` | GPC-Native | WAES | 否 | 是 | 可生成草案，不自动确认 | planned / reached / delayed / skipped | 运输在途节点 |
| 签收回单 | ProofOfDelivery | `POD-*` | GPC-Native | GFIS / WAES | 否 | 是 | 否 | pending / signed / disputed / rejected / archived | 客户签收与回单 |
| 外部协同异常 | ExternalException | `EEX-*` | GPC-Native | WAES / GFIS | 否 | 是 | 可生成草案，不自动关闭 | raised / assigned / resolving / closed / escalated | 客户、供应商、承运商协同异常 |

### 4.4 L3 工厂执行对象（GFIS 主账）

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 工厂 | Factory | `FAC-*` | GFIS | PVAOS / WAES | 是 | 否 | 否 | active / inactive | 工厂实体 |
| 车间 | Workshop | `WS-*` | GFIS | WAES | 是 | 否 | 否 | active / inactive | 车间 |
| 仓库 | Warehouse | `WH-*` | GFIS | GPC-Native / WAES | 是 | 否 | 否 | active / blocked | 仓库 |
| 工厂订单 | FactoryOrder | `FO-*` | GFIS | GPC-Native / WAES | 否 | 是 | 否 | accepted / planned / in_production / completed / shipped / cancelled | 工厂接收并确认的订单 |
| 物料 | Material | `MAT-*` | GFIS | GPC-Native | 是 | 否 | 否 | active / blocked / obsolete | 物料主数据 |
| 批次 | MaterialLot | `LOT-*` | GFIS | GPC-Native / WAES | 否 | 是 | 否 | pending_inspection / qualified / quarantined / rejected / consumed / shipped | 物料或成品批次 |
| BOM | BillOfMaterial | `BOM-*` | GFIS | WAES | 是 | 否 | 否 | draft / active / retired | 物料清单 |
| 生产工单 | WorkOrder | `WO-*` | GFIS | WAES | 否 | 是 | 否 | draft / released / in_progress / paused / completed / cancelled | 生产执行主对象 |
| 作业卡 | JobCard | `JC-*` | GFIS | WAES | 否 | 是 | 否 | queued / started / completed / rejected | 工序作业 |
| 齐套检查 | KittingCheck | `KC-*` | GFIS | WAES | 否 | 是 | 可生成建议，不自动通过 | pending / pass / shortage / blocked / waived | 工单开工前物料齐套 |
| 线边配送 | LineSideDelivery | `LSD-*` | GFIS | WAES / XGD | 否 | 是 | 可生成建议，不自动完成 | created / picked / dispatched / delivered / confirmed / exception | 线边配送任务 |
| 厂内物流任务 | LogisticsTask | `LT-*` | GFIS | WAES / XGD | 否 | 是 | 可生成建议，不自动关闭 | created / assigned / executing / completed / failed / rerouted | AGV、叉车、人工等任务 |
| 线边库存 | LineSideStock | `LSS-*` | GFIS | WAES | 否 | 是 | 否 | available / low / blocked / consumed | 线边库存状态 |
| 库存事务 | InventoryTransaction | `INVTX-*` | GFIS | WAES | 否 | 是 | 否 | posted / reversed / disputed | 库存增减事实 |
| 质量检验 | QualityInspection | `QI-*` | GFIS | WAES | 否 | 是 | 可生成建议，不自动放行 | pending / accepted / rejected / rework / quarantined | 质量检验事实 |
| 设备 | Equipment | `EQ-*` | GFIS | WAES / XGD | 是 | 否 | 否 | available / running / maintenance / down / retired | 设备主数据 |
| 维修工单 | MaintenanceOrder | `MO-*` | GFIS | WAES / XGD | 否 | 是 | 可生成建议，不自动验收 | created / assigned / repairing / completed / verified | 设备维修 |
| 发货出库 | FactoryShipmentRelease | `FSR-*` | GFIS | GPC-Native / WAES | 否 | 是 | 否 | pending / released / handed_over / reversed | 工厂发货出库事实 |
| 边缘节点 | EdgeNode | `EDG-*` | Edge | GFIS / WAES | 是 | 否 | 否 | online / degraded / offline / retired | 现场网关、工位终端或边缘计算节点 |
| 设备信号 | DeviceSignal | `SIG-*` | Edge | GFIS / WAES | 否 | 遥测事实 | 否 | received / buffered / forwarded / dropped | PLC、DCS、SCADA、传感器、AGV 等现场信号；Edge 不得在自身数据库落地业务主账事实，进入 GFIS 规则后才可触发业务流程 |

### 4.5 L4 数据与事件对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 连接器 | Connector | `CON-*` | WAES / Connector Registry | 各系统 | 是 | 否 | 否 | draft / active / degraded / disabled | 系统连接器注册；体系只承认 5 个根连接器编号，详见 [总架构] §4 |
| API 合同 | ApiContract | `API-*` | Connector Registry | 各系统 | 否 | 否 | 否 | draft / active / deprecated | OpenAPI 或接口合同 |
| 事件 | DomainEvent | `EVT-*` | 生产系统 | WAES / Event Bus | 否 | 是 | 仅 AI 建议类事件可由 AI 发起 | published / consumed / failed / replayed | 领域事件 |
| Outbox 记录 | OutboxRecord | `OUT-*` | 各生产系统 | Event Bus | 否 | 否 | 否 | pending / published / failed / dead_letter | 事件发布暂存 |
| Inbox 记录 | InboxRecord | `IN-*` | 消费系统 | Event Bus | 否 | 否 | 否 | received / processed / duplicate / failed | 事件消费幂等 |
| 主数据映射 | MasterDataMapping | `MDM-*` | WAES / GPC-Native / GFIS | 各系统 | 是 | 否 | 否 | proposed / active / conflict / retired | 跨系统主数据映射 |
| 指标定义 | MetricDefinition | `MET-*` | WAES | GFIS / GPC-Native | 是 | 否 | 否 | draft / active / retired | 指标口径 |
| 指标快照 | MetricSnapshot | `MS-*` | WAES | 各系统 | 否 | 是 | 否 | calculated / stale / invalid | 指标计算结果 |
| 追踪链 | TraceContext | `TRC-*` | WAES / Event Bus | 各系统 | 否 | 否 | 否 | open / closed | 跨事件 traceId |

### 4.6 L5 控制塔与 AI 对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 协同系统 | 主数据 | 业务事实 | 允许 AI 写入 | 关键状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 控制塔视图 | ControlTowerView | `CTV-*` | WAES | 各系统 | 否 | 否 | 否 | draft / active / retired | 控制塔页面或视图 |
| 证据记录 | EvidenceRecord | `EVD-*` | WAES | Harness / 各系统 | 否 | 证据事实 | 可提交草案，不自动确证 | captured / verified / rejected / archived | 证据台账；不是生产、质量、库存、发货、签收等业务主账事实 |
| 治理审批 | GovernanceApproval | `GAP-*` | WAES / Harness | 各系统 | 否 | 是 | 可生成草案，不自动批准 | draft / submitted / approved / rejected / expired | 规则、指标、AI 授权、证据确证和状态升级审批 |
| 证据确证 | EvidenceVerification | `EVF-*` | WAES / Harness | 各系统 | 否 | 是 | 可生成候选，不自动确证 | pending / verified / rejected / superseded | 证据是否可作为验收、审计或状态依据 |
| 业务审批引用 | BusinessApprovalReference | `BAR-*` | GFIS / GPC-Native | WAES | 否 | 是 | 否 | referenced / missing / stale / invalid | 引用业务系统内部审批结果，WAES 不承办具体事务审批 |
| AI 建议 | AISuggestion | `AIS-*` | WAES / Hermes | Brain / XiaoC / XGD | 否 | 否 | 是 | draft / submitted / needs_evidence / governance_authorized / rejected / business_action_referenced / closed | AI 输出的建议，不是业务事实；`governance_authorized` 只表示治理授权，不表示业务批准 |
| Agent 任务 | AgentTask | `AGT-*` | Hermes / WAES | XGD / XiaoC | 否 | 否 | 是 | queued / running / waiting_governance / completed / failed | Agent 执行任务；具体业务执行仍进入 GFIS/GPC-Native |
| 知识条目 | KnowledgeEntry | `KN-*` | Brain | XiaoC / WAES | 是 | 否 | 可生成候选，不自动 canonical | working / source_verified / human_confirmed / archived | Brain 知识服务层中的候选知识条目、SOP、案例、复盘；不等于企业正式知识真源 |
| Prompt 模板 | PromptTemplate | `PT-*` | XiaoC | WAES / Hermes | 是 | 否 | 可生成候选，需审核 | draft / active / deprecated | Agent prompt 模板 |
| 模型配置 | ModelConfig | `MC-*` | XiaoC | Hermes / WAES | 是 | 否 | 否 | active / disabled / retired | 模型与 provider 配置 |

## 5. 四流优化补充对象

本节根据四流综合架构补充对象目录，用于支撑治理流、业务流、数据流和 AI 服务流的可执行合同。以下对象进入后续连接器合同、SOP 模板、AI 服务模型、数据治理模型和验收矩阵扩展。

### 5.1 治理流补充对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 关键状态 | 说明 |
|---|---|---|---|---|---|
| 治理规则 | GovernanceRule | `GR-*` | WAES | draft / active / frozen / retired | 单条治理规则，不等同于业务审批规则 |
| 治理规则版本 | GovernanceRuleVersion | `GRV-*` | WAES | draft / active / superseded / retired | 规则版本、生效范围、兼容性和回滚关系 |
| 策略绑定 | PolicyAssignment | `PAO-*` | WAES | draft / active / suspended / retired | 将规则绑定到项目、链、厂、角色、连接器或 Agent |
| 状态转换请求 | StatusTransitionRequest | `STR-*` | WAES / Harness | requested / approved / rejected / expired | 用于 `partial`、`ready_for_human_acceptance`、`accepted`、`complete` 等状态流转 |
| 发布门 | ReleaseGate | `RGATE-*` | WAES / Harness | pending / passed / failed / waived | 发布、试运营、正式运营和阶段验收的门禁 |
| 连接器生命周期记录 | ConnectorLifecycleRecord | `CLR-*` | Connector Registry / WAES | online / degraded / recovered / offline / retired | 连接器上线、降级、恢复、下线和回滚审计 |
| 证据补证请求 | EvidenceReworkRequest | `ERW-*` | WAES / Harness | requested / submitted / accepted / rejected | 证据被驳回后的补证路径 |

### 5.2 业务流补充对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 关键状态 | 说明 |
|---|---|---|---|---|---|
| 工厂分配规则 | FactoryAllocationRule | `FAR-*` | GPC-Native / WAES | draft / active / retired | 一链多厂或多链多厂的订单分发规则 |
| 工厂分配结果 | FactoryAllocation | `FA-*` | GPC-Native | proposed / confirmed / rejected / closed | 平台订单分配到工厂的结果；工厂执行仍由 GFIS 确认 |
| 产能承诺 | CapacityCommitment | `CC-*` | GFIS | proposed / committed / reduced / expired | 工厂对订单、品类或时段的可承诺产能 |
| 产能快照 | CapacitySnapshot | `CS-*` | GFIS | calculated / stale / invalid | 工厂当前产能、瓶颈和可用窗口 |
| 库存可见性快照 | InventoryVisibilitySnapshot | `IVS-*` | GFIS / GPC-Native | calculated / stale / invalid | 多厂库存可见性，不替代 GFIS 库存主账 |
| 质量追溯范围 | QualityTraceScope | `QTS-*` | GFIS / WAES | open / closed / incomplete | 跨厂、跨链批次追溯范围 |
| 追溯片段 | TraceSegment | `TSG-*` | WAES / Event Bus | linked / missing / disputed | 订单、批次、发货、POD 等追踪片段 |
| 跨厂异常 | CrossFactoryException | `CFE-*` | GPC-Native / WAES | raised / assigned / resolving / closed | 多厂协同异常和责任链 |

### 5.3 数据流补充对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 关键状态 | 说明 |
|---|---|---|---|---|---|
| Schema 版本 | SchemaVersion | `SCH-*` | Connector Registry | draft / active / deprecated / retired | API 和事件 schema 版本 |
| Schema 兼容性检查 | SchemaCompatibilityCheck | `SCC-*` | Connector Registry | running / pass / fail / waived | 发布前检查 schema 兼容性 |
| 死信记录 | DeadLetterRecord | `DLQ-*` | Event Bus | created / triaged / replayed / discarded | 失败事件、消费失败和无法投递记录 |
| 重放请求 | ReplayRequest | `RR-*` | WAES / Event Bus | requested / approved / rejected / running / closed | 事件重放请求 |
| 重放运行 | ReplayRun | `RPR-*` | Event Bus | running / completed / failed / cancelled | 事件重放执行记录 |
| 数据质量规则 | DataQualityRule | `DQR-*` | WAES | draft / active / retired | 完整性、唯一性、时效性、范围和一致性规则 |
| 数据质量问题 | DataQualityIssue | `DQI-*` | WAES | detected / assigned / resolved / waived | 数据质量缺陷和处理记录 |
| 数据血缘 | LineageRecord | `LIN-*` | WAES / Data Platform | linked / incomplete / disputed | 指标、证据、报表和 AI 建议的数据来源链 |
| 保留策略 | RetentionPolicy | `RET-*` | WAES / Data Platform | draft / active / retired | 事件、证据、日志、截图和模型输出的保留策略 |
| 租户数据边界 | TenantDataBoundary | `TDB-*` | PVAOS / WAES | active / violated / suspended | 多租户、多链、多厂隔离边界 |
| 边缘缓存策略 | EdgeBufferPolicy | `EBP-*` | Edge / WAES | draft / active / retired | 断网缓存、补传、去重、丢弃和回放策略 |

### 5.4 AI 服务流补充对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 关键状态 | 说明 |
|---|---|---|---|---|---|
| Agent 工具授权 | AgentToolGrant | `ATG-*` | WAES | draft / submitted / approved / active / suspended / revoked / expired | Agent 可用工具、风险等级和有效期 |
| Agent 工具策略 | AgentToolPolicy | `ATP-*` | WAES / XiaoC | draft / active / retired | 工具允许动作、禁止动作、参数范围和证据要求 |
| Agent 运行 | AgentRun | `AR-*` | Hermes / WAES | queued / running / waiting_governance / waiting_business_reference / completed / failed / cancelled | Agent 运行实例 |
| Agent 运行步骤 | AgentRunStep | `ARS-*` | Hermes | started / completed / failed / skipped | Agent 工具调用和推理步骤审计 |
| AI 建议结果 | AISuggestionOutcome | `AIO-*` | WAES | adopted / rejected / superseded / business_action_referenced / no_action | AI 建议采纳、驳回、业务引用和效果 |
| Prompt 评估 | PromptEvaluation | `PE-*` | XiaoC / WAES | not_started / running / pass / fail / blocked / superseded | Prompt 发布前和回归评估 |
| 模型评估 | ModelEvaluation | `ME-*` | XiaoC / WAES | not_started / running / pass / fail / blocked / superseded | 模型配置、降级和切换评估 |
| 模型能力画像 | ModelCapabilityProfile | `MCP-*` | XiaoC / WAES | draft / active / retired | 模型能力、上下文窗口、工具调用、结构化输出、推理等级和风险等级画像 |
| 模型授权策略 | ModelAuthorizationPolicy | `MAP-*` | WAES | draft / active / suspended / retired | 模型允许使用范围、角色、场景、项目、租户、密级和证据要求 |
| 模型授权记录 | ModelAuthorizationGrant | `MAG-*` | WAES | draft / approved / active / suspended / revoked / expired | 模型在具体项目、Agent、场景或用户范围内的治理授权记录 |
| 模型路由决策 | ModelRouteDecision | `MRD-*` | XiaoC / WAES | proposed / selected / blocked / overridden / closed | 模型选择、降级、切换和回退决策记录 |
| 模型使用记录 | ModelUsageRecord | `MUR-*` | XiaoC / Hermes / WAES | captured / verified / disputed / archived | 单次模型调用的输入输出摘要、token、延迟、费用、证据引用和治理结果 |
| 模型计量快照 | ModelMeterSnapshot | `MMS-*` | WAES / Data Platform | calculated / stale / invalid | 按项目、租户、Agent、模型、时间窗汇总的 token、费用、成功率、阻断率等计量快照 |
| 证据引用 | EvidenceCitation | `EC-*` | WAES / Agent | linked / missing / invalid | AI 建议中的结构化证据引用 |
| AI 越权拦截 | AIOverreachBlocked | `AOB-*` | WAES | blocked / reviewed / closed | Agent 越权动作被拦截的审计记录 |
| 模型越权拦截 | ModelOverreachBlocked | `MOB-*` | WAES | blocked / reviewed / closed | 模型调用违反授权策略、密级、预算、场景或输出约束时的阻断审计记录 |

### 5.5 知识主存域与结构化数据库域补充对象

| 中文名 | 英文名 | ID 前缀 | 主责系统 | 关键状态 | 说明 |
|---|---|---|---|---|---|
| 知识文档 | KnowledgeDocument | `KDOC-*` | 知识主存服务 | draft / in_review / approved / effective / retired / archived | 企业级知识真源主对象 |
| 知识版本 | KnowledgeVersion | `KVER-*` | 知识主存服务 | draft / approved / effective / superseded / retired | 知识内容版本 |
| 知识发布 | KnowledgeRelease | `KREL-*` | 知识主存服务 / WAES | draft / submitted / approved / effective / rolled_back / archived | 知识发布、生效、回滚记录 |
| 知识访问策略 | KnowledgeAccessPolicy | `KAP-*` | WAES / 知识主存服务 | draft / active / retired | 项目、角色、密级和 AI 可见范围策略 |
| 知识审计日志 | KnowledgeAuditLog | `KAL-*` | 知识主存服务 | captured / archived | 知识查看、引用、导出、发布审计 |
| 知识编制视图 | KnowledgeCompileView | `KCV-*` | LLM Wiki | draft / active / archived | 面向人工编制、章节组织和规范表达的知识视图；不是真源，不反写主存层 |
| 知识引擎索引 | KnowledgeEngineIndex | `KEI-*` | Brain | building / active / stale / retired | 主知识引擎索引、RAG、图谱和引用回指承载对象；不是真源 |
| 知识服务目录 | KnowledgeServiceCatalog | `KSC-*` | Brain | draft / active / retired | Brain 对外提供的 SOP、案例、复盘、问答等知识服务目录；不直接发布正式知识版本 |
| 知识入库任务 | KnowledgeIngestJob | `KIJ-*` | 知识主存服务 / Brain | queued / running / completed / failed / cancelled | 从知识主存发布到 LLM Wiki 编制视图和 Brain 主知识引擎的 ingest 任务，Brain 只消费引擎结果 |
| 数据库域定义 | DatabaseDomain | `DBD-*` | WAES / Data Platform | draft / active / retired | 结构化数据库域边界定义 |
| 数据库访问策略 | DatabaseAccessPolicy | `DAP-*` | WAES / Data Platform | draft / active / suspended / retired | 数据库读写、审计和跨域访问规则 |
| 读模型投影 | ReadModelProjection | `RMP-*` | Data Platform | building / active / stale / retired | 控制塔与跨系统查询使用的读模型 |
| 连接器治理结论 | ConnectorDecision | `CDN-*` | WAES / Connector Registry | draft / approved / rejected / superseded | 连接器上线、下线、降级、恢复治理结论 |
| 状态要求 | StatusRequirement | `SRQ-*` | WAES / Harness | draft / active / retired | 对项目、阶段、验收或对象的状态门要求 |
| AI 授权结论 | AIAuthorizationGrant | `AAG-*` | WAES | draft / approved / active / suspended / revoked / expired | AI 与 Agent 的治理授权结论 |
| 阶段验收结论 | AcceptanceConclusion | `ACN-*` | WAES / Harness | draft / accepted / rejected / superseded | 阶段验收和整体验收结论 |

## 6. AI 写入边界

| 对象类型 | AI 可写 | AI 不可写 |
|---|---|---|
| 业务事实 | 无 | 工单完成、质量放行、库存扣减、发货确认、签收确认、设备维修验收 |
| 外部协同 | 建议、异常草案、摘要 | 车辆改派确认、交期承诺、客户签收确认、POD 确证 |
| 治理与证据 | 建议草案、证据候选、治理审批草案 | 规则生效、人工确认、证据确证、状态升级 |
| 知识 | working 候选、复盘草案 | canonical 事实、合同/资金/外部回执结论 |
| Prompt | 草案和评估样例 | 未审核上线到关键生产流程 |

## 7. 优先补齐对象

一期优先补齐：

1. `PlatformOrder`
2. `OrderMapping`
3. `FactoryOrder`
4. `WorkOrder`
5. `KittingCheck`
6. `LineSideDelivery`
7. `LogisticsTask`
8. `QualityInspection`
9. `MaterialLot`
10. `FactoryShipmentRelease`
11. `Shipment`
12. `ProofOfDelivery`
13. `ExceptionCase` / `ExternalException`
14. `EvidenceRecord`
15. `AISuggestion`
16. `GovernanceApproval`
17. `EvidenceVerification`
18. `BusinessApprovalReference`
19. `EdgeNode`
20. `DeviceSignal`
21. `GovernanceRule`
22. `StatusTransitionRequest`
23. `ConnectorLifecycleRecord`
24. `SchemaVersion`
25. `DeadLetterRecord`
26. `ReplayRequest`
27. `DataQualityIssue`
28. `AgentToolGrant`
29. `AgentRun`
30. `AISuggestionOutcome`
31. `AIOverreachBlocked`
32. `ModelAuthorizationGrant`
33. `ModelUsageRecord`
34. `ModelMeterSnapshot`
35. `ModelOverreachBlocked`
36. `KnowledgeDocument`
37. `KnowledgeVersion`
38. `KnowledgeRelease`
39. `KnowledgeAccessPolicy`
40. `KnowledgeIngestJob`
41. `DatabaseDomain`
42. `DatabaseAccessPolicy`
43. `ReadModelProjection`
44. `ConnectorDecision`
45. `StatusRequirement`
46. `AIAuthorizationGrant`
47. `AcceptanceConclusion`
