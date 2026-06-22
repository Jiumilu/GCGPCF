---
doc_id: GPCF-DOC-52D30A36F6
title: GlobalCloud 绿色供应链分布式知识系统对象字段与 11 池映射清单
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链分布式知识系统对象字段与 11 池映射清单

日期：2026-06-20
轮次：`GPCF-KDS-DKS-059`
状态：`controlled_object_field_pool_mapping`

## 1. 状态边界

本文定义 P0 阶段最小对象字段、统一编号、状态机和 KDS 11 池挂接规则。本文不创建正式数据库表，不写真实 API，不确认业务事实，不确认积分、收益、额度、悬赏或争议。

## 2. 统一编号规则

| 前缀 | 对象 | 示例 | 默认状态 |
|---|---|---|---|
| `KNO` | KnowledgeObject | `KNO-GH-202606-0001` | `candidate` |
| `SRC` | SourceRecord | `SRC-HBLC-202606-0001` | `registered` |
| `EVD` | EvidenceRecord | `EVD-GH-LY-202606-0001` | `candidate` |
| `AST` | AssistantOutputRecord | `AST-GH-KQA-202606-0001` | `candidate_output` |
| `EVL` | EvalRecord | `EVL-GH-KQA-202606-0001` | `pending_eval` |
| `DFT` | DefectRecord | `DFT-GH-AST-202606-0001` | `open` |
| `FAC` | FactCandidate | `FAC-GH-LY-202606-0001` | `candidate` |
| `SOP` | SOPCandidate | `SOP-GH-POO-202606-0001` | `suggestion_only` |
| `WBC` | WritebackCandidate | `WBC-GH-GFIS-202606-0001` | `no_write` |
| `DSR` | DemandSourceRecord | `DSR-GH-202606-0001` | `source_captured` |
| `POO` | PreOperationOrder | `POO-GH-202606-0001` | `pre_operation_candidate` |
| `OEM` | OEMResponsibilityRecord | `OEM-GH-MJ-202606-0001` | `responsibility_candidate` |
| `QER` | QualityEvidenceRecord | `QER-GH-202606-0001` | `metadata_only` |
| `POD` | DeliveryPODRecord | `POD-GH-202606-0001` | `metadata_only` |
| `FEI` | FinanceEvidenceIndex | `FEI-GH-202606-0001` | `sensitive_metadata_only` |
| `KGR` | GapRecord | `KGR-HBLC-RAW-202606-0001` | `open` |
| `KGB` | BountyRecord | `KGB-GH-LY-202606-0001` | `bounty_candidate` |
| `CTR` | ContributionRecord | `CTR-GH-KNO-202606-0001` | `candidate` |
| `REV` | RevenueRecord | `REV-GH-202606-0001` | `candidate` |
| `QUO` | QuotaRecord | `QUO-HBLC-202606-0001` | `registered` |
| `DEC` | DecisionRecord | `DEC-COM-202606-0001` | `draft` |
| `DSP` | DisputeRecord | `DSP-GH-202606-0001` | `open` |
| `RAG` | RAGAdmissionRecord | `RAG-KNO-GH-202606-0001` | `repair_required` |
| `WGR` | WAESGateRecord | `WGR-GH-202606-0001` | `pending` |

编号不得复用。候选对象被驳回、撤回或冻结后保留原编号，不删除。

## 3. 通用必填字段

所有对象至少包含：

| 字段 | 说明 |
|---|---|
| `objectId` | 统一编号 |
| `objectType` | 对象类型 |
| `sourceProject` | 葛化、湖北磷材、辽宁远航、现代精工、平台或项目组 |
| `sourceUnit` | 提交单位或责任单位 |
| `sourceRefs` | 来源编号、文档、会议、邮件、系统记录、权威网站或人工确认引用 |
| `evidenceRefs` | 证据编号、哈希、附件索引或受控原件位置 |
| `basePoolRefs` | 至少一个 KDS 底座池 |
| `enhancedLedgerRefs` | 积分、收益、额度、悬赏、争议、贡献、SOP 等增强账本引用 |
| `classificationLevel` | `DSR-L0` / `DSR-L1` / `DSR-L2` / `DSR-L3` |
| `trustLevel` | `T0` / `T1` / `T2` / `T3` / `T4` / `T5` |
| `status` | 当前状态 |
| `confirmationStatus` | `candidate` / `human_review_pending` / `committee_review_pending` / `confirmed` / `rejected` |
| `waesGateRefs` | WAES 规则记录、阻断、人工确认或委员会路径 |
| `ragAdmission` | `safe` / `limited` / `repair_required` / `blocked` / `sensitive_metadata_only` |
| `responsibleSubject` | 责任主体 |
| `allowedOperations` | 当前允许动作 |
| `forbiddenOperations` | 禁止动作 |
| `promotionBlockers` | 不能升级的原因 |
| `nextAction` | 下一步 |
| `loopEvidenceRefs` | LOOP 记录或 Harness evidence |

