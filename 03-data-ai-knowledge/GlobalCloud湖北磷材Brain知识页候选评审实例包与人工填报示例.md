---
doc_id: GPCF-DOC-3501E53D2C
title: GlobalCloud 湖北磷材 Brain 知识页候选评审实例包与人工填报示例
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选评审实例包与人工填报示例.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选评审实例包与人工填报示例.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材 Brain 知识页候选评审实例包与人工填报示例

日期：2026-06-17  
状态：`virtual_review_example`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-035 的湖北磷材 Brain 知识页候选运行评审空白台账与发布前问题清单，使用虚拟脱敏样例演示三类页面如何从候选态进入评审态：

1. 拓厂项目知识页候选。
2. 行业资料页候选。
3. 订单线索页候选。

本文只做填报演练，不表示：

- 湖北磷材已经提交真实资料；
- 本文样例对应真实区域、真实客户、真实订单、真实合同、真实价格或真实政策适用结论；
- Brain 页面已经正式发布；
- WAES 已经真实放行；
- KDS、WAES、GFIS、GPC 或其他业务系统已经发生真实写入；
- 积分、收益、悬赏、潜在产值或 SOP 已经确认。

## 2. 虚拟样例总规则

| 项 | 规则 |
|---|---|
| 样例类型 | `virtual_redacted_example` |
| 数据来源 | 人工构造的脱敏演练值 |
| 禁止用途 | 不得作为真实业务事实、真实投资、真实订单、真实收入或正式发布依据 |
| AI 作用 | 生成候选摘要、候选缺口、候选问题和候选写回建议 |
| 人工作用 | 演示评分、红线、退回、发布建议和责任确认 |
| WAES 作用 | 演示规则边界和门禁结果，不替代业务事实确认 |
| KDS 挂接 | 每条样例必须挂接至少一个 KDS 11 池 |
| 增强账本 | 只形成候选，不形成正式积分、收益、悬赏或潜在产值 |

## 3. VirtualSourceSummary 样例

| virtualSourceId | linkedBrainPageId | sourceType | redactedSummary | sourceIndexStatus | trustLayer | ownerRole | timestampStatus |
|---|---|---|---|---|---|---|---|
| `VSS-HBLC-FEA-202606-0001` | `BKP-HBLC-FEA-202606-0001` | 虚拟会议纪要摘要 | 某区域存在拓厂讨论，涉及用地条件、设备需求、产能假设和政策咨询；不含真实地点、金额或责任人姓名 | complete | T1-candidate | 湖北磷材项目负责人 | present |
| `VSS-HBLC-IND-202606-0001` | `BKP-HBLC-IND-202606-0001` | 虚拟公开资料索引 | 某行业标准可能影响原料质量指标和出厂检测口径；来源链接待补权威站点和检索时间 | partial | T2-candidate | 行业资料责任方 | missing |
| `VSS-HBLC-ORD-202606-0001` | `BKP-HBLC-ORD-202606-0001` | 虚拟电话需求摘要 | 匿名客户提出规格、数量区间和交期意向；不含客户实名、合同、订单原文、开票或到账材料 | partial | T1-candidate | 销售或渠道责任方 | present |

## 4. ReviewExampleFilledRegister

| reviewId | linkedBrainPageId | pageType | sourceIndexStatus | redactionStatus | kdsPoolCheck | ledgerCheck | waesGateStatus | manualScore | redlineStatus | publishSuggestion | currentStatus |
|---|---|---|---|---|---|---|---|---:|---|---|---|
| `BPR-HBLC-FEA-202606-EX01` | `BKP-HBLC-FEA-202606-0001` | 拓厂项目知识页候选 | complete | pass | pass | pass | record | 88 | pass | project_review | reviewing |
| `BPR-HBLC-IND-202606-EX01` | `BKP-HBLC-IND-202606-0001` | 行业资料页候选 | partial | pass | pass | not_applicable | return | 76 | return | keep_candidate | returned |
| `BPR-HBLC-ORD-202606-EX01` | `BKP-HBLC-ORD-202606-0001` | 订单线索页候选 | partial | pass | pass | committee_required | record | 82 | pass | keep_candidate | reviewing |

## 5. ExampleDecisionTrace

