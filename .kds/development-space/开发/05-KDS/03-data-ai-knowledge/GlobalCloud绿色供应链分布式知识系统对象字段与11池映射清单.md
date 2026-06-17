---
doc_id: GPCF-DOC-52D30A36F6
title: GlobalCloud 绿色供应链分布式知识系统对象字段与11池映射清单
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链分布式知识系统对象字段与11池映射清单

日期：2026-06-17
状态：v0.1 受控实施映射草案
适用范围：KDS、WAES、GFIS、GPC、PVAOS、Brain、XiaoC、Hermes/XGD、小即、楚商云、葛化、湖北磷材及后续绿色供应链合作单位。

## 1. 定位

本文是 `GlobalCloud 绿色供应链分布式知识系统实施治理方案` 的字段化落地清单，用于把方案中的对象、编号、状态、责任边界和 KDS 11 池映射拆成可执行的治理结构。

本文只定义对象字段、映射关系、候选状态和检查规则，不定义真实业务收入、不确认真实积分、不触发收益分配、不写 GFIS / GPC / PVAOS 业务主账。

## 2. 基本边界

1. KDS 是知识主存和受控口径，不替代业务主账。
2. KDS 11 池是资源语义聚合和事实基础数据底座，不是直接录入层。
3. AI 建议只能形成 `AISuggestion`、候选事实包、SOP 建议、证据缺口或风险提示。
4. WAES 只确认规则、证据、越权、状态和责任边界，不替代业务审批。
5. GFIS / GPC / PVAOS 仍是对应业务事实的主责系统。
6. 用户保留治理急停权；具体争议和分配裁决由知识收益治理委员会按多数决形成 `DecisionRecord`。

## 3. 编号总表

| 编号前缀 | 对象 | 示例 | 生效条件 |
|---|---|---|---|
| AIS | AI 建议 | `AIS-GH-SOP-202606-0003` | KDS 候选登记后生效为建议，不等于业务事实 |
| CEV | 贡献事件 | `CEV-GH-202606-0001` | 有来源对象和贡献主体后登记 |
| PTS | 积分记录 | `PTS-GH-202606-0001` | 候选或确认积分均可登记，需区分状态 |
| PEN | 负积分 / 处罚 | `PEN-GH-202606-0001` | 违规事实成立或风险冻结后登记 |
| KGR | 知识缺口请求 | `KGR-GH-EVD-202606-0001` | 系统、人员或单位发起后登记 |
| KGB | 悬赏任务 | `KGB-GH-EVD-202606-0001` | 悬赏资源冻结后生效 |
| KGS | 缺口提交 | `KGS-GH-202606-0001` | 提交成果进入 KDS 候选 |
| BTS | 悬赏结算 | `BTS-GH-202606-0001` | 验收、裁决或协商完成后登记 |
| PVR | 潜在产值 | `PVR-GH-202606-0001` | 未到账但存在可追踪业务机会 |
| INV | 开票记录 | `INV-GH-202606-0001` | 进入统计和财务过程口径 |
| CAS | 到账记录 | `CAS-GH-202606-0001` | 进入正式收入和收益池分配口径 |
| REV | 收益记录 | `REV-KNO-202606-0001` | 与到账、分配规则和裁决记录关联 |
| AQA | AI 额度账户 | `AQA-GH-202606-0001` | 分配、购买、贡献或共享额度后登记 |
| AQU | AI 使用记录 | `AQU-GH-202606-0001` | 每次额度消耗或兑换后登记 |
| DRC | 委员会裁决 | `DRC-POINT-202606-0001` | 多数决、备案和审计记录齐全后登记 |
| DSR | 需求来源 | `DSR-GH-202606-0001` | 电话、会议、邮件、聊天或第三方介绍形成需求后登记 |
| POO | 预运营期订单 | `POO-GH-202606-0001` | 人工确认后生效，AI 只能生成建议 |
| OEP | OEM 证据包 | `OEP-GH-202606-0001` | OEM 承接方生产、质量、发货、POD、金融凭证成包后登记 |
| FEA | 拓厂评估 | `FEA-HBLC-202606-0001` | 湖北磷材或后续拓厂项目评估启动后登记 |

