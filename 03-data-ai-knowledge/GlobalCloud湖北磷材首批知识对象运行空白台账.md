---
doc_id: GPCF-DOC-BA9F35E2AA
title: GlobalCloud 湖北磷材首批知识对象运行空白台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材首批知识对象运行空白台账.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材首批知识对象运行空白台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材首批知识对象运行空白台账

日期：2026-06-17  
状态：`planned_empty_ledger`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-019、DKS-022 和 DKS-029 的结构，将湖北磷材第一阶段的拓厂项目知识库、原料/行业/订单知识库和新工厂复制模板转成可填报、可评分、可追责、可挂接 KDS 11 底座池的首批知识对象运行空白台账。

本文只建立空白运行记录和候选对象编号，不表示：

- 湖北磷材已经提交真实资料；
- 拓厂项目已经通过评估；
- 原料、供应商、价格、订单、合同、POD、到账或收益已经确认；
- GFIS 深度运行已经启动；
- 新工厂复制模板已经生效；
- 悬赏、积分、收益或 AI 额度已经确认或分配；
- 已完成真实 KDS API、WAES API 或业务系统写入。

## 2. 总边界

| 边界 | 当前规则 |
|---|---|
| GFIS 深度 | 第一阶段不做，只记录未来接入 readiness |
| 资料状态 | 默认 `candidate` 或 `waiting_source` |
| AI 输出 | 只允许生成候选事实、候选 SOP、候选积分、候选写回建议 |
| KDS 11 池 | 所有对象必须至少挂接一个底座资源池 |
| 增强账本 | 只能作为挂接账本，不得游离存在 |
| 收入口径 | 到账前不得进入正式收入；开票只作统计和财务过程口径 |
| 自购额度 | 自购 AI 额度先自用，可计量但不进入统一收益池 |
| 确认机制 | WAES 记录规则，人工确认事实，委员会处理积分、收益、悬赏、争议和重大违规 |

## 3. PilotSession 台账

| pilotSessionId | pilotScope | pilotPhase | owner | participantRefs | allowedDataScope | restrictedDataScope | defaultStatus | waesGateStatus | kdsWritebackStatus | finalStatus |
|---|---|---|---|---|---|---|---|---|---|---|
| `PILOT-HBLC-KDS-202606-0001` | FEA / RAW / IND / ORD / TPL | knowledge_object_preparation | KDS / GPCF 治理负责人 | 湖北磷材项目组、平台治理、WAES、必要委员会 | 脱敏摘要、来源索引、公开政策标准、候选资料包、葛化母版结构 | DSR-L3 原文、供应商报价原文、客户订单原文、合同原文、未授权跨单位资料 | planned_empty_ledger | pending | candidate / no_write | planned |

## 4. 首批 KnowledgeObject 空白台账

| objectId | packageId | objectType | sourceType | sourceRefs | sourceParty | baseResourcePools | enhancedLedgerLinks | classificationLevel | trustLevel | confirmationStatus | responsibleSubject | waesGateRefs | reuseFromGH | gfisDepthStatus | revenueStatus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `HBLC-FEA-202606-0001` | `KPK-HBLC-FEA-202606-0001` | expansion_project | factory_expansion | TBD | 湖北磷材项目负责人待确认 | 装备池、产能池、政策池、数据池、场景池 | SOP 账本、贡献账本、积分池、悬赏池 | DSR-L1 / DSR-L2 | T0 | candidate | 待确认 | pending | structure_only | readiness_only | knowledge_only |
| `HBLC-RAW-202606-0001` | `KPK-HBLC-RAW-202606-0001` | raw_material_source | raw_material | TBD | 原料责任方待确认 | 原料池、数据池、资金池、场景池 | 贡献账本、积分池、悬赏池、争议池 | DSR-L1 / DSR-L2 / DSR-L3 | T0 | candidate | 待确认 | pending | no | not_applicable | knowledge_only |
| `HBLC-IND-202606-0001` | `KPK-HBLC-IND-202606-0001` | industry_source | industry | TBD | 行业资料责任方待确认 | 政策池、数据池、场景池 | 贡献账本、积分池、悬赏池 | DSR-L0 / DSR-L1 / DSR-L2 | T0 | candidate | 待确认 | pending | no | not_applicable | knowledge_only |
| `HBLC-ORD-202606-0001` | `KPK-HBLC-ORD-202606-0001` | order_lead | order_lead | TBD | 销售或渠道责任方待确认 | 订单池、资金池、原料池、数据池、场景池 | 潜在产值池、收益池、贡献账本、争议池 | DSR-L2 / DSR-L3 | T0 | candidate | 待确认 | pending | optional_structure | readiness_only | potential_value |
| `HBLC-TPL-202606-0001` | `KPK-HBLC-TPL-202606-0001` | factory_replication_template | factory_template | `GH-DKS-029` structure reference | KDS / Brain / 湖北磷材项目组 | 装备池、产能池、人才池、数据池、场景池 | SOP 账本、贡献账本、积分池、权限账本 | DSR-L1 / DSR-L2 | T1 | candidate | 待确认 | pending | structure_only | future_candidate | knowledge_only |

