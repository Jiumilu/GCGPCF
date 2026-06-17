---
doc_id: GPCF-DOC-95631D1C11
title: GlobalCloud 湖北磷材 Brain 知识页候选运行评审空白台账与发布前问题清单
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选运行评审空白台账与发布前问题清单.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选运行评审空白台账与发布前问题清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材 Brain 知识页候选运行评审空白台账与发布前问题清单

日期：2026-06-17  
状态：`planned_review_register`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-034 的湖北磷材 Brain 知识页候选结构与发布门禁，把六类页面候选转成可填报的运行评审空白台账、发布前问题清单、退回原因、发布建议和撤回登记。

本文只建立空白评审结构，不表示：

- 湖北磷材已经提交真实资料；
- DSR-L2 / DSR-L3 原文已经进入系统；
- 任何 Brain 页面已经发布；
- 任何人工评分、WAES 门禁、委员会裁决或收益分配已经完成；
- 任何 KDS、WAES、GFIS、GPC 或其他业务系统已经发生真实写入；
- 任何积分、收益、额度、悬赏、争议、潜在产值或 SOP 已经生效。

## 2. 运行评审总规则

| 项 | 规则 |
|---|---|
| 默认状态 | `blank_review_register` |
| 评审对象 | DKS-034 的 `BKP-HBLC-*` 页面候选 |
| 允许填报 | 来源索引、脱敏摘要状态、KDS 池挂接、增强账本挂接、人工评分、红线、问题、建议 |
| 禁止填报 | 未授权原文、客户订单原文、合同原文、供应商报价原文、个人敏感信息、跨单位不可见事实 |
| AI 角色 | 只能生成候选摘要、候选缺口、候选问题、候选 SOP 建议和候选写回建议 |
| 人工角色 | 负责评分、红线检查、退回原因、发布建议和责任确认 |
| WAES 角色 | 只确认规则、权限、证据、边界和例外，不替代业务主账 |
| 委员会角色 | 处理正式积分、收益、争议、重大违规、复议和规则适用差异 |
| 发布边界 | 未完成发布前检查不得从候选态升级为正式发布态 |
| 收益边界 | 到账才算正式收入；开票只作为统计、财务和流程口径 |

## 3. BrainPageReviewRegister 空白台账

| reviewId | linkedBrainPageId | pageType | reviewerRole | sourceIndexStatus | redactionStatus | kdsPoolCheck | ledgerCheck | waesGateStatus | manualScore | redlineStatus | publishSuggestion | currentStatus |
|---|---|---|---|---|---|---|---|---|---:|---|---|---|
| `BPR-HBLC-FEA-202606-0001` | `BKP-HBLC-FEA-202606-0001` | 拓厂项目知识页候选 | 人工评测人 / WAES 规则复核 | blank | blank | blank | blank | blank | 0 | blank | blank | planned |
| `BPR-HBLC-RAW-202606-0001` | `BKP-HBLC-RAW-202606-0001` | 原料知识页候选 | 人工评测人 / 原料责任方 | blank | blank | blank | blank | blank | 0 | blank | blank | planned |
| `BPR-HBLC-IND-202606-0001` | `BKP-HBLC-IND-202606-0001` | 行业资料页候选 | 人工评测人 / WAES 规则复核 | blank | blank | blank | blank | blank | 0 | blank | blank | planned |
| `BPR-HBLC-ORD-202606-0001` | `BKP-HBLC-ORD-202606-0001` | 订单线索页候选 | 人工评测人 / 销售责任方 | blank | blank | blank | blank | blank | 0 | blank | blank | planned |
| `BPR-HBLC-TPL-202606-0001` | `BKP-HBLC-TPL-202606-0001` | 新工厂复制模板页候选 | 人工评测人 / 模板编制责任方 | blank | blank | blank | blank | blank | 0 | blank | blank | planned |
| `BPR-HBLC-MIX-202606-0001` | `BKP-HBLC-MIX-202606-0001` | 治理映射页候选 | GPCF / WAES / KDS | blank | blank | blank | blank | blank | 0 | blank | blank | planned |

## 4. ReviewFieldDefinition