## 4. `AISuggestion` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| suggestionId | string | 是 | 统一编号，格式 `AIS-{单位}-{类型}-{年月}-{序号}` |
| unitCode | enum | 是 | `GH`、`HBLC`、`CSY` 或后续合作单位代码 |
| suggestionType | enum | 是 | `KNO`、`SOP`、`EVD`、`BIZ`、`RSK`、`REV` |
| scenario | enum | 是 | 建设、工厂运营、订单、原料、拓厂、质量、发货、POD、金融凭证、政策、行业 |
| sourceRefs | array | 是 | 文档、会议、邮件、聊天、GFIS/GPC/PVAOS 引用、网站或第三方材料引用 |
| sourceTrustLevel | enum | 是 | 一般、合作单位、业务系统、权威政策/标准、WAES确认 |
| classificationLevel | enum | 是 | `DSR-L0`、`DSR-L1`、`DSR-L2`、`DSR-L3` 或对应密级 |
| confidence | enum | 是 | `low`、`medium`、`high` |
| confidenceReason | text | 是 | 置信度理由，必须说明证据充分或不足之处 |
| candidateFactRefs | array | 否 | 候选事实包引用 |
| sopSuggestionRefs | array | 否 | SOP 建议引用 |
| evidenceGapRefs | array | 否 | 证据缺口引用 |
| targetSystem | enum | 是 | KDS、WAES、GFIS、GPC、PVAOS；仅表示建议路径 |
| proposedAction | text | 是 | 建议动作 |
| forbiddenOperations | array | 是 | 明确 AI 不得直接执行的动作 |
| kdsCandidateStatus | enum | 是 | draft、registered、rejected、superseded |
| waesGateStatus | enum | 是 | pending、governance_recorded、governance_approved、governance_rejected、governance_blocked |
| humanConfirmationRequired | boolean | 是 | 默认 true |
| contributionEventId | string | 否 | 关联贡献事件 |
| decisionRecordId | string | 否 | 争议、规则或重大事项裁决记录 |

## 5. `ContributionEvent` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| eventId | string | 是 | `CEV-{单位}-{年月}-{序号}` |
| contributorType | enum | 是 | person、company、project_group、committee_member、external_expert、ai_agent |
| contributorId | string | 是 | 贡献主体标识 |
| beneficiary | enum | 是 | 默认平台；AI 生成内容的知识归属统一归平台 |
| contributionType | enum | 是 | knowledge、value、channel、governance、reuse、evidence |
| sourceObjectType | enum | 是 | AISuggestion、Document、Meeting、Order、Evidence、BountySubmission、DecisionRecord |
| sourceObjectId | string | 是 | 来源对象编号 |
| evidenceRefs | array | 是 | 原始证据引用 |
| projectCode | string | 是 | GH、HBLC 或后续项目 |
| phase | enum | 是 | initial、pilot、scale、operating |
| candidatePointId | string | 否 | 候选积分记录 |
| confirmedPointId | string | 否 | 确认积分记录 |
| potentialValueRecordId | string | 否 | 潜在产值记录 |
| revenueRecordId | string | 否 | 实际收益记录 |
| status | enum | 是 | candidate、confirmed、frozen、disputed、deducted、cancelled |

## 6. `PointLedger` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| pointId | string | 是 | `PTS-{单位}-{年月}-{序号}` |
| pointStatus | enum | 是 | candidate、confirmed、frozen、deducted、available、expired |
| pointType | enum | 是 | knowledge、value、channel、governance、reuse、bounty、penalty |
| contributionEventId | string | 是 | 关联贡献事件 |
| baseScore | number | 是 | 基础分 |
| stageWeight | number | 是 | 阶段权重；初始阶段知识和产值权重较高 |
| projectCoefficient | number | 是 | 项目系数，可随项目和市场变化 |
| contributionTypeCoefficient | number | 是 | 不同积分权重兑换系数 |
| evidenceCoefficient | number | 是 | 客户确认函、POD、到账凭证等原始证据可使用高系数 |
| riskCorrectionCoefficient | number | 是 | 证据不足、争议、密级风险、违规风险修正 |
| finalScore | number | 是 | 计算后积分 |
| confirmerRole | enum | 是 | 资料管理员、WAES、财务/项目负责人、委员会 |
| confirmedAt | date | 否 | 确认时间 |
| decisionRecordId | string | 否 | 重大或争议事项必须关联 |
| visibilityScope | enum | 是 | own_unit、project_group、committee、platform_admin |

积分兑换系数必须可版本化，不得写死为永久规则。候选积分不得进入正式收益分配，冻结积分不得兑换 AI 服务。

