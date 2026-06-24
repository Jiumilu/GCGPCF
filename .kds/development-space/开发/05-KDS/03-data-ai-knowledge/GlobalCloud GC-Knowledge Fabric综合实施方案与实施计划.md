---
doc_id: GPCF-DOC-934A1F0623
title: GlobalCloud GC-Knowledge Fabric 综合实施方案与实施计划
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, MMC, Studio]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud GC-Knowledge Fabric综合实施方案与实施计划.md
source_path: 03-data-ai-knowledge/GlobalCloud GC-Knowledge Fabric综合实施方案与实施计划.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud GC-Knowledge Fabric 综合实施方案与实施计划

日期：2026-06-19  
版本：v1.1
状态：`draft`  
用途：作为 GC-Knowledge Fabric 后续受控文档、上会材料、工程拆解、试点推进和 LOOP 跟踪的总底稿。  

## 0. 状态边界

本文档是实施方案与实施计划，不代表任何业务系统已经完成写回、任何收益已经确认、任何积分已经结算、任何委员会事项已经裁决，或任何 RAG 强引用已经准入。

当前推进必须遵守以下边界：

1. AI 只生成候选，不直接形成正式事实。
2. KDS 是知识事实底座，不是普通文档库，也不被 Brain、PKC 或 GFIS 替代。
3. WAES 是规则与门禁治理层，不是业务主账，不替代 GFIS、GPC、ERP、MES 或委员会。
4. GFIS / GPC / 业务系统只接收确认后的业务事实。
5. 模板不是事实。葛化母版、湖北磷材模板、新工厂复制模板只能作为候选结构。
6. 有实际收入才进入正式产值。潜在产值不得自动转为正式收益分配依据。
7. Harness / LOOP 留存 evidence 与状态门禁，不自动把状态升为完成。

## 0.1 v1.1 修订摘要

本版根据完整评审问题清单，将 v1.0 从“总架构蓝图”补强为“受控规则版”的起点。修订重点如下：

1. P0 文档包从 8 份扩展为 11 份，补入统一编号规则、统一状态机、核心对象关系与最小字段契约。
2. 工程顺序明确为：规则 -> 状态机 -> 对象契约 -> Gate fixture -> no-write API -> UI。
3. WAES 门禁必须补充输入、输出、hard-stop、reasonCodes、requiredActions、allowedOperations 和 Harness evidence 引用。
4. RAG 准入必须增加引用强度 L0-L5，避免把 `safe` 误解成可直接业务决策。
5. GFIS 写回必须先进入 Writeback Sandbox，P1 前只允许 `no-write` 和 `sandbox`，禁止 `approved-write` 和 `production-write`。
6. 所有候选对象必须能解释为什么不能升级，至少包含 promotionBlockers、missingEvidence、requiredReviewer、requiredGate 和 nextAction。

## 1. 总体定位

GC-Knowledge Fabric 是 GlobalCloud 绿色供应链体系的分布式可信知识工程底座。

它不是单一知识库，也不是单一 Brain 前端改造，而是一套覆盖知识接入、知识归集、事实候选、规则门禁、人工确认、委员会裁决、业务写回、收益积分、AI 额度、知识悬赏、RAG 准入、LOOP 工程治理和指挥舱闭环的综合系统。

系统总定位如下：

| 组件 | 定位 |
|---|---|
| KDS | 知识事实底座、状态机、KDS 十一池挂接中心 |
| OKF | 知识契约、对象语言、规则配置层 |
| WAES | 规则、门禁、风险拦截与确认路径触发层 |
| KWE | 知识流程引擎、工单和确认包编排层 |
| PKC | 个人、团队、项目知识使用入口 |
| Brain | 多角色知识工作台、审阅中心和指挥舱 |
| MMC | AI / Agent / Connector / MCP / API 能力网关 |
| Harness | evidence、验收、审计、Knowledge CI 和状态门禁 |
| LOOP | 持续工程治理闭环 |
| GFIS / GPC | 已确认业务事实的执行系统和业务入口 |

最终形成的闭环：

```text
多单位分布式接入
-> KDS 十一池统一事实底座
-> OKF 定义对象、规则、流转、准入
-> WAES 执行门禁与风险拦截
-> AI 生成候选事实 / 候选 SOP / 候选写回
-> KWE 推动工单、确认、补证、脱敏、发布、争议处理
-> 人工 / 委员会确认
-> GFIS / GPC / 业务系统执行
-> Brain / PKC / 指挥舱安全引用
-> 积分 / 收益 / 额度 / 悬赏联动
-> Harness / LOOP 留证与闭环
-> 新工厂、区域供应链、多单位复制扩张
```

一句话定义：

GC-Knowledge Fabric 是由用户掌控规则与底座，由合作单位贡献知识与业务事实，由 AI 提供候选智能，由 KDS / WAES / Harness 保证可信治理，最终服务绿色供应链建设、订单、生产、交付、收益分配和复制扩张的分布式可信知识系统。

## 2. 核心原则

### 2.1 AI 候选原则

AI 可以生成：

| 可生成对象 | 进入状态 |
|---|---|
| 候选事实 | `candidate` |
| 候选 SOP | `candidate` |
| 候选字段 | `candidate` |
| 候选状态 | `candidate` |
| 候选风险 | `candidate` 或 `repair_required` |
| 候选缺口 | `open` |
| 候选积分 | `candidate` |
| 候选收益贡献 | `candidate` |
| 候选验收建议 | `candidate` |
| 候选写回建议 | `candidate` |
| 候选政策解释 | `limited` 或 `repair_required` |
| 候选 RAG 引用建议 | `blocked`、`limited` 或 `repair_required` |