## 4. 核心对象字段

| 对象 | 追加字段 | 说明 |
|---|---|---|
| KnowledgeObject | `title`、`summary`、`domainTags`、`validityWindow` | 统一知识主对象 |
| SourceRecord | `sourceType`、`capturedAt`、`capturedBy`、`sourceHash`、`originalLocation` | 来源登记 |
| EvidenceRecord | `evidenceType`、`hash`、`redactionStatus`、`custodian`、`verificationMethod` | 证据登记 |
| AssistantOutputRecord | `assistantType`、`promptVersion`、`questionOrInputRef`、`answerSummary`、`sourceCoverage` | 三件套输出 |
| EvalRecord | `evalSetId`、`score`、`redlineHit`、`expectedOutputRef`、`actualOutputRef` | 助手评测 |
| DefectRecord | `defectType`、`severity`、`owner`、`fixStatus`、`retestRef` | 缺陷 |
| FactCandidate | `factType`、`factText`、`confidence`、`requiredEvidence`、`writebackIntent` | 候选事实 |
| SOPCandidate | `targetStage`、`inputFields`、`outputFields`、`requiredEvidence`、`humanConfirmationRequired` | 候选 SOP |
| WritebackCandidate | `targetSystem`、`targetObject`、`writeMode`、`sandboxOnly`、`approvalRef` | 候选写回 |
| DemandSourceRecord | `demandSourceType`、`customerAlias`、`communicationRef`、`receivedAt` | 需求来源 |
| PreOperationOrder | `targetFactory`、`oemCarrier`、`productSpec`、`quantity`、`customerConfirmationRefs` | 预运营期订单 |
| OEMResponsibilityRecord | `targetFactoryResponsibility`、`oemResponsibility`、`qualityResponsibility`、`deliveryResponsibility` | OEM 责任拆分 |
| QualityEvidenceRecord | `qualityObjectRef`、`inspectionItems`、`resultStatus`、`releaseStatus` | 质量证据 |
| DeliveryPODRecord | `deliveryRef`、`carrierRef`、`signer`、`signedAt`、`podStatus` | 发货/POD |
| FinanceEvidenceIndex | `invoiceStatus`、`cashReceiptStatus`、`custodian`、`sealedOriginalRef` | 金融凭证索引 |
| GapRecord | `gapType`、`missingFields`、`priority`、`bountyEligible`、`requestOwner` | 知识缺口 |
| BountyRecord | `rewardType`、`frozenResourceRef`、`acceptanceCriteria`、`disputeWindow` | 悬赏 |
| ContributionRecord | `contributionType`、`candidatePoints`、`confirmedPoints`、`coefficientVersion` | 积分贡献 |
| RevenueRecord | `revenueType`、`invoiceRef`、`cashReceiptRef`、`allocationStatus` | 收益 |
| QuotaRecord | `quotaType`、`purchasedBy`、`scope`、`usageMeter`、`poolEntryAllowed` | AI 额度 |
| DecisionRecord | `decisionType`、`committeeRef`、`voteRule`、`decisionResult`、`filingRef` | 委员会决议 |
| DisputeRecord | `disputeType`、`claimants`、`frozenRefs`、`resolutionRef` | 争议 |
| RAGAdmissionRecord | `citationStrength`、`safeForDashboard`、`safeForAssistant`、`reasonCodes` | RAG 准入 |
| WAESGateRecord | `gateType`、`gateInputRef`、`gateResult`、`requiredActions`、`hardStop` | WAES 门禁 |

## 5. KDS 11 池定义