## 7. `RevenueLedger` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| revenuePoolId | string | 是 | `REV-{类型}-{年月}-{序号}` |
| revenuePoolType | enum | 是 | knowledge、system、business |
| sourceIncomeType | enum | 是 | AI 服务、知识服务、系统服务、项目服务、订单业务、第三方服务 |
| invoiceRecordId | string | 否 | 开票进入统计和财务过程口径 |
| cashReceivedRecordId | string | 否 | 到账后进入正式收益池分配口径 |
| amount | number | 是 | 金额 |
| currency | string | 是 | 币种 |
| sourceContractRef | string | 否 | 合同或订单引用 |
| allocationRuleVersion | string | 是 | 分配规则版本 |
| allocationRunId | string | 否 | 分配执行批次 |
| decisionRecordId | string | 否 | 委员会裁决或备案记录 |
| status | enum | 是 | statistical、cash_received、allocation_pending、allocated、frozen、disputed |

合作单位自购 AI 额度初期只自用，不进入收益池；可进入计量视图，供合作单位参考和后续治理评估。

## 8. `KnowledgeGapBounty` 字段

| 对象 | 关键字段 | 说明 |
|---|---|---|
| KnowledgeGapRequest | requestId、initiatorType、initiatorId、gapType、scenario、requiredEvidence、visibilityScope、deadline、classificationLevel | 系统、人员或单位均可发起 |
| KnowledgeGapBounty | bountyId、requestId、rewardMix、frozenPointAmount、frozenCashAmount、frozenAIQuota、serviceRights、sponsorId、status | 支持积分、现金、AI额度、服务权益混合悬赏 |
| KnowledgeGapSubmission | submissionId、bountyId、submitterId、submissionRefs、evidenceRefs、aiAssisted、originalityDeclaration、status | 提交后先进入 KDS 候选 |
| BountySettlement | settlementId、bountyId、acceptedParts、rejectedParts、allocationRatio、settlementPointId、cashSettlementRef、aiQuotaSettlementRef、decisionRecordId | 可多人分配、部分通过、部分退回或进入争议 |

知识缺口悬赏允许公开、半公开、定向和私密四类可见范围。悬赏冻结资源在结算或撤销前不得重复使用。

## 9. `DisputeCase` 与 `DecisionRecord` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| disputeId | string | 是 | 争议编号 |
| disputeType | enum | 是 | point、revenue、bounty、evidence、authority、confidentiality、penalty |
| relatedObjectRefs | array | 是 | 关联对象 |
| claimantId | string | 是 | 发起方 |
| respondentIds | array | 否 | 被申诉方 |
| evidenceRefs | array | 是 | 争议证据 |
| committeeScope | enum | 是 | project_only、platform、external_expert_required |
| decisionRecordId | string | 否 | 裁决记录 |
| status | enum | 是 | submitted、reviewing、decided、appealed、closed |

`DecisionRecord` 必须包含：事项类型、参与委员、回避人员、投票结果、多数决结论、适用规则、备案状态、用户治理急停是否触发、KDS/WAES 审计引用。

## 10. `AIQuotaAccount` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| accountId | string | 是 | `AQA-{单位}-{年月}-{序号}` |
| accountOwnerType | enum | 是 | platform、company、project_group、person |
| quotaSource | enum | 是 | platform_provided、self_purchased、contributed、shared、bounty_reward |
| quotaBalance | number | 是 | 当前可用额度 |
| quotaFrozen | number | 是 | 悬赏或争议冻结额度 |
| usagePolicyVersion | string | 是 | 使用规则版本 |
| revenuePoolEligible | boolean | 是 | 自购额度初期为 false |
| visibilityScope | enum | 是 | own_unit、project_group、platform_admin |

AI 使用记录 `AIQuotaUsageRecord` 必须记录调用场景、模型、成本、使用人、受益对象、是否用于悬赏、是否可计贡献和是否含敏感资料。

## 11. 葛化 `DemandSourceRecord` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| demandSourceId | string | 是 | `DSR-GH-YYYYMM-0001` |
| sourceType | enum | 是 | phone、meeting、email、chat、third_party_intro、document、system_record |
| sourceOwner | string | 是 | 来源责任人 |
| customerRef | string | 否 | 客户引用，如辽宁远航 |
| demandSummary | text | 是 | 需求摘要 |
| originalEvidenceRefs | array | 是 | 原始证据引用 |
| classificationLevel | enum | 是 | `DSR-L0`、`DSR-L1`、`DSR-L2`、`DSR-L3` |
| aiSuggestionId | string | 否 | AI 可生成需求整理建议 |
| preOperationOrderCandidateId | string | 否 | 可关联预运营期订单候选 |
| waesGateStatus | enum | 是 | pending、governance_recorded、governance_blocked |