AI 不能直接形成：

| 禁止对象 | 必经路径 |
|---|---|
| 正式业务事实 | KDS 候选入池 -> WAES -> KWE -> 人工/委员会确认 |
| 正式 GFIS 写回 | WritebackCandidate -> WAES Writeback Gate -> 业务负责人确认 |
| 正式收益分配 | RevenueRecord -> Revenue Gate -> 委员会或授权人确认 |
| 正式积分确认 | ContributionRecord -> Contribution Gate -> 人工/委员会确认 |
| 正式产值贡献 | RevenueRecord -> 收入口径确认 -> 决议或备案 |
| 正式 RAG 强引用 | RAG Gate -> evidence 完整 -> 权限与敏感资料检查 |
| 重大违规结论 | Freeze Gate -> Committee Gate -> Harness evidence |
| 供应链责任归因 | evidence -> 责任边界 -> 委员会或授权确认 |

标准链路：

```text
AI 建议
-> KDS 候选入池
-> WAES 规则检查
-> KWE 流程流转
-> 人工 / 委员会确认
-> KDS 正式入账
-> GFIS / GPC / 业务系统写回
-> Harness evidence 固化
```

### 2.2 KDS 事实底座原则

所有高价值对象必须满足：

1. 有编号。
2. 有来源。
3. 有状态。
4. 有 KDS 十一池挂接。
5. 有权限和可见范围。
6. 有证据链。
7. 有责任边界。
8. 有流转记录。
9. 有 RAG 准入状态。
10. 有 WAES 门禁记录。

KDS 不负责人工裁决、委员会裁决、业务系统正式执行、AI 自主确认事实或收益分配最终判定。

### 2.3 WAES 门禁原则

WAES 负责判断：

| 判断事项 | 可能结果 |
|---|---|
| 是否可进入 RAG | `safe`、`limited`、`repair_required`、`blocked` |
| 是否可进入 GFIS 候选写回 | `passed`、`human_required`、`committee_required`、`blocked` |
| 是否需要人工确认 | `human_required` |
| 是否需要委员会确认 | `committee_required` |
| 是否需要脱敏 | `redaction_required` |
| 是否需要冻结 | `freeze_required` |
| 是否可进入积分候选 | `passed` 或 `repair_required` |
| 是否可进入收益候选 | `passed`、`committee_required` 或 `blocked` |
| 是否可进入正式产值 | 仅在收入证据成立后进入确认流程 |
| 是否可对外共享 | 通过 ACL、敏感资料、外部共享门禁 |
| 是否可进入指挥舱强引用 | 通过 RAG Gate 和 evidence 检查 |

WAES 不替代 KDS 存储，不替代 GFIS 执行业务，不替代委员会裁决。

## 3. 九层总体架构

| 层级 | 名称 | 主要职责 |
|---|---|---|
| 1 | 数据接入层 | 飞书、小即、WIKI、Hermes、GFIS、GPC、ERP、MES、邮件、会议、文档、政策网站、标准网站、合作单位资料接入 |
| 2 | Ingestion 解析层 | 导入、OCR、解析、去重、分类、元数据提取、来源登记、初步挂池 |
| 3 | 知识对象层 | KnowledgeObject、SourceRecord、EvidenceRecord、FactCandidate、SOPCandidate、WritebackCandidate、GapRecord 等 |
| 4 | KDS 十一池底座层 | 订单池、运力池、产能池、资金池、政策池、装备池、数据池、能源池、原料池、人才池、场景池 |
| 5 | OKF 知识契约层 | Ontology、Schema、Domain Policy、Pool Binding Policy、Trust Policy、Flow Policy、RAG Policy 等 |
| 6 | WAES 规则与门禁治理层 | 来源、证据、权限、RAG、写回、收益、积分、悬赏、委员会、冻结、外部共享、敏感资料门禁 |
| 7 | KWE 知识流程引擎 | 工单、确认包、缺口、悬赏、脱敏、发布、争议、委员会、写回候选、收益审查、积分审查 |
| 8 | Brain + PKC + 业务入口层 | Brain 多角色工作台、PKC、GFIS 助手、GPC 助手、指挥舱、供应链图谱、外部协作门户 |
| 9 | Harness + LOOP 可信治理层 | Evidence、Acceptance、Audit、Knowledge CI、LOOP 记录、状态门禁、工程治理、追溯审计 |

## 4. KDS 十一池与知识域

### 4.1 知识域

| Domain | 定义 | 默认可见边界 |
|---|---|---|
| `private` | 个人私密草稿 | 仅本人 |
| `workspace` | 个人/团队整理区、Agent 临时输出 | 团队或授权范围 |
| `project` | 项目事实中心，如葛化、湖北磷材、GFIS、GPC | 项目授权范围 |
| `org` | 组织级 SOP、标准、模板、复用资产 | 组织内部 |
| `supply_chain` | 工厂、客户、供应商、物料、订单、碳、质检、合规 | ACL 授权 |
| `public` | 对外发布内容 | 公开 |
| `governance` | evidence、audit、acceptance、Knowledge CI、Agent 日志 | 治理授权范围 |

旧七空间迁移：

| 旧空间 | 新处理 |
|---|---|
| private | `private` |
| personal | `workspace` |
| family | collection，不作为一级 Domain |
| team | `project` 或 `org` |
| partner | `supply_chain` + external_account ACL |
| public | `public` |
| ops | `domainTags: ops` |

### 4.2 KDS 十一池

