---
doc_id: GPCF-DOC-09655E45C0
title: ADR：GPC 从 Odoo 二开调整为原生公共服务平台
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, XiaoC, XGD, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/ADR-GPC从Odoo二开调整为原生公共服务平台.md
source_path: 01-architecture/ADR-GPC从Odoo二开调整为原生公共服务平台.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ADR：GPC 从 Odoo 二开调整为原生公共服务平台

日期：2026-06-07
状态：已纳入 GlobalCloud 绿色供应链体系设计
决策范围：GlobalCloud GPC 在 GlobalCloud 绿色供应链体系中的技术路线和系统边界
当前口径：GPC 归入运营与协同层；WAES 归入治理与监控层，只做规则、监控、治理、证据、状态和 AI 授权，不参与具体事务审批。

当前阅读口径：

1. `GPC` 是绿色供应链平台一期主线系统。
2. `WAES` 不承办平台业务事务审批。
3. `GFIS` 保持工厂事实源地位。
4. 宪法内容主要通过治理规则、证据门禁、状态升级和 AI 授权约束进入平台。

## 1. 背景

GlobalCloud GPC 的原始思路是基于 Odoo 19 进行二开，形成“绿色供应链公共服务平台”。经过本地实践和项目群架构分析，这条路线暴露出明显风险：

1. Odoo 是完整 ERP 套件，不是轻量跨企业公共服务平台。
2. 继续改 Odoo core 会形成私有 Odoo 发行版，长期维护成本高。
3. Odoo 的模块、权限、前端、升级和上游合并复杂度，会压过 GPC 的真实业务目标。
4. GFIS 已经承担工厂本地 ERP/MES/QMS/WMS 执行主账，GPC 再走重 ERP 路线会与 GFIS 边界重叠。
5. GPC 的核心需求实际是供应商协同、客户协同、订单流转、TMS、签收回单、公共服务、监管/园区/联盟协同，更适合原生 API 与事件驱动架构。

## 2. 决策

GlobalCloud GPC 主线从：

```text
基于 Odoo 19 的二开公共平台
```

调整为：

```text
GPC：轻量绿色供应链协同平台
```

现有 `/Users/lujunxiang/Projects/GlobalCloud GPC` 中的 Odoo 项目不再作为主架构底座继续 core 二开，降级为：

1. 历史原型。
2. 流程验证样本。
3. 可选 back-office connector。

## 3. 新系统定位

GPC 只做跨企业协同和外部服务：

- 供应商协同。
- 客户协同。
- 平台订单流转。
- 到货预约。
- 车辆、月台、承运商管理。
- TMS 运输跟踪。
- POD 签收回单。
- 绿色供应链公共服务。
- 园区、监管、联盟协同。
- 与 GFIS、WAES、PVAOS 的事件/API 集成。

GPC 不做：

- 工厂生产执行。
- 库存主账。
- 质量放行主账。
- 设备维护主账。
- 复杂财务 ERP。
- 直接改写 GFIS 的生产、质量、库存、发货事实。

## 4. 推荐技术架构

| 层 | 推荐 |
|---|---|
| 前端 | React / Vite / TypeScript |
| 后端 | FastAPI 或 NestJS，按团队维护能力二选一 |
| 数据库 | Postgres |
| 接口 | OpenAPI |
| 集成 | API Gateway + Connector Registry |
| 事件 | Outbox/Inbox + 幂等键 + 重试 + 补偿 |
| 权限 | 租户 / 组织 / 角色 / 外部伙伴 / 业务确认权限 |
| 工作流 | 轻量状态机，先不引入重 BPM |
| 证据 | Evidence Ledger |
| AI | 通过 WAES/Hermes/XiaoC 进入治理授权链；具体业务执行仍进入 GPC/GFIS 内部确认流程，不直接写业务事实 |

四流优化补充：

