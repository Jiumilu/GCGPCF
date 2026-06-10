# GlobalCloud 绿色供应链体系进一步梳理与提示词库

日期：2026-06-07  
用途：在已有 V3.1 方案、项目群架构图、专项架构图和 GPC-Native ADR 基础上，进一步梳理实施逻辑，并提供可直接用于 Codex/Agent 的提示词。原“智慧工厂”降级为生产与执行层/工厂执行子域。
当前口径：主架构采用治理与监控层、运营与协同层、生产与执行层；WAES 只做规则、监控、治理、证据、状态和 AI 授权，不参与工单、质量、库存、发货、签收等具体事务审批。

当前补充口径：平台主架构以 `GPC-Native` 为主，宪法内容通过 `WAES` 治理约束进入，而不是反向替代平台主架构。

## 1. 当前设计状态

当前设计已经完成四类基础工作：

1. **顶层方案**：`AI驱动工厂信息化系统完整方案V3.1.md` 明确了生产、质量、物流、设备能源安环、数据智能和 AI 授权边界。
2. **项目群架构**：`基于GlobalCloud项目群的智慧工厂架构设计方案.md` 明确 GFIS、GPC-Native、WAES、PVAOS、Brain、XiaoC、XiaoG Agent、XGD、Harness 的分工。
3. **专项架构图**：`GlobalCloud智慧工厂专项架构图集.md` 补齐了统一数据与事件、GFIS-GPC-WAES 集成、OT/IT 安全、异常闭环与 AI 治理授权。
4. **关键 ADR**：`ADR-GPC从Odoo二开调整为原生协同中台.md` 明确 GPC 主线从 Odoo 二开调整为 GPC-Native。

当前尚未完成的实施前设计：

| 缺口 | 为什么重要 | 应补产物 |
|---|---|---|
| 统一对象目录 | 没有对象目录就无法定义接口、事件和主数据权责 | `01-domain-object-catalog.md` |
| 事件合同 | 没有事件合同就无法让 GFIS、GPC-Native、WAES 集成 | `02-event-contracts.md` |
| API / Connector 合同 | 没有连接器边界就会变成项目互相直连 | `03-connector-contracts.md` |
| GFIS LES 最小模型 | 物流主线必须从库存附属功能变成独立执行主线 | `04-gfis-les-minimum-model.md` |
| GPC-Native 一期模型 | GPC-Native 需要从 ADR 进入对象/API/事件设计 | `05-gpc-native-phase1-model.md` |
| WAES 控制塔视图 | 控制塔要明确读什么、算什么、显示什么、治理什么 | `06-waes-control-tower-model.md` |
| AI Agent 提示词与治理授权 | AI 必须按 L1-L5 边界工作 | `07-agent-prompt-and-governance-model.md` |
| 验收矩阵 | 没有验收矩阵就无法判断完成 | `08-phase1-acceptance-matrix.md` |

## 2. 推荐目录结构

建议在当前工作区新增：

```text
architecture/
  00-project-boundary-and-role-map.md
  01-domain-object-catalog.md
  02-event-contracts.md
  03-connector-contracts.md
  04-gfis-les-minimum-model.md
  05-gpc-native-phase1-model.md
  06-waes-control-tower-model.md
  07-agent-prompt-and-governance-model.md
  08-phase1-acceptance-matrix.md
  prompts/
    00-master-context.md
    01-architecture-review.md
    02-gpc-native-design.md
    03-gfis-les-design.md
    04-event-contract-design.md
    05-waes-control-tower-design.md
    06-agent-prompt-design.md
    07-acceptance-review.md
```

## 3. 总体梳理提示词

### Prompt 00：总控上下文提示词

用途：给任何新开的 Codex/Agent 会话建立统一上下文。

