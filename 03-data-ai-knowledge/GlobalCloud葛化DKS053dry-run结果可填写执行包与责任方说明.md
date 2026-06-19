---
doc_id: GPCF-DOC-A22E7CBF43
title: GlobalCloud 葛化 DKS-053 dry-run 结果可填写执行包与责任方说明
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化DKS053dry-run结果可填写执行包与责任方说明.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化DKS053dry-run结果可填写执行包与责任方说明.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 DKS-053 dry-run 结果可填写执行包与责任方说明

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-054`  
状态：`controlled_submission_instruction_pack`

## 1. 定位

本文承接 `GPCF-KDS-DKS-053`，把 17 个 dry-run 用例转成责任方可阅读、可填写、可退回、可人工确认、可委员会备案候选的执行包说明。

本文不派发真实请求，不接收真实材料，不保存原始敏感资料，不写入 GFIS、WAES、KDS API、GPC、PVAOS、Finance 或生产系统主账，不确认人工签认、委员会裁决、积分、收益、悬赏、POD、质量、到账或业务完成。

## 2. 输入依据

| 来源 | 本文使用方式 |
|---|---|
| `GPCF-KDS-DKS-053` dry-run 验收视图 | 转换为责任方填写说明、字段示例、退回原因和队列准备项 |
| `GlobalCloud葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包.md` | 沿用 `KSP-GH-LY-D052-001` 与 `FEI-GH-D052-001` 字段 |
| `GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` | 沿用预运营期订单、统一编号、OEM 责任拆分、底座 11 池和 SOP 建议格式 |
| `GlobalCloud葛化GFISAI助手内测运行记录模板.md` | 沿用 AssistantOutputRecord、EvalRecord、DefectRecord、WritebackCandidate 字段 |
| `GlobalCloud积分收益额度悬赏争议联动规则.md` | 沿用积分、收益、AI 额度、悬赏、争议和到账/开票口径 |
| `GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md` | 沿用 KGR、RRT、KGB 缺口和悬赏候选状态 |
| `08-evidence-samples/GFIS/loop-state.md` 与状态矩阵 | 保持 GFIS `real_business_lane=repair_required`，不升级业务状态 |

## 3. 多 agent 判断

本轮适合只读多 agent 核查，不适合并行写入。原因是责任方执行包、LOOP 记录、KDS 镜像、文档控制登记册和状态口径必须保持单一来源；字段、门禁和边界可分线核查。

| 核查线 | 范围 | 写入权限 |
|---|---|---|
| 字段与责任方 | 辽宁远航、现代精工 OEM、质量、发货、POD、金融索引 | none |
| GFIS 三件套与 SOP | AI 输出记录、候选写回、候选 SOP、Defect open 状态 | none |
| WAES/RAG/积分收益 | DSR、RAG、人工确认、委员会、积分收益悬赏 | none |

## 4. 执行包总规则

| 规则 | 口径 |
|---|---|
| 统一编号 | 使用 `SUB-GH-D054-*` 作为本轮提交说明编号；业务对象仍使用 `KSP`、`FEI`、`HRC`、`CRC`、`WBC`、`AIS` 等既有前缀 |
| 来源要求 | 每个填写项必须有来源类型、来源责任方、来源索引或缺口编号 |
| 状态要求 | 默认状态只能是 `submission_instruction`、`waiting_source`、`candidate_only`、`returned_for_evidence`、`manual_review_pending`、`committee_review_required`、`no_write` 或 `suggestion_only` |
| 证据要求 | DSR-L2 以上材料只填脱敏索引、摘要、hash、封存编号或线下保管索引 |
| 核验路径 | 先结构检查，再 WAES 规则记录或阻断，再人工确认，必要时委员会备案或裁决 |
| 禁写边界 | 不得写 GFIS 主账、WAES 主账、真实 KDS API、财务主账、生产系统、收益池或积分确认账 |

## 5. 责任方执行包目录

| 执行包编号 | 责任方 | 对应对象 | 填写目标 | 当前状态 |
|---|---|---|---|---|
| `SUB-GH-D054-LY-001` | 项目负责人 / 订单责任方 | `KSP-GH-LY-D052-001` | 补齐客户确认、报价、责任主体和来源真实性 | waiting_source |
| `SUB-GH-D054-QPOD-001` | 质量 / 发货 / POD 责任人 | `KSP-GH-LY-D052-001` | 补齐样箱反馈、质量、发货、POD 脱敏索引或明确缺口 | waiting_source |
| `SUB-GH-D054-OEM-001` | 目标工厂 / OEM 承接方 | `OEM-GH-MJ-*` / `KSP-GH-LY-D052-001` | 拆分现代精工等 OEM 当前事实责任与目标工厂未来承接责任 | waiting_source |
| `SUB-GH-D054-FIN-001` | 财务责任人 / 资料保管人 | `FEI-GH-D052-001` | 补齐金融凭证 DSR-L3 metadata_only 索引和保管责任 | waiting_source |
| `SUB-GH-D054-WAES-001` | WAES 规则记录人 | `WGR-GH-D052-001` | 记录规则内、阻断、人工确认或委员会路径 | governance_instruction |
| `SUB-GH-D054-AI-001` | GFIS AI 助手内测负责人 | `AOR/EVAL/DEF/WBC/AIS-GH-D053-*` | 记录 AI 输出、评测、缺陷、候选写回和候选 SOP | candidate_only |
| `SUB-GH-D054-KGB-001` | KDS 记录人 / 缺口发起方 | `KGR/RRT/KGB-GH-*` | 准备知识缺口、资料回收和悬赏候选 | bounty_candidate_not_published |

## 6. 责任方填写字段与示例

| 执行包编号 | 必填字段 | 示例值 | 允许状态 | 退回或阻断原因 |
|---|---|---|---|---|
| `SUB-GH-D054-LY-001` | `submitterUnit`、`submitterPersonOrRole`、`sourceAuthenticityStatement`、`linkedQuoteRef`、`customerConfirmationRef`、`classificationLevel`、`visibleScope`、`forbiddenClaimsAccepted` | `葛化项目组`、`订单责任方`、`报价索引 QTE-GH-LY-202606-0001`、`客户确认待补 KGR-GH-LY-202606-0001`、`DSR-L2`、`directed`、`true` | `received_for_structure_check` / `manual_review_pending` / `returned_for_evidence` | 缺客户确认、缺来源声明、用口述替代正式确认、暴露客户敏感原文 |
| `SUB-GH-D054-QPOD-001` | `sampleBoxFeedbackRefs`、`qualityEvidenceRefs`、`deliveryEvidenceRefs`、`podRefs`、`sourceOwner`、`redactionMode`、`waesGateExpected` | `SBF-GH-202606-0001 pending`、`QER-GH-202606-0001 metadata_only`、`POD-GH-202606-0001 pending`、`partial`、`manual_confirmation_required` | `returned_for_sample_feedback` / `returned_for_quality` / `returned_for_delivery` / `returned_for_pod` / `manual_review_pending` | 缺样箱反馈、缺质量索引、发货记录不可追溯、POD 只有计划无签收、无责任主体 |
| `SUB-GH-D054-OEM-001` | `targetFactory`、`oemCarrier`、`responsibilitySplit`、`productionFactOwner`、`futureOperationOwner`、`capacityDispatchNeed` | `葛化目标工厂`、`现代精工`、`OEM 负责当前生产质量发货，目标工厂负责未来承接准备`、`true` | `responsibility_split_recorded` / `responsibility_disputed` / `returned_for_oem` | 把 OEM 事实写成目标工厂已投产、缺产线或批次责任、责任边界不清 |
| `SUB-GH-D054-FIN-001` | `financeEvidenceIndexId`、`evidenceType`、`custodianRole`、`redactionStatus`、`visibleScope`、`invoiceStatus`、`cashReceivedStatus`、`accountInfoRedacted`、`sourceHashOrOfflineSeal`、`storageLocationIndex` | `FEI-GH-D052-001`、`invoice`、`财务保管人`、`metadata_only`、`finance_only`、`invoice_statistical`、`no_cash_received`、`true`、`offline-seal-001` | `index_received_for_structure_check` / `manual_confirmation_required` / `governance_blocked` | 暴露账户、完整金额、流水原文、缺保管人、缺封存索引、把开票写成到账 |
| `SUB-GH-D054-WAES-001` | `waesGateRecordId`、`sourceObjectRefs`、`classificationLevel`、`ruleDecision`、`humanConfirmationRequired`、`committeeRequired`、`blockedReason` | `WGR-GH-D054-001`、`KSP/FEI/HRC/CRC refs`、`DSR-L2/L3`、`governance_recorded`、`true`、`false` | `governance_recorded` / `blocked` / `manual_confirmation_required` / `committee_review_required` | 缺密级、缺权限范围、DSR-L3 试图开放问答、收益或争议绕过委员会 |
| `SUB-GH-D054-AI-001` | `outputId`、`sampleId`、`assistantType`、`sourceRefsReturned`、`factLayerReturned`、`waesActionReturned`、`forbiddenOutputDetected`、`writebackCandidateId`、`suggestionId` | `AOR-GH-D054-001`、`QS-GH-D054-001`、`DVA/SOP`、`true`、`true`、`manual_confirmation_required`、`false`、`WBC-GH-D054-001`、`AIS-GH-SOP-D054-001` | `dry_run` / `ready_for_eval` / `candidate_only` / `suggestion_only` | AI 输出正式事实、缺来源、混淆事实层、试图写主账、输出 accepted/complete/integrated |
| `SUB-GH-D054-KGB-001` | `requestId`、`recoveryTaskId`、`bountyCandidateId`、`gapSummary`、`requiredSources`、`frozenResourceState`、`acceptanceRule`、`disputeRule` | `KGR-GH-LY-202606-0001`、`RRT-GH-LY-202606-0001`、`KGB-GH-LY-202606-0001`、`客户确认/POD/真实回执缺口`、`not_frozen` | `candidate_only` / `recovery_open` / `ready_for_committee` | 未冻结资源、缺验收规则、缺争议路径、缺来源责任主体时不得发布 |

## 7. 人工确认准备清单

| queueItemId | 来源执行包 | 人工角色 | 准备材料 | 未满足时状态 |
|---|---|---|---|---|
| `HRC-GH-D054-LY-001` | `SUB-GH-D054-LY-001` | 项目负责人 / 订单责任方 | 客户确认或等效正式确认脱敏索引、报价来源、来源声明 | `returned_for_evidence` |
| `HRC-GH-D054-QPOD-001` | `SUB-GH-D054-QPOD-001` | 质量 / 发货 / POD 责任人 | 质量、发货、POD 脱敏索引或缺口说明 | `returned_for_quality_or_pod` |
| `HRC-GH-D054-OEM-001` | `SUB-GH-D054-OEM-001` | 目标工厂 / OEM 责任方 | 当前 OEM 事实责任与目标工厂未来承接责任说明 | `responsibility_disputed` |
| `HRC-GH-D054-FIN-001` | `SUB-GH-D054-FIN-001` | 财务责任人 | DSR-L3 metadata_only 索引、保管人、封存编号、开票/到账状态 | `manual_confirmation_required` |
| `HRC-GH-D054-WAES-001` | `SUB-GH-D054-WAES-001` | WAES 规则记录人 | 密级、可见范围、阻断原因、人工或委员会路径 | `governance_blocked` |

人工确认行只代表准备清单，不代表已派发、已签认、已通过或已形成业务事实。

## 8. 委员会准备清单

| queueItemId | 来源执行包 | 触发事项 | 准备材料 | 当前状态 |
|---|---|---|---|---|
| `CRC-GH-D054-REV-001` | `SUB-GH-D054-FIN-001` | 到账收入、收益池分配、贡献比例 | 到账人工确认、贡献来源、争议范围 | committee_candidate |
| `CRC-GH-D054-PV-001` | `SUB-GH-D054-LY-001` | 潜在产值转正式产值 | 客户确认、到账或委员会确认依据 | committee_candidate |
| `CRC-GH-D054-DSP-001` | `SUB-GH-D054-WAES-001` | 密级、可见范围、跨单位权益争议 | 争议主体、证据索引、临时保护状态 | committee_candidate |
| `CRC-GH-D054-VIO-001` | 任一执行包 | 重大违规、泄密、越权确认、虚构 verified artifact | 违规事实索引、影响范围、冻结建议 | committee_candidate |
| `CRC-GH-D054-KGB-001` | `SUB-GH-D054-KGB-001` | 悬赏发布、资源冻结、验收结算争议 | 悬赏规则、资源冻结、验收标准、争议规则 | committee_candidate |

委员会行只代表备案或裁决准备，不代表委员会已经多数决、备案、裁决、结算、扣减或分配。

## 9. AI 输出、候选写回与候选 SOP

| 对象 | 字段 | 允许值 | 禁止值 |
|---|---|---|---|
| AssistantOutputRecord | `outputStatus` | `ready_for_eval` / `dry_run` / `quarantined` / `rejected` | `confirmed_fact`、`accepted`、`complete`、`integrated` |
| EvalRecord | `decision` | `pass_dry_run` / `rework` / `fail` / `hard_fail` | `business_pass`、`production_pass` |
| DefectRecord | `status` | `open` / `fixed_candidate` / `retest_required` / `deferred` | `closed_by_business_fact` |
| WritebackCandidate | `writebackMode` | `local_mirror` / `manual_record` / `no_write` / `blocked` | `gfis_formal_write`、`waes_api_write`、`finance_write` |
| SOPSuggestion | `suggestionStatus` | `suggestion_only` / `pending_human_review` / `rejected` | `approved_for_execution_without_human` |

候选 SOP 必须说明 `sourceCandidateRefs`、`targetSopStage`、`inputFields`、`outputFields`、`requiredEvidence`、`waesGate`、`gfisActionMode`、`humanConfirmationRequired`、`committeeRequired` 和 `forbiddenOperations`。

## 10. RAG、WAES、DSR 与可见范围

| 数据 | DSR | RAG 口径 | WAES 口径 | 执行包填写要求 |
|---|---|---|---|---|
| WAES 规则说明 | DSR-L1 | safe | governance_recorded | 可填规则编号和下一步，不确认业务完成 |
| 报价来源元数据 | DSR-L2 | limited | manual_confirmation_required_if_used_for_business | 只填来源索引、版本、责任人、缺口 |
| 客户确认索引 | DSR-L2 / DSR-L3 | limited / blocked_by_default | manual_confirmation_required | 只填脱敏索引或封存编号 |
| POD / 质量脱敏索引 | DSR-L2 | limited | manual_confirmation_required | 只在项目授权范围内使用 |
| 金融凭证元数据 | DSR-L3 | blocked_by_default | manual_confirmation_required / committee_review_required | 只填 metadata_only、保管人、封存索引 |
| 收益、到账、分配字段 | DSR-L3 | blocked_by_default | committee_review_required | 到账后仍需人工或委员会确认 |

负例规则：`ragInclude=true` 但对象不是 `safe_reuse_candidate` 时必须阻断；`limited_report_candidate` 不得进入 RAG 强引用或指挥舱强引用。

### 10.1 只能填写脱敏索引的字段

以下字段不得填写原文、账户、完整金额、未授权截图、合同全文、客户敏感正文或可直接识别个人/单位的未授权信息，只能填写脱敏索引、元数据、hash、封存编号或线下保管位置：

| 字段 | 限制 |
|---|---|
| `customerConfirmationRef` | 客户确认原件只能使用脱敏索引、受控摘要或线下封存编号 |
| `purchaseOrderOrContractRef` | 采购订单、合同或签章件只能使用脱敏索引、版本号、hash 或封存编号 |
| `financeIndexRefs` / `financeEvidenceIndexId` | 金融凭证只进入 `FEI-GH-*` metadata_only 索引 |
| `sourcePartyAlias` | 金融、客户、供应商敏感主体可使用受控别名 |
| `amountVisibility` | 普通问答不可见；只允许 hidden、range_only、finance_private、committee_only |
| `accountInfoRedacted` | 必须为 true，否则进入 `governance_blocked` |
| `sourceHashOrOfflineSeal` | 记录 hash、封存编号或线下保管索引，不记录原文 |
| `storageLocationIndex` | 记录受控位置索引，不记录敏感资料正文 |

## 11. 积分、收益、AI 额度与悬赏口径

| 对象 | 本轮可登记 | 禁止登记为 |
|---|---|---|
| 知识积分 | 填写结构、脱敏索引、补证、SOP 建议的候选贡献 | confirmed_points |
| 产值积分 | 到账前不登记正式产值；可登记潜在产值候选 | formal_value_without_cash |
| 潜在产值 | 客户确认缺口、业务机会、辽宁远航链路候选 | formal_revenue |
| AI 自购额度 | 自用计量、使用场景、受益对象 | unified_revenue_pool_resource |
| 贡献 / 共享 / 奖励额度 | 候选来源、用途、备案需求 | issued_credit_without_confirmation |
| 收益池 | 开票统计、到账待确认、收益分配待委员会 | allocated_revenue_without_cash |
| 悬赏 | 发布前置条件、资源冻结需求、验收规则、争议规则 | published_bounty_without_freeze |

## 12. 全局断言

本轮所有对象必须满足：

```text
realKdsApiWrite=false
waesWrite=false
gfisWrite=false
businessLedgerWrite=false
financeLedgerWrite=false
settlementWrite=false
ragAdmission=false
dispatchSent=false
createsConfirmationFact=false
createsCommitteeDecision=false
statusUpgrade=false
```

## 13. 完成定义

本文完成表示：

1. DKS-053 dry-run 用例已转换为责任方可填写执行包说明。
2. 每个执行包都有统一编号、责任主体、字段、示例、状态、退回或阻断原因。
3. 人工确认和委员会准备清单已形成候选视图。
4. AI 输出、候选写回、候选 SOP、RAG、WAES、积分、收益、额度和悬赏均有禁写边界。
5. 本文纳入 LOOP、文档控制和 KDS 本地镜像。

本文不表示：

1. 任何真实资料已经收到。
2. 任何请求已经派发。
3. 任何人工确认或委员会裁决已经完成。
4. 任何真实 GFIS、WAES、KDS API、财务或生产系统已经写入。
5. GFIS `real_business_lane=repair_required` 已关闭。
6. 本专题可升级 `accepted`、`complete` 或 `integrated`。

## 14. 下一轮建议

建议 `GPCF-KDS-DKS-055` 进入“葛化 DKS-054 执行包派发授权信封与负例拒收门禁”，定义未来如需真实派发时必须具备的授权信封、接收人确认、派发渠道确认、回执路径和负例拒收规则；未获得显式授权前仍不发送外部通知。