| field | allowedValue | meaning | hardStop |
|---|---|---|---|
| `sourceIndexStatus` | blank / missing / partial / complete / invalid | 来源索引状态 | invalid |
| `redactionStatus` | blank / pending / pass / return / block | 脱敏检查状态 | block |
| `kdsPoolCheck` | blank / missing / pass / mismatch | KDS 11 池挂接状态 | missing / mismatch |
| `ledgerCheck` | blank / not_applicable / pass / orphan / committee_required | 增强账本挂接状态 | orphan |
| `waesGateStatus` | blank / planned / record / return / block | WAES 规则门禁状态 | block |
| `manualScore` | 0-100 | 人工评测分；0 表示未评 | score_lt_85_when_publish |
| `redlineStatus` | blank / pass / return / block | 红线状态 | return / block |
| `publishSuggestion` | blank / keep_candidate / internal_draft / project_review / publish_ready / withdraw | 发布建议 | publish_ready_without_gates |
| `currentStatus` | planned / reviewing / returned / blocked / publish_ready_candidate / withdrawn | 当前状态 | blocked |

## 5. PrePublishIssueList 空白台账

| issueId | linkedReviewId | issueType | issueDescription | severity | ownerRole | requiredAction | dueStage | closeEvidence | status |
|---|---|---|---|---|---|---|---|---|---|
| `PPI-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-0001` | source_gap | 待填：拓厂资料来源索引、责任主体或时间戳缺口 | normal | 湖北磷材项目负责人 | 补齐脱敏摘要和来源索引 | before_project_review | pending | planned |
| `PPI-HBLC-RAW-202606-0001` | `BPR-HBLC-RAW-202606-0001` | redaction_gap | 待填：原料资料是否存在供应商、报价或质量敏感信息 | major | 原料责任方 | 完成脱敏与边界确认 | before_project_review | pending | planned |
| `PPI-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-0001` | trust_gap | 待填：行业资料权威来源、检索时间和适用范围是否完整 | normal | 行业资料责任方 | 补齐权威来源索引 | before_internal_draft | pending | planned |
| `PPI-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-0001` | revenue_boundary | 待填：订单线索是否误写成正式订单、开票或到账收入 | major | 销售或渠道责任方 | 区分线索、开票统计和到账收入 | before_project_review | pending | planned |
| `PPI-HBLC-TPL-202606-0001` | `BPR-HBLC-TPL-202606-0001` | reuse_boundary | 待填：葛化母版复用是否只复用结构、控制点和授权经验 | normal | 模板编制责任方 | 标注差异项和复用授权边界 | before_project_review | pending | planned |
| `PPI-HBLC-MIX-202606-0001` | `BPR-HBLC-MIX-202606-0001` | governance_gap | 待填：增强账本是否全部挂接 KDS 11 池并保留门禁记录 | major | GPCF / KDS / WAES | 补齐挂接关系和 evidence | before_publish_ready | pending | planned |

## 6. ReturnReasonCatalog

| returnReasonId | reasonType | appliesTo | returnCondition | nextAction |
|---|---|---|---|---|
| `RRC-HBLC-001` | source_missing | FEA / RAW / IND / ORD / TPL / MIX | 缺少来源索引、责任主体或时间戳 | 退回补证 |
| `RRC-HBLC-002` | redaction_failed | FEA / RAW / ORD / TPL | 含未授权原文、商业敏感信息或个人敏感信息 | 退回脱敏或阻断 |
| `RRC-HBLC-003` | trust_layer_unclear | IND / FEA / RAW | 可信层级、检索时间或适用范围不完整 | 退回补充来源 |
| `RRC-HBLC-004` | kds_pool_missing | all | 页面未挂接 KDS 11 池 | 退回补齐挂接 |
| `RRC-HBLC-005` | orphan_ledger | all | 增强账本脱离 KDS 11 池 | 退回治理映射 |
| `RRC-HBLC-006` | waes_block | all | WAES 门禁为 block | 阻断发布并登记原因 |
| `RRC-HBLC-007` | manual_score_low | all | 人工评分低于发布阈值 | 保持候选或内部草案 |
| `RRC-HBLC-008` | revenue_boundary_mixed | ORD | 混淆订单线索、开票统计和到账收入 | 退回财务口径澄清 |
| `RRC-HBLC-009` | reuse_fact_mixed | TPL | 把葛化事实直接复制为湖北磷材事实 | 退回差异项确认 |
| `RRC-HBLC-010` | permission_unclear | all | 可见范围、不可见字段或邀请关系不清 | 退回权限过滤配置 |

## 7. PublishSuggestionRule

| suggestion | allowedWhen | forbiddenWhen | nextRecord |
|---|---|---|---|
| `keep_candidate` | 来源、脱敏、评分或门禁未完成 | 无 | 保持候选评审记录 |
| `internal_draft` | 脱敏通过但来源或评分仍不完整 | 红线 return / block | 内部草案登记 |
| `project_review` | 来源、脱敏、KDS 挂接和权限过滤基本完整 | WAES block 或重大红线 | 项目组评审登记 |
| `publish_ready` | 发布前门禁全部通过，人工评分达标，WAES 记录存在 | 涉及正式积分、收益、争议但未进入委员会 | 发布准备候选记录 |
| `withdraw` | 来源错误、权限事故、重大违规或合作单位撤回授权 | 无 | 撤回登记 |

