---
doc_id: GPCF-DOC-E2FDF91E39
title: GlobalCloud 绿色供应链体系资源仓库-业务对象映射总表
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系资源仓库-业务对象映射总表

日期：2026-06-07
状态：实施硬约束表 v1
适用范围：资源仓库域、对象目录、读模型、知识引擎、控制塔与多项目扩展。

## 1. 定位

资源仓库是资源语义聚合层，不是业务主账层，不是直接录入层，也不是独立业务系统。

它的职责是：

1. 聚合资源语义。
2. 建立跨系统对象映射。
3. 为控制塔、分析、知识引擎和 AI 提供稳定资源视角。

## 2. 资源仓库映射总表

| 资源池 | 当前状态 | 主责系统 | 来源对象 | 是否主账 | 是否可直接录入 | AI 是否可写 | 主要使用方 | 说明 |
|---|---|---|---|---|---|---|---|---|
| 订单池 | 已定义 | PVAOS / GPC | ProgramProject、PlatformOrder、OrderMapping、FactoryOrder 引用 | 否 | 否 | 否 | WAES、GPC、知识引擎 | 统一客户、项目、订单和交付语义 |
| 运力池 | 已定义 | GPC | Carrier、Vehicle、Shipment、TransitCheckpoint、POD | 否 | 否 | 否 | WAES、GPC、AI 服务 | 统一运输资源与在途协同语义 |
| 产能池 | 已定义 | GFIS | Factory、Workshop、Equipment、CapacityCommitment、CapacitySnapshot | 否 | 否 | 否 | WAES、GPC、知识引擎 | 统一工厂、产线、设备与产能语义 |
| 资金池 | 已定义 | WAES / PVAOS / GPC 引用 | 合同、回款、融资建议、资金缺口、风险证据 | 否 | 否 | 可生成建议，不可落账 | WAES、知识引擎 | 当前应以引用和聚合为主，避免形成新的资金主账 |
| 政策池 | 已定义 | WAES / 知识主存 | 政策文档、合规要求、补贴条款、监管规则 | 否 | 否 | 可生成候选知识，不自动生效 | WAES、知识引擎、AI 服务 | 强依赖知识主存与知识引擎 |
| 装备池 | 已定义 | GFIS / Edge | Equipment、MaintenanceOrder、EdgeNode、DeviceSignal 引用 | 否 | 否 | 否 | GFIS、WAES、知识引擎 | 设备台账与设备能力语义聚合 |
| 数据池 | 已定义 | WAES / Data Platform | SchemaVersion、DataQualityRule、DataQualityIssue、LineageRecord、RetentionPolicy | 否 | 否 | 否 | WAES、知识引擎 | 反映数据质量、来源与治理状态 |
| 能源池 | 已定义 | GFIS / Edge / WAES | 能耗、绿电、时序采集、碳相关指标与证据 | 否 | 否 | 可生成分析建议，不可落账 | WAES、知识引擎 | 当前适合先做指标与证据聚合 |
| 原料池 | 已定义 | GFIS | Material、MaterialLot、质量结果、供应商引用 | 否 | 否 | 否 | GFIS、GPC、WAES | 原料与批次追溯语义主域 |
| 人才池 | 已定义 | PVAOS / WAES / 知识主存 | 组织、角色、岗位、能力、授权、培训知识 | 否 | 否 | 可生成候选画像，不自动确证 | WAES、AI 服务 | 当前为占位池，建议 P2 深化 |
| 场景池 | 已定义 | WAES | GovernanceRule、SOPDefinition、ConnectorPolicy、AIAuthorizationPolicy | 否 | 否 | 可生成草案，不自动生效 | WAES、知识引擎、AI 服务 | 规则与编排池，不是事实池 |

## 3. 后续可扩展池建议

| 新增池候选 | 建议优先级 | 说明 |
|---|---:|---|
| 信用池 | P1 | 客户、供应商、承运商、项目与履约信用视图 |
| 碳资产池 | P1 | 碳排、绿电、碳汇、碳资产路径与证据 |
| 服务池 | P2 | 运维服务、售后服务、驻厂服务、协同服务能力 |
| 算法池 | P2 | 规则、模型、算法、优化策略、评估结果 |
| 生态池 | P2 | 平台伙伴、园区、监管、金融、渠道生态关系 |

## 4. 强制解释规则

1. 资源池对象不替代来源系统主账对象。
2. 资源池状态默认来自事件投影或受控聚合，不通过人工直接改写。
3. AI 只能生成建议、候选标签或分析草案，不能直接写资源池中的业务确定性状态。
4. 新增池必须先定义：
   - 主责系统
   - 来源对象
   - 是否主账
   - 是否允许 AI 写入
   - 主要使用方

## 5. 实施建议

1. 一期只做与 P0 闭环直接相关的池：订单池、运力池、产能池、原料池、场景池、数据池。
2. 资金池、能源池、人才池先做聚合视图，不急于深建。
3. 后续新增池时，不改总层次结构，只扩展资源仓库域内部定义。