| 维度 | GPC 责任 | 边界 |
|---|---|---|
| 治理流 | 接受 WAES 的规则、指标、连接器和 AI 授权约束 | 不承办 WAES 治理审批 |
| 业务流 | 平台订单、ASN、预约、运输、POD、外部异常、多厂分单 | 不做 GFIS 工厂执行主账 |
| 数据流 | 通过连接器合同发布事件、业务确认引用和证据 | 不共享 GFIS/WAES 数据库 |
| AI 服务流 | 接收 AI 建议和草案，业务动作在 GPC 内部确认 | 不接受 AI 直接写签收、承诺或异常关闭事实 |

## 5. 一期最小对象

| 对象 | 说明 |
|---|---|
| `PlatformOrder` | 平台订单或客户协同订单 |
| `OrderMapping` | GPC 平台订单与 GFIS 工厂订单映射 |
| `Supplier` | 供应商 |
| `Customer` | 客户 |
| `ASN` | 供应商到货通知 |
| `Appointment` | 到货或发货预约 |
| `Carrier` | 承运商 |
| `Vehicle` | 车辆 |
| `DockSlot` | 月台时段 |
| `Shipment` | 运输/发运单 |
| `ProofOfDelivery` | 签收回单 |
| `ExceptionCase` | 外部协同异常 |
| `EvidenceRecord` | 证据记录 |

## 6. 一期事件

```text
gpc.order.received
gpc.order.dispatched_to_factory
gpc.asn.created
gpc.appointment.confirmed
gpc.vehicle.arrived
gpc.shipment.created
gpc.shipment.in_transit
gpc.shipment.signed
gpc.pod.attached
gpc.exception.raised
gpc.exception.closed
gfis.shipment.released
gfis.quality.status_changed
gfis.inventory.availability_changed
```

## 7. 与 GFIS 的边界

| 事项 | 主责系统 |
|---|---|
| 工厂订单确认 | GFIS |
| 生产工单 | GFIS |
| 质量检验/放行/隔离 | GFIS |
| 库存和批次主账 | GFIS |
| 厂内物流任务 | GFIS |
| 发货出库事实 | GFIS |
| 客户/供应商外部协同 | GPC |
| 车辆、承运商、在途、签收、回单 | GPC |
| 跨系统看板、治理规则、证据、状态审计 | WAES |

## 8. 迁移路径

1. 冻结现有 Odoo GPC，不再新增 core 二开。
2. 从现有 Odoo GPC 文档和 smoke 脚本中抽取真实业务对象。
3. 在绿色供应链体系设计文档中建立 GPC 对象目录、事件目录、接口目录。
4. 建立 GPC 最小服务原型，只覆盖订单、预约、运输、签收、回单。
5. GFIS 输出发货事件给 GPC。
6. GPC 输出签收回传给 GFIS。
7. WAES 读取 GFIS/GPC 事件并进入控制塔、治理规则和证据台账。
8. 如未来确需财务、会计、CRM back-office，再通过 Odoo connector 接入，不把 Odoo 放回主线。

## 9. 验收口径

GPC 一期不能用“页面存在”作为完成标准，必须满足：

1. 一张平台订单能映射到 GFIS 工厂订单。
2. 一次 GFIS 发货能生成 GPC 运输/发运记录。
3. 一次客户签收能形成 POD，并回传 GFIS。
4. 一次运输异常能进入 `ExceptionCase` 并闭环。
5. WAES 能只读展示订单、运输、签收、异常和证据。
6. AI 只能生成建议和摘要，不能直接改写发货、签收、质量和库存事实。

## 10. 影响

正向影响：

- 避免长期维护私有 Odoo 发行版。
- 降低平台复杂度。
- 边界更清晰，GFIS 专注工厂执行，GPC 专注外部协同。
- 更适合事件驱动、API 集成和控制塔证据链。

代价：

- 需要新建 GPC 项目或重构当前 GPC 工作区。
- 需要重新设计对象模型、API 和事件合同。
- 现有 Odoo GPC 的部分成果需要抽取为业务样本，而不是直接复用为主线系统。

最终判断：

**GPC 是更稳、更可控、更符合 GlobalCloud 绿色供应链体系边界的路线。**