| 池 | 范围 |
|---|---|
| 订单池 | 订单、订单状态、客户需求、订单证据、交付闭环 |
| 运力池 | 物流、车辆、发货、签收、POD、运输资源 |
| 产能池 | 工厂、产线、产能、生产计划、OEM 承接方 |
| 资金池 | 到账、开票、财务凭证、金融门禁、收益 |
| 政策池 | 政策、标准、合规、行业协会、政府网站 |
| 装备池 | 设备、产线、工艺装备、维护记录 |
| 数据池 | 文档、台账、报告、系统数据、指标 |
| 能源池 | 能耗、碳、绿色能源、节能资料 |
| 原料池 | 原料、材料、供应商资源、上下游供需 |
| 人才池 | 团队、专家、服务商、岗位能力 |
| 场景池 | 项目场景、区域机会、应用案例、复制模板 |

质量类内容第一阶段挂接：数据池 + 场景池 + 订单池。后续质量治理权重上升时，可评估新增质量池，但不得在 P0 自动扩池。

## 5. 核心对象模型

第一阶段统一对象清单：

| 对象 | 用途 | 初始状态 |
|---|---|---|
| KnowledgeObject | 统一知识对象主记录 | `draft`、`candidate`、`reviewing` |
| SourceRecord | 来源登记 | `registered` |
| EvidenceRecord | 证据登记 | `candidate`、`verified` |
| FactCandidate | 候选事实 | `candidate` |
| SOPCandidate | 候选 SOP | `candidate` |
| WritebackCandidate | 候选写回 | `candidate` |
| GapRecord | 知识缺口 | `open` |
| BountyRecord | 悬赏记录 | `candidate` |
| ContributionRecord | 贡献记录 | `candidate` |
| RevenueRecord | 收益记录 | `candidate`、`under_review` |
| QuotaRecord | AI 额度记录 | `registered`、`candidate` |
| DecisionRecord | 决策记录 | `draft`、`confirmed` |
| DisputeRecord | 争议记录 | `open`、`under_review` |
| EventRecord | 事件记录 | `recorded` |

KnowledgeObject 必需字段：

| 字段 | 说明 |
|---|---|
| `id` | 内部唯一 ID |
| `uri` | 可追溯 URI |
| `tenantId` | 租户 |
| `domain` | 七类知识域之一 |
| `objectType` | 对象类型 |
| `poolRefs` | KDS 十一池挂接 |
| `projectId` | 项目 ID |
| `supplyChainNodeId` | 供应链节点 |
| `businessSystemRef` | GFIS / GPC / ERP / MES 等业务系统引用 |
| `ownerType` / `ownerId` | 责任主体 |
| `visibility` | 可见范围 |
| `lifecycle` | 生命周期 |
| `trustLevel` | T0-T5 |
| `ragAdmission` | RAG 准入状态 |
| `confirmationStatus` | 确认状态 |
| `sourceRefs` | 来源引用 |
| `evidenceRefs` | 证据引用 |
| `lineageRefs` |  lineage 引用 |
| `createdAt` / `updatedAt` | 时间戳 |

## 6. 可信等级与 RAG 准入

### 6.1 可信等级

| 等级 | 来源 |
|---|---|
| T0 | 系统正式业务记录、到账记录、正式合同、人工确认记录 |
| T1 | 权威政策/标准网站、政府/行业协会/正式标准 |
| T2 | 合作单位正式文档、盖章资料、验收资料 |
| T3 | 会议、电话、邮件、飞书、WIKI、项目沟通记录 |
| T4 | 网络搜索、行业文章、第三方报告 |
| T5 | LLM 分析结果，仅为候选 |

### 6.2 RAG 准入

| 准入状态 | 含义 |
|---|---|
| `safe` | 可强引用 |
| `limited` | 可有限引用 |
| `repair_required` | 需补证 |
| `blocked` | 禁止引用 |
| `sensitive_metadata_only` | 仅可用元数据，不可暴露原文 |

准入原则：

| 条件 | 默认准入 |
|---|---|
| T0 + evidence 完整 | `safe` |
| T1 + 来源范围明确 | `safe` 或 `limited` |
| T2 + 验收资料完整 | `limited` 或 `safe` |
| T3 + 人工确认前 | `repair_required` |
| T4 | `limited` 或 `repair_required` |
| T5 | `blocked`，除非转为 source-backed 并通过确认 |

## 7. 敏感资料处理

金融凭证、合同敏感信息、门禁资料、POD、质量争议、客户责任边界、供应链责任归因材料不得直接进入开放知识库。

KDS 只记录：

1. 编号。
2. 状态。
3. 哈希。
4. 摘要。
5. 权限。
6. 证据链位置。
7. 受控原件位置。
8. 可引用范围。

原件保留在受控空间。进入 Brain / PKC / RAG / 指挥舱前必须通过 Sensitive Data Gate 和 External Share Gate。

## 8. 业务赋能范围

GC-Knowledge Fabric 服务绿色供应链全过程 SOP：

| SOP | 必含治理字段 |
|---|---|
| 体系建设 SOP | 适用范围、责任主体、KDS 挂池、WAES 门禁、证据留存 |
| 项目拓展 SOP | 客户、工厂、政策、渠道、潜在产值、责任边界 |
| 工厂建设 SOP | 建设资料、产线、设备、产能、验收、风险 |
| 预运营期订单 SOP | 目标工厂与 OEM 承接方责任拆分、订单字段、单据映射 |
| 正式订单 SOP | 已确认订单、交付、质量、POD、回款闭环 |
| OEM 过渡 SOP | 承接方授权、生产责任、质量责任、交付责任 |
| 原料采购 SOP | 原料、供应商、价格、政策、采购订单 |
| 生产运营 SOP | 产能、排产、质量、能耗、异常处理 |
| 质量验收 SOP | 质量记录、争议、责任边界、证据级别 |
| 发货/POD SOP | 运力、发货、签收、POD、客户确认 |
| 金融凭证 SOP | 开票、到账、金融凭证、资金池门禁 |
| 客户交付 SOP | 交付确认、客户反馈、争议处理 |
| 异常争议 SOP | 争议立项、冻结、委员会裁决、追溯扣减 |
| 收益分配 SOP | 收入口径、贡献确认、委员会裁决、备案 |

