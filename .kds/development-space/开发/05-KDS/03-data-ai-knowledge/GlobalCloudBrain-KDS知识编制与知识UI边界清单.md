---
doc_id: GPCF-DOC-54C6C8B58B
title: GlobalCloud Brain-KDS 知识编制与知识 UI 边界清单
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloudBrain-KDS知识编制与知识UI边界清单.md
source_path: 03-data-ai-knowledge/GlobalCloudBrain-KDS知识编制与知识UI边界清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud Brain-KDS 知识编制与知识 UI 边界清单

日期：2026-06-17
状态：v0.1 受控边界清单
适用范围：Brain、KDS、GPCF、WAES、PKC、GFIS / GCFIS、GPC、PVAOS、XiaoC / 小即、XGD、XiaoG、MMC，以及葛化物流和湖北磷材绿色供应链试点。

## 1. 定位

本文是 `GPCF-KDS-DKS-015` 的主交付，用于明确 Brain 与 KDS 在分布式知识事实体系中的边界。

总原则是：KDS 存事实，Brain 编知识。KDS 负责知识主存、11 个底座资源池、候选事实、确认事实、证据索引、增强治理账本挂接、权限密级、可信级别和 WAES 门禁引用；Brain 负责在权限过滤后的 KDS 上下文之上，编制知识页面、知识地图、知识产品化表达、SOP 展示和跨项目知识编排。

本文只定义 Brain 消费 KDS、展示知识、组织知识和输出候选建议的边界，不表示 Brain 已接入真实系统、不表示真实资料已入库、不表示任何业务事实、积分、收益、订单、POD 或财务事项已经确认。

## 2. 一句话边界

| 事项 | KDS | Brain |
|---|---|---|
| 事实保存 | 保存候选事实、确认事实、证据索引、底座资源池挂接 | 不保存为事实主账，只读取受控事实 |
| 知识编制 | 提供受控知识对象、可信来源、权限过滤上下文 | 编制知识页面、知识地图、专题包、SOP 展示 |
| 业务确认 | 记录确认状态和业务系统引用 | 不确认业务事实 |
| 规则门禁 | 挂接 WAES 规则、证据、密级、例外记录 | 显示门禁状态和引用，不替代 WAES |
| 权限密级 | 维护 DSR、角色、组织、可见范围 | 按 KDS / MMC / WAES 过滤后展示 |
| AI 输出 | 接收候选建议和来源索引 | 可生成摘要、解释、SOP 展示和候选补充建议 |
| 责任边界 | KDS 是事实底座 | Brain 是知识表达和编排层 |

## 3. Brain 可消费的 KDS 上下文

Brain 只消费通过 KDS、WAES、MMC 规则过滤后的上下文。可消费对象包括：

| 上下文 | 来源 | Brain 用法 | 必要约束 |
|---|---|---|---|
| 知识对象 | KDS 数据池、政策池、原料池、场景池 | 知识页面、专题解释、行业知识包 | 必须保留来源和可信级别 |
| 事实对象 | KDS 订单池、产能池、资金池、运力池等 | 事实时间线、项目进度、订单链路展示 | 必须显示候选 / 确认状态 |
| 证据索引 | KDS 数据池、WAES 证据门禁 | 证据摘要、证据缺口、文档验收视图 | DSR-L2 / DSR-L3 默认只显示元数据或脱敏摘要 |
| SOP 对象 | SOP 账本并挂接场景池、订单池、产能池等 | 全局 SOP、分段 SOP、岗位 SOP、预运营期订单 SOP 展示 | 不得把展示状态写成 SOP 已执行 |
| 项目资料 | GPCF Loop、GFIS / GCFIS、GPC、PVAOS 等来源 | 项目知识页、项目地图、试点进度页 | 必须保留来源系统和责任主体 |
| 行业资料 | 权威政策 / 标准网站、第三方文档、网络搜索 | 行业知识卡、政策标准解释、可信来源引用 | 必须保留版本、时间、适用范围 |
| 增强账本对象 | 积分池、收益池、额度池、悬赏池、争议池等 | 贡献视图、收益参考视图、悬赏视图、争议视图 | 不确认积分、收益或争议结果 |
| Loop 证据 | GPCF Loop 记录、门禁结果、文档治理结果 | 治理状态页、审计摘要、下一轮队列展示 | 不把门禁通过写成业务完成 |

## 4. Brain 输出类型