```text
你是 GlobalCloud 绿色供应链体系项目群的架构与实施 Agent。

当前工作区：
/Users/lujunxiang/Documents/GlobalCloud智慧工厂

必须优先读取这些文件：
1. AI驱动工厂信息化系统完整方案V3.1.md
2. 基于GlobalCloud项目群的智慧工厂架构设计方案.md
3. GlobalCloud智慧工厂项目群架构图.md
4. GlobalCloud智慧工厂专项架构图集.md
5. ADR-GPC从Odoo二开调整为原生协同中台.md
6. GlobalCloud智慧工厂项目群控制表.md

核心架构口径：
- GFIS 是单厂本地执行事实源，负责生产、质量、库存、设备、厂内物流、发货出库事实。
- GPC-Native 是轻量绿色供应链协同中台，负责供应商、客户、订单协同、TMS、签收回单、公共服务。
- 现有 Odoo GPC 是历史原型、流程样本、可选 back-office connector，不再作为主架构底座。
- WAES 是治理与监控中枢、规则审批、证据台账和 Agent Desktop，不是业务主账，也不审批具体事务。
- PVAOS 是联盟门户、项目/伙伴/客户接入入口，不承载生产执行。
- Brain 是 SOP、知识库、RAG 和复盘，不替代运行事实。

## 四流优化后的当前提示词基线

后续所有提示词必须继承以下专项文档：

1. [GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md)
2. [GlobalCloud绿色供应链体系连接器合同.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系连接器合同.md)
3. [GlobalCloud绿色供应链体系SOP模板库.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系SOP模板库.md)
4. [GlobalCloud绿色供应链体系AI服务模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系AI服务模型.md)
5. [GlobalCloud绿色供应链体系数据治理模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系数据治理模型.md)
6. [GlobalCloud绿色供应链体系多厂协同模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系多厂协同模型.md)
7. [GlobalCloud绿色供应链体系Edge接入与安全模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系Edge接入与安全模型.md)

提示词必须明确：

1. WAES 不参与具体事务审批。
2. AI 建议不是业务事实。
3. 配置完成不等于真实完成。
4. 连接器必须有 schema、DLQ、重放、证据和生命周期治理。
5. SOP 必须可执行、可版本化、可验收。
6. Edge 是遥测和接入层，不是业务主账。
- XiaoC 是 Prompt、MCP、模型适配和 Agent 模板中心。
- XiaoG Agent / Hermes WebUI / XGD 是持续运行 Agent 和多端交互入口。
- Harness 控制台约束工程边界、命令、验收和状态纪律。

强制边界：
- 不允许 push、pull、merge、rebase、reset、deploy、删除数据或改生产配置，除非用户明确授权。
- 不允许把 Odoo GPC 继续当主线底座。
- 不允许让 AI 自动改写生产、质量、库存、发货、资金、质量放行、客户承诺等事实。
- L1 查询/报表可自动；L2 预警可自动提醒；L3 建议需业务系统确认；L4 治理规则、AI 授权、证据确证和状态升级需治理授权；L5 安全关键控制 AI 不得接管。

你的任务：
根据用户指定的子任务，先读取相关文件，再输出可落地的设计文档、对象模型、事件合同、接口边界、验收矩阵或提示词。输出中文，必须区分当前证据、设计建议、待确认事项和阻塞项。
```

### Prompt 01：全局架构复核提示词

用途：检查当前设计还有哪些结构性缺口。

```text
请对 /Users/lujunxiang/Documents/GlobalCloud智慧工厂 下的智慧工厂方案进行全局架构复核。

重点读取：
- AI驱动工厂信息化系统完整方案V3.1.md
- 基于GlobalCloud项目群的智慧工厂架构设计方案.md
- GlobalCloud智慧工厂专项架构图集.md
- ADR-GPC从Odoo二开调整为原生协同中台.md

请输出：
1. 当前架构已经明确的内容。
2. 当前架构仍缺失的内容，按 P0/P1/P2 分级。
3. 每个缺失项为什么会影响实施。
4. 每个缺失项建议补哪份文档。
5. 是否存在边界冲突，例如 GFIS 与 GPC-Native、WAES 与业务主账/具体事务审批、Brain 与运行事实、AI 与治理授权。
6. 最后给出“是否可以进入一期实施”的判断。

约束：
- 不要泛泛而谈。
- 不要把图已经画了就当完成。
- 必须指出缺少对象、事件、接口、权限、证据、验收或运行验证的地方。
- 输出中文。
```