## 9. 试点与并行线

### 9.1 葛化 P1 GFIS 母版

目标：形成第一个可复制的 GFIS 知识母版。

优先知识源：

1. 建设资料。
2. 工厂运营资料。
3. 订单资料。
4. 辽宁远航链路资料。
5. 现代精工 OEM 过渡资料。
6. 质量资料。
7. 发货/POD 资料。
8. 金融凭证门禁资料。
9. 会议纪要。
10. 政策与标准资料。

交付：

| 交付项 | 状态目标 | 验收方式 |
|---|---|---|
| GFIS 知识问答助手 | no-write 可评测 | 首批 KQA 样本评测 |
| GFIS 使用助手 | no-write 可评测 | 使用场景问答评测 |
| GFIS 文档验收助手 | no-write 可评测 | 文档验收样本评测 |
| 预运营期订单母版 | candidate SOP | 人工确认 |
| 建设资料入池 | metadata + source + evidence | Source/Evidence 检查 |
| 工厂运营资料入池 | metadata + source + evidence | Source/Evidence 检查 |
| 订单资料入池 | candidate only | WAES Gate |
| 质量/发货/POD/金融门禁 | metadata-only 或受控原件 | DSR-L2 / DSR-L3 检查 |
| 辽宁远航链路入池 | gap + bounty candidate | 补证清单 |
| 现代精工 OEM 过渡资料入池 | candidate + responsibility boundary | 人工确认 |
| 候选事实 -> WAES -> GFIS 写回闭环 | candidate writeback | 不写 GFIS 主账，先跑模拟闭环 |

P1 验收边界：

1. 葛化知识可问答，但仅限已准入知识。
2. GFIS 字段可解释，但不代替业务负责人填写或确认。
3. 文档可验收，但验收结果先进入候选状态。
4. 候选事实可进入 KDS，但不直接写业务主账。
5. WAES 可判断是否写回，但不替代业务负责人确认。
6. 敏感资料不直接暴露。
7. 预运营期目标工厂与 OEM 承接方责任可区分。

### 9.2 湖北磷材 P2 并行线

目标：不先做 GFIS 深度，而是建设三类知识库。

交付：

| 知识库 | 覆盖范围 | 验收方式 |
|---|---|---|
| 拓厂项目知识库 | 新工厂选址、建设条件、设备需求、产线规划、项目资料、合作单位资料、政策与标准、建设期风险、预运营准备 | 资料目录预检 + 知识对象样表 |
| 原料/行业/订单知识库 | 磷材原料、市场供需、行业价格、上下游客户、销售订单、采购订单、渠道资源、政策影响、区域供应链机会 | 来源白名单 + 候选事实评审 |
| 新工厂复制模板 | 葛化母版复用、差异化工厂、预运营阶段、责任拆分、建设/订单/产能/质量/发货/POD/财务凭证闭环 | 模板审查 + 差异项确认 |

P2 验收边界：

1. 湖北磷材不依赖 GFIS 深度即可运行。
2. 可形成拓厂知识包。
3. 可形成原料/行业/订单问答。
4. 可形成新工厂复制模板。
5. 可记录潜在产值与渠道贡献。
6. 不自动转为正式收益或正式产值。

## 10. 积分池、收益池、额度池、悬赏池

### 10.1 知识积分

适用于提供有效资料、补齐知识缺口、提供高质量 SOP、提供行业知识、提供权威来源、提供证据链、参与验收、参与纠错、参与争议处理。

无实际收入时，只能列入知识贡献或潜在产值贡献，不能直接进入正式收益分配。

### 10.2 产值与收益

| 口径 | 定义 | 是否进入正式分配 |
|---|---|---|
| 正式收益 | 已到账收入 | 是，需确认 |
| 财务统计 | 已开票收入 | 不直接等于收益分配 |
| 潜在收益 | 未到账但可追踪机会 | 否 |
| 知识潜在价值 | 有知识价值但无收入 | 否 |

### 10.3 AI 额度

| 类型 | 规则 |
|---|---|
| 平台额度 | 楚商云统一提供 |
| 自购额度 | 合作单位购买，先自用，不进入统一收益池 |
| 贡献额度 | 合作单位贡献给体系，需登记 |
| 共享额度 | 用于合作单位或项目组共享服务 |
| 奖励额度 | 用于积分兑换或激励 |

### 10.4 悬赏机制

标准流程：

```text
缺口发现
-> 缺口编号
-> 挂接 KDS 十一池
-> 发布悬赏候选
-> 单位/个人提交资料
-> AI 初审
-> WAES 门禁
-> 人工验收
-> 接受 / 部分接受 / 退回 / 拒绝
-> 积分结算候选
-> 争议期
-> 关闭缺口
-> Harness evidence 固化
```

真实悬赏发布前必须具备：冻结资源、验收标准、争议入口、责任主体、委员会或授权人备案。

## 11. 委员会机制

委员会处理用户不直接裁决但必须被治理的事项。

委员会负责：

1. 积分确认。
2. 收益分配争议。
3. 重大违规认定。
4. 悬赏结算。
5. 潜在产值转正式产值。
6. 跨单位贡献争议。
7. 第三方池子分配。
8. 项目组内部争议。
9. 规则解释建议。
10. 重大 RAG 强引用争议。
11. 收益池规则争议。

