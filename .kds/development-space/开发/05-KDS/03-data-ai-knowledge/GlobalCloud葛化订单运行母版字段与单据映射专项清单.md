---
doc_id: GPCF-DOC-486DF4F549
title: GlobalCloud 葛化订单运行母版字段与单据映射专项清单
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化订单运行母版字段与单据映射专项清单

日期：2026-06-19
轮次：`GPCF-KDS-DKS-049`
状态：`controlled_master_draft`

## 1. 定位

本文定义葛化第一阶段“预运营期订单”的订单运行母版。它用于把客户需求、报价、OEM 承接、质量、发货、POD、金融凭证和 WAES/KDS 记录统一为可治理的候选对象，支撑 GFIS 使用助手、文档验收助手和候选事实驱动 SOP 建议。

本文不创建正式订单，不写 GFIS 主账，不确认收入、质量放行、POD、到账、积分、收益、悬赏或争议裁决，不证明葛化自建工厂已正式运营。

## 2. 母版原则

| 原则 | 口径 |
|---|---|
| 从需求开始 | 需求来源可以是电话、会议、邮件、聊天记录、第三方介绍、平台线索或合作单位转交资料。无来源只能形成缺口，不能形成订单候选。 |
| 阶段名称 | 统一使用“预运营期订单”。这是每个新工厂正式运营前的必备阶段。 |
| 双主体记录 | GFIS 同时记录目标工厂和 OEM 承接方。目标工厂记录未来承接和建设/运营准备责任，OEM 承接方记录当前生产、质量、发货等事实责任。 |
| 候选优先 | KDS、WAES、GFIS 在缺少真实 source-of-record 前只能记录候选、缺口、风险、建议或待确认事项。 |
| WAES 分层 | 规则以内事项只做 governance_recorded；缺证、越权、跨主体、收益、重大扣减或争议事项进入 manual_confirmation_required 或 committee_review_required。 |
| 用户掌控 | 人工确认、委员会备案、收益分配、积分确认、正式写回和状态升级必须保留人工或委员会路径。 |

## 3. 对象链

预运营期订单从需求线索到正式运营准备，采用以下对象链：

```text
DemandSourceRecord
  -> PreOperationOrderCandidate
  -> QuoteOrOfferEvidence
  -> CustomerConfirmationEvidence
  -> OEMResponsibilityRecord
  -> SampleBoxFeedbackRecord
  -> QualityEvidenceRecord
  -> DeliveryPODRecord
  -> FinanceEvidenceIndex
  -> WAESGateRecord
  -> SOPSuggestion
  -> FormalOperationReadinessCandidate
```

任一对象缺少来源、责任主体、状态或证据时，不得向后升级为业务事实。AI 可以输出缺口、候选字段、候选 SOP 和下一步建议，但不得替代业务确认。

## 4. 统一编号

| 编号前缀 | 对象 | 示例 | 状态范围 |
|---|---|---|---|
| `DSR-GH-YYYYMM-0001` | 需求来源记录 | `DSR-GH-202606-0001` | candidate / evidence_missing / controlled_source |
| `POO-GH-YYYYMM-0001` | 预运营期订单候选 | `POO-GH-202606-0001` | candidate / evidence_collecting / blocked / manual_review |
| `QTE-GH-LY-YYYYMM-0001` | 报价或要约证据 | `QTE-GH-LY-202606-0001` | candidate / customer_unconfirmed / confirmed_by_source |
| `CCE-GH-YYYYMM-0001` | 客户确认证据 | `CCE-GH-202606-0001` | missing / candidate / verified_by_human |
| `OEM-GH-MJ-YYYYMM-0001` | OEM 责任记录 | `OEM-GH-MJ-202606-0001` | candidate / responsibility_split_recorded / disputed |
| `SBF-GH-YYYYMM-0001` | 样箱反馈记录 | `SBF-GH-202606-0001` | missing / partial / candidate / verified_by_human |
| `QER-GH-YYYYMM-0001` | 质量证据记录 | `QER-GH-202606-0001` | missing / partial / candidate / release_unconfirmed |
| `POD-GH-YYYYMM-0001` | 发货与 POD 记录 | `POD-GH-202606-0001` | missing / delivery_planned / candidate / signed_by_source |
| `FEI-GH-YYYYMM-0001` | 金融凭证脱敏索引 | `FEI-GH-202606-0001` | index_only / invoice_statistical / cash_received_candidate |
| `WGR-GH-YYYYMM-0001` | WAES 门禁记录 | `WGR-GH-202606-0001` | governance_recorded / blocked / manual_confirmation_required / committee_review_required |
| `AIS-GH-SOP-YYYYMM-0001` | AI SOP 建议 | `AIS-GH-SOP-202606-0001` | suggestion_only / pending_human_review / rejected / approved_for_use |
| `DRC-BIZ-GH-YYYYMM-0001` | 正式运营准备候选 | `DRC-BIZ-GH-202606-0001` | candidate / manual_review / committee_review / not_allowed |
| `KGR-GH-YYYYMM-0001` | 知识缺口请求 | `KGR-GH-202606-0001` | open / bounty_candidate / fulfilled_candidate / closed_by_human |
| `KGB-GH-YYYYMM-0001` | 知识缺口悬赏候选 | `KGB-GH-202606-0001` | draft / frozen / submitted / disputed / settled_by_committee |

