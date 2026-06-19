---
doc_id: GPCF-DOC-EE793CBD55
title: GlobalCloud 葛化辽宁远航与金融凭证缺口专项台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化辽宁远航与金融凭证缺口专项台账.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化辽宁远航与金融凭证缺口专项台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化辽宁远航与金融凭证缺口专项台账

日期：2026-06-19
轮次：`GPCF-KDS-DKS-051`
状态：`controlled_gap_special_register`

## 1. 定位

本文承接 DKS-050 的两个 P1 缺口，把辽宁远航报价链路和金融凭证门禁拆成可填报、可验收、可追溯、可形成知识缺口悬赏候选的专项台账。

本文只建立缺口、字段、责任、验收、门禁和候选 SOP 输入结构，不证明任何客户确认、采购订单、合同、样箱反馈、质量放行、POD、开票、到账、收益、积分、悬赏或 GFIS 运行层主账事实已经成立。

## 2. 输入依据

| 来源 | 关键结论 | 本文使用方式 |
|---|---|---|
| DKS-050 dry-run 评测 | `KGR-GH-D050-LY-001` 缺客户确认、原始凭证和责任方提交包 | 作为辽宁远航专项主缺口 |
| DKS-050 dry-run 评测 | `KGR-GH-D050-FIN-001` 缺金融凭证脱敏索引、保管责任和可见范围 | 作为金融凭证专项主缺口 |
| 葛化订单运行母版 | `FEI-GH-*` 为金融凭证脱敏索引；预运营期订单不得写成正式订单 | 约束编号、状态机和禁写动作 |
| 辽宁远航悬赏草案 | 金融凭证为 DSR-L3，允许只提交脱敏索引，原件线下核验 | 约束密级、验收和悬赏边界 |
| GFIS evidence index | 正式报价 PDF 已受控，但 `customer_confirmations=0`、`purchase_orders=0`、`runtime_ready=0`、`verified=0` | 作为不得升级运行层的阻断依据 |
| GFIS evidence index | 运行层 12 个对象、62 个凭证槽位仍 `complete_slots=0`、`missing_slots=62` | 作为责任方提交包缺口依据 |
| 辽宁远航报价元数据 | 报价 PDF 有 sha256、报价编号、采购单位、产品、有效期等字段 | 仅作为报价来源锚点，不替代客户确认 |

## 3. 缺口优先级

| gapId | 来源对象 | 优先级 | 缺口类型 | 当前状态 | 阻断范围 |
|---|---|---|---|---|---|
| `KGR-GH-D050-LY-001` | `DEF-GH-D050-003` | P1 | evidence_gap | open_candidate | DVA 验收、预运营期订单升级、候选 SOP 闭环、GFIS runtime intake |
| `KGR-GH-D050-FIN-001` | `DEF-GH-D050-004` | P1 | governance_gap | open_candidate | 金融凭证问答、收益口径、资金池引用、RAG 开放引用 |
| `KGR-GH-D051-HUMAN-001` | 本文新增 | P1 | governance_gap | open_candidate | dry-run 进入人工评测和资料真实接收 |

## 4. 辽宁远航责任方提交包

专项提交包编号：`KSP-GH-LY-D051-001`

| 字段 | 必填 | 口径 |
|---|---:|---|
| `submissionPackageId` | 是 | `KSP-GH-LY-D051-001` |
| `linkedGapIds` | 是 | `KGR-GH-D050-LY-001`, `KGR-GH-LY-202606-0001` |
| `linkedQuoteRef` | 是 | `QTE-GH-LY-202606-0001` 或受控报价 PDF 元数据 |
| `customerConfirmationRefs` | 是 | 客户确认函、采购订单、合同、平台订单回执或等效正式确认原件的脱敏索引 |
| `originalProofRefs` | 是 | 报价原件、报价版本、客户确认来源、样箱反馈、发货、POD、质量、金融索引 |
| `sourceRecordHashOrSeal` | 条件必填 | 文件 hash、线下封存编号或受控索引编号 |
| `responsibleParty` | 是 | 提交单位、提交人、责任角色和联系方式 |
| `timestamp` | 是 | 证据形成时间、提交时间、复核时间，三者不得混同 |
| `targetFactory` | 是 | 葛化目标工厂或未来复制工厂 |
| `oemCarrier` | 条件必填 | 现代精工或其他预运营期承接方 |
| `responsibilitySplit` | 是 | 目标工厂负责未来承接和建设运营准备；OEM 承接方负责当前生产、质量、发货等事实责任 |
| `waesGateRef` | 是 | WAES 规则记录、阻断或人工确认候选 |
| `gfisActionMode` | 是 | `no_write` / `candidate_only` / `manual_entry_after_confirmation` / `blocked` |
| `kdsPoolRefs` | 是 | 订单池、物流池、资金池、数据池、场景池 |
| `forbiddenClaims` | 是 | 不得声明客户确认已取得、POD 已取得、到账已确认、GFIS verified artifact 已形成 |