决策记录进入 `governance` domain，并生成 DecisionRecord。必要时冻结相关积分、收益、RAG 准入或相关对象。

## 12. API 与工程模块路线

### 12.1 KDS v2 API

| API | P0 目标 | P1 目标 |
|---|---|---|
| `GET /api/v2/domains` | 返回七类 domain | 接 ACL |
| `GET /api/v2/pools` | 返回十一池 | 接 pool policy |
| `GET /api/v2/projects` | 返回项目列表 | 接项目 ACL |
| `POST /api/v2/search` | 搜索契约草案 | 接 RAG gate |
| `GET /api/v2/objects/{uri}` | 对象详情草案 | 接 source/evidence enrichment |
| `POST /api/v2/sources/import` | SourceRecord 候选 | 接 ingestion |
| `POST /api/v2/fact-candidates` | 候选事实 | 接 WAES |
| `POST /api/v2/sop-candidates` | 候选 SOP | 接 KWE |
| `POST /api/v2/writeback-candidates` | 候选写回 | 接 Writeback Gate |
| `GET /api/v2/graph` | 图谱契约 | 接权限过滤 |
| `GET /api/v2/governance/evidence` | evidence 查询 | 接 Harness |

### 12.2 WAES API

| API | 目标 |
|---|---|
| `POST /api/v2/waes/gates/run` | 统一运行门禁 |
| `POST /api/v2/waes/rag-admission/check` | RAG 准入检查 |
| `POST /api/v2/waes/writeback/check` | 写回候选检查 |
| `POST /api/v2/waes/revenue/check` | 收益门禁 |
| `POST /api/v2/waes/contribution/check` | 贡献门禁 |
| `POST /api/v2/waes/external-share/check` | 外部共享门禁 |
| `POST /api/v2/waes/freeze` | 冻结门禁 |

### 12.3 KWE API

| API | 目标 |
|---|---|
| `POST /api/v2/kwe/work-items` | 创建工单 |
| `GET /api/v2/kwe/work-items` | 查询工单 |
| `POST /api/v2/kwe/gaps` | 缺口登记 |
| `POST /api/v2/kwe/bounties` | 悬赏候选 |
| `POST /api/v2/kwe/confirmations` | 确认包 |
| `POST /api/v2/kwe/committees` | 委员会事项 |
| `POST /api/v2/kwe/promotions` | 状态提升请求 |
| `POST /api/v2/kwe/redactions` | 脱敏请求 |
| `POST /api/v2/kwe/writebacks` | 写回候选流程 |

### 12.4 GFIS Assistant API

| API | 目标 |
|---|---|
| `POST /api/v2/gfis/knowledge-assistant/query` | 已准入知识问答 |
| `POST /api/v2/gfis/usage-assistant/query` | GFIS 使用解释 |
| `POST /api/v2/gfis/document-acceptance/check` | 文档验收检查 |
| `POST /api/v2/gfis/writeback-candidates` | GFIS 写回候选，不直接写主账 |

### 12.5 Governance / LOOP API

| API | 目标 |
|---|---|
| `POST /api/v2/governance/loop` | 创建 LOOP 记录 |
| `GET /api/v2/governance/loop/{id}` | 查询 LOOP |
| `POST /api/v2/governance/evidence` | 写入 evidence |
| `POST /api/v2/governance/knowledge-ci/run` | 运行 Knowledge CI |
| `GET /api/v2/governance/ledger/contributions` | 贡献台账 |
| `GET /api/v2/governance/ledger/revenue` | 收益台账 |
| `GET /api/v2/governance/ledger/quota` | 额度台账 |

## 13. 物理数据模型

第一阶段建议表清单：

| 表 | 用途 |
|---|---|
| `knowledge_objects` | 知识对象主表 |
| `knowledge_sources` | 来源 |
| `knowledge_evidence` | 证据 |
| `fact_candidates` | 候选事实 |
| `sop_candidates` | 候选 SOP |
| `writeback_candidates` | 候选写回 |
| `knowledge_events` | 知识事件 |
| `knowledge_acl` | 权限 |
| `knowledge_embeddings` | 向量 |
| `knowledge_index_jobs` | 索引任务 |
| `kds_pools` | 十一池定义 |
| `object_pool_bindings` | 对象挂池 |
| `waes_gate_results` | 门禁结果 |
| `waes_gate_policies` | 门禁策略 |
| `kwe_work_items` | KWE 工单 |
| `kwe_workpacks` | 确认包 |
| `gap_records` | 缺口 |
| `bounty_records` | 悬赏 |
| `confirmation_records` | 人工确认 |
| `committee_records` | 委员会 |
| `dispute_records` | 争议 |
| `contribution_records` | 贡献 |
| `revenue_records` | 收益 |
| `quota_records` | 额度 |
| `decision_records` | 决策 |
| `loop_records` | LOOP |
| `harness_evidence_records` | Harness evidence |
| `capability_invocations` | MMC 能力调用 |
| `agent_used_knowledge` | Agent 使用知识证据 |
| `okf_policy_versions` | OKF 策略版本 |

P0 只建立最小表契约和迁移草案，不直接承诺生产库上线。

## 14. Brain / PKC / 指挥舱

Brain Workbench：

```text
Brain Workbench
├── Knowledge Command Center
├── PKC Console
├── GFIS Knowledge Assistant
├── GFIS Usage Assistant
├── GFIS Document Acceptance Assistant
├── KDS Object Center
├── WAES Gate Center
├── KWE Work Queue
├── Supply Chain Graph
├── Governance Center
├── Committee Center
├── Revenue / Contribution Center
├── AI Quota Center
├── Gap & Bounty Center
└── LOOP Dashboard
```