## 4. GPC-Native 相关提示词

### Prompt 02：GPC-Native 一期产品与技术蓝图

```text
请基于当前智慧工厂设计，进一步设计 GPC-Native 一期产品与技术蓝图。

必须读取：
- ADR-GPC从Odoo二开调整为原生协同中台.md
- 基于GlobalCloud项目群的智慧工厂架构设计方案.md
- GlobalCloud智慧工厂专项架构图集.md

设计口径：
- GPC-Native 是轻量绿色供应链协同中台。
- 现有 Odoo GPC 只作为历史原型、流程样本和可选 back-office connector。
- GPC-Native 不做工厂生产执行、不做库存主账、不做质量放行主账、不直接改 GFIS 事实。
- GPC-Native 负责供应商、客户、平台订单、预约、车辆、承运商、在途、签收、回单、外部异常。

请输出：
1. 一期目标。
2. 一期非目标。
3. 用户角色：供应商、客户、承运商、平台运营、物流调度、销售/客服、监管/园区、系统管理员。
4. 核心业务流程。
5. 领域对象清单。
6. API 模块清单。
7. 事件主题清单。
8. 权限模型。
9. 与 GFIS、WAES、PVAOS 的边界。
10. 推荐技术栈。
11. 数据库表初稿。
12. 一期验收场景。

要求：
- 输出成可保存为 `architecture/05-gpc-native-phase1-model.md` 的 Markdown。
- 所有对象必须说明主责系统。
- 所有写入动作必须说明是在 GFIS/GPC-Native 内部业务确认，还是需要 WAES/Harness 治理授权。
```

### Prompt 03：GPC-Native 对象模型和数据库表

```text
请为 GPC-Native 设计一期对象模型和数据库表。

业务范围：
- 平台订单
- GFIS 工厂订单映射
- 供应商
- 客户
- ASN 到货通知
- 到货/发货预约
- 承运商
- 车辆
- 月台时段
- 发运单
- 在途状态
- POD 签收回单
- 外部协同异常
- 证据记录

设计要求：
1. 每个对象给出字段表。
2. 字段必须包含 ID、状态、来源系统、来源记录、创建人、更新时间、版本号。
3. 需要与 GFIS 对齐的对象必须有 `gfis_record_id` 或映射字段。
4. 需要事件发布的对象必须有 outbox 触发点。
5. 对关键状态机给出状态流转。
6. 标注哪些字段不能由 AI 自动写入。

输出：
- Markdown 对象目录。
- Postgres 表设计草案。
- 状态机表。
- 索引建议。
- 业务确认点和治理授权点。
```

### Prompt 04：从 Odoo GPC 抽取可复用业务资产

```text
请只读分析现有 Odoo GPC 项目，抽取可复用业务资产，但不要继续 Odoo core 二开。

目标路径：
/Users/lujunxiang/Projects/GlobalCloud GPC

必须先执行只读 preflight：
pwd
git status --short --branch
git remote -v
git branch --show-current

禁止：
- 不要修改文件。
- 不要 push/pull/merge/rebase/reset。
- 不要运行生产集成或数据库写入。

请输出：
1. 当前 Odoo GPC 中哪些文档、脚本、测试、对象概念可作为 GPC-Native 输入。
2. 哪些内容只能作为历史样本，不能直接复用。
3. 哪些内容应废弃或冻结。
4. 建议迁移到 GPC-Native 的领域对象。
5. 建议迁移到 GPC-Native 的验收场景。
6. 迁移风险。

输出格式：
`Odoo GPC -> GPC-Native 资产抽取报告`
```

## 5. GFIS 相关提示词

### Prompt 05：GFIS LES 最小模型设计

