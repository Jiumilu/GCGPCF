---
doc_id: GPCF-DOC-E361BE8080
title: GlobalCloud 葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包

日期：2026-06-19
轮次：`GPCF-KDS-DKS-052`
状态：`controlled_blank_submission_pack`

## 1. 定位

本文承接 DKS-051，把辽宁远航补证请求包和金融凭证脱敏索引转为责任方可填写、人工可验收、WAES 可记录、委员会可备案的空白填报包。

本文只定义填报字段、接收条件、退回条件、验收动作和候选写回边界，不证明任何真实资料已经收到，不证明客户确认、采购订单、合同、质量、POD、开票、到账、金融凭证、积分、收益、悬赏或 GFIS 运行层事实已经成立。

## 2. 输入依据

| 来源 | 关键结论 | 本文使用方式 |
|---|---|---|
| DKS-051 专项台账 | `KSP-GH-LY-D051-001` 与 `FEI-GH-D051-001` 已定义字段骨架 | 转为可填报空白包 |
| 辽宁远航缺口草案 | 客户确认、样箱反馈、OEM 事实、质量、POD、金融凭证均为 candidate | 保持验收和悬赏前置门禁 |
| 葛化订单运行母版 | 预运营期订单不得写成正式订单；金融凭证使用 `FEI-GH-*` | 约束编号、状态和禁写 |
| GFIS evidence | `customer_confirmations=0`、`purchase_orders=0`、`runtime_ready=0`、`verified=0` | 作为不得释放运行层的依据 |
| GFIS evidence | 12 个运行对象、62 个凭证槽位仍缺责任方响应 | 作为补证包必填来源 |
| 积分收益规则 | 到账才进入正式收益池；开票只作统计和财务过程口径 | 约束积分、收益和产值字段 |

## 3. 本轮对象

| objectId | 对象 | 来源缺口 | 当前状态 | 目标状态 |
|---|---|---|---|---|
| `KSP-GH-LY-D052-001` | 辽宁远航补证请求包 | `KGR-GH-D050-LY-001`, `KGR-GH-LY-202606-0001` | blank_submission_pack | waiting_source |
| `FEI-GH-D052-001` | 金融凭证 DSR-L3 脱敏索引填报表 | `KGR-GH-D050-FIN-001`, `KGR-GH-FIN-202606-0001` | blank_index_pack | index_requested |
| `HRC-GH-D052-001` | 人工确认队列候选 | `KGR-GH-D051-HUMAN-001` | queue_candidate | pending_human_assignment |
| `WGR-GH-D052-001` | WAES 门禁记录候选 | 本轮两个填报包 | gate_candidate | governance_recorded_or_blocked_pending |

## 4. 辽宁远航补证请求包

填报包编号：`KSP-GH-LY-D052-001`