| traceId | linkedReviewId | decision | reason | nextAction | hardStop |
|---|---|---|---|---|---|
| `EDT-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | 允许进入项目组评审候选 | 来源索引完整、脱敏通过、KDS 池挂接完整、人工评分高于 85、红线通过；但仍不代表投资或建设确认 | 进入项目组评审候选，补充真实资料前保持候选态 | false |
| `EDT-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | 退回补权威来源 | 缺少权威来源链接、检索时间和适用范围；WAES 规则候选为 return | 补齐权威政策/标准来源后重评 | false |
| `EDT-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | 保持候选态 | 电话需求只能作为订单线索，不能写成正式订单、开票或到账收入；涉及潜在产值需委员会或人工确认 | 补客户匿名编号、来源记录和财务口径边界 | false |

## 6. ExampleIssueCloseRecord

| issueCloseId | linkedIssueId | linkedReviewId | issueType | exampleCloseAction | closeEvidence | status |
|---|---|---|---|---|---|---|
| `EIC-HBLC-FEA-202606-0001` | `PPI-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | source_gap | 虚拟样例已补来源类型、责任角色和时间戳 | virtual_source_summary_present | example_closed |
| `EIC-HBLC-IND-202606-0001` | `PPI-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | trust_gap | 虚拟样例未补权威来源，保持退回 | missing_authoritative_source | example_open |
| `EIC-HBLC-ORD-202606-0001` | `PPI-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | revenue_boundary | 已明确电话需求不等同正式订单、开票或到账收入 | revenue_boundary_marked | example_closed_candidate |

## 7. ExampleKdsPoolAndLedgerMapping

| mappingId | linkedReviewId | kdsPoolRefs | enhancedLedgerRefs | mappingStatus | note |
|---|---|---|---|---|---|
| `EKM-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | SOP 账本 / 贡献账本 / 悬赏池 | pass | 拓厂评审只形成项目评审候选和 SOP 候选，不形成建设事实 |
| `EKM-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | 政策池 / 数据池 / 场景池 | 贡献账本 | pass | 行业资料必须补权威来源后才可升级可信层级 |
| `EKM-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | 订单池 / 产能池 / 资金池 / 数据池 | 潜在产值池 / 贡献账本 / 悬赏池 | pass | 潜在产值只能做候选；正式收入按到账确认 |

## 8. ExampleWaesGateRecord

| waesExampleId | linkedReviewId | gateType | gateResult | ruleConfirmed | nextStep |
|---|---|---|---|---|---|
| `EWG-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | publish_boundary | record | 拓厂评审候选不得等同投资、合作或建设启动确认 | 项目组评审候选 |
| `EWG-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | trusted_source | return | T3 可信来源升级必须补权威来源、检索时间和适用范围 | 退回补源 |
| `EWG-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | revenue_boundary | record | 电话需求不得等同正式订单、开票或到账收入 | 保持候选并补证 |

## 9. ExampleAiWritebackSuggestion

| suggestionId | linkedReviewId | targetSystem | candidateWriteback | confirmationRequired | forbiddenAction |
|---|---|---|---|---|---|
| `AWS-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | KDS / Brain | 写回拓厂页面候选摘要、KDS 池挂接、项目组评审候选状态 | 人工确认 / WAES 记录 | 不写投资通过、合作确认、建设启动 |
| `AWS-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | KDS / Brain | 写回行业资料退回原因、补权威来源任务、可信层级待补 | 人工确认 / WAES 记录 | 不写权威结论或 T3 通过 |
| `AWS-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | KDS / Brain | 写回订单线索候选、潜在产值边界、补证任务 | 人工确认 / 委员会条件触发 | 不写正式订单、开票、到账收入或 GFIS 主账 |

## 10. 人工填报步骤示例

| step | action | input | output | gate |
|---|---|---|---|---|
| 1 | 选择页面候选 | `BKP-HBLC-*` | 对应评审记录 | page_candidate_present |
| 2 | 填来源摘要 | 虚拟脱敏摘要 | `sourceIndexStatus` | source_check |
| 3 | 做脱敏检查 | 不含原文和敏感字段 | `redactionStatus=pass` | redaction_check |
| 4 | 做 KDS 挂接 | KDS 11 池至少一个 | `kdsPoolCheck=pass` | kds_pool_check |
| 5 | 做账本检查 | 增强账本不可游离 | `ledgerCheck` | ledger_check |
| 6 | 做 WAES 规则记录 | 发布、可信、收益边界 | `waesGateStatus` | waes_check |
| 7 | 填人工评分和红线 | 评分、红线结论 | `manualScore` / `redlineStatus` | manual_check |
| 8 | 生成发布建议 | 规则匹配 | `publishSuggestion` | publish_gate |
| 9 | 生成写回建议 | 候选字段 | `candidateWriteback` | human_confirm_required |

## 11. 完成定义

本文完成条件：

1. 至少三条虚拟脱敏样例覆盖拓厂、行业资料和订单线索。
2. 每条样例均有来源摘要、评审记录、决策轨迹、问题闭合或保留、KDS 池挂接和 WAES 规则记录。
3. 订单线索样例明确不得写成正式订单、开票或到账收入。
4. 行业资料样例明确缺权威来源时退回。
5. 拓厂样例明确只能进入项目组评审候选，不形成投资、合作或建设事实。
6. AI 写回建议全部保持候选态，并要求人工或 WAES 确认。
7. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 12. DKS-037 建议

下一轮建议建立“湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则”，把虚拟样例中的评审结果转成候选 SOP 控制点、候选 KDS 字段、候选 WAES 规则和禁止写回清单。