## 8. WithdrawalRegister 空白台账

| withdrawalId | linkedBrainPageId | trigger | requestedBy | action | ledgerImpact | committeeRequired | evidenceRequired | status |
|---|---|---|---|---|---|---|---|---|
| `WDR-HBLC-FEA-202606-0001` | `BKP-HBLC-FEA-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | conditional | 来源复核记录 | planned |
| `WDR-HBLC-RAW-202606-0001` | `BKP-HBLC-RAW-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | conditional | 脱敏复核记录 | planned |
| `WDR-HBLC-IND-202606-0001` | `BKP-HBLC-IND-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | conditional | 可信来源复核记录 | planned |
| `WDR-HBLC-ORD-202606-0001` | `BKP-HBLC-ORD-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | conditional | 订单边界复核记录 | planned |
| `WDR-HBLC-TPL-202606-0001` | `BKP-HBLC-TPL-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | conditional | 复用授权复核记录 | planned |
| `WDR-HBLC-MIX-202606-0001` | `BKP-HBLC-MIX-202606-0001` | blank | blank | withdraw_or_downgrade | candidate_only | yes_if_major | 治理映射复核记录 | planned |

## 9. KnowledgeGapBountyCandidate

| bountyCandidateId | linkedIssueId | gapType | proposedPoints | eligibleParticipants | settlementRule | status |
|---|---|---|---:|---|---|---|
| `KGB-HBLC-FEA-202606-0001` | `PPI-HBLC-FEA-202606-0001` | 拓厂来源补证 | 0 | 湖北磷材项目组 / 受邀合作单位 | 发起方与参与方协商，必要时委员会备案 | planned |
| `KGB-HBLC-RAW-202606-0001` | `PPI-HBLC-RAW-202606-0001` | 原料资料脱敏与质量指标补证 | 0 | 原料责任方 / 受邀合作单位 | 按知识贡献候选记录，正式积分需确认 | planned |
| `KGB-HBLC-IND-202606-0001` | `PPI-HBLC-IND-202606-0001` | 权威政策/标准来源补证 | 0 | 所有授权人员或单位 | T3 可信来源升级需保留来源证据 | planned |
| `KGB-HBLC-ORD-202606-0001` | `PPI-HBLC-ORD-202606-0001` | 订单线索补证 | 0 | 销售责任方 / 渠道方 / 受邀合作单位 | 无到账前只能列入知识或潜在产值候选 | planned |
| `KGB-HBLC-TPL-202606-0001` | `PPI-HBLC-TPL-202606-0001` | 母版复用差异项补证 | 0 | 模板编制责任方 / 葛化授权人员 | 复用贡献按协商或委员会规则处理 | planned |
| `KGB-HBLC-MIX-202606-0001` | `PPI-HBLC-MIX-202606-0001` | KDS 11 池与增强账本映射补证 | 0 | GPCF / KDS / WAES | 进入治理贡献候选，需 evidence | planned |

## 10. 硬停止规则

出现以下情形时不得进入发布准备候选：

1. 来源索引缺失或无法追溯责任主体。
2. 脱敏检查未通过。
3. 页面未挂接 KDS 11 池。
4. 增强账本脱离 KDS 11 池。
5. WAES 门禁为 block。
6. 红线状态为 return 或 block。
7. 人工评分低于发布阈值却被建议发布。
8. 订单线索被写成正式订单、开票或到账收入。
9. 葛化母版事实被直接复制成湖北磷材事实。
10. 任何候选记录试图触发真实 API 写入、生产主账写入或外部通知发送。

## 11. 完成定义

本文完成条件：

1. 六类 Brain 页面候选均具备空白评审记录。
2. 字段定义覆盖来源、脱敏、KDS 挂接、增强账本、WAES、人工评分、红线、发布建议和状态。
3. 发布前问题清单覆盖拓厂、原料、行业、订单、模板和治理映射六类缺口。
4. 退回原因、发布建议和撤回登记均具备统一编号。
5. 知识缺口悬赏候选保持 planned，积分为候选参考，不形成正式积分交易。
6. 所有输出只形成候选，不确认真实事实、正式积分、正式收益或正式 SOP。
7. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 12. DKS-036 建议

下一轮建议建立“湖北磷材 Brain 知识页候选评审实例包与人工填报示例”，使用虚拟脱敏样例演示一条拓厂页面、一条行业资料页面和一条订单线索页面如何从候选态进入评审态，但仍不接收真实资料、不形成正式发布。
