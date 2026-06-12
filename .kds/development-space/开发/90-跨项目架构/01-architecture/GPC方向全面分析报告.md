---
doc_id: GPCF-DOC-D54AF3DD5D
title: GlobalCloud 绿色供应链体系 — 全面分析报告
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GPC方向全面分析报告.md
source_path: 01-architecture/GPC方向全面分析报告.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系 — 全面分析报告

分析日期：2026-06-10
分析来源：`/Users/lujunxiang/Documents/GlobalCloud GPCF/`（160份体系设计文档）
目标：明确 GPC 在整体架构中的定位，校正方向

---

## 一、全局架构总览

### 1.1 三层主架构

```
治理与监控层 (WAES)
  ├── 规则、监控、治理、证据、状态、AI 授权、复盘
  ├── 不审批具体事务
  └── 主系统: WAES / Harness / Brain / XiaoC / Hermes / XGD（大象）

运营与协同层 (GPC / PVAOS)
  ├── 跨企业协同、订单池、TMS、POD、外部异常
  ├── 不做工厂生产执行、库存主账、质量放行
  └── 主系统: GPC（轻量公共服务平台）+ PVAOS（生态入口）

生产与执行层 (GFIS / Edge)
  ├── 工厂生产、质量、库存、批次、厂内物流、设备、发货出库
  ├── 单厂本地执行事实源（唯一权威）
  └── 主系统: GFIS（ERPNext）+ Edge（现场采集与协议转换）
```

### 1.2 四阶段生命周期 (S1-S4)

| 阶段 | 内容 | 主责 |
|------|------|------|
| S1 项目初始化 | 建立供应链项目、链厂模板、连接器 | WAES 发起 |
| S2 配置与 SOP | 补齐业务配置和 SOP（模板化、可版本化） | 运营+工厂 |
| S3 正式运营 | 真实 SOP 执行、事件、证据、复盘 | GPC + GFIS |
| S4 持续治理 | WAES 监控项目、连接器、事件、SOP、AI | WAES |

### 1.3 四流模型

| 流 | 责任 |
|----|------|
| 治理流 | WAES 规则、状态、证据、AI 授权不参与审批 |
| 业务流 | GPC 协同 + GFIS 执行 |
| 数据流 | 事件总线 + 连接器合同 + Evidence Ledger |
| AI 服务流 | 建议/摘要/预警，不得改写业务事实 |

---

## 二、GPC 项目的真实定位

### 2.1 历史沿革

```text
第一阶段: GFIS（ERPNext 工厂信息化系统）
  → 仓库: /Users/lujunxiang/Projects/GlobalCloud GFIS
  → 方向: 单厂执行系统（MES/QMS/WMS）

第二阶段: GC-FIS → GPC（考虑 Odoo 二开）
  → 仓库: /Users/lujunxiang/Projects/GlobalCloud GPC（当前）
  → 方向: 基于 Odoo 19 的公共平台（已废弃）

第三阶段: GPC（轻量公共服务平台） ← 当前官方方向
  → 仓库: 尚待建立
  → 方向: FastAPI/NestJS + React + Postgres 的原生公共服务平台
```

### 2.2 关键 ADR 结论

> **"GPC 从 Odoo 二开调整为原生公共服务平台"**（2026-06-07）

| 决定 | 内容 |
|------|------|
| 冻结 Odoo GPC | 不再新增 core 二开 |
| Odoo 降级 | 历史原型 + 流程验证样本 + 可选 back-office connector |
| 主线切换 | 新建 `GPC` 轻量公共服务平台 |
| 技术栈 | FastAPI 或 NestJS + React/Vite + Postgres + 事件驱动 |

### 2.3 当前 `/Users/lujunxiang/Projects/GlobalCloud GPC` 的状态

**这个仓库是已经废弃的历史原型**，不是 GPC 的正式主线。