## 5. 辽宁远航最低验收条件

| 验收项 | 最低通过条件 | 不通过条件 | 输出状态 |
|---|---|---|---|
| 报价来源 | 受控报价原件、版本、hash、报价单位、采购单位、产品、有效期可追溯 | 只有口述、文件名、AI 摘要或无 hash 截图 | `quote_source_recorded` / `returned_for_source` |
| 客户确认 | 有客户确认函、采购订单、合同、平台订单回执或等效正式确认原件索引 | 只有报价、会议纪要、沟通摘要、弱确认线索 | `customer_confirmed_by_human` / `customer_confirmation_missing` |
| 责任方提交 | 有提交人、单位、角色、时间、来源真实性声明和可见范围 | 无责任主体、无提交时间、不可追溯 | `owner_response_candidate` / `owner_response_missing` |
| OEM 责任 | 区分现代精工等 OEM 当前承接与葛化目标工厂未来承接 | 把 OEM 生产写成葛化自建工厂已投产 | `responsibility_split_recorded` / `responsibility_disputed` |
| 质量 / 发货 / POD | 至少形成签收、检验、发货、承运或 POD 的脱敏索引或明确缺口 | 只有发货计划就确认交付 | `indexed_or_gap_recorded` / `returned_for_evidence` |
| GFIS 运行层 | 人工确认前只允许候选隔离，不进入 runtime intake | 用报价 PDF 或 KDS 候选替代 live proof | `candidate_only` / `runtime_blocked` |

## 6. 金融凭证脱敏索引模板

专项索引编号：`FEI-GH-D051-001`

| 字段 | 必填 | 口径 |
|---|---:|---|
| `financeEvidenceIndexId` | 是 | `FEI-GH-D051-001` |
| `linkedGapIds` | 是 | `KGR-GH-D050-FIN-001`, `KGR-GH-FIN-202606-0001` |
| `linkedOrderCandidateRefs` | 条件必填 | `POO-GH-*`、`QTE-GH-LY-*` 或对应缺口编号 |
| `evidenceType` | 是 | invoice / receipt / bank_record / receivable / payment_plan / other |
| `sourceParty` | 是 | 凭证来源单位或受控别名 |
| `custodianRole` | 是 | 财务负责人、资料保管人或线下封存责任人 |
| `redactionStatus` | 是 | `metadata_only` / `redacted_summary` / `sealed_offline` |
| `classificationLevel` | 是 | 默认 `DSR-L3`，降密必须人工或委员会备案 |
| `visibleScope` | 是 | private / finance_only / project_authorized / committee_only |
| `invoiceStatus` | 是 | no_invoice / invoice_statistical / invoice_pending_review |
| `cashReceivedStatus` | 是 | no_cash_received / cash_received_candidate / cash_received_confirmed_by_human |
| `amountVisibility` | 是 | hidden / range_only / finance_private / committee_only |
| `accountInfoRedacted` | 是 | true |
| `sourceHashOrOfflineSeal` | 条件必填 | hash、封存编号或线下保管索引 |
| `storageLocation` | 是 | 只写受控位置或封存索引，不写敏感原文 |
| `humanReviewer` | 是 | 财务责任人或授权复核人，未确认时填待确认 |
| `waesGateRef` | 是 | governance_blocked / manual_confirmation_required / committee_review_required |
| `kdsPoolRefs` | 是 | 资金池、订单池、数据池、争议池 |
| `forbiddenUses` | 是 | 不得进入开放问答，不得确认到账，不得作为收益分配依据 |

## 7. 金融凭证状态机

```text
index_requested
  -> metadata_received
  -> redaction_checked
  -> waes_rule_recorded_or_blocked
  -> human_review_pending
  -> committee_review_required(optional)
  -> index_usable_for_candidate
```

任何一步缺少保管责任、可见范围、脱敏状态或 WAES 门禁时，状态保持 `governance_blocked`，不得进入 RAG 开放问答、收益分配或正式产值积分。

## 8. DSR 与 RAG 准入

| 等级 | 允许进入知识库的内容 | RAG 准入 | 说明 |
|---|---|---|---|
| DSR-L1 | 非敏感流程、公开规则、普通培训摘要 | safe | 可用于普通问答 |
| DSR-L2 | 客户、订单、POD、质量等脱敏摘要 | limited | 只能按授权角色调用 |
| DSR-L3 | 金融凭证、金额、账户、合同敏感信息、到账、收益分配 | blocked_by_default | 默认只保留元数据或封存索引 |

DSR-L3 不进入共享知识库正文，不进入普通 AI 问答。AI 只能回答“需要提交什么索引、由谁确认、当前为什么阻断”，不能输出敏感字段或确认资金事实。

## 9. 知识缺口悬赏候选