| 字段 | 必填 | 填报值 | 验收口径 | 未填处理 |
|---|---:|---|---|---|
| `submissionPackageId` | 是 | `KSP-GH-LY-D052-001` | 固定编号 | returned_for_id |
| `submitterUnit` | 是 | 待填 | 提交单位或受控别名 | returned_for_owner |
| `submitterPersonOrRole` | 是 | 待填 | 提交人、岗位或授权角色 | returned_for_owner |
| `sourceAuthenticityStatement` | 是 | 待填 | 提交方声明来源真实性和完整性 | returned_for_statement |
| `linkedQuoteRef` | 是 | 待填 | 报价编号、报价 PDF 元数据或报价来源索引 | returned_for_quote_source |
| `customerConfirmationRef` | 是 | 待填 | 客户确认函、采购订单、合同、平台订单回执或等效正式确认原件索引 | customer_confirmation_missing |
| `purchaseOrderOrContractRef` | 条件必填 | 待填 | 有采购订单或合同时必须填脱敏索引 | returned_for_contract_index |
| `sampleBoxFeedbackRefs` | 条件必填 | 待填 | 样箱编号、签收、测试反馈或问题记录 | returned_for_sample_feedback |
| `qualityEvidenceRefs` | 条件必填 | 待填 | 质量报告、检验记录、放行或质量缺口 | returned_for_quality |
| `deliveryEvidenceRefs` | 条件必填 | 待填 | 发货单、承运记录、发货计划或缺口 | returned_for_delivery |
| `podRefs` | 条件必填 | 待填 | 签收主体、签收时间、POD 原件或脱敏索引 | returned_for_pod |
| `financeIndexRefs` | 条件必填 | 待填 | `FEI-GH-*` 脱敏索引或金融缺口编号 | returned_for_finance_index |
| `targetFactory` | 是 | 待填 | 葛化目标工厂或复制工厂 | returned_for_factory |
| `oemCarrier` | 条件必填 | 待填 | 现代精工或其他预运营期承接方 | returned_for_oem |
| `responsibilitySplit` | 是 | 待填 | 目标工厂、OEM、销售、质量、发货、财务责任边界 | returned_for_responsibility |
| `classificationLevel` | 是 | 待填 | DSR-L1 / DSR-L2 / DSR-L3 | returned_for_classification |
| `visibleScope` | 是 | 待填 | project / directed / private / committee_only | returned_for_access |
| `waesGateExpected` | 是 | 待填 | governance_recorded / blocked / manual_confirmation_required | returned_for_waes_gate |
| `gfisWriteMode` | 是 | `candidate_only` | 不允许自动写 GFIS 主账 | blocked_if_formal_write |
| `kdsPoolRefs` | 是 | 订单池、物流池、资金池、数据池、场景池 | 必须挂接底座 11 池 | returned_for_pool_mapping |
| `forbiddenClaimsAccepted` | 是 | 待填 | 提交方确认不得声明业务完成 | returned_for_redline_ack |

## 5. 辽宁远航接收判定

| 判定 | 条件 | 后续动作 | 禁止动作 |
|---|---|---|---|
| `received_for_structure_check` | 必填字段齐全，且未暴露 DSR-L3 原文 | 进入结构验收 | 不进入 GFIS runtime intake |
| `returned_for_evidence` | 缺客户确认、责任主体、POD、质量或来源真实性声明 | 退回责任方补证 | 不计积分，不发布悬赏 |
| `metadata_only_required` | 涉及合同、金融、敏感客户或金额 | 改为脱敏索引或线下封存 | 不进入普通问答 |
| `manual_review_pending` | 结构合格但需人工确认业务适用性 | 进入人工确认队列 | 不形成正式业务事实 |
| `committee_review_required` | 争议、潜在产值转正式产值、跨单位权益、重大违规 | 进入委员会备案或裁决 | 不由 AI 或 WAES 单独裁决 |

## 6. 金融凭证脱敏索引填报表

索引编号：`FEI-GH-D052-001`

| 字段 | 必填 | 填报值 | 验收口径 | 未填处理 |
|---|---:|---|---|---|
| `financeEvidenceIndexId` | 是 | `FEI-GH-D052-001` | 固定编号 | returned_for_id |
| `linkedOrderCandidateRefs` | 条件必填 | 待填 | `POO-GH-*`、`QTE-GH-LY-*` 或缺口编号 | returned_for_linked_object |
| `linkedGapIds` | 是 | `KGR-GH-D050-FIN-001`, `KGR-GH-FIN-202606-0001` | 固定关联 | returned_for_gap |
| `evidenceType` | 是 | 待填 | invoice / receipt / bank_record / receivable / payment_plan / other | returned_for_type |
| `sourcePartyAlias` | 是 | 待填 | 来源单位或受控别名 | returned_for_source_party |
| `custodianRole` | 是 | 待填 | 财务负责人、资料保管人或线下封存责任人 | returned_for_custodian |
| `redactionStatus` | 是 | metadata_only | DSR-L3 默认 metadata_only 或 sealed_offline | governance_blocked |
| `classificationLevel` | 是 | DSR-L3 | 降密必须人工或委员会备案 | blocked_by_classification |
| `visibleScope` | 是 | private / finance_only / committee_only | 默认非公开 | returned_for_access |
| `invoiceStatus` | 是 | no_invoice / invoice_statistical / invoice_pending_review | 开票只作统计和财务过程口径 | returned_for_invoice_status |
| `cashReceivedStatus` | 是 | no_cash_received / cash_received_candidate / cash_received_confirmed_by_human | 到账需人工确认 | returned_for_cash_status |
| `amountVisibility` | 是 | hidden / range_only / finance_private / committee_only | 普通问答不可见 | returned_for_visibility |
| `accountInfoRedacted` | 是 | true | 必须脱敏 | governance_blocked |
| `sourceHashOrOfflineSeal` | 条件必填 | 待填 | hash、封存编号或线下保管索引 | returned_for_seal |
| `storageLocationIndex` | 是 | 待填 | 受控位置或封存索引，不写原文 | returned_for_storage |
| `humanReviewer` | 是 | 待确认 | 授权财务或人工复核人 | pending_human_assignment |
| `waesGateExpected` | 是 | manual_confirmation_required / committee_review_required | 金融凭证默认需人工或委员会 | returned_for_waes_gate |
| `forbiddenUsesAccepted` | 是 | 待填 | 不确认到账、不进入收益分配、不开放问答 | returned_for_redline_ack |