| 资产 | 评估 |
|------|------|
| README.md（刚才改的） | 内容已错——GPC 不是供应链平台，GPC 才是 |
| gpc_sop_engine/（刚才建的） | 方向正确但归属错——应归 GPC，不归废弃的 GFIS 仓库 |
| index.html / app.js | 历史演示，无继续维护价值 |
| gcfis_custom/ | ERPNext 适配器——应归 GFIS 仓库，不是 GPC 仓库 |
| docs/ 44篇 | GFIS 历史文档，与 GPC 无关 |
| scripts/ 36个 | GFIS 验证脚本，与 GPC 无关 |

---

## 三、GPC 应建什么

### 3.1 一期最小对象（来自 ADR + 对象目录）

| 对象 | 说明 | 优先级 |
|------|------|--------|
| PlatformOrder | 平台订单（客户协同订单） | P0 |
| OrderMapping | 平台订单 → GFIS 工厂订单映射 | P0 |
| Supplier / Customer | 供应商/客户主数据 | P0 |
| ASN | 供应商到货通知 | P0 |
| Appointment | 到货/发货预约 | P0 |
| Carrier / Vehicle / DockSlot | 承运商/车辆/月台 | P0 |
| Shipment | 发运单/运输 | P0 |
| ProofOfDelivery | 签收回单 | P0 |
| ExceptionCase | 外部协同异常 | P0 |
| EvidenceRecord | 证据记录 | P0 |

### 3.2 一期事件

```
gpc.order.received
gpc.order.dispatched_to_factory
gpc.asn.created
gpc.appointment.confirmed
gpc.shipment.created / in_transit / signed
gpc.pod.attached
gpc.exception.raised / closed
```

### 3.3 GPC 的边界

| GPC 做 | GPC 不做 |
|---------------|----------------|
| 跨企业协同订单 | 工厂生产执行 |
| 运输管理(TMS) | 库存主账 |
| 签收回单(POD) | 质量放行 |
| 供应商/客户门户 | 设备维护 |
| 到货预约/月台 | 财务 ERP |
| 外部协同异常 | 改写 GFIS 事实 |

---

## 四、SOP 引擎的正确归属

### 4.1 您的"虚拟工厂 + SOP 引擎"概念分析

| 概念 | 在体系中的位置 |
|------|---------------|
| 虚拟工厂 | → 对应 S1-S2 的 `ProjectTopology` + `Factory` 对象 |
| 全局 SOP 库 | → 对应 S2 的 `SOPDefinition` + `SOPVersion` |
| SOP 段提取/下发 | → WAES 治理流程的一部分（SOP 模板 + 发布验证） |
| SOP 执行追踪 | → S3 的 `SOPExecution` 对象 |
| 数据权限隔离 | → `DataScopePolicy` / 连接器合同权限模型 |

**关键判断**：SOP 引擎不是 GPC 的一部分。SOP 的**管理、版本、发布、治理**归 WAES，SOP 的**执行**发生在 GPC（协同层）和 GFIS（执行层）。

### 4.2 建议的归属调整

```
SOP 引擎拆分为两层：

WAES 侧（治理层）
  ├── 全局 SOP 库管理（SOPDefinition / SOPVersion）
  ├── SOP 段提取与适配（按工厂合作范围）
  ├── SOP 版本管理与发布
  ├── SOP 合规度评分
  └── SOP 执行状态聚合

GPC / GFIS 侧（执行层）
  ├── 接收下发的 SOP 段
  ├── 在业务执行中引用 SOP（订单关联 → SOP 执行记录）
  ├── 回传执行状态和合规数据
  └── 不管理 SOP 版本和发布
```

---

## 五、三个项目仓库的正确分工

### 当前混乱状态

| 仓库 | 实际内容 | 应归系统 |
|------|---------|---------|
| `/Projects/GlobalCloud GFIS` | ERPNext 工厂信息化 | ✅ GFIS（正确） |
| `/Projects/GlobalCloud GPC` | GFIS 改名的 GPC + SOP 原型 | ❌ 应废弃或拆分为两个 |
| 无 | GPC | ❌ 待建 |

