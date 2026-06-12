---
doc_id: GPCF-DOC-D48C6EB801
title: GlobalCloud 绿色供应链体系企业级知识库方案
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库方案.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系企业级知识库方案

日期：2026-06-07
状态：知识底座专项方案 v1
适用范围：GlobalCloud 绿色供应链体系的数据层、知识层、WAES 治理层、Brain/XiaoC/Hermes/XGD AI 服务链。

## 1. 方案定位

当前 `LLM Wiki` 与 `Brain` 都可以承担知识整理、索引、检索、RAG 和 Agent 消费能力，但两者都还不适合直接充当 GlobalCloud 绿色供应链体系的企业级知识库真源。

因此本方案的核心结论是：

1. 企业级知识库必须单独定义为 **知识主存层**。
2. `LLM Wiki` 与 `Brain` 应归入 **知识引擎层** 或 **知识编制/检索层**。
3. `WAES` 负责知识准入、证据分级、引用审计、AI 授权和知识发布治理。
4. 测试结束后可以对 `LLM Wiki` 与 `Brain` 做唯一性选择，但这个唯一性应优先发生在知识引擎层，而不是企业知识真源层。

## 2. 为什么当前两者都还不是企业级知识库

### 2.1 当前能力更像知识工作台

`LLM Wiki` 与 `Brain` 当前更擅长：

1. 知识整理与页面化表达。
2. 知识切片、索引和检索。
3. RAG 上下文提供。
4. Agent 问答、摘要、复盘和建议。

### 2.2 企业级知识库必须具备的能力

企业级知识库至少需要：

1. 统一知识对象编号。
2. 文档版本和发布状态。
3. 组织、项目、角色、密级级别权限。
4. 发布审批、废止、归档和保留策略。
5. 审计日志和引用日志。
6. 与项目、工厂、SOP、证据、事件、审批的主数据绑定。
7. 单向同步到索引层，禁止 AI 直接反写真源。
8. 灾备、备份、恢复和跨环境迁移能力。

## 3. 目标架构

### 3.1 AI 与数据层中的知识架构

```text
业务事实层
-> 资源仓库域（当前已定义十一池）
-> 结构化数据库域
-> 知识主存域（企业级知识库）
-> 知识引擎域（LLM Wiki 或 Brain）
-> AI 服务域
-> WAES 治理与审计
```

### 3.2 分层职责

| 层 | 主责 | 主组件 | 不做什么 |
|---|---|---|---|
| 业务事实层 | 产生业务事实 | PVAOS / GPC / GFIS / Edge | 不承载知识真源 |
| 资源语义层 | 用资源仓库组织资源语义，当前已定义十一池 | WAES / Data Platform / 对象目录 | 不等于数据库 |
| 结构化数据库层 | 保存业务、治理、指标、知识元和读模型结构化数据 | 各类结构化数据库 | 不等于知识真源全文 |
| 知识主存层 | 保存企业级原文档和发布版本 | 企业级知识库 | 不直接做 AI 推理 |
| 知识引擎层 | 切片、索引、RAG、图谱、引用回指 | LLM Wiki / Brain | 不应反写主存层 |
| 治理与授权层 | 准入、发布、证据、引用、AI 授权 | WAES | 不替代业务系统 |

## 4. 企业级知识库的对象模型

建议新增以下知识对象：

| 对象 | 说明 |
|---|---|
| KnowledgeDocument | 企业级知识文档主对象 |
| KnowledgeVersion | 文档版本 |
| KnowledgeRelease | 发布记录 |
| KnowledgeFolder | 目录与空间 |
| KnowledgeClassification | 密级与分类 |
| KnowledgeAccessPolicy | 访问控制策略 |
| KnowledgeCitation | 引用记录 |
| KnowledgeIngestJob | 向知识引擎发布的同步任务 |
| KnowledgeRetentionPolicy | 保留和归档策略 |
| KnowledgeAuditLog | 查看、下载、发布、引用审计日志 |

### 4.1 核心字段建议

`KnowledgeDocument` 至少包含：

1. `knowledgeDocumentId`
2. `title`
3. `documentType`
4. `tenantId`
5. `organizationId`
6. `projectId`
7. `spaceId`
8. `classificationLevel`
9. `ownerId`
10. `source_refs`
11. `currentVersionId`
12. `releaseStatus`
13. `retentionPolicyId`

## 5. 文档生命周期

建议统一采用：

```text
draft -> in_review -> approved -> effective -> superseded -> retired -> archived
draft -> rejected
effective -> frozen
frozen -> effective
```

说明：

1. `approved` 表示发布审批通过。
2. `effective` 表示正式生效并可作为标准知识源。
3. `superseded` 表示被新版本替代。
4. `retired` 表示退役，不再作为现行依据。
5. `archived` 表示归档保存。

## 6. LLM Wiki 与 Brain 在新架构中的角色

### 6.1 LLM Wiki 建议定位

建议优先作为：

1. 规范内容编制层。
2. 历史沉淀和人工维护层。
3. 宪法、体系、项目方法论的内容组织层。

### 6.2 Brain 建议定位

建议优先作为：

1. 新一代知识引擎层。
2. RAG、索引、图谱和引用回指层。
3. Agent 检索服务层。

### 6.3 不建议的用法

1. 不建议把 `LLM Wiki` 直接当企业知识真源数据库。
2. 不建议把 `Brain` 直接当唯一规范发布源。
3. 不建议让 Agent 自动改写主存层正式文档。

## 7. 基于两者的升级方案

### 7.1 对 LLM Wiki 的升级方向

建议补齐：

1. 文档编号和统一元数据。
2. 发布状态与版本链。
3. 发布审批记录。
4. 目录级、项目级和密级权限。
5. 标准引用锚点与 `source_refs`。
6. 与知识引擎发布的单向同步任务。

### 7.2 对 Brain 的升级方向

建议补齐：

1. ingest 来源标识和版本绑定。
2. 引用切片回指。
3. space / project / classification 级隔离。
4. 知识删除、失效和重建策略。
5. 审计日志和 Agent 消费记录。
6. 结果可信等级输出。

### 7.3 双轨测试期的推荐架构

```text
企业级知识主存层
-> LLM Wiki 编制与规范视图
-> Brain 索引与检索视图
-> Brain 知识服务
-> XiaoC / Hermes / XGD
-> WAES 审计与授权
```

## 8. WAES 在企业知识库中的职责

`WAES` 只做治理，不做知识正文编制主账。

主责包括：

1. 知识准入规则。
2. 知识发布治理审批。
3. `source_refs` 与证据等级校验。
4. AI 可见范围与知识域授权。
5. 引用审计。
6. 知识引擎发布验证。
7. 失效知识拦截。

## 9. 本阶段重点工作建议

本阶段不要求立即落成完整企业级知识产品，但应优先完成以下重点工作：

1. 定义企业级知识对象模型。
2. 定义知识主存层与知识引擎层的边界。
3. 为 `LLM Wiki` 和 `Brain` 建立统一 ingest 元数据。
4. 建立知识发布链和审计链。
5. 建立 `WAES` 的知识准入与授权门。
6. 完成双轨测试的评估矩阵。

## 10. 结论

当前最稳妥的方向不是在 `LLM Wiki` 和 `Brain` 中直接挑一个充当企业级知识库，而是：

1. 先建立企业级知识主存层。
2. 再让 `LLM Wiki` 和 `Brain` 在其之上承担知识编制、索引和检索职责。
3. 测试结束后再决定知识引擎层的唯一性。