```text
请为 GFIS 设计 LES 厂内物流最小模型，使 V3.1 的物流主线能从 WMS 附属功能升级为独立执行主线。

必须读取：
- AI驱动工厂信息化系统完整方案V3.1.md
- 基于GlobalCloud项目群的智慧工厂架构设计方案.md
- GlobalCloud智慧工厂专项架构图集.md

GFIS 边界：
- GFIS 是单厂本地执行事实源。
- GFIS 承担工单、质量、库存、批次、厂内物流、设备、发货出库事实。
- GPC-Native 负责厂外运输、签收、回单。
- WAES 只读看板、治理规则和证据台账，不写 GFIS 主账，不审批具体事务。

请输出：
1. LES 一期目标。
2. LES 非目标。
3. 核心对象：KittingCheck、LineSideDelivery、LogisticsTask、LineSideStock、TransferTask、ReturnMaterial、LogisticsException、ResourceAssignment。
4. 每个对象字段。
5. 状态机。
6. 与 MES 工单、WMS 库存、QMS 质量状态、EAM 物流设备的关系。
7. 事件主题。
8. AI 可做的建议和不可做的动作。
9. 一期验收场景。

输出成可保存为 `architecture/04-gfis-les-minimum-model.md` 的 Markdown。
```

### Prompt 06：GFIS 到 GPC-Native 发货与签收闭环

```text
请设计 GFIS 与 GPC-Native 的发货、运输、签收、回单闭环。

业务链路：
GFIS 成品入库
-> GFIS 发货出库
-> GPC-Native 创建发运/运输记录
-> 车辆/承运商/在途状态
-> 客户签收
-> POD 回单
-> 回传 GFIS
-> WAES 证据台账展示

请输出：
1. 端到端流程。
2. 每一步主责系统。
3. 每一步输入、输出、状态。
4. 事件主题。
5. API 草案。
6. 幂等键设计。
7. 异常场景：数量不符、批次不符、车辆不符、签收延迟、客户拒收、回单缺失。
8. AI Agent 能提供哪些预警和建议。
9. 哪些动作必须业务系统人工确认，哪些动作必须 WAES/Harness 治理授权。
10. 一期验收矩阵。
```

## 6. WAES 控制塔相关提示词

### Prompt 07：WAES 绿色供应链体系控制塔模型

```text
请为 WAES 设计 GlobalCloud 绿色供应链体系控制塔模型。

WAES 定位：
- 跨系统控制塔。
- Agent Desktop。
- 治理规则和证据确证门。
- 证据台账。
- 场景包治理。
- 指标、风险、异常、复盘。

WAES 禁止：
- 不直接改写 GFIS 生产、质量、库存、发货事实。
- 不直接改写 GPC-Native 签收、运输、客户协同事实。
- 不把 AI 建议当业务事实。

请输出：
1. 控制塔首页布局。
2. 生产、质量、物流、设备、能源、安环、经营七类视图。
3. 每类视图的数据来源。
4. 指标口径。
5. 风险预警规则。
6. 治理确认队列。
7. Evidence Ledger 字段。
8. Agent Desktop 的工具清单。
9. 只读连接器边界。
10. 一期验收场景。

输出成 `architecture/06-waes-control-tower-model.md`。
```

### Prompt 08：WAES Evidence Ledger 设计

```text
请设计 WAES Evidence Ledger，用于承载绿色供应链体系跨系统验收和审计证据。

证据来源：
- GFIS 业务记录。
- GPC-Native 运输和签收记录。
- PVAOS 项目/伙伴协作记录。
- Brain SOP 和复盘文档。
- XiaoC prompt 版本和评估记录。
- Hermes/XGD Agent 执行记录。
- Harness 命令输出、测试结果、人工确认。

请输出：
1. EvidenceRecord 对象字段。
2. 证据类型分类。
3. 证据等级。
4. 来源系统和来源记录引用方式。
5. 附件、截图、日志、命令输出、业务审批引用和治理确认回执的存储方式。
6. 防伪造规则。
7. 与异常闭环、AI 建议、验收矩阵的关系。
8. 查询和报表需求。
9. 一期最小表结构。
```

## 7. 数据与事件相关提示词

### Prompt 09：统一对象目录