| 池 | 代码 | 覆盖对象 |
|---|---|---|
| 订单池 | `order_pool` | 需求、报价、订单、预运营期订单、客户确认、订单缺口 |
| 运力池 | `logistics_pool` | 发货、承运、POD、运输资源 |
| 产能池 | `capacity_pool` | 工厂、产线、OEM 承接、排产、产能调度 |
| 资金池 | `capital_pool` | 开票、到账、财务凭证、收益池 |
| 政策池 | `policy_pool` | 政策、标准、合规、权威来源 |
| 装备池 | `equipment_pool` | 设备、模具、产线、维护、工艺装备 |
| 数据池 | `data_pool` | 文档、证据、台账、报告、RAG、LOOP |
| 能源池 | `energy_pool` | 能耗、绿色能源、碳、节能资料 |
| 原料池 | `raw_material_pool` | 原料、供应商、价格、批次、质量 |
| 人才池 | `talent_pool` | 责任人、审核人、专家、委员会、岗位能力 |
| 场景池 | `scenario_pool` | 葛化母版、湖北磷材、拓厂、新工厂复制、区域运营 |

## 6. 功能域默认挂池

| 功能域 | 必挂池 | 可选池 |
|---|---|---|
| 葛化 GFIS 知识问答助手 | 数据池、场景池、人才池 | 订单池、产能池、政策池 |
| GFIS 使用助手 | 数据池、场景池、订单池 | 产能池、运力池、资金池 |
| GFIS 文档验收助手 | 数据池、人才池、场景池 | 订单池、资金池、政策池 |
| 候选事实与 SOP | 数据池、场景池 | 相关业务池 |
| 预运营期订单 | 订单池、产能池、数据池、场景池 | 运力池、资金池、原料池 |
| 辽宁远航链路 | 订单池、数据池、场景池 | 资金池、运力池、人才池 |
| 现代精工 OEM | 产能池、装备池、数据池、场景池 | 订单池、人才池 |
| 质量 / 发货 / POD | 数据池、订单池、运力池 | 资金池、场景池 |
| 金融凭证门禁 | 资金池、数据池 | 订单池、人才池 |
| 湖北磷材拓厂 | 装备池、产能池、政策池、数据池、场景池 | 能源池、资金池、人才池 |
| 原料 / 行业 / 订单知识 | 原料池、政策池、订单池、数据池 | 资金池、场景池 |
| 新工厂复制模板 | 场景池、产能池、装备池、数据池 | 政策池、人才池、能源池 |
| 积分 / 贡献 | 人才池、数据池、场景池 | 相关业务池 |
| 收益池 | 资金池、订单池、场景池 | 产能池、原料池、运力池 |
| AI 额度 | 资金池、数据池、人才池、场景池 | 订单池、政策池 |
| 悬赏 | 数据池、人才池、场景池 | 缺口对应业务池 |
| 委员会 / 争议 | 人才池、数据池、资金池、场景池 | 争议对应业务池 |
| RAG 准入 | 数据池、政策池、人才池 | 场景池、相关业务池 |

## 7. 状态机

通用状态机：

```text
draft
  -> candidate
  -> submitted
  -> waes_checked
  -> human_review_pending
  -> committee_review_pending
  -> confirmed
```

保护状态：

```text
candidate
  -> returned_for_evidence
  -> repair_required
  -> blocked
  -> frozen
  -> disputed
  -> rejected
  -> archived_candidate
```

业务写回状态机：

```text
no_write
  -> candidate_only
  -> sandbox_ready
  -> manual_confirmation_required
  -> approved_for_manual_entry
```

P0 阶段禁止进入 `approved_production_write`。

## 8. 来源与证据要求

| 来源类型 | 默认 trustLevel | 默认 RAG | 是否可成为正式事实 |
|---|---|---|---|
| 系统正式业务记录 / 到账记录 / 正式合同 | T0 | safe | 可，但需权限和核验 |
| 权威政策 / 标准网站 | T1 | safe 或 limited | 只能用于政策/标准事实 |
| 合作单位正式资料 | T2 | limited 或 safe | 需人工验收 |
| 会议 / 电话 / 邮件 / 飞书 / WIKI | T3 | repair_required | 只作线索或候选 |
| 网络搜索 / 第三方文章 | T4 | limited 或 repair_required | 不直接成为业务事实 |
| LLM 分析 | T5 | blocked | 不得作为事实 |

## 9. 禁止升级口径

对象字段完整不等于业务完成。若 `sourceRefs`、`evidenceRefs`、`waesGateRefs`、`confirmationStatus`、`responsibleSubject` 任一缺失，必须保持 `candidate`、`repair_required` 或 `blocked`。
