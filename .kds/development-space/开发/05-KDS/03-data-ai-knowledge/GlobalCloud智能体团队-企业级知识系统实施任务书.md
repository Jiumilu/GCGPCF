---
doc_id: GPCF-DOC-0A5E8FD5E6
title: GlobalCloud智能体团队-企业级知识系统实施任务书
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud智能体团队-企业级知识系统实施任务书.md
source_path: 03-data-ai-knowledge/GlobalCloud智能体团队-企业级知识系统实施任务书.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud智能体团队-企业级知识系统实施任务书

日期：2026-06-08
适用范围：GlobalCloud 绿色供应链体系中的企业级知识主存域、LLM Wiki、Brain、WAES 知识治理域、XiaoC/Hermes/XGD 知识消费域。
状态：实施任务书。用于组织实施，不代表系统已运行完成。

## 1. 任务目标

本任务书用于指导小即团队实施企业级知识系统，建立：

1. 唯一正式知识真源；
2. 编制视图、知识引擎、知识服务三层协同机制；
3. WAES 的知识准入、发布验证、引用审计和 AI 授权门禁；
4. 面向 AI 与业务应用的可控知识消费链；
5. 可验收、可审计、可失效、可回滚的知识生命周期。

## 2. 必须继承的当前基线

实施过程中必须严格继承以下口径：

1. 企业级知识真源位于 **知识主存层**。
2. `LLM Wiki` 只负责知识编制与组织视图。
3. `Brain` 是主知识引擎。
4. `Brain` 是知识服务层。
5. `WAES` 只做知识治理与审计，不做知识正文主账。
6. AI 不能直接改正式知识版本。
7. 正式发布链必须是单向链路：
   - 知识主存层
   - -> `KnowledgeIngestJob`
   - -> `LLM Wiki`
   - -> `Brain`
   - -> `Brain`
   - -> `XiaoC / Hermes / XGD`
   - -> `WAES` 审计与授权

## 3. 最终系统分工

### 3.1 知识主存层

负责：

1. `KnowledgeDocument`
2. `KnowledgeVersion`
3. `KnowledgeRelease`
4. `KnowledgeAccessPolicy`
5. `KnowledgeAuditLog`

不负责：

1. RAG
2. 检索服务
3. AI 直接消费接口
4. 知识编制视图

### 3.2 LLM Wiki

负责：

1. 知识编制视图
2. 知识章节组织
3. 规范表达
4. 人工可维护知识页面

不负责：

1. 正式知识真源
2. 反写知识主存层
3. 取代 Brain 成为主知识引擎

### 3.3 Brain

负责：

1. 主知识引擎
2. 索引
3. 检索
4. RAG
5. 图谱
6. 引用回指

不负责：

1. 正式知识真源
2. 正式版本发布主账
3. 直接修改知识主存层

### 3.4 Brain

负责：

1. 知识服务层
2. SOP、案例、复盘知识服务目录
3. 面向 AI、控制塔、业务应用的知识消费编排
4. 对外统一知识服务接口

不负责：

1. 正式知识真源
2. 主知识引擎唯一承载
3. 正式文档直接发布

### 3.5 WAES

负责：

1. 知识准入
2. 证据等级
3. 引用审计
4. 发布验证
5. 失效拦截
6. AI 授权
7. 治理结论

不负责：

1. 知识正文编制
2. 知识正文真源
3. 事务审批

## 4. 实施工作包

### WP1 知识主存层实施包

目标：

1. 建立正式知识真源模型；
2. 建立版本、发布、权限、归档、审计骨架；
3. 建立结构化元数据库映射。

交付物：

1. 知识主存对象实现清单
2. 知识主存状态机
3. 知识主存元数据表/对象映射
4. 发布链与回滚链说明

### WP2 LLM Wiki 编制视图实施包

目标：

1. 建立知识编制视图；
2. 建立章节组织和规范表达能力；
3. 对接知识主存发布链。

交付物：