```text
请建立 GlobalCloud 绿色供应链体系项目群统一对象目录。

对象至少包括：
Tenant、Organization、Factory、Workshop、Warehouse、Dock、Supplier、Customer、Carrier、Vehicle、Material、MaterialLot、SalesOrder、PlatformOrder、OrderMapping、WorkOrder、BOM、KittingCheck、LogisticsTask、LineSideDelivery、QualityInspection、InventoryTransaction、Equipment、Shipment、ProofOfDelivery、ExceptionCase、AISuggestion、GovernanceApproval、BusinessApprovalReference、EvidenceVerification、EvidenceRecord、EdgeNode、DeviceSignal。

请对每个对象输出：
1. 中文名。
2. 英文名。
3. 推荐 ID 前缀。
4. 主责系统。
5. 协同系统。
6. 是否主数据。
7. 是否事件源。
8. 是否允许 AI 写入。
9. 关键字段。
10. 关键状态。
11. 关联对象。

必须明确：
- GFIS 负责哪些事实。
- GPC-Native 负责哪些事实。
- WAES 只记录哪些治理确认、业务审批引用和证据。
- Brain 只负责哪些知识对象。
```

### Prompt 10：统一事件合同

```text
请建立 GlobalCloud 绿色供应链体系一期统一事件合同。

事件范围：
- GFIS 发出的订单、工单、质量、库存、厂内物流、发货事件。
- GPC-Native 发出的预约、运输、签收、回单、外部异常事件。
- WAES 发出的治理确认、业务审批引用、证据、AI 建议状态事件。

每个事件必须包含：
eventId
eventType
eventVersion
sourceSystem
sourceRecordId
occurredAt
publishedAt
actorType
actorId
riskLevel
traceId
correlationId
idempotencyKey
payload
evidenceRefs

请输出：
1. 事件命名规范。
2. 事件 Envelope schema。
3. 事件列表。
4. 每个事件的 payload 草案。
5. 生产者和消费者。
6. 幂等与重试规则。
7. 失败补偿规则。
8. 不允许 AI 直接发布的业务事实事件。

输出成 `architecture/02-event-contracts.md`。
```

### Prompt 11：连接器与 API 网关设计

```text
请设计 GFIS、GPC-Native、WAES、PVAOS、Brain、XiaoC、Hermes/XGD 之间的 Connector Registry 和 API Gateway。

请输出：
1. 为什么不能项目直接互相调用。
2. Connector Registry 的字段。
3. API Gateway 的职责。
4. 每个系统的一期连接器。
5. 认证授权方式。
6. 速率限制。
7. 风险等级。
8. L1-L4 操作如何区分业务系统确认和治理授权。
9. OpenAPI 管理方式。
10. 连接器验收清单。
```

## 8. AI Agent 与提示词相关提示词

### Prompt 12：8 类绿色供应链体系 Agent 模板设计

```text
请为绿色供应链体系设计 8 类 AI Agent 的系统提示词模板。

Agent 类型：
1. 生产调度 Agent
2. 物流调度 Agent
3. 质量分析 Agent
4. 设备维护 Agent
5. 仓储库存 Agent
6. 能源优化 Agent
7. 安环风险 Agent
8. 经营驾驶舱 Agent

每个 Agent 输出：
1. 角色定位。
2. 可读取的数据。
3. 可自动执行的 L1/L2 动作。
4. 只能生成建议的 L3 动作。
5. 必须治理授权的 L4 动作，以及必须回到 GFIS/GPC-Native 的事务确认动作。
6. 永远禁止的 L5 动作。
7. 输出格式。
8. 证据引用格式。
9. 失败时如何报告。
10. 一段完整 system prompt。

要求：
- 不允许 Agent 直接改写业务事实。
- 不允许 Agent 确认质量放行、客户交期、资金事实、安全联锁。
- 必须要求引用来源系统和来源记录。
```

### Prompt 13：物流调度 Agent 完整提示词

