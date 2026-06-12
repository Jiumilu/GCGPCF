---
doc_id: GPCF-DOC-04D6680E14
title: GlobalCloud 绿色供应链体系知识与Agent授权治理总表
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系知识与Agent授权治理总表

日期：2026-06-07
状态：实施硬约束表 v1
适用范围：KDS（知识主存域）、知识引擎域、WAES、XiaoC（蚁后）、Hermes/XGD（大象）、Brain、LLM Wiki。

## 1. 目的

本表用于明确：

1. 知识从哪里来、谁能发布、谁能索引、谁能消费。
2. Agent 分层与权限边界。
3. 哪些动作只能建议，哪些需要治理授权，哪些永远禁止。

## 2. 知识治理总表

| 知识域 | 真源位置 | 发布主责 | 索引主责 | 消费方 | AI 可做 | AI 禁止 |
|---|---|---|---|---|---|---|
| 宪法 / 制度 | 企业级知识主存域 | 知识主存服务 + WAES 确认 | LLM Wiki / Brain | WAES、知识引擎、AI 服务 | 摘要、引用、差异分析 | 直接改正文、直接生效新版本 |
| SOP 标准 | 企业级知识主存域 | 知识主存服务 + WAES | LLM Wiki / Brain | WAES、GPC、GFIS、AI 服务 | 草案、复盘建议、引用 | 直接替换生效版 SOP |
| 项目方案 / 决策 | 企业级知识主存域 | 知识主存服务 + 人工确认 | LLM Wiki / Brain | WAES、知识引擎、AI 服务 | 摘要、对比、引用 | 直接形成正式决策 |
| 纪要 / 合同 / 验收 | 企业级知识主存域 | 知识主存服务 | LLM Wiki / Brain | WAES、知识引擎、AI 服务 | 提取要点、候选引用 | 篡改正式文本、生成伪回执 |
| 案例 / 复盘 / 提示词 | 知识主存域 / Brain | Brain / XiaoC / WAES 审核 | Brain | AI 服务、WAES | 生成候选、评估、回归 | 未审直接进关键生产流 |

## 3. Agent 分层与权限矩阵

| Agent 类型 | 主责 | 默认权限 | 可升级权限 | 永久禁止 |
|---|---|---|---|---|
| 治理 Agent | 规则、证据、状态、验收辅助 | read、summarize、request_governance | request_governance、create_draft | approve_transaction、write_business_fact |
| 知识 Agent | 知识检索、摘要、引用、复盘草案 | read、summarize、cite | create_draft | publish_effective_knowledge、edit_official_text |
| 运营 Agent | 订单、运输、异常协同建议 | read、summarize、suggest | create_draft、request_governance | confirm_pod、close_exception_as_fact、write_business_fact |
| 工厂 Agent | 工单、质量、库存、设备建议 | read、summarize、suggest | create_draft、request_governance | release_work_order、accept_quality、post_inventory |
| 证据 Agent | 证据归集、缺证提示、引用检查 | read、summarize、link_evidence | create_draft | verify_evidence、upgrade_status |

## 4. 知识生命周期与 AI 可见性

| 状态 | 是否进入知识引擎 | 是否允许 AI 默认消费 | 说明 |
|---|---|---|---|
| draft | 否，默认不进入 | 否 | 仅在受限测试环境可选进入 |
| in_review | 受限进入 | 受限 | 仅特定评审 Agent 可见 |
| approved | 可进入 | 可受限消费 | 已通过审批，未必已生效 |
| effective | 是 | 是 | 正式有效知识版本 |
| superseded | 可保留历史索引 | 仅显式查询 | 默认不作为首选引用 |
| retired | 不应默认进入 | 否 | 仅审计与历史查阅可见 |
| archived | 否 | 否 | 归档保存 |

## 5. WAES 输出接口标准化

建议固定为以下 6 类治理输出：

1. `GovernancePolicy`
2. `MetricDefinition`
3. `StatusRequirement`
4. `ConnectorDecision`
5. `KnowledgeAccessPolicy`
6. `AIAuthorizationGrant`
7. `AcceptanceConclusion`

说明：这些是治理输出，不是业务事务审批结果。

## 6. 强制禁止清单

### 6.1 AI 永久禁止

1. 直接写 `GFIS`、`GPC`、`PVAOS` 业务主账。
2. 直接批准工单、质量放行、库存调整、发货、签收、维修验收。
3. 直接发布正式知识生效版本。
4. 直接确证证据。
5. 直接升级项目完成状态为 `accepted` 或 `complete`。

### 6.2 仅可生成草案

1. 治理审批请求草案。
2. SOP 草案。
3. Prompt 草案。
4. 知识候选条目。
5. 异常处理建议。
6. 证据补证建议。

## 7. 实施建议

1. 先把 `AgentToolGrant` 和 `KnowledgeAccessPolicy` 做成强约束对象。
2. 先实现只读和建议能力，再逐步开放草案能力。
3. 所有高风险动作默认拒绝，按白名单增开。
4. 所有 AI 输出必须携带引用或证据来源，否则降级为不可治理结论。