`DSR-L3` 默认仅用户、委员会授权人员、相关项目负责人和必要 WAES 治理人员可见。

## 12. 葛化 `PreOperationOrder` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| preOperationOrderId | string | 是 | `POO-GH-YYYYMM-0001` |
| demandSourceId | string | 是 | 来源需求 |
| customerRef | string | 是 | 客户引用 |
| targetFactoryRef | string | 是 | 葛化目标工厂 |
| oemExecutorRef | string | 否 | 现代精工或其他 OEM 承接方 |
| responsibilitySplit | text | 是 | 目标工厂与 OEM 承接方事实责任划分 |
| orderScenario | enum | 是 | sample_box、trial_order、transition_order、capacity_reserve、conversion_prepare |
| productRefs | array | 是 | 产品、规格、箱型、工艺引用 |
| qualityRequirementRefs | array | 是 | 质量要求引用 |
| shipmentRequirementRefs | array | 否 | 发货和 POD 要求 |
| financeEvidenceRequirementRefs | array | 否 | 金融凭证门禁要求 |
| oemEvidencePackageId | string | 否 | OEM 证据包 |
| conversionCriteria | array | 是 | 客户确认、质量证据、WAES规则确认/记录、GFIS映射 |
| capacitySchedulingRequired | boolean | 是 | 是否纳入产能调度准备 |
| gfisMappingStatus | enum | 是 | not_mapped、candidate_mapped、mapped、blocked |
| waesGateStatus | enum | 是 | pending、governance_recorded、governance_approved、governance_rejected、governance_blocked |
| status | enum | 是 | candidate、confirmed、running、converted_to_operating_order、closed_as_knowledge_case、cancelled、frozen、in_dispute |

预运营期订单可由 AI 建议生成候选，但必须人工确认后生效。投产运营后，葛化自有 GFIS 为主要事实源，OEM 保留为产能调度、特殊工艺、临时补位、应急交付和样箱小批量外协路径。

## 13. `OEMProductionEvidencePackage` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| evidencePackageId | string | 是 | `OEP-GH-YYYYMM-0001` |
| preOperationOrderId | string | 是 | 预运营期订单 |
| oemExecutorRef | string | 是 | OEM 承接方 |
| productionEvidenceRefs | array | 是 | 生产事实证据 |
| qualityEvidenceRefs | array | 是 | 质量证据 |
| shipmentEvidenceRefs | array | 否 | 发货证据 |
| podEvidenceRefs | array | 否 | POD / 签收证据 |
| financeEvidenceRefs | array | 否 | 金融凭证、开票或到账引用 |
| customerConfirmationRefs | array | 否 | 客户确认函、测试反馈、转量产批准 |
| waesEvidenceCompleteness | enum | 是 | incomplete、partial、complete |
| responsibilityReviewStatus | enum | 是 | pending、reasonable、disputed、blocked |
| contributionEligible | boolean | 是 | 是否可进入积分/收益贡献模型，需与合作单位确认协商 |

## 14. 湖北磷材 `FactoryExpansionAssessment` 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| assessmentId | string | 是 | `FEA-HBLC-YYYYMM-0001` |
| expansionProjectRef | string | 是 | 拓厂项目引用 |
| ghTemplateVersion | string | 是 | 葛化母版版本 |
| rawMaterialKnowledgeRefs | array | 是 | 原料知识引用 |
| industryKnowledgeRefs | array | 是 | 行业和政策知识引用 |
| orderKnowledgeRefs | array | 是 | 销售订单和客户需求知识 |
| preOperationOrderWeight | number | 是 | 已有预运营期订单为高权重加权项，不是一票通过 |
| oemTransitionCapability | enum | 是 | none、candidate、available、verified |
| gfisReadiness | enum | 是 | not_ready、partial、ready、blocked |
| greenSupplyChainRevenuePotential | enum | 是 | low、medium、high |
| aiSuggestionRefs | array | 否 | AI 形成的拓厂、原料、订单或行业建议 |
| waesGateStatus | enum | 是 | pending、governance_recorded、governance_approved、governance_blocked |