## 7. 金融凭证接收判定

| 判定 | 条件 | 后续动作 | 禁止动作 |
|---|---|---|---|
| `index_received_for_structure_check` | 只提交元数据、脱敏摘要或封存索引 | 进入结构验收 | 不打开原文，不公开金额 |
| `governance_blocked` | 暴露账户、敏感金额、未授权原文或缺保管责任 | 阻断并退回 | 不进入 RAG，不计收益 |
| `manual_confirmation_required` | 索引结构合格但需财务责任人确认 | 进入人工确认队列 | 不确认到账 |
| `committee_review_required` | 涉及收益分配、争议、重大违规或潜在产值转正式产值 | 进入委员会 | 不由 AI 结算 |
| `index_usable_for_candidate` | 人工确认索引可用于候选问答 | 只可回答补证路径和状态 | 不输出敏感字段 |

## 8. 人工确认队列候选

队列编号：`HRC-GH-D052-001`

| queueItemId | 来源对象 | 人工角色 | 必须确认事项 | 当前状态 |
|---|---|---|---|---|
| `HRC-GH-D052-LY-001` | `KSP-GH-LY-D052-001` | 项目负责人 / 订单责任方 | 客户确认来源、责任主体、目标工厂和 OEM 责任拆分 | pending_human_assignment |
| `HRC-GH-D052-QPOD-001` | `KSP-GH-LY-D052-001` | 质量 / 发货 / POD 责任人 | 质量、发货、POD 是否有可追溯索引 | pending_human_assignment |
| `HRC-GH-D052-FIN-001` | `FEI-GH-D052-001` | 财务责任人 | 金融凭证保管、脱敏、可见范围、开票/到账状态 | pending_human_assignment |
| `HRC-GH-D052-WAES-001` | `WGR-GH-D052-001` | WAES 规则记录人 | 规则内记录、阻断或人工确认要求 | pending_human_assignment |

人工确认队列只代表待确认事项，不代表已派发、已签认或已通过。

## 9. 委员会触发条件

| triggerId | 触发事项 | 决策对象 | 当前状态 |
|---|---|---|---|
| `CRC-GH-D052-REV-001` | 到账收入、收益池分配、贡献比例 | DecisionRecord / SettlementRecord | not_triggered |
| `CRC-GH-D052-PV-001` | 潜在产值转正式产值 | PotentialValueRecord / DecisionRecord | not_triggered |
| `CRC-GH-D052-DSP-001` | 跨单位权益、密级、可见范围或证据权属争议 | DisputeCase / AccessDecision | not_triggered |
| `CRC-GH-D052-VIO-001` | 重大违规、证据失真、泄密或追溯扣减 | ViolationRecord / DecisionRecord | not_triggered |
| `CRC-GH-D052-KGB-001` | 悬赏发布、资源冻结、验收结算争议 | KnowledgeGapBounty / BountySettlement | not_triggered |