PKC Console：

```text
PKC Console
├── 我的知识
├── 我的草稿
├── 我的收藏
├── 最近使用
├── 我的待办
├── 我的 Agent 输出
├── 我的 KWE 工单
├── 我的贡献记录
├── 我的积分记录
├── 我的 AI 额度
├── 我参与的悬赏
├── 我的项目知识包
└── 推荐复用知识
```

底座可用知识闭环率：

```text
底座可用知识闭环率 =
状态覆盖率 * 20%
+ 事实成熟度 DQ * 25%
+ 来源/证据合格率 * 20%
+ registry/台账/报告一致性 * 15%
+ 自动化处理有效率 * 10%
+ 写回缺口闭环率 * 10%
```

辅助指标：

1. RAG safe 率。
2. blocked 知识占比。
3. repair_required 缺口数。
4. WAES 拦截次数。
5. 人工确认完成率。
6. 委员会事项闭环率。
7. 收益候选转正式收益率。
8. 悬赏关闭率。
9. AI 候选采纳率。
10. 外部共享违规数。
11. 敏感资料 metadata-only 处理率。

## 15. P0-P4 实施路线

### 15.1 P0 当前立即执行

目标：完成制度、编号、目录、门禁、台账、LOOP 模板的底座固化。

交付：

| 编号 | 交付 | 验收 |
|---|---|---|
| P0-01 | 固化分布式知识系统总体规则 | 受控文档通过污染检查 |
| P0-02 | 建立统一编号体系 | 每类对象有前缀、序列、归属和状态规则 |
| P0-03 | 建立 KDS 十一池挂接规则 | 每类内容有默认挂池和例外规则 |
| P0-04 | 建立葛化 GFIS 知识库首批目录 | 七类资料包目录、密级、责任人、缺口 |
| P0-05 | 建立湖北磷材并行知识库目录 | 拓厂、原料/行业/订单、复制模板三类目录 |
| P0-06 | 建立积分池/收益池/额度池/悬赏池台账模型 | 候选与确认状态分离 |
| P0-07 | 建立 WAES 门禁口径 | Gate 类型、输入、输出、状态 |
| P0-08 | 建立 RAG 准入规则 | T0-T5 与 safe/limited/repair/blocked 映射 |
| P0-09 | 建立 LOOP 跟踪模板 | 每轮目标、输入、输出、风险、下一步 |
| P0-10 | 建立敏感资料入库规则 | metadata-only 与受控原件路径 |
| P0-11 | 建立委员会事项触发规则 | 触发条件、冻结、DecisionRecord |
| P0-12 | 建立 AI 候选输出边界规则 | candidate-only 硬约束 |
| P0-13 | 建立 GFIS 写回候选规则 | WAES + 人工确认前不得写主账 |

P0 验收：

1. 所有新资料都有编号规则。
2. 所有关键对象都有池子挂接规则。
3. 所有 AI 输出只能进入 candidate。
4. 所有 GFIS 写回必须经过 WAES。
5. 所有收益/积分均有候选与确认状态区分。
6. 所有敏感资料都有 metadata-only 或受控原件规则。

### 15.2 P1 葛化 GFIS 母版

目标：形成第一个可复制的 GFIS 知识母版。

交付：

1. GFIS 知识问答助手。
2. GFIS 使用助手。
3. GFIS 文档验收助手。
4. 预运营期订单母版。
5. 建设资料入池。
6. 工厂运营资料入池。
7. 订单资料入池。
8. 质量/发货/POD/金融凭证资料门禁。
9. 辽宁远航链路入池。
10. 现代精工 OEM 过渡资料入池。
11. 候选事实 -> WAES -> GFIS 写回候选闭环。

验收：

1. 葛化知识可问答。
2. GFIS 字段可解释。
3. 文档可验收。
4. 候选事实可进入 KDS。
5. WAES 可判断是否写回。
6. 敏感资料不直接暴露。
7. 预运营期目标工厂与 OEM 承接方责任可区分。

### 15.3 P2 湖北磷材并行线

目标：建设拓厂、原料、行业、订单、新工厂复制模板知识体系。

交付：

1. 拓厂项目知识库。
2. 原料/行业/订单知识库。
3. 新工厂复制模板。
4. 区域绿色供应链知识图谱。
5. 潜在产值与渠道贡献计量。
6. 政策池与原料池联动。

验收：

1. 湖北磷材不依赖 GFIS 深度即可运行。
2. 可形成拓厂知识包。
3. 可形成原料/行业/订单问答。
4. 可形成新工厂复制模板。
5. 可记录潜在产值与渠道贡献。

### 15.4 P3 多单位复制

目标：从葛化与湖北磷材扩展到更多工厂与区域运营单位。

交付：

1. 类似葛化工厂复制。
2. 区域绿色供应链运营单位接入。
3. 跨单位知识协作。
4. 统一收益池参考机制。
5. 知识悬赏市场。
6. 第三方服务池。
7. 外部伙伴门户。

验收：

1. 新单位可按模板接入。
2. 跨单位资料有 ACL。
3. 贡献与收益可区分。
4. 悬赏可发布与结算。
5. 委员会可处理争议。
6. 外部伙伴只看授权视图。

### 15.5 P4 自运行与协同进化

目标：AI 负责发现、生成、初审、推荐，人和委员会只处理关键确认、例外、争议、收益和违规。

交付：

1. AI 自动发现缺口。
2. AI 自动生成候选 SOP。
3. AI 自动生成候选事实。
4. AI 自动生成验收建议。
5. AI 自动推荐贡献分配。
6. AI 自动生成 WAES 风险提示。
7. AI 自动维护知识健康度。
8. AI 自动生成 LOOP 建议。