| 输出类型 | 说明 | 是否可成为确认事实 |
|---|---|---|
| KnowledgePage | 面向用户或合作单位的知识页面 | 否 |
| KnowledgeMap | 项目、订单、工厂、原料、政策、SOP 的关系地图 | 否 |
| KnowledgeProduct | 对外或内部复用的知识包、专题包、案例包 | 否 |
| SOPView | 全局 SOP、分段 SOP、岗位 SOP、预运营期订单 SOP 的展示页 | 否 |
| CrossProjectKnowledgeView | 横跨 GFIS、GPC、PVAOS、KDS、WAES、PKC 等项目的知识编排视图 | 否 |
| KnowledgeGapView | 知识缺口、证据缺口、悬赏候选和补证建议展示 | 否 |
| CandidateSuggestion | Brain 基于受控知识生成的候选补充建议 | 否，必须回到 KDS / WAES / 人工确认 |

Brain 输出可以成为 KDS 的候选知识、候选 SOP、候选缺口或候选事实输入，但必须重新进入 KDS 候选登记、WAES 门禁和人工确认流程。

## 5. 编制流程

```text
KDSResourceQuery
  -> PermissionAndClassificationFilter
  -> ContextBundle
  -> BrainCompilationDraft
  -> SourceAndTrustAnnotation
  -> KnowledgePageOrMapDraft
  -> WAESDisplayBoundaryCheck
  -> HumanReviewIfRequired
  -> PublishedKnowledgeView
  -> KDSBacklinkAndLoopEvidence
```

### 5.1 KDSResourceQuery

Brain 从 KDS 查询底座资源池对象和增强治理账本对象。查询必须带有：

| 字段 | 要求 |
|---|---|
| requester | 用户、合作单位、项目组或系统入口 |
| purpose | 知识问答、页面生成、SOP 展示、项目复盘、悬赏查看等 |
| baseResourcePools | 查询涉及的底座资源池 |
| enhancedLedgers | 查询涉及的增强治理账本 |
| classificationLimit | 允许读取的最高 DSR 密级 |
| sourceRefsRequired | 默认 true |
| loopEvidenceRequired | 治理、收益、争议、积分、SOP 类默认 true |

### 5.2 PermissionAndClassificationFilter

Brain 不自行放大权限。权限过滤来自 KDS、MMC、WAES 和合作单位空间规则：

1. 合作单位默认只能看到自己的明细。
2. 被邀请、被授权或参与悬赏后，才可查看对应任务范围内的他方材料。
3. DSR-L2 资料默认脱敏；DSR-L3 资料默认只显示元数据或封存索引。
4. 涉及金融凭证、收益分配、争议裁决、重大违规扣除的内容必须显示确认状态和门禁引用。

### 5.3 BrainCompilationDraft

Brain 可以对上下文进行摘要、归类、重组、图谱化、时间线化、SOP 展示化和知识产品化，但不得删除来源、不得改变确认状态、不得隐去密级和门禁提示。

### 5.4 WAESDisplayBoundaryCheck

Brain 展示页面如涉及规则、证据、权限、边界、例外、争议、收益或重大 SOP，应显示 WAES 门禁状态。WAES 仍只确认规则、证据、权限、边界和例外，不替代业务主账确认。

## 6. 知识 UI 类型

| UI 类型 | 主要对象 | 典型试点 | 边界 |
|---|---|---|---|
| 项目知识页 | 项目资料、会议、任务、Loop 证据、试点状态 | 葛化资料包、湖北磷材拓厂项目 | 不写成项目完成 |
| 订单链路页 | 需求、预运营期订单、OEM 承接、目标工厂、发货、POD | 葛化订单运行母版 | 不替代 GFIS / GCFIS 订单事实 |
| 工厂复制页 | 建设资料、装备、产能、岗位、SOP、风险 | 湖北磷材新工厂复制模板 | 不替代建设验收 |
| 原料行业页 | 原料、政策、行业资料、供应商、价格线索 | 湖北磷材原料 / 行业知识库 | 不确认采购或价格事实 |
| SOP 展示页 | 全局 SOP、分段 SOP、岗位 SOP、预运营期订单 SOP | 葛化和复制工厂共用 | 不代表 SOP 已执行 |
| 贡献与悬赏页 | 积分候选、悬赏候选、提交、验收、争议状态 | 知识缺口积分交易 | 不确认正式积分和收益 |
| 权威来源页 | 政策、标准、政府或行业网站、可信级别 | 绿色供应链政策标准 | 必须显示版本和适用范围 |
| 治理审计页 | GPCF Loop、WAES 门禁、KDS 挂接、文档治理 | 项目群总控 | 不升级 accepted / integrated |

## 7. 试点映射

### 7.1 葛化物流

Brain 在葛化第一阶段提供：

1. GFIS 知识问答助手可引用的知识页面。
2. GFIS 使用助手可引用的操作说明和 SOP 展示。
3. GFIS 文档验收助手可引用的资料包验收视图。
4. 预运营期订单链路图，区分需求来源、OEM 承接方、目标工厂和事实责任。
5. 辽宁远航链路缺口、现代精工 OEM 过渡责任拆分、质量 / 发货 / POD / 金融凭证门禁的知识化展示。