委员会按多数决形成备案或裁决。用户保留治理权和急停权，不承担日常裁决。

## 10. 候选写回与 SOP 输入

| candidateId | 来源对象 | 目标 | 写回模式 | 当前状态 |
|---|---|---|---|---|
| `WBC-GH-D052-LY-001` | `KSP-GH-LY-D052-001` | KDS / GFIS | candidate_only / no_write | planned_candidate |
| `WBC-GH-D052-FIN-001` | `FEI-GH-D052-001` | KDS / WAES | metadata_only / pending_confirmation | planned_candidate |
| `AIS-GH-SOP-D052-LY-001` | `KSP-GH-LY-D052-001` | 辽宁远航补证 SOP | suggestion_only | planned_candidate |
| `AIS-GH-SOP-D052-FIN-001` | `FEI-GH-D052-001` | 金融凭证脱敏索引 SOP | suggestion_only | planned_candidate |

候选写回不得自动进入 GFIS 主账、WAES 主账、真实 KDS API、GPC、PVAOS、Finance 或生产系统。SOP 输入只能作为建议，必须经人工或委员会确认后才能采用。

## 11. 积分、收益、额度和悬赏边界

| 项 | DKS-052 口径 |
|---|---|
| 知识积分 | 填报包结构、脱敏索引、补证材料可形成候选知识贡献，确认积分为 0 |
| 产值积分 | 没有到账不得进入正式产值积分 |
| 潜在产值积分 | 可在客户确认或业务机会可追踪后形成候选，转正式必须人工或委员会确认 |
| AI 额度 | 合作单位自购额度先自用，不进入统一收益池 |
| 收益池 | 到账后才进入正式收益池；开票只作统计和财务过程口径 |
| 悬赏 | `KGB-*` 仍为候选，未冻结资源不得发布 |
| 争议 | 贡献比例、收益、密级、可见范围、违规扣减必须进委员会 |

## 12. DSR 与 RAG 安全

| 数据 | DSR | RAG 状态 | 可用范围 |
|---|---|---|---|
| 报价来源元数据 | DSR-L2 | limited | 仅回答来源、缺口和补证路径 |
| 客户确认索引 | DSR-L2 / DSR-L3 | limited / blocked_by_default | 需授权角色 |
| POD / 质量脱敏索引 | DSR-L2 | limited | 项目授权范围 |
| 金融凭证索引 | DSR-L3 | blocked_by_default | 财务、委员会或授权角色 |
| WAES 门禁记录 | DSR-L1 / DSR-L2 | safe / limited | 只显示规则状态和下一步 |

## 13. 完成定义

本轮完成表示：

1. 辽宁远航补证请求包具备可填写字段、接收判定、人工确认队列和委员会触发条件。
2. 金融凭证脱敏索引具备 DSR-L3 字段、接收判定、保管责任、可见范围和 WAES 门禁。
3. 候选写回、候选 SOP、积分、收益、额度和悬赏均有状态和禁写边界。
4. 文档进入 LOOP 记录、文档控制和 KDS 本地镜像。

本轮不表示：

1. 任何真实资料、客户确认、采购订单、合同、POD、质量、开票、到账或金融凭证已经收到。
2. 任何人工确认、委员会裁决、悬赏发布、积分确认或收益分配已经完成。
3. GFIS、WAES、KDS API、GPC、PVAOS、Finance 或生产系统已经写入。
4. GFIS `real_business_lane=repair_required` 已关闭。
5. 本专题可以升级为 `accepted`、`complete` 或 `integrated`。

## 14. 下一轮建议

建议 `GPCF-KDS-DKS-053` 进入“葛化 DKS-052 填报包 dry-run 验收与人工确认队列视图”，使用虚拟脱敏样例验证：

1. 缺客户确认时是否正确退回。
2. 金融凭证暴露敏感字段时是否正确阻断。
3. 人工确认队列和委员会触发条件是否完整。
4. 候选写回和候选 SOP 是否仍保持 no_write / suggestion_only。