验收：

1. AI 候选采纳率可度量。
2. WAES 拦截有效。
3. 人工确认负担下降。
4. 委员会只处理高价值事项。
5. 系统可自我发现缺口并推动闭环。

## 16. P0 首批 11 份受控文档包

首批 P0 文档包从 8 份扩展为 11 份。原 8 份负责治理、目录、台账和 LOOP，新增 3 份负责统一编号、统一状态机、对象关系与字段契约。没有这 3 份，后续 KDS 表结构、WAES Gate、KWE 流程和 API contract 容易漂移。

| 顺序 | 文件 | 目标 | 验收 |
|---|---|---|---|
| 1 | 统一编号规则 | 固化所有对象、候选、证据、工单、门禁、收益、额度、悬赏、决议的编号规则 | 每类对象有前缀、归属、序列、状态和防碰撞规则 |
| 2 | 统一状态机与状态提升规则 | 固化 draft/candidate/reviewing/evidence_ready/confirmed/accepted/frozen 等状态语义 | 每个状态说明谁能创建、谁能提升、能否 RAG、能否写回、能否计入收益 |
| 3 | 核心对象关系与最小字段契约 | 固化 Source/Evidence/Object/Candidate/Gate/KWE/Decision/Writeback/Ledger/LOOP 的关系 | 后续 schema、API、表结构有同一契约源 |
| 4 | KDS 十一池挂接规则 | 固化内容类型到业务事实底座的挂接关系 | 每类内容有默认池、例外池和责任边界 |
| 5 | WAES 门禁规则 | 固化 Gate 类型、输入、输出、状态、hard-stop 和 reasonCodes | 每类对象有门禁路径和可 dry-run 的输入输出 |
| 6 | RAG 准入与引用强度规则 | 固化 T0-T5、RAG 状态和 L0-L5 引用强度关系 | T5 默认 blocked，safe 不自动等于业务决策 |
| 7 | 葛化 GFIS 知识库目录 | 固化葛化七类资料包和 GFIS 三件套目录 | 有编号、来源、密级、缺口 |
| 8 | 湖北磷材知识库目录 | 固化拓厂、原料/行业/订单、复制模板目录 | 不依赖 GFIS 深度即可运行 |
| 9 | 积分/收益/额度/悬赏台账模型 | 固化四类治理账本 | 候选与确认状态分离 |
| 10 | 敏感资料入库规则 | 固化 metadata-only、受控原件、哈希、摘要 | 金融、POD、质量争议、合同不开放原文 |
| 11 | LOOP 跟踪模板 | 固化每轮推进记录结构 | 可追踪输入、输出、门禁、风险、下一轮 |

建议文件路径：

```text
03-data-ai-knowledge/GC-Knowledge-Fabric-统一编号规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-统一状态机与状态提升规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-核心对象关系与最小字段契约.md
03-data-ai-knowledge/GC-Knowledge-Fabric-KDS十一池挂接规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-WAES门禁规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-RAG准入与引用强度规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-葛化GFIS知识库目录.md
03-data-ai-knowledge/GC-Knowledge-Fabric-湖北磷材知识库目录.md
03-data-ai-knowledge/GC-Knowledge-Fabric-积分收益额度悬赏台账模型.md
03-data-ai-knowledge/GC-Knowledge-Fabric-敏感资料入库规则.md
03-data-ai-knowledge/GC-Knowledge-Fabric-LOOP跟踪模板.md
```

## 17. 首批执行任务包

### Task Pack 0：规则固化

| 任务 | 输出 | 验收 |
|---|---|---|
| T0-01 | 总体架构文档 | 文档控制通过 |
| T0-02 | 统一编号规则 | 对象编号可复用 |
| T0-03 | KDS 十一池定义 | 池定义完整 |
| T0-04 | Domain + Pool 双维模型 | 旧七空间迁移路径清晰 |
| T0-05 | AI 候选边界规则 | AI 不直接写正式事实 |
| T0-06 | 敏感资料入库规则 | metadata-only 成立 |

### Task Pack 1：OKF 契约

| 任务 | 输出 | 验收 |
|---|---|---|
| T1-01 | `ontology.yaml` | 对象、域、池、关系完整 |
| T1-02 | `knowledge-object.schema.json` | schema 校验通过 |
| T1-03 | `pool-binding-policy.yaml` | 默认挂池规则完整 |
| T1-04 | `waes-gate-policy.yaml` | Gate 状态完整 |
| T1-05 | `rag-admission-policy.yaml` | RAG 准入规则完整 |
| T1-06 | contribution / revenue / quota / bounty policy | 候选与确认分离 |

### Task Pack 2：KDS v2 最小骨架

| 任务 | 输出 | 验收 |
|---|---|---|
| T2-01 | `knowledge_objects` 表 | 迁移草案通过 |
| T2-02 | `object_pool_bindings` 表 | 对象挂池可追溯 |
| T2-03 | `fact_candidates` 表 | AI 候选可登记 |
| T2-04 | evidence 表 | 证据可绑定 |
| T2-05 | `POST /api/v2/search` | ACL、Domain、Pool、RAG filter 有契约 |
| T2-06 | Source / Evidence / Pool 详情接口 | 可回源 |

### Task Pack 3：WAES 最小门禁

| 任务 | 输出 | 验收 |
|---|---|---|
| T3-01 | Source Gate | 来源等级判断 |
| T3-02 | Evidence Gate | 证据完整性判断 |
| T3-03 | RAG Gate | safe/limited/repair/blocked |
| T3-04 | Writeback Gate | 写回候选门禁 |
| T3-05 | Contribution Gate | 积分候选门禁 |
| T3-06 | Revenue Gate | 收益候选门禁 |