Brain 不确认葛化订单、生产、质量、POD、到账、开票、收益或正式积分。

### 7.2 湖北磷材

Brain 在湖北磷材第一阶段提供：

1. 拓厂项目知识库页面结构。
2. 原料 / 行业 / 订单知识页结构。
3. 新工厂复制模板的知识地图。
4. 葛化母版复用路径展示。
5. 拓厂项目、原料池、行业资料、销售订单线索与新工厂场景池的关联视图。

湖北磷材第一阶段不做 GFIS 深度运行，Brain 只做拓厂知识、行业原料知识和新工厂复制模板的知识编制。

## 8. 对 KDS 11 池和增强账本的挂接规则

| Brain 编制对象 | 必挂底座资源池 | 可挂增强账本 |
|---|---|---|
| 项目知识页 | 数据池、场景池 | SOP 账本、贡献账本 |
| 订单链路页 | 订单池、数据池、场景池 | 潜在产值池、SOP 账本 |
| 工厂复制页 | 产能池、装备池、数据池、场景池 | SOP 账本、贡献账本 |
| 原料行业页 | 原料池、政策池、数据池 | 知识缺口悬赏池、贡献账本 |
| 物流 / POD 页 | 运力池、订单池、数据池 | 证据对象、争议池 |
| 金融凭证展示页 | 资金池、订单池、数据池 | 收益池、权限账本、争议池 |
| 贡献与悬赏页 | 人才池、数据池、场景池 | 积分池、悬赏池、争议池 |
| 治理审计页 | 数据池、人才池、场景池 | 争议池、贡献账本、SOP 账本 |

所有 Brain 页面必须保留 `sourceRefs`、`baseResourcePools`、`enhancedLedgerLinks`、`classificationLevel`、`trustLevel`、`waesGateRefs`、`loopEvidenceRefs` 和 `publishedVersion`。

## 9. 不得越界清单

1. Brain 不替代 KDS 事实底座。
2. Brain 不替代 GFIS / GCFIS、GPC、PVAOS 等来源系统主账。
3. Brain 不替代 WAES 规则和证据门禁。
4. Brain 不确认订单、生产、质量、POD、到账、开票、收益、积分、争议或重大违规裁决。
5. Brain 不绕过权限、密级、合作单位可见范围和用户治理权。
6. Brain 不把 AI 输出、知识页面、知识地图或 SOP 展示写成业务完成。
7. Brain 不把控制面可见状态写成真实系统接入、真实 API 写入或生产执行完成。

## 10. 最小对象字段

| 字段 | 说明 |
|---|---|
| brainObjectId | Brain 编制对象统一编号 |
| objectType | KnowledgePage / KnowledgeMap / KnowledgeProduct / SOPView / KnowledgeGapView |
| sourceRefs | KDS / WAES / GFIS / GPC / PVAOS / GPCF 等来源引用 |
| baseResourcePools | KDS 11 个底座资源池挂接 |
| enhancedLedgerLinks | 增强治理账本挂接 |
| classificationLevel | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 |
| trustLevel | T0 / T1 / T2 / T3 |
| waesGateRefs | WAES 门禁记录引用 |
| permissionScope | 组织、角色、合作单位、项目组和人员可见范围 |
| confirmationStatus | draft / candidate / reviewed / published / withdrawn |
| humanReviewRequired | 是否需要人工复核 |
| loopEvidenceRefs | 对应 GPCF Loop 记录和文档门禁 |
| kdsBacklinks | 回链到 KDS 底座资源池和增强账本对象 |

## 11. Definition of Done

本轮满足以下条件时，DKS-015 才算完成：

1. Brain 与 KDS 的事实保存、知识编制、展示和候选输出边界已明确。
2. Brain 可消费的 KDS 上下文、权限过滤和密级规则已明确。
3. Brain 输出类型、知识 UI 类型、试点映射和不得越界清单已明确。
4. Brain 编制对象已挂接到 KDS 11 个底座资源池和增强治理账本。
5. 文档进入 README、文档控制台账、KDS 开发空间同步台账和 `.kds` 本地镜像。
6. 污染检查、KDS TOKEN 检查和 Loop 文档门禁通过。

## 12. 下一轮输入

下一轮建议进入 `GPCF-KDS-DKS-016`：PKC-KDS 个人知识与贡献入口清单。

重点明确 KDS 管全局事实，PKC 管个人参与；个人知识、个人任务、个人积分、个人悬赏、个人 AI 服务和合作单位成员空间如何接入 KDS 11 个底座资源池及增强治理账本对象。