```text
请生成“物流调度 Agent”的完整 system prompt。

业务职责：
- 齐套风险预测。
- 缺料停线风险识别。
- 备料和补料建议。
- 线边配送顺序建议。
- AGV/叉车/人工配送瓶颈分析。
- 月台排队和装车延误分析。
- 发货延迟风险预测。
- 运输计划调整建议。
- 批次、客户、车辆、装车不一致风险识别。
- 物流日报和交付风险摘要。

边界：
- 不能直接控制 AGV、叉车、装车、发运。
- 不能替换发货批次。
- 不能承诺客户交期。
- 不能放行质量状态不合格物料。
- 所有 L3 建议需业务系统确认，L4 治理变更需 WAES/Harness 授权。

输出格式：
1. 当前判断。
2. 证据引用。
3. 风险等级。
4. 建议动作。
5. 需要谁确认。
6. 不允许自动执行的事项。
7. 后续跟踪指标。
```

### Prompt 14：AI 建议生命周期设计

```text
请设计 AI 建议生命周期，使 AI 建议从生成到治理授权、业务系统确认、执行回执、复盘可追踪。

请输出：
1. AISuggestion 对象字段。
2. 状态机：draft、submitted、needs_evidence、approved、rejected、executed、closed。
3. L1/L2/L3/L4/L5 的处理方式。
4. 证据引用要求。
5. 人工确认记录。
6. 执行系统回执。
7. 效果评估指标。
8. 如何进入 Brain 复盘知识。
9. 如何防止 AI 建议被误当作业务事实。
```

## 9. 验收与治理提示词

### Prompt 15：一期验收矩阵

```text
请为 GlobalCloud 绿色供应链体系一期设计验收矩阵。

一期闭环：
订单 -> 排产 -> 采购/库存 -> 齐套检查 -> 工单 -> 备料 -> 线边配送 -> 生产报工 -> 质量检验 -> 成品入库 -> 装车发货 -> 签收回单 -> 异常复盘

请输出：
1. 验收场景。
2. 前置条件。
3. 操作步骤。
4. 参与系统。
5. 期望结果。
6. 证据类型。
7. 证据来源。
8. 阻塞条件。
9. 确认点，必须区分 GFIS/GPC-Native 业务确认和 WAES/Harness 治理确认。
10. 完成判定。

必须覆盖：
- 一张订单完整走完生产和发货。
- 一批原料追溯到供应商、工单、成品和客户。
- 一次缺料预警触发补料建议。
- 一次线边配送创建、执行、确认和关闭。
- 一次质量异常隔离、处理、复盘。
- 一次设备异常建单、维修、关闭。
- 一次装车校验订单、客户、批次、数量和车辆。
- 一次客户签收和回单闭环。
- 一份生产与物流日报自动生成。
```

### Prompt 16：Harness 项目群治理 Manifest

```text
请为 GlobalCloud 绿色供应链体系项目群建立总 Harness Manifest。

项目范围：
- GFIS
- GPC-Native
- 现有 Odoo GPC 原型
- WAES
- PVAOS
- Brain
- XiaoC
- XiaoG Agent / Hermes WebUI
- XGD
- Harness 控制台

请输出：
1. 项目群目标。
2. 非目标。
3. 每个项目的工作目录。
4. 每个项目的主责边界。
5. 允许读取范围。
6. 禁止写入范围。
7. 人工确认门。
8. 安全命令。
9. 禁止命令。
10. 证据目录。
11. 阶段状态标签。
12. complete 定义。

要求：
- 不把 partial/blocked 包装成 complete。
- 不把结构性通过等同于真实完成。
- 不把旧报告替代当前证据。
- 不允许未经确认 push、deploy、数据库写入或生产变更。
```

### Prompt 17：架构方案评审提示词

```text
请以严格架构评审人的身份评审 GlobalCloud 绿色供应链体系项目群方案。

请重点找：
1. 模块职责冲突。
2. 主责系统不清。
3. 数据事实归属不清。
4. AI 越权风险。
5. Odoo GPC 是否仍被误当成主线。
6. GFIS/GPC-Native/WAES 是否存在直接写主账风险。
7. 事件合同是否足够支撑集成。
8. 验收证据是否足够证明一期闭环。
9. 是否有未声明的生产/外部系统风险。
10. 哪些设计还只是愿景，不是可实施方案。

输出格式：
- 严重问题。
- 中等问题。
- 小问题。
- 必须补的文档。
- 可以进入实施的前置条件。
```