### 建议的仓库方案

```
/Projects/GlobalCloud GFIS          ← 保持，专做工厂适配器
  → ERPNext + gcfis_custom
  → 工厂执行事实源（MES/QMS/WMS）

/Projects/GlobalCloud GPC    ← 新建
  → FastAPI/NestJS + React/Vite
  → 轻量公共服务平台（订单/TMS/POD/异常）
  → 独立仓库，不继承 GFIS 代码

/Projects/GlobalCloud GPC           ← 废弃或归档
  → 移出 gpc_sop_engine/ 到 GPC
  → 移出 ERPNext 相关内容到 GFIS
  → 其余保留为历史参考
```

---

## 六、对刚才工作的纠偏

### 已完成的工作中哪些需要调整

| 我刚才做的事 | 评估 | 调整建议 |
|------------|------|---------|
| 改 README 为 GPC | ⚠️ 方向偏了 | 应改为 GPC 介绍，不是 GPC |
| 改 index.html 品牌 | ✅ 可行但不紧急 | 历史演示可保留但不作为主线 |
| 建 gpc_sop_engine/ | ✅ 内容正确，但位置错 | 迁移到 GPC 或 WAES 仓库 |
| 12段全局 SOP 库实例 | ✅ 质量好 | 保留，归 WAES 侧 SOP 治理 |
| 葛化 SOP 映射 | ✅ 有真实参考价值 | 保留，可作为 GFIS 适配器参考 |
| 虚拟工厂原型 | ✅ 方向正确 | 细化后归 GPC + WAES |

### 原来 GPC 方案中需要修正的内容

| 原来方案中的内容 | 问题 |
|-----------------|------|
| "GPC 不是 GFIS 的升级版" | 没说明 GPC 是 GPC |
| 三层架构（供应链基础服务/虚拟工厂/适配器） | 对标 GPC 而不是 GFIS |
| SOP 引擎全归 GPC | 应拆分 WAES 治理 + 执行层引用 |
| 7大池服务 | 应重新映射到体系各层 |

---

## 七、明确的方向建议

### 7.1 核心判断

**GPC 是轻量公共服务平台，不是重平台。** 它不是 GFIS 的替代，也是不是 Odoo 的替代。它是一个独立的、专注于跨企业协同的中间层系统。SOP 引擎和虚拟工厂是其治理层（WAES）和执行层（GPC + GFIS）协同的结果。

### 7.2 下一步做什么

根据模块分级判定表，P0 最小闭环中需要 **全面重构** 的两个模块就是 GPC 的起点：

1. **平台订单 (PlatformOrder)** — 当前分级：全面重构
2. **签收 (ProofOfDelivery)** — 当前分级：全面重构

**建议第一步**：在新建的 GPC 仓库中，从这两个对象开始建立最小服务原型。

### 7.3 六个专项中的"链同专项"

链同专项（PVAOS + GPC 协同域）已经完成了只读预检，下一阶段是首轮实施前验证。这正是 GPC 应该纳入的专项轨道。

---

## 八、总结

| 问题 | 答案 |
|------|------|
| GPC 的正确方向是什么？ | GPC — 轻量公共服务平台 |
| 当前 `GlobalCloud GPC` 仓库是什么？ | 废弃的历史原型（原 Odoo 路线） |
| SOP 引擎归哪里？ | WAES 治理解 + GPC/GFIS 执行引用 |
| 虚拟工厂归哪里？ | S1-S2 的 ProjectTopology |
| 下一步做什么？ | 新建 GPC 仓库，从 PlatformOrder + POD 开始 |
| 和 GFIS 是什么关系？ | GPC 协同层 ↔ GFIS 执行层，事件驱动 |
| 和 WAES 是什么关系？ | WAES 治理约束 → GPC 业务执行 |