## 5. FactoryExpansionAssessment 空白台账

| assessmentId | expansionProjectRef | linkedObjectId | ghTemplateVersion | demandSourceEvidence | rawMaterialCoordination | industryPolicyFit | orderAndCustomerPotential | factoryReplicationFit | logisticsAndRegionFit | gfisReadiness | revenuePotential | evidenceCompleteness | waesGateStatus | assessmentStatus |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `FEA-HBLC-202606-0001` | TBD | `HBLC-FEA-202606-0001` | `GH-DKS-029` structure reference | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending | pending | planned |

评分只能用于候选拓厂机会排序和资源投入参考，不得作为自动投资、合作、接入、积分确认或收益分配依据。

## 6. KnowledgeSource 运行记录

| sourceRecordId | linkedObjectId | sourceCategory | sourceName | sourceRefs | sourceCaptureMode | trustedSourceLevel | usableForAI | redactionStatus | owner | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `KSO-HBLC-RAW-202606-0001` | `HBLC-RAW-202606-0001` | raw_material | TBD | TBD | document_or_meeting_summary | T0 | redacted_only | pending | 待确认 | waiting_source |
| `KSO-HBLC-IND-202606-0001` | `HBLC-IND-202606-0001` | industry | TBD | TBD | web_or_policy_source_index | T0 / T3 candidate | redacted_or_public | pending | 待确认 | waiting_source |
| `KSO-HBLC-ORD-202606-0001` | `HBLC-ORD-202606-0001` | order_lead | TBD | TBD | call_meeting_email_or_document_index | T0 | redacted_only | pending | 待确认 | waiting_source |

权威政策或标准网站可进入更高可信级别，但必须记录来源、检索时间、适用范围、引用片段边界和 WAES 规则记录。

## 7. ReplicationTemplateCandidate 台账

| templateCandidateId | linkedObjectId | sourceTemplate | reuseScope | requiredAdaptation | forbiddenReuse | outputType | waesGateStatus | status |
|---|---|---|---|---|---|---|---|---|
| `RTC-HBLC-TPL-202606-0001` | `HBLC-TPL-202606-0001` | 葛化母版结构 | 资料包结构、预运营期订单机制、知识缺口、悬赏、SOP 控制点 | 湖北磷材单位边界、原料场景、区域政策、产能和装备条件 | 不复用葛化未确认事实、客户资料、OEM 事实责任、金融凭证原文 | factory_replication_template_candidate | pending | planned |

## 8. GapAndBountyCandidate 台账

| gapCandidateId | linkedObjectId | gapType | gapSummary | requiredEvidence | suggestedBounty | bountyResourceFrozen | committeeRequired | kdsPoolMapping | status |
|---|---|---|---|---|---|---|---|---|---|
| `KGR-HBLC-FEA-202606-0001` | `HBLC-FEA-202606-0001` | project_source | 拓厂项目来源、区域条件、建设计划和审批条件缺口 | 目标区域、工厂条件、政策来源、项目负责人确认 | 知识积分或 AI 服务候选 | false | true | 装备池、产能池、政策池、数据池、场景池 | candidate |
| `KGR-HBLC-RAW-202606-0002` | `HBLC-RAW-202606-0001` | raw_material | 原料类别、供应商、行情、质量指标和采购线索缺口 | 原料来源索引、供应商脱敏摘要、质量或价格来源 | 知识积分候选 | false | true | 原料池、数据池、资金池、场景池 | candidate |
| `KGR-HBLC-IND-202606-0003` | `HBLC-IND-202606-0001` | industry_policy | 行业政策、标准、客户场景和高可信来源缺口 | 政策/标准来源、行业资料、适用范围 | 知识积分候选 | false | false | 政策池、数据池、场景池 | candidate |
| `KGR-HBLC-ORD-202606-0004` | `HBLC-ORD-202606-0001` | order_lead | 销售订单线索、报价、采购意向和潜在产值缺口 | 客户需求来源、报价或意向索引、责任主体 | 潜在产值贡献候选 | false | true | 订单池、资金池、原料池、数据池、场景池 | candidate |
| `KGR-HBLC-TPL-202606-0005` | `HBLC-TPL-202606-0001` | sop_template | 新工厂复制模板差异项、SOP 候选和复用边界缺口 | 葛化母版结构、HBLC 差异项、WAES 规则记录 | 知识积分或 SOP 贡献候选 | false | true | 装备池、产能池、人才池、数据池、场景池 | candidate |

候选悬赏不等于已发布悬赏。发布前必须明确发起主体、资源冻结、验收标准、可见范围、争议处理和委员会是否参与。

## 9. WritebackCandidate 台账