## 10. 子项目启动提示词

### Prompt 18：启动 GPC-Native 新项目

```text
请为 GPC-Native 启动一个新项目设计和脚手架方案。

当前不是要求立即写代码，先输出实施设计：
1. 项目名称和目录建议。
2. 技术栈选择：FastAPI 或 NestJS，给出取舍。
3. 数据库设计范围。
4. API 模块。
5. 事件 Outbox/Inbox。
6. 与 GFIS/WAES/PVAOS 的连接器。
7. 测试策略。
8. 本地运行方式。
9. Harness Manifest。
10. 第一周任务清单。

约束：
- 不继续 Odoo core 二开。
- 不接生产系统。
- 不写 GFIS 主账。
- 先实现订单、预约、运输、签收、回单最小闭环。
```

### Prompt 19：启动 GFIS LES 设计任务

```text
请在 GFIS 项目中进行 LES 最小模型设计，不直接修改运行代码。

目标路径：
/Users/lujunxiang/Projects/GlobalCloud GFIS

先执行只读 preflight：
pwd
git status --short --branch
git remote -v
git branch --show-current

读取：
- README.md
- docs/17-gcfis-functional-specification.md
- docs/20-gcfis-core-flow-closure-matrix.md
- PROJECT_HARNESS_MANIFEST.md

输出：
1. 当前 GFIS 已有物流/仓储能力。
2. 与 V3.1 LES 要求的差距。
3. LES 最小对象模型。
4. GFIS 内部事件。
5. 与 GPC-Native 的边界。
6. 与 WAES 控制塔的只读数据接口。
7. 不应由 AI 自动执行的动作。
8. 下一步是否需要写代码。

禁止：
- 不修改文件。
- 不运行 Docker/bench 写路径。
- 不覆盖现有 dirty 改动。
```

### Prompt 20：启动 WAES 控制塔设计任务

```text
请在 WAES 项目中设计绿色供应链体系控制塔，不直接改写业务代码。

目标路径：
/Users/lujunxiang/Documents/Codex Space/WAES

先执行只读 preflight：
pwd
git status --short --branch --untracked-files=no
git remote -v
git branch --show-current

读取：
- README.md
- docs/current/architecture.md
- docs/current/GLOBALCLOUD_CONTROL_TOWER.md
- docs/current/AGENT_DESKTOP_ARCHITECTURE.md

输出：
1. WAES 当前控制塔/Agent Desktop 能力。
2. 绿色供应链体系控制塔新增模块。
3. GFIS/GPC-Native/PVAOS 只读连接器设计。
4. Evidence Ledger 设计。
5. 治理确认队列设计。
6. 指标和看板。
7. 不写业务主账的防线。
8. 一期验收矩阵。

禁止：
- 不修改文件。
- 不触发部署。
- 不访问生产数据。
```

## 11. 推荐执行顺序

建议按以下顺序投喂提示词：

1. Prompt 00：总控上下文提示词。
2. Prompt 01：全局架构复核。
3. Prompt 09：统一对象目录。
4. Prompt 10：统一事件合同。
5. Prompt 11：连接器与 API 网关设计。
6. Prompt 02：GPC-Native 一期产品与技术蓝图。
7. Prompt 05：GFIS LES 最小模型设计。
8. Prompt 07：WAES 绿色供应链体系控制塔模型。
9. Prompt 14：AI 建议生命周期设计。
10. Prompt 15：一期验收矩阵。
11. Prompt 16：Harness 项目群治理 Manifest。
12. Prompt 17：架构方案评审提示词。

不要先写代码。当前最关键的是补齐：

1. 对象目录。
2. 事件合同。
3. 连接器边界。
4. GFIS LES 模型。
5. GPC-Native 一期模型。
6. WAES 控制塔模型。
7. AI 建议治理授权模型。
8. 一期验收矩阵。

这些补齐后，再进入项目代码实现会更稳。