1. `KnowledgeCompileView` 实施说明
2. 编制视图同步规则
3. 与知识主存层的单向同步规则

### WP3 Brain 主知识引擎实施包

目标：

1. 建立主知识引擎；
2. 建立索引、检索、RAG、引用回指能力；
3. 建立 `KnowledgeEngineIndex` 与 `KnowledgeIngestJob` 执行链。

交付物：

1. 索引结构说明
2. 引擎 ingest 流程
3. 引用回指结构
4. 索引刷新与失效处理规则

### WP4 Brain 知识服务层实施包

目标：

1. 建立 `KnowledgeServiceCatalog`；
2. 面向 SOP、案例、复盘、Agent 提供统一知识服务能力；
3. 严格只消费引擎结果，不直接改正式知识。

交付物：

1. Brain 知识服务目录
2. 服务接口与消费边界
3. 对 XiaoC / Hermes / XGD 的消费说明

### WP5 WAES 知识治理实施包

目标：

1. 建立知识准入门
2. 建立知识发布验证门
3. 建立知识引用审计门
4. 建立 AI 可见范围和失效拦截机制

交付物：

1. 准入规则
2. 发布验证规则
3. 审计与引用策略
4. 失效拦截规则

## 5. 关键对象

实施过程中必须至少覆盖以下对象：

1. `KnowledgeDocument`
2. `KnowledgeVersion`
3. `KnowledgeRelease`
4. `KnowledgeAccessPolicy`
5. `KnowledgeAuditLog`
6. `KnowledgeCompileView`
7. `KnowledgeEngineIndex`
8. `KnowledgeServiceCatalog`
9. `KnowledgeIngestJob`

## 6. 关键事件

实施过程中必须至少覆盖以下事件：

1. `knowledge.document.created`
2. `knowledge.version.approved`
3. `knowledge.release.effective`
4. `knowledge.release.rolled_back`
5. `knowledge.access_policy.changed`
6. `knowledge.compile_view.published`
7. `knowledge.engine_index.refreshed`
8. `knowledge.service.catalog.published`
9. `knowledge.ingest.completed`
10. `knowledge.ingest.failed`
11. `knowledge.audit_recorded`

## 7. 验收主线

企业级知识系统验收至少应覆盖以下最小闭环：

1. 样本文档创建
2. 版本审批
3. 发布生效
4. LLM Wiki 编制视图同步
5. Brain 索引刷新
6. Brain 服务目录可消费
7. AI 消费结果可回指
8. WAES 审计记录可追踪
9. 知识失效后 AI 被拦截
10. 发布回滚可同步生效

## 8. 明确禁止事项

实施过程中禁止：

1. 把 `LLM Wiki` 当企业级知识真源。
2. 把 `Brain` 当企业级知识真源。
3. 让 `LLM Wiki` 反写知识主存层。
4. 让 `Brain` 直接修改正式文档。
5. 让 `Brain` 直接发布正式知识版本。
6. 让 `WAES` 成为知识正文主账。
7. 让 AI 直接修改正式知识版本。
8. 同时把 `LLM Wiki` 和 `Brain` 都定义成主知识引擎而不区分主次。

## 9. 状态纪律

本任务书遵循 Harness Engineering 与 PMBOK：

1. 当前只能确认设计和实施任务基线；
2. 不得把实施任务书存在写成知识系统已完成；
3. 未获得真实发布、ingest、索引、引用回指、失效拦截、审计日志证据前，不得写成运行完成；
4. 未通过人工确认前，不得写成 `complete`。

## 10. 当前结论

当前企业级知识系统实施的正确方向不是“在 `LLM Wiki` 和 `Brain` 中二选一直接充当企业级知识库”，而是：

1. 先建立知识主存层；
2. 再建立 `LLM Wiki` 编制视图；
3. 再由 `Brain` 作为主知识引擎；
4. 再由 `Brain` 承担知识服务层；
5. 最后由 `WAES` 统一做治理和审计。

这份任务书用于后续真实实施，不代表当前系统已联调完成或运行完成。