## 5. 预运营期订单核心字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| `objectId` | 是 | 预运营期订单候选编号，使用 `POO-GH-*`。 |
| `sourceProject` | 是 | 所属项目，默认 `葛化 GFIS 第一阶段`。 |
| `sourceUnit` | 是 | 提交或记录单位，如葛化、湖北磷材、辽宁远航、现代精工或项目组。 |
| `demandSourceRefs` | 是 | 需求来源编号，至少一个 `DSR-GH-*`。 |
| `demandSourceType` | 是 | phone / meeting / email / chat / third_party / platform / document。 |
| `customerNameOrAlias` | 是 | 客户名称或受控别名；DSR-L2/DSR-L3 场景可只记录脱敏别名。 |
| `productCategory` | 是 | 产品类别，例如中空板、周转箱、包装制品或其他绿色供应链产品。 |
| `productSpec` | 条件必填 | 规格、材质、尺寸、颜色、克重、质量标准等；未知时记录缺口。 |
| `quantity` | 条件必填 | 数量或预估量；未知时记录为 `pending_quantity`。 |
| `targetDeliveryDate` | 条件必填 | 目标交期或需求窗口。 |
| `orderStage` | 是 | 固定为 `pre_operation_candidate`，不得写成 formal_order。 |
| `targetFactory` | 是 | 目标工厂，如葛化工厂或未来复制工厂。 |
| `oemCarrier` | 条件必填 | 预运营期承接生产的 OEM 单位，如现代精工或其他承接方。 |
| `responsibilitySplit` | 是 | 目标工厂、OEM、销售/渠道、质量、发货、财务各自责任边界。 |
| `quoteRefs` | 条件必填 | 报价、要约、价格说明或商务沟通引用。 |
| `customerConfirmationRefs` | 条件必填 | 客户确认来源；缺失时订单不得升级。 |
| `sampleBoxRefs` | 条件必填 | 样箱、签样、测试反馈或缺口编号。 |
| `qualityRefs` | 条件必填 | 质量检验、放行或缺口编号。 |
| `deliveryRefs` | 条件必填 | 发货计划、发货单、承运记录或缺口编号。 |
| `podRefs` | 条件必填 | 签收、POD 或缺口编号。 |
| `financeIndexRefs` | 条件必填 | 开票、到账、应收或凭证脱敏索引；不得暴露敏感原文。 |
| `waesGateRefs` | 是 | WAES 规则记录、阻断或人工确认记录。 |
| `kdsPoolRefs` | 是 | 底座 11 池挂接编号。 |
| `classificationLevel` | 是 | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3。 |
| `trustLevel` | 是 | T0 / T1 / T2 / T3。 |
| `confirmationStatus` | 是 | source_captured / candidate_registered / evidence_collecting / human_review_pending / committee_review_pending / verified_by_human / blocked。 |
| `revenueStatus` | 是 | no_revenue / invoice_statistical_only / cash_received_pending / cash_received_confirmed_by_human。 |
| `potentialValueStatus` | 是 | none / potential_value_candidate / potential_value_review / formal_value_not_allowed / formal_value_confirmed_by_committee。 |
| `gfisWriteMode` | 是 | no_write / candidate_only / manual_entry_after_confirmation / blocked。 |
| `forbiddenOperations` | 是 | 不允许自动执行的写入、放行、结算、分配或状态升级。 |
| `nextAction` | 是 | 下一步补证、人工确认、委员会、评测或阻断动作。 |
| `ownerRole` | 是 | 当前责任角色。 |
| `loopEvidenceRefs` | 是 | 关联 LOOP 轮次、文档或证据路径。 |

## 6. 状态机

```text
source_captured
  -> candidate_registered
  -> evidence_collecting
  -> waes_recorded_or_blocked
  -> human_review_pending
  -> committee_review_pending(optional)
  -> ready_for_formal_operation_candidate
  -> formal_operation_allowed_by_human
```

异常状态：