### Task Pack 4：KWE 最小流程

| 任务 | 输出 | 验收 |
|---|---|---|
| T4-01 | KnowledgeWorkItem | 工单可创建 |
| T4-02 | GapRecord | 缺口可登记 |
| T4-03 | BountyRecord | 悬赏候选可登记 |
| T4-04 | ConfirmationWorkpack | 人工确认包 |
| T4-05 | 候选事实 -> 人工确认 -> KDS 状态更新 | no-write 流程先跑通 |
| T4-06 | 候选写回 -> WAES -> GFIS 写回候选 | 不写 GFIS 主账 |

### Task Pack 5：葛化 GFIS 试点

| 任务 | 输出 | 验收 |
|---|---|---|
| T5-01 | 葛化 GFIS 知识目录 | 七类资料包目录 |
| T5-02 | 建设资料导入 | metadata + evidence |
| T5-03 | 订单资料导入 | candidate fact |
| T5-04 | 辽宁远航链路资料导入 | gap + bounty candidate |
| T5-05 | 现代精工 OEM 过渡资料导入 | 责任边界候选 |
| T5-06 | GFIS 知识问答助手 | no-write 评测 |
| T5-07 | GFIS 使用助手 | no-write 评测 |
| T5-08 | GFIS 文档验收助手 | no-write 评测 |

### Task Pack 6：LOOP 与指挥舱

| 任务 | 输出 | 验收 |
|---|---|---|
| T6-01 | LOOP 模板 | 每轮可记录 |
| T6-02 | LOOP API | 契约草案 |
| T6-03 | 底座可用知识闭环率指标 | dry-run 可计算 |
| T6-04 | Contribution Ledger | 候选贡献可查 |
| T6-05 | Revenue Ledger | 收益口径可查 |
| T6-06 | Quota Ledger | AI 额度可查 |
| T6-07 | Bounty Ledger | 悬赏候选可查 |

## 18. 实施节奏

建议节奏：

| 周期 | 工作重点 | 产物 | 状态上限 |
|---|---|---|---|
| 第 1 周 | P0 11 份文档包 | 受控文档草案 + LOOP 记录 | `draft` / `controlled_analysis` |
| 第 2 周 | OKF 契约与对象模型 | YAML / JSON Schema / policy 草案 | `candidate` |
| 第 3 周 | KDS v2 最小骨架 | 表结构草案 + API 契约 + no-write fixture | `candidate` |
| 第 4 周 | WAES 最小门禁 | Source/Evidence/RAG/Writeback Gate dry-run | `evidence_ready`，不写主账 |
| 第 5 周 | KWE 最小流程 | WorkItem / Confirmation / Gap / Bounty 流程 | `candidate` |
| 第 6 周 | 葛化 GFIS 三件套评测 | AssistantOutputRecord / EvalRecord / DefectRecord | `partial` |
| 第 7 周 | 湖北磷材目录预检 | HBLC 知识目录、来源白名单、潜在产值候选 | `partial` |
| 第 8 周 | LOOP 与指挥舱 dry-run | 闭环率、台账、风险、下一轮动作 | `partial` |

不得在没有真实证据、人工确认和委员会记录前升级为 `accepted`、`complete` 或 `integrated`。

## 19. 验收门禁

### 19.1 文档门禁

1. 每个 Markdown 文档必须有 frontmatter。
2. 新目录必须有 README。
3. 文档污染检查必须通过。
4. KDS TOKEN 检查必须通过，且不得打印或写入 TOKEN 明文。
5. LOOP 文档门禁必须通过。

### 19.2 工程门禁

1. schema 校验通过。
2. API contract 测试通过。
3. Gate dry-run fixture 通过。
4. 无真实业务写入副作用。
5. 敏感资料不进入开放索引。

### 19.3 业务门禁

1. 资料来源明确。
2. 证据链完整。
3. 责任主体明确。
4. WAES 门禁结果记录。
5. 人工确认或委员会决议记录。
6. Harness evidence 固化。

## 20. 风险与控制

| 风险 | 控制 |
|---|---|
| 把方案写成完成 | 所有计划文档标注状态边界 |
| AI 候选被误用为正式事实 | candidate-only + WAES + KWE + Harness |
| Brain 被误当 KDS 主存 | 明确 Brain 只是工作台和指挥舱 |
| WAES 被误当业务主账 | 明确 WAES 只做规则与门禁 |
| GFIS 写回越权 | Writeback Gate + 业务负责人确认 |
| 敏感资料扩散 | metadata-only + 受控原件 + hash + ACL |
| 收益/积分提前结算 | 候选与确认分离，委员会确认 |
| 模板污染事实 | 模板只作为结构，事实必须来自具体项目和证据 |
| 多单位数据越权 | tenant isolation + ACL + external_account |
| LOOP 自动升级状态 | LOOP 只推动 evidence，不自动 accepted |

## 21. 下一步建议

立即执行顺序：

1. 以本文档作为总底稿，拆出 P0 首批 11 份受控文档。
2. 为 11 份文档补齐 frontmatter、编号、KDS 路径和状态边界。
3. 运行文档污染、KDS TOKEN、LOOP 文档门禁。
4. 建立 P0 LOOP 记录，状态保持 `partial` 或 `controlled_analysis`。
5. 再进入 OKF 契约和 KDS v2 no-write 工程骨架。

本轮不建议直接创建 API、UI 或生产数据库表。理由是当前方案仍处于制度固化和候选闭环阶段，真实业务写回、收益结算、委员会裁决和 RAG 强引用尚未形成 evidence。
