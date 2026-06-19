---
doc_id: GPCF-DOC-62E56B6121
title: GlobalCloud 葛化 DKS-052 填报包 dry-run 验收与人工确认队列视图
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化DKS052填报包dry-run验收与人工确认队列视图.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化DKS052填报包dry-run验收与人工确认队列视图.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 DKS-052 填报包 dry-run 验收与人工确认队列视图

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-053`  
状态：`controlled_dry_run_acceptance`

## 1. 定位

本文承接 `GPCF-KDS-DKS-052`，用虚拟脱敏样例验证辽宁远航补证请求包、金融凭证脱敏索引、人工确认队列、委员会触发、候选写回和候选 SOP 的运行边界。

本文只形成 dry-run 验收视图，不接收真实资料，不派发真实补证请求，不保存金融凭证原文，不写入 GFIS、WAES、KDS API、GPC、PVAOS、Finance 或生产系统主账，不确认积分、收益、悬赏、争议或业务完成。

## 2. 输入依据

| 来源 | 本轮使用方式 |
|---|---|
| `GlobalCloud葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包.md` | 作为字段、判定、队列和禁写边界来源 |
| `GlobalCloud葛化辽宁远航与金融凭证缺口专项台账.md` | 作为辽宁远航和金融凭证缺口来源 |
| `GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` | 作为预运营期订单、OEM 责任拆分、SOP 建议和 GFIS 写入模式来源 |
| `GlobalCloud积分收益额度悬赏争议联动规则.md` | 作为积分、收益、额度、悬赏、争议和到账/开票口径来源 |
| `base-knowledge-human-confirmation-queue-20260619.md` | 作为人工确认队列样式来源 |
| `base-knowledge-committee-review-queue-20260619.md` | 作为委员会队列样式来源 |
| `08-evidence-samples/GFIS/loop-state.md` | 作为 GFIS 真实业务线仍 `repair_required` 的边界来源 |
| `09-status/gpcf-project-status-matrix.md` | 作为项目群状态不得升级的依据 |

## 3. dry-run 范围

| 范围 | 本轮做 | 本轮不做 |
|---|---|---|
| 辽宁远航补证包 | 用虚拟脱敏字段测试退回、结构验收、人工确认、委员会触发 | 不接收客户确认、采购订单、合同、POD 或质量原件 |
| 金融凭证索引 | 用虚拟元数据测试 DSR-L3 阻断、脱敏索引、财务人工确认 | 不接收银行流水、发票原文、账户、金额明细或到账凭证 |
| GFIS 写回 | 测试 `candidate_only`、`no_write`、`blocked_if_formal_write` | 不创建 GFIS runtime primary key、review queue、runtime intake 或 verified artifact |
| WAES / RAG | 测试 governance_recorded、blocked、manual_confirmation_required、committee_review_required | 不写真实 WAES，不开放 DSR-L3 普通问答 |
| 积分收益悬赏 | 测试候选状态和委员会触发 | 不确认积分，不发布悬赏，不冻结真实资源，不分配收益 |

## 4. 验收用例

默认基线：除测试行故意置空、置错或模拟越权外，`KSP-GH-LY-D052-001` 与 `FEI-GH-D052-001` 的其它必填字段均使用虚拟脱敏合法值，所有输出保持 `dry_run`、`candidate_only`、`pending_human_assignment`、`not_triggered`、`no_write` 或 `suggestion_only`。

| caseId | 虚拟输入 | 触发规则 | 预期判定 | 人工/委员会路径 | 禁止动作 |
|---|---|---|---|---|---|
| `DKS053-LY-STRUCT-OK-001` | `KSP-GH-LY-D052-001` 字段齐全，客户确认、质量、发货、POD、金融均为脱敏索引，`gfisWriteMode=candidate_only` | 结构合规但需人工确认 | `received_for_structure_check` / `manual_review_pending` | `HRC-GH-D053-LY-002` 与 `HRC-GH-D053-QPOD-001` | 不进入 GFIS runtime intake，不形成正式业务事实 |
| `DKS053-LY-MISSING-CUSTOMER-001` | `customerConfirmationRef` 为空，或只有报价、会议纪要、摘要 | 客户确认缺失 | `customer_confirmation_missing` / `returned_for_evidence` | 人工确认队列 `HRC-GH-D053-LY-001` | 不计积分，不发布悬赏，不生成正式订单 |
| `DKS053-LY-MISSING-QPOD-001` | `qualityEvidenceRefs`、`deliveryEvidenceRefs` 或 `podRefs` 缺失或不可追溯 | 质量、发货、POD 缺口 | `returned_for_quality` / `returned_for_delivery` / `returned_for_pod` | `HRC-GH-D053-QPOD-001` | 不确认质量放行、发货完成或 POD |
| `DKS053-LY-OEM-RESP-SPLIT-001` | `oemCarrier` 缺失，或把现代精工 OEM 事实写成葛化自建工厂事实 | 目标工厂与 OEM 责任混同 | `returned_for_oem` / `returned_for_responsibility` / `responsibility_disputed` | `HRC-GH-D053-OEM-001` | 不声明目标工厂已投产，不作为产能事实 |
| `DKS053-LY-SENSITIVE-METADATA-001` | 合同、客户敏感信息、金额或 DSR-L3 原文进入补证包 | 敏感字段暴露 | `metadata_only_required` 或 `governance_blocked` | `HRC-GH-D053-WAES-001`，必要时 `CRC-GH-D053-DSP-001` | 不进入普通问答，不进入 RAG 强引用 |
| `DKS053-LY-FORMAL-WRITE-BLOCK-001` | `gfisWriteMode=formal_write` 或声明已形成 verified artifact | 写回越权 | `blocked_if_formal_write` | `HRC-GH-D053-WAES-002`，重大越权进 `CRC-GH-D053-VIO-001` | 不创建主键，不进入 review/runtime/WAES/verified |
| `DKS053-FIN-INDEX-OK-001` | `FEI-GH-D052-001` 只含凭证类型、封存索引、保管角色、开票统计状态，`accountInfoRedacted=true` | DSR-L3 metadata_only 合规 | `index_received_for_structure_check` / `manual_confirmation_required` | `HRC-GH-D053-FIN-001` | 不确认到账，不进入收益池，不进入普通问答 |
| `DKS053-FIN-LEAKAGE-BLOCK-001` | 金融索引暴露账户、完整金额、未授权截图或原文 | 金融敏感字段暴露 | `governance_blocked` / `blocked_by_classification` | `HRC-GH-D053-FIN-002`，重大泄密进 `CRC-GH-D053-VIO-002` | 不入 RAG，不计收益，不留公开正文 |
| `DKS053-FIN-MISSING-CUSTODIAN-001` | 缺 `custodianRole`、`visibleScope`、`sourceHashOrOfflineSeal`、`storageLocationIndex` 或 WAES 门禁 | 保管和门禁不完整 | `returned_for_custodian` / `returned_for_access` / `returned_for_seal` / `returned_for_storage` / `returned_for_waes_gate` | `HRC-GH-D053-FIN-001` | 不作为候选问答材料 |
| `DKS053-FIN-INVOICE-NO-CASH-001` | `invoiceStatus=invoice_statistical` 且 `cashReceivedStatus=no_cash_received` | 开票不等于到账 | `index_usable_for_candidate` / `no_formal_revenue` | 财务人工确认后仍只作统计 | 不进入正式收益池，不列正式产值 |
| `DKS053-CRC-REV-001` | 到账、收益池、贡献比例或结算请求出现 | 收益分配事项 | `committee_review_required` | `CRC-GH-D053-REV-001` | 不由 AI/WAES 结算，不分配收益 |
| `DKS053-CRC-PV-001` | 潜在产值转正式产值请求 | 潜在产值转正 | `committee_review_required` | `CRC-GH-D053-PV-001` | 不确认正式产值 |
| `DKS053-CRC-DSP-001` | 跨单位权益、密级、可见范围、证据权属争议 | 权益或权限争议 | `committee_review_required` | `CRC-GH-D053-DSP-001` | 不自动裁决访问权或权属 |
| `DKS053-CRC-VIO-001` | 证据失真、泄密、重大违规、追溯扣减 | 重大违规 | `committee_review_required` / `governance_blocked` | `CRC-GH-D053-VIO-001` 或 `CRC-GH-D053-VIO-002` | 不计积分，不写回 |
| `DKS053-CRC-KGB-001` | `KGB-*` 悬赏发布、资源冻结、验收结算争议 | 悬赏发布或结算 | `committee_review_required` | `CRC-GH-D053-KGB-001` | 不发布悬赏，不冻结真实资源，不结算 |
| `DKS053-WBC-SOP-NOWRITE-001` | `WBC-GH-D052-*`、`AIS-GH-SOP-D052-*` 输出 | 候选写回和 SOP 建议 | `candidate_only` / `no_write` / `suggestion_only` | 人工或委员会确认后才可形成下一步 | 不写 GFIS/WAES/KDS API，不发布正式 SOP |
| `DKS053-GLOBAL-STATE-GUARD-001` | 全量 dry-run 输出扫描 | 状态升级保护 | `status_upgrade=not_allowed` | 不适用 | 不输出 `accepted`、`complete`、`integrated` |

## 5. dry-run 记录对象

| recordId | 类型 | 来源用例 | 状态 | 说明 |
|---|---|---|---|---|
| `AOR-GH-D053-001` | AssistantOutputRecord | `DKS053-LY-MISSING-CUSTOMER-001` | dry_run | 输出缺客户确认退回建议 |
| `AOR-GH-D053-002` | AssistantOutputRecord | `DKS053-FIN-LEAKAGE-BLOCK-001` | dry_run | 输出 DSR-L3 金融凭证阻断建议 |
| `AOR-GH-D053-003` | AssistantOutputRecord | `DKS053-WBC-SOP-NOWRITE-001` | dry_run | 输出候选写回 no_write 建议 |
| `EVAL-GH-D053-001` | EvalRecord | LY cases | dry_run_pass_with_blockers | 字段退回、人工确认和责任拆分规则可表达 |
| `EVAL-GH-D053-002` | EvalRecord | FIN / RAG cases | dry_run_pass_with_blockers | DSR-L3、RAG 和收益口径阻断可表达 |
| `DEF-GH-D053-001` | DefectRecord | all | open | 当前仍未接入真实助手服务，不能证明三件套真实上线 |
| `DEF-GH-D053-002` | DefectRecord | LY / FIN | open | 当前仍缺客户确认、POD、质量、金融凭证人工确认 |
| `WBC-GH-D053-LY-001` | WritebackCandidate | `KSP-GH-LY-D052-001` | candidate_only / no_write | 可写入本地候选台账，不写 GFIS 主账 |
| `WBC-GH-D053-FIN-001` | WritebackCandidate | `FEI-GH-D052-001` | metadata_only / no_write | 可写入脱敏索引候选，不写财务或收益主账 |
| `AIS-GH-SOP-D053-LY-001` | SOPSuggestion | 辽宁远航补证 | suggestion_only | 只建议补证 SOP |
| `AIS-GH-SOP-D053-FIN-001` | SOPSuggestion | 金融凭证索引 | suggestion_only | 只建议金融凭证脱敏索引 SOP |

### 5.1 记录字段底线

| 记录 | 必须字段 | 本轮限制 |
|---|---|---|
| AssistantOutputRecord | `outputId`、`sampleId`、`assistantType`、`sourceRefsReturned`、`factLayerReturned`、`waesActionReturned`、`nextActionReturned`、`forbiddenOutputDetected`、`redlineRefsTriggered`、`outputStatus` | `outputStatus=dry_run`，不得返回正式事实 |
| EvalRecord | `evalRunId`、`outputId`、`testCaseRefs`、`totalScore`、`hardFail`、`decision`、`retestRequired` | 只能形成 dry-run 评分，不能形成正式通过 |
| DefectRecord | `defectId`、`evalRunId`、`defectType`、`severity`、`requiredFix`、`owner`、`dueRound`、`status` | 缺真实助手、缺人工确认、缺原始凭证必须保持 open |
| WritebackCandidate | `writebackCandidateId`、`sourceObjectRefs`、`targetSystem`、`targetObjectType`、`writebackMode`、`allowedByPolicy`、`humanConfirmationRequired`、`sensitiveFieldsRedacted`、`writebackStatus` | GFIS 目标必须 `no_write`；KDS/WAES 只能 `candidate` 或 `pending_confirmation` |

## 6. 人工确认队列视图

| queueItemId | 来源 case | 人工角色 | 必须确认事项 | queue_status | write_authority |
|---|---|---|---|---|---|
| `HRC-GH-D053-LY-001` | `DKS053-LY-MISSING-CUSTOMER-001` | 项目负责人 / 订单责任方 | 客户确认或等效正式确认原件是否存在 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-LY-002` | `DKS053-LY-STRUCT-OK-001` | 项目负责人 / 订单责任方 | 客户确认索引、目标工厂和 OEM 责任拆分 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-QPOD-001` | `DKS053-LY-MISSING-QPOD-001` | 质量 / 发货 / POD 责任人 | 质量、发货、POD 索引是否可追溯 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-OEM-001` | `DKS053-LY-OEM-RESP-SPLIT-001` | 目标工厂 / OEM 责任方 | 现代精工等 OEM 当前事实责任与目标工厂未来承接责任 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-FIN-001` | `DKS053-FIN-INDEX-OK-001` | 财务责任人 | 金融凭证保管、脱敏、可见范围、开票/到账状态 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-FIN-002` | `DKS053-FIN-LEAKAGE-BLOCK-001` | 财务责任人 / WAES 记录人 | 敏感字段暴露处理、退回或封存 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-FIN-003` | `DKS053-CRC-REV-001` | 财务责任人 | 到账确认是否有人工确认记录 | candidate_only | none_dry_run_only |
| `HRC-GH-D053-WAES-001` | `DKS053-LY-SENSITIVE-METADATA-001` | WAES 规则记录人 | DSR-L3 原文是否阻断、是否改为 metadata_only | candidate_only | none_dry_run_only |
| `HRC-GH-D053-WAES-002` | `DKS053-LY-FORMAL-WRITE-BLOCK-001` | WAES 规则记录人 | GFIS 写回越权是否阻断 | candidate_only | none_dry_run_only |

## 7. 委员会队列视图

| queueItemId | 来源 case | 触发原因 | next_action | queue_status | write_authority |
|---|---|---|---|---|---|
| `CRC-GH-D053-REV-001` | `DKS053-CRC-REV-001` | 到账收入、收益池分配或贡献比例 | committee_review_required_before_revenue_allocation | candidate_only | none_dry_run_only |
| `CRC-GH-D053-PV-001` | `DKS053-CRC-PV-001` | 潜在产值转正式产值 | committee_review_required_before_formal_value | candidate_only | none_dry_run_only |
| `CRC-GH-D053-DSP-001` | `DKS053-CRC-DSP-001` | 密级、可见范围或跨单位权益争议 | committee_review_required_before_visibility_change | candidate_only | none_dry_run_only |
| `CRC-GH-D053-VIO-001` | `DKS053-CRC-VIO-001` | 越权写回或虚构 verified artifact | committee_review_required_before_any_downstream_action | candidate_only | none_dry_run_only |
| `CRC-GH-D053-VIO-002` | `DKS053-FIN-LEAKAGE-BLOCK-001` | 金融敏感字段泄露风险 | committee_review_required_if_major_violation | candidate_only | none_dry_run_only |
| `CRC-GH-D053-KGB-001` | `DKS053-CRC-KGB-001` | 缺客户确认可能转悬赏，但资源未冻结 | committee_filing_required_before_bounty_publication | candidate_only | none_dry_run_only |

说明：上表所有委员会行均为 review candidate，不代表备案、裁决、结算、扣减或分配已经完成。

## 8. RAG 与 WAES 准入视图

| 数据类型 | DSR | RAG decision | WAES decision | 说明 |
|---|---|---|---|---|
| WAES 门禁规则说明 | DSR-L1 | safe | governance_recorded | 可说明规则和下一步，不确认业务完成 |
| 报价来源元数据 | DSR-L2 | limited | manual_confirmation_required_if_used_for_business | 仅回答来源、缺口、补证路径 |
| 客户确认脱敏索引 | DSR-L2 / DSR-L3 | limited / blocked_by_default | manual_confirmation_required | 需授权角色，不向无关单位开放 |
| POD / 质量脱敏索引 | DSR-L2 | limited | manual_confirmation_required | 可用于项目授权范围内的资料验收 |
| 金融凭证元数据 | DSR-L3 | blocked_by_default | manual_confirmation_required / committee_review_required | 只回答需要什么索引、由谁确认、为何阻断 |
| 收益、到账、分配字段 | DSR-L3 | blocked_by_default | committee_review_required | 到账后仍需人工或委员会确认 |

负例规则：`ragInclude=true` 但对象不属于 `safe_reuse_candidate` 时，必须触发 RAG 越权阻断；`limited_report_candidate` 不得进入 RAG 强引用或指挥舱强引用。

## 9. 积分、收益、额度、悬赏状态

| 对象 | dry-run 状态 | 可做 | 禁止 |
|---|---|---|---|
| 知识积分 | candidate_only | 记录补证结构贡献候选 | 不确认积分、不兑换 |
| 产值积分 | not_allowed_without_cash_received | 到账后再进入正式口径 | 无到账不得列正式产值 |
| 潜在产值积分 | potential_value_candidate | 可跟踪客户确认或业务机会 | 不转正式产值 |
| AI 自购额度 | self_use_only | 可计量供合作单位参考 | 不进入统一收益池 |
| 贡献 / 共享 / 奖励额度 | candidate_only | 可登记来源和用途候选 | 不发放真实额度 |
| 收益池 | no_formal_revenue | 开票可作统计口径 | 无到账不分配 |
| 悬赏 | bounty_candidate_not_published | 可形成发布前置条件 | 未冻结资源不得发布 |
| 争议 | committee_candidate | 可登记触发条件 | 不由 AI 或 WAES 裁决 |

全局断言：`realKdsApiWrite=false`、`waesWrite=false`、`businessLedgerWrite=false`、`settlementWrite=false`、`ragAdmission=false`、`createsConfirmationFact=false`、`createsCommitteeDecision=false`。

## 10. dry-run 结论

| 项 | 结论 |
|---|---|
| 补证包字段验收 | dry-run 可表达退回、阻断、人工确认和委员会触发 |
| 金融凭证门禁 | DSR-L3 默认阻断成立，只能进入脱敏索引和人工/委员会路径 |
| 人工确认队列 | 已形成候选视图，不代表派发、签认或通过 |
| 委员会队列 | 已形成候选视图，不代表备案、裁决或结算 |
| 候选写回 | 仅 `candidate_only` / `no_write` |
| SOP 建议 | 仅 `suggestion_only` |
| GFIS 真实业务线 | 仍保持 `real_business_lane=repair_required` |
| 状态升级 | 不允许升级 `accepted`、`complete` 或 `integrated` |

## 11. 下一轮建议

建议 `GPCF-KDS-DKS-054` 进入“葛化 DKS-053 dry-run 结果到可填写执行包与责任方说明”，把本轮用例转成责任方可阅读的提交说明、字段示例、退回原因说明和人工确认准备清单，仍不派发真实请求。