| 状态 | 触发条件 | 处理 |
|---|---|---|
| `evidence_missing` | 无需求来源、无客户确认、无质量/POD/金融索引或责任主体不明 | 生成 `KGR-GH-*` 缺口请求 |
| `waes_blocked` | 超出规则、缺证、越权、跨单位争议或密级不符 | 进入 WAES 阻断或人工确认 |
| `committee_review_required` | 收益、积分、重大违规、潜在产值转正式产值、跨单位权益争议 | 进入委员会 DecisionRecord |
| `rejected` | 来源不合格、证据伪造、密级违规或事实冲突 | 停止向后升级，按违规规则处理 |
| `archived_candidate` | 长期无补证或项目终止 | 保留追溯，不删除 |

正式运营候选的最低条件：

1. 至少一个合格需求来源。
2. 至少一个客户确认或客户确认缺口的人工处理结论。
3. OEM 与目标工厂事实责任已区分。
4. 质量、发货、POD、金融凭证至少形成可追溯索引或明确缺口。
5. WAES 规则记录或阻断记录完整。
6. GFIS 写入模式仍为 no_write / candidate_only，除非人工确认允许手工录入。
7. LOOP 证据链和 KDS 本地镜像已记录。

## 7. 单据与 GFIS 映射

| 资料或事件 | GFIS 候选落点 | 必要证据 | 禁止写法 |
|---|---|---|---|
| 需求来源 | 客户、项目、附件、需求登记候选 | 电话纪要、会议纪要、邮件、聊天、第三方介绍或平台线索 | 写成正式订单 |
| 报价或要约 | 报价单、销售订单候选 | 报价原件、版本、责任人、客户反馈 | 写成客户已确认订单 |
| 客户确认 | 客户确认附件、合同链候选 | 采购订单、确认函、邮件确认、签章件或平台回执 | 用口述或 AI 总结替代确认 |
| OEM 承接 | 工单、作业卡、生产记录候选 | 承接单位、产线、批次、时间、责任人 | 写成葛化自建工厂已投产 |
| 样箱反馈 | 打样、签样、质量检查候选 | 样箱编号、签收、测试反馈、问题闭环 | 无编号仍通过 |
| 质量证据 | 质量检验、放行候选 | 检验对象、指标、结果、人员、时间 | 直接确认质量放行 |
| 发货/POD | 发货单、承运、POD 候选 | 发货单、承运记录、签收主体、签收时间 | 只有发货计划就确认交付 |
| 金融凭证 | 凭证脱敏索引、应收、开票/到账引用 | 保管人、凭证类型、开票状态、到账状态 | 将开票统计写成收入到账 |
| WAES 门禁 | 规则记录、阻断、人工确认 | 规则编号、状态、责任方 | 写成业务主账 |
| KDS 记录 | 知识对象、缺口、SOP 建议 | 来源、证据、状态、编号 | 写成真实 KDS API 回执 |

## 8. 底座 11 池挂接

| 底座池 | 预运营期订单挂接 |
|---|---|
| 订单池 | `POO-GH-*`、报价、客户确认、订单缺口。 |
| 产能池 | 目标工厂产能、OEM 承接产能、预运营期产能调度。 |
| 数据池 | 需求、证据、候选事实、台账、LOOP 记录和 RAG 准入状态。 |
| 资金池 | 开票统计、到账候选、正式到账确认、收益池入口。 |
| 物流池 | 发货计划、承运、POD、异常签收。 |
| 原料池 | PP、改性料、供应商、批次、价格和质量证据。 |
| 设备池 | 目标工厂设备、OEM 产线、工艺能力。 |
| 人才池 | 录入人、责任人、审核人、委员会成员和外部专家。 |
| 政策池 | 权威政策、标准、法规和 T3 来源。 |
| 能源池 | 绿色供应链能耗、节能、碳相关证据候选。 |
| 场景池 | 葛化母版、湖北磷材复制、新工厂项目和区域绿色供应链场景。 |

## 9. AI SOP 建议格式

AI 从候选事实生成 SOP 建议时，必须使用以下结构：

| 字段 | 说明 |
|---|---|
| `suggestionId` | `AIS-GH-SOP-*` |
| `sourceCandidateRefs` | `DSR-GH-*`、`POO-GH-*`、`QTE-*`、`OEM-*` 等来源 |
| `targetSopStage` | 需求、报价、客户确认、OEM、样箱、生产、质量、发货、POD、金融、正式运营准备 |
| `inputFields` | SOP 进入前字段 |
| `outputFields` | SOP 输出字段 |
| `requiredEvidence` | 必要附件、原始凭证或脱敏索引 |
| `waesGate` | governance_recorded / blocked / manual_confirmation_required / committee_review_required |
| `gfisActionMode` | no_write / guided_manual_entry / blocked |
| `kdsWritebackCandidate` | 是否形成 KDS 候选写回 |
| `humanConfirmationRequired` | 默认 true |
| `committeeRequired` | 只有收益、重大违规、潜在产值转正式产值或跨单位争议时为 true |
| `forbiddenOperations` | 禁止自动写入、确认、结算、分配或升级状态 |

