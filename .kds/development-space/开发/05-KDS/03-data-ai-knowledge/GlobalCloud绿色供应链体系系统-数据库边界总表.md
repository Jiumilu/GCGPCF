---
doc_id: GPCF-DOC-062D4DA687
title: GlobalCloud 绿色供应链体系系统-数据库边界总表
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系系统-数据库边界总表.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系系统-数据库边界总表.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系系统-数据库边界总表

日期：2026-06-07
状态：实施硬约束表 v1
适用范围：PVAOS、GPC、GFIS、WAES、资源仓库、知识主存、知识引擎、AI 服务、读模型与分析域。

## 1. 目的

本表用于把“结构化数据库域”从架构概念收敛成实施约束，重点回答：

1. 每类数据库归谁主责。
2. 哪些对象允许写入。
3. 哪些系统只能读、不能写。
4. 哪些协同必须通过 API、事件、证据引用或读模型完成。

## 2. 总原则

1. 不共享业务主账表。
2. 一个业务事实只能有一个主账系统。
3. 跨系统协同默认走 `API + Event`。
4. 跨系统查询默认走读模型或受控查询服务，不直连他方主账库。
5. WAES 可以聚合、审计、引用，但不反写业务主账事实。
6. AI 服务域不直接写任何业务主账库或正式知识正文库。

## 3. 数据库边界总表

| 数据库域 | 主责系统 | 存储内容 | 允许写入方 | 允许读取方 | 禁止事项 | 推荐协同方式 |
|---|---|---|---|---|---|---|
| PVAOS 业务主账库 | PVAOS | Tenant、Organization、ProgramProject、Partner、PortalAccount、RoleGrant | PVAOS | WAES、GPC、读模型服务 | GFIS、WAES、AI 直接写表 | API、事件、读模型 |
| GPC 业务主账库 | GPC | PlatformOrder、OrderMapping、ASN、Appointment、Shipment、POD、ExternalException、多厂协同对象 | GPC | WAES、GFIS、读模型服务 | GFIS、WAES、AI 直接写表 | API、事件、BusinessApprovalReference、读模型 |
| GFIS 业务主账库 | GFIS | FactoryOrder、WorkOrder、QualityInspection、InventoryTransaction、MaterialLot、Equipment、FactoryShipmentRelease 等 | GFIS | WAES、GPC、读模型服务 | GPC、WAES、AI 直接写表 | API、事件、BusinessApprovalReference、读模型 |
| WAES 治理审计库 | WAES | GovernancePolicy、GovernanceApproval、EvidenceRecord、EvidenceVerification、MetricDefinition、MetricSnapshot、StatusAudit、AgentToolGrant | WAES | PVAOS、GPC、GFIS、知识引擎、读模型服务 | 业务系统把事务审批写入此库替代主账 | API、事件、审计查询 |
| 资源仓库结构化库 | WAES / Data Platform | 资源池索引、聚合关系、主数据映射、资源标签、资源状态投影 | 资源仓库服务 | WAES、读模型服务、知识引擎 | 业务系统把资源仓库当主账直接录入业务事实 | 事件投影、受控管理 API |
| 指标时序库 | WAES / Data Platform | MetricSnapshot、时序信号、趋势、风险、告警聚合 | 指标计算服务、时序采集服务 | WAES、读模型服务、知识引擎 | 业务系统手工修改指标结果 | 事件流、批处理、流处理 |
| 证据与追踪库 | WAES / Data Platform | EvidenceRecord、TraceContext、LineageRecord、回执索引、日志索引 | WAES、证据采集服务 | WAES、知识引擎、读模型服务 | 业务系统把证据库当业务主账 | 事件、日志采集、引用索引 |
| 知识元数据库 | 知识主存服务 | KnowledgeDocument 元数据、KnowledgeVersion、KnowledgeRelease、KnowledgeAccessPolicy、KnowledgeCitation | 知识主存服务 | WAES、知识引擎、读模型服务 | LLM Wiki、Brain、AI 直接改正式版本元数据 | 发布链、ingest 任务 |
| 正式知识正文存储 | 知识主存服务 | 制度、宪法、SOP、方案、纪要、合同、验收、复盘正文与附件 | 知识主存服务 | 知识主存服务、知识引擎 ingest | AI、知识引擎直接改正式正文 | 发布链、对象存储、文档服务 |
| 知识引擎索引库 | LLM Wiki / Brain | 切片、索引、向量、图谱、回指索引、查询缓存 | 知识引擎服务 | WAES、XiaoC、Hermes/XGD、读模型服务 | 被当作企业级知识真源 | ingest、检索 API |
| AI 运行状态库 | XiaoC / Hermes / XGD | PromptEvaluation、ModelEvaluation、AgentRun、AgentRunStep、AISuggestion、运行日志 | XiaoC、Hermes/XGD | WAES、读模型服务 | AI 运行结果回写业务主账或正式知识正文 | API、事件、审计流 |
| 查询读模型库 | Query Service / Data Platform | 控制塔视图、跨系统报表、聚合投影、轻量查询表 | 投影服务、ETL/流处理服务 | WAES、GPC、GFIS、PVAOS、知识引擎 | 当作真实主账回写来源系统 | 事件投影、定时同步 |

## 4. 强制边界

### 4.1 绝对禁止

1. `GPC` 直写 `GFIS` 业务主账表。
2. `GFIS` 直写 `GPC` 业务主账表。
3. `WAES` 直写任何业务主账表。
4. `LLM Wiki`、`Brain` 直写正式知识版本元数据或正文。
5. `XiaoC`、`Hermes`、`XGD` 直写业务主账表或正式知识正文。

### 4.2 允许但受控

1. 通过 API 创建草稿。
2. 通过事件同步投影。
3. 通过 `BusinessApprovalReference` 引用业务确认结果。
4. 通过 `EvidenceRecord` 引用证据与附件。

## 5. 实施建议

1. 先做数据库域边界清单，再做表设计。
2. 先定义写权限，再开放读权限。
3. 查询需求优先走读模型，不为读方便破坏主账隔离。
4. 所有跨域读写都应保留审计记录。