| bountyId | 关联缺口 | 发布前条件 | 可奖励类型 | 当前状态 |
|---|---|---|---|---|
| `KGB-GH-D050-LY-001` | `KGR-GH-D050-LY-001` | 资源冻结、验收标准、可见范围、争议路径、委员会备案 | 知识积分、AI 服务权益、潜在产值贡献候选 | `bounty_candidate_not_published` |
| `KGB-GH-D051-FIN-001` | `KGR-GH-D050-FIN-001` | 财务保管责任、脱敏模板、可见范围、WAES 门禁、委员会备案 | 治理贡献、知识贡献 | `bounty_candidate_not_published` |
| `KGB-GH-D051-HUMAN-001` | `KGR-GH-D051-HUMAN-001` | 人工评测角色、评分表、签认格式 | 治理贡献 | `bounty_candidate_not_published` |

悬赏候选不得自动发布。发布必须满足资源冻结、验收条件、争议处理和委员会备案。没有实际收入时不得列入正式产值贡献；到账后才可进入正式收益池参考。

## 10. 候选 SOP 输入

| sopCandidateId | 来源 | SOP 阶段 | AI 可建议 | 不得自动执行 |
|---|---|---|---|---|
| `AIS-GH-SOP-D051-LY-001` | `KSP-GH-LY-D051-001` | 辽宁远航补证链路 | 责任方提交包、客户确认补证、GFIS 候选隔离、WAES 阻断说明 | 不创建正式订单、不放行 runtime intake、不确认 verified artifact |
| `AIS-GH-SOP-D051-FIN-001` | `FEI-GH-D051-001` | 金融凭证脱敏索引 | 脱敏索引字段、保管责任、可见范围、问答边界 | 不输出敏感原文、不确认到账、不触发收益分配 |
| `AIS-GH-SOP-D051-HUMAN-001` | `KGR-GH-D051-HUMAN-001` | 人工评测签认 | 评分表、红线、退回原因、复测条件 | 不替代人工签认或委员会裁决 |

## 11. 底座 11 池与增强账本挂接

| 对象 | 底座 11 池 | 增强账本 |
|---|---|---|
| 辽宁远航责任方提交包 | 订单池、物流池、资金池、数据池、场景池 | SOP 账本、贡献账本、悬赏池、潜在产值池、争议池 |
| 金融凭证脱敏索引 | 资金池、订单池、数据池 | 权限账本、收益池候选、争议池、贡献账本 |
| 人工评测签认 | 数据池、人才池、场景池 | 贡献账本、积分池、委员会记录 |

积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本和贡献账本统一纳入 KDS 底座 11 池的事实基础数据体系，但不替代底座 11 池。增强账本必须挂接到底座池后才能作为收益、系统、业务分配参考。

## 12. WAES 与人工确认

| 场景 | WAES 规则口径 | 人工或委员会口径 |
|---|---|---|
| 规则以内的字段缺口 | 记录 `governance_recorded` 或 `returned_for_evidence` | 资料责任人补证 |
| 缺客户确认或原始凭证 | 记录 `governance_blocked` | 责任方提交原始凭证或等效确认 |
| 金融凭证 DSR-L3 | 记录 `manual_confirmation_required` 或 `committee_review_required` | 财务责任人确认保管、脱敏和可见范围 |
| 潜在产值转正式产值 | WAES 记录规则和证据状态 | 到账证据与委员会或授权人工确认 |
| 争议或重大违规 | WAES 触发争议规则 | 委员会多数决并备案 |

## 13. 本轮结论

1. 辽宁远航报价 PDF 可作为报价来源锚点，但不能替代客户确认、采购订单、合同、POD 或 GFIS live proof。
2. 辽宁远航运行层仍缺客户确认和 62 个责任方凭证槽位响应，不得进入 runtime intake、WAES review、verified 或 accepted。
3. 金融凭证必须先形成 `FEI-GH-D051-001` 类型脱敏索引，默认 DSR-L3，默认不进入普通问答。
4. 本轮新增的悬赏、积分、贡献、SOP 和写回均为候选，不产生确认积分或收益分配。
5. 下一步应进入人工填报包和确认队列，而不是系统写入或状态升级。

## 14. 本轮不升级声明

本轮不证明：

1. 辽宁远航客户确认、采购订单、合同、POD、质量或到账已经取得。
2. 金融凭证可以开放问答、共享正文、确认到账或进入收益分配。
3. 葛化 GFIS AI 助手三件套已经真实上线或人工评测通过。
4. GFIS、WAES、KDS API、GPC、PVAOS、Finance 或生产系统已经写入。
5. 知识缺口悬赏已经发布，积分、额度、收益或潜在产值已经确认。
6. 本专题可以进入 `accepted`、`complete` 或 `integrated`。

## 15. 下一轮建议

建议 `GPCF-KDS-DKS-052` 进入“葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包”，形成两个可交给责任方填报的模板：

1. `KSP-GH-LY-D052-001`：辽宁远航客户确认、采购订单/合同、POD、质量、责任方提交包。
2. `FEI-GH-D052-001`：金融凭证 DSR-L3 脱敏索引、保管责任、可见范围和 WAES 门禁填报表。