## 10. 收入、产值与积分口径

| 项 | 口径 |
|---|---|
| 正式收入 | 以到账为准，进入收益池需要人工或委员会确认。 |
| 开票 | 只作为统计和财务过程口径，不等于收益池正式收入。 |
| 产值积分 | 有实际收入的事项才能列入产值贡献。 |
| 潜在产值 | 可积累潜在产值贡献，但转正式产值必须确认或委员会处理。 |
| 知识积分 | 无实际收入的有效资料、补证、SOP 建议、知识缺口解决只能先计知识贡献。 |
| AI 额度 | 合作单位自购额度先自用，不进入统一收益池；贡献、共享、奖励额度需单独计量。 |
| 知识缺口悬赏 | 只在发布条件、冻结资源、验收标准、争议路径齐备后进入悬赏候选。 |

## 11. RAG 与可见范围

| 数据状态 | RAG 准入 | 可见范围 |
|---|---|---|
| `controlled_source` | safe | 按密级和授权可用于问答和 SOP 建议 |
| `candidate_registered` | limited | 只能用于提示缺口、候选答案和下一步建议 |
| `evidence_collecting` | repair | 不进入强引用，只可作为补证任务 |
| `waes_blocked` | blocked | 不可用于 RAG 调用 |
| `committee_review_required` | blocked | 委员会结论前不可下游调用 |
| `DSR-L3` | blocked_by_default | 默认不进入开放问答，只能用脱敏索引 |

## 12. 红线

本母版明确禁止：

1. 把需求线索、报价、会议纪要、AI 总结或本地镜像写成正式客户订单。
2. 把 OEM 承接生产写成葛化自建工厂已投产。
3. 把开票统计写成到账收入。
4. 把文档验收通过写成业务事实成立。
5. 把 KDS 本地镜像写成真实 KDS API 已同步。
6. 把 WAES 规则记录写成业务主账或最终裁决。
7. 自动确认积分、收益、悬赏、违规扣减或争议处理。
8. 自动生成或写入 GFIS 正式订单、工单、质量放行、POD、金融凭证或正式运营状态。
9. 自动输出 `accepted`、`complete` 或 `integrated` 状态升级。

## 13. 第一阶段执行清单

| 优先级 | 动作 | 产物 | 门禁 |
|---|---|---|---|
| P0 | 将本母版纳入 GFIS 使用助手 | `GUA-GH-002`、`GUA-GH-007` 的字段和状态机 | 评测通过，不写主账 |
| P0 | 建立预运营期订单样例空白记录 | `POO-GH-*` 空白模板 | 只填字段结构，不填真实业务事实 |
| P0 | 建立辽宁远航链路映射 | `DSR-GH-*`、`QTE-GH-LY-*`、`KGR-GH-*` | 缺客户确认时阻断升级 |
| P0 | 建立现代精工 OEM 责任拆分 | `OEM-GH-MJ-*` | 不写成目标工厂已投产 |
| P0 | 建立质量/发货/POD/金融索引门禁 | `QER-GH-*`、`POD-GH-*`、`FEI-GH-*` | 缺证只形成缺口 |
| P1 | 生成湖北磷材复制差异项 | HBLC 预运营期订单差异清单 | 以葛化母版为标准母版 |
| P1 | 建立知识缺口悬赏前置门禁 | `KGB-GH-*` 草案 | 未冻结资源不发布 |

## 14. Definition of Done

本文完成的 DoD：

1. 明确“预运营期订单”名称、对象链、统一编号、字段、状态机和红线。
2. 区分目标工厂和 OEM 承接方事实责任。
3. 明确 GFIS、KDS、WAES、RAG、底座 11 池和收益积分的映射边界。
4. 保持所有业务事实为候选、缺口或待确认状态。
5. 纳入 DKS-049 LOOP 记录、文档控制和 KDS 本地镜像。

本文未完成也不声明：

1. 真实订单、客户确认、质量放行、POD、到账或收益成立。
2. GFIS AI 助手已部署或评测通过。
3. GFIS 主账、WAES、KDS API、GPC、PVAOS、Finance 或生产系统已写入。
4. 委员会已裁决或人工已确认。