| writebackCandidateId | sourceObjectRefs | targetSystem | targetObjectType | writebackMode | allowedByPolicy | humanConfirmationRequired | sensitiveFieldsRedacted | writebackStatus |
|---|---|---|---|---|---|---|---|---|
| `WBC-HBLC-FEA-202606-0001` | `HBLC-FEA-202606-0001`, `FEA-HBLC-202606-0001` | KDS / WAES | ExpansionAssessmentCandidate | candidate_only | true | true | true | planned |
| `WBC-HBLC-RAW-202606-0001` | `HBLC-RAW-202606-0001`, `KSO-HBLC-RAW-202606-0001` | KDS | RawMaterialKnowledgeCandidate | candidate_only | true | true | true | planned |
| `WBC-HBLC-IND-202606-0001` | `HBLC-IND-202606-0001`, `KSO-HBLC-IND-202606-0001` | KDS / Brain | IndustryKnowledgePageCandidate | candidate_only | true | true | true | planned |
| `WBC-HBLC-ORD-202606-0001` | `HBLC-ORD-202606-0001`, `KSO-HBLC-ORD-202606-0001` | KDS / WAES | OrderLeadCandidate | candidate_only | true | true | true | planned |
| `WBC-HBLC-TPL-202606-0001` | `HBLC-TPL-202606-0001`, `RTC-HBLC-TPL-202606-0001` | KDS / Brain | FactoryReplicationTemplateCandidate | pending_confirmation | true | true | true | planned |

## 10. ContributionEventCandidate 台账

| contributionEventId | contributorRef | contributionType | sourceObjectRefs | pointType | candidatePoints | confirmedPoints | revenueRelated | revenueConfirmed | settlementRequired | decisionRecordRequired |
|---|---|---|---|---|---:|---:|---|---|---|---|
| `CEV-HBLC-FEA-202606-0001` | 湖北磷材项目来源提交方待确认 | project_source_submitter | `HBLC-FEA-202606-0001` | knowledge / potential_value | 待评估 | 0 | false | false | true | true |
| `CEV-HBLC-RAW-202606-0001` | 原料资料提交方待确认 | raw_material_source_submitter | `HBLC-RAW-202606-0001` | knowledge | 待评估 | 0 | false | false | false | true |
| `CEV-HBLC-IND-202606-0001` | 行业资料提交方待确认 | industry_source_submitter | `HBLC-IND-202606-0001` | knowledge | 待评估 | 0 | false | false | false | true |
| `CEV-HBLC-ORD-202606-0001` | 订单线索提交方待确认 | order_lead_submitter | `HBLC-ORD-202606-0001` | potential_value / channel | 待评估 | 0 | false | false | true | true |
| `CEV-HBLC-TPL-202606-0001` | 复制模板编制方待确认 | sop_template_contributor | `HBLC-TPL-202606-0001` | knowledge / reuse | 待评估 | 0 | false | false | true | true |

未到账事项只能记录为知识贡献、渠道贡献、潜在产值贡献或模板复用贡献候选。正式收益分配必须等待到账、规则、人工和委员会流程。

## 11. KDS 11 底座池挂接检查

| 对象 | 必挂底座池 | 当前状态 |
|---|---|---|
| `HBLC-FEA-202606-0001` | 装备池、产能池、政策池、数据池、场景池 | pass_for_template |
| `HBLC-RAW-202606-0001` | 原料池、数据池、资金池、场景池 | pass_for_template |
| `HBLC-IND-202606-0001` | 政策池、数据池、场景池 | pass_for_template |
| `HBLC-ORD-202606-0001` | 订单池、资金池、原料池、数据池、场景池 | pass_for_template |
| `HBLC-TPL-202606-0001` | 装备池、产能池、人才池、数据池、场景池 | pass_for_template |

## 12. 红线暂停规则

后续真实资料进入时，出现以下任一情形必须暂停相关对象：

- 把候选拓厂项目写成已通过投资或合作确认；
- 把原料线索、供应商摘要或价格线索写成采购事实；
- 把行业搜索或 AI 分析写成权威结论；
- 把订单线索、报价、会议或电话写成正式订单、合同、到账或收益；
- 把葛化母版未确认事实直接复制成湖北磷材事实；
- 把自购 AI 额度写入统一收益池；
- 未经确认直接确认积分、收益、扣罚、争议或 SOP 生效；
- 将 DSR-L3 原文进入普通 AI 问答或共享正文；
- 将本地 KDS 镜像写成真实 KDS API 已同步。

## 13. 完成定义

本台账完成条件：

1. 五类首批知识对象均具备统一编号。
2. 拓厂评估、知识源、复制模板、缺口、写回、贡献候选均有空白记录。
3. 所有对象保持候选、待来源、待评或待确认状态。
4. 所有增强账本均挂接 KDS 11 底座池。
5. 所有贡献确认值为 0。
6. 不生成真实订单、原料采购、投资、收益、POD、GFIS 深度运行或正式 SOP 生效事实。
7. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 14. DKS-031 建议

下一轮建议建立“湖北磷材拓厂评估与原料/行业/订单知识源评测集”，把本文五类对象转成可评分样本，覆盖：

- 拓厂项目来源完整性；
- 原料知识源可信度；
- 行业政策/标准来源可信级别；
- 订单线索潜在产值与禁止声明；
- 葛化母版复制边界；
- KDS 11 池挂接和增强账本合规性。