湖北磷材第一阶段不做 GFIS 深度，优先形成拓厂项目知识库、原料/行业/订单知识库和新工厂复制模板。

## 15. KDS 11 池映射清单

| 对象 | 订单池 | 运力池 | 产能池 | 资金池 | 政策池 | 装备池 | 数据池 | 能源池 | 原料池 | 人才池 | 场景池 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AISuggestion | 订单建议 | 发货/POD建议 | 产能建议 | 收益建议 | 政策建议 | 设备建议 | 来源/置信度 | 能耗建议 | 原料建议 | 角色建议 | SOP建议 |
| ContributionEvent | 订单贡献 | 运输贡献 | 产能贡献 | 产值贡献 | 知识贡献 | 装备贡献 | 证据贡献 | 能源贡献 | 原料贡献 | 人员贡献 | 复用贡献 |
| PointLedger | 订单积分 | 运力积分 | 产能积分 | 产值积分 | 政策知识积分 | 装备积分 | 数据治理积分 | 能源积分 | 原料积分 | 人才积分 | SOP积分 |
| RevenueLedger | 业务收益 | 物流收益 | 产能收益 | 收益主挂 | 政策服务收益 | 设备服务收益 | 数据服务收益 | 能源服务收益 | 原料服务收益 | 培训服务收益 | 系统/SOP收益 |
| KnowledgeGapBounty | 订单缺口 | POD缺口 | 产能缺口 | 凭证缺口 | 政策缺口 | 装备缺口 | 数据缺口 | 能源缺口 | 原料缺口 | 专家缺口 | SOP缺口 |
| DisputeCase | 订单争议 | POD争议 | 产能争议 | 收益争议 | 规则争议 | 装备争议 | 证据争议 | 能源争议 | 原料争议 | 贡献主体争议 | SOP争议 |
| AIQuotaAccount | 订单问答 | 物流问答 | 产能问答 | 额度计量 | 政策问答 | 设备问答 | 使用计量 | 能源问答 | 原料问答 | 培训问答 | SOP助手 |
| DemandSourceRecord | 需求来源 | 可选 | 产能需求 | 潜在产值 | 可选 | 可选 | 原始来源 | 可选 | 可选 | 来源责任人 | 场景入口 |
| PreOperationOrder | 主挂 | 发货/POD | 目标工厂/OEM产能 | 潜在产值/到账 | 可选 | 可选 | 证据链 | 可选 | 物料需求 | 责任人 | 预运营SOP |
| OEMProductionEvidencePackage | 订单证据 | 发货/POD | OEM承接能力 | 金融凭证 | 可选 | 设备/产线 | 证据完整性 | 可选 | 原料批次 | OEM责任人 | 责任划分规则 |
| FactoryExpansionAssessment | 订单潜力 | 区域运力 | 新工厂产能 | 收益潜力 | 行业政策 | 装备条件 | 拓厂知识 | 能耗条件 | 原料条件 | 项目团队 | 复制模板 |

## 16. 门禁检查清单

| 检查项 | 通过标准 |
|---|---|
| AI 建议边界 | `AISuggestion` 不直接写业务主账，必须有禁止越权说明 |
| 来源证据 | 所有积分、收益、悬赏、争议对象必须能追溯到来源引用 |
| 候选与确认区分 | 候选积分、候选事实、候选 SOP 不得当作确认结果 |
| 收入口径 | 开票只进入统计和财务过程口径；到账才进入正式收益池 |
| 自购额度 | 合作单位自购 AI 额度初期只自用，不进入收益池 |
| 预运营责任 | 目标工厂与 OEM 承接方必须区分事实责任 |
| WAES 规则内事项 | 规则内使用 `governance_recorded`，超规则才审批或阻断 |
| 委员会裁决 | 争议和重大分配必须有 `DecisionRecord`，并备案 |
| 用户掌控 | 用户不做具体裁决，但保留治理急停权 |
| KDS 11 池 | 对象必须至少挂接一个资源池，不得成为游离账本 |

## 17. 下一轮落点

建议下一轮进入：

```text
GPCF-KDS-DKS-003：
建立葛化订单运行母版字段/单据映射专项，优先围绕辽宁远航链路、现代精工 OEM 过渡、质量/发货/POD/金融凭证门禁形成可验收清单。
```

本文当前只完成对象字段和 11 池映射，不证明业务系统可用、不证明真实收入成立、不证明 GFIS SOP E2E 通过，也不得自动升级为 accepted、complete 或 integrated。
