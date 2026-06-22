---
doc_id: GPCF-DOC-8454CB5BDD
title: GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练

日期：2026-06-17  
状态：`virtual_rehearsal_only`  
批次：`PILOT-HBLC-KDS-202606-0002`

## 1. 定位

本文承接 DKS-039《GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批空白执行台账》，用虚拟脱敏样例演练“底座可用知识闭环率”如何驱动人工确认、退回补源、悬赏候选、委员会触发和硬停止。

本文不是实际填报记录，不接收真实资料，不证明真实来源、真实订单、真实收入、真实项目进展或真实业务完成。所有样例均为 `virtual_sample`，不得写入真实 KDS API、WAES 放行、Brain 正式页面、GFIS、GPC、PVAOS 或任何业务系统主账。

## 2. 演练目标

1. 验证 DKS-039 的空白执行字段能承载拓厂、行业、订单三类典型样例。
2. 验证“底座可用知识闭环率”可以区分可有限引用、候选修复、退回补源和硬停止。
3. 验证缺口悬赏候选不会被误写成已发布悬赏。
4. 验证人工确认和委员会机制不会被 AI 代替。
5. 验证开票、到账、潜在产值、正式收入和自购 AI 额度边界仍然清晰。

## 3. 评分口径

沿用 DKS-039：

```text
底座可用知识闭环率 =
状态覆盖率 x 20%
+ 事实成熟度 DQ x 25%
+ 来源/证据合格率 x 20%
+ registry/台账/报告一致性 x 15%
+ 自动化处理有效率 x 10%
+ 写回缺口闭环率 x 10%
```

本轮采用虚拟判定等级：

| 分数区间 | 虚拟判定 | 允许动作 | 禁止动作 |
|---:|---|---|---|
| 85-100 | `safe_reuse_candidate` | 可作为受控知识候选进入人工发布前复核 | 不自动发布、不自动进入强经营引用 |
| 70-84 | `limited_report_candidate` | 可进入有限报告候选，必须显示待确认或置信度 | 不进入 RAG 强引用，不写业务主账 |
| 60-69 | `repair_candidate` | 可形成补源、悬赏或人工确认任务 | 不关闭缺口，不确认事实 |
| 50-59 | `return_for_source` | 退回补源或补责任主体 | 不进入报告，不进入 RAG |
| 0-49 | `blocked_or_invalid` | 阻断、退回或触发违规审查 | 不进入任何业务链路 |

若出现一票否决项，即使分数较高，也必须按硬停止处理。

## 4. 虚拟样例集

| sampleId | linkedRegisterId | sampleType | virtualInputSummary | statusCoverage | dqScore | evidencePassRate | consistencyRate | automationEffectiveness | writebackClosureRate | calculatedRate | virtualDecision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `VRS-HBLC-FEA-202606-0001` | `MER-HBLC-FEA-202606-0001` | 拓厂项目来源样例 | 虚拟区域政策摘要、虚拟项目会议纪要摘要、虚拟负责人确认占位齐备，但缺第三方佐证 | 100 | 65 | 60 | 80 | 0 | 30 | 63.25 | `repair_candidate` |
| `VRS-HBLC-IND-202606-0001` | `MER-HBLC-IND-202606-0001` | 行业权威来源样例 | 虚拟权威标准链接、检索时间、适用范围齐备，但尚未完成人工可信层级确认 | 100 | 82 | 90 | 85 | 0 | 40 | 75.25 | `limited_report_candidate` |
| `VRS-HBLC-ORD-202606-0001` | `MER-HBLC-ORD-202606-0001` | 订单线索样例 | 虚拟电话纪要摘要有需求方向，但缺客户匿名编号、责任人确认和收益边界 | 100 | 45 | 35 | 50 | 0 | 20 | 47.75 | `blocked_or_invalid` |
| `VRS-HBLC-ORD-202606-0002` | `MER-HBLC-ORD-202606-0002` | 越权收入样例 | 虚拟线索被错误写成正式订单和正式收入 | 100 | 30 | 20 | 20 | 0 | 0 | 34.50 | `blocked_or_invalid` |

## 5. 样例判定与动作

### 5.1 拓厂项目来源样例

| 字段 | 虚拟填报 |
|---|---|
| linkedTask | `MCT-HBLC-FEA-202606-0001` |
| executionState | `source_submitted_candidate` |
| sourceReceiptStatus | `metadata_received` |
| waesRecordStatus | `planned` |
| humanReviewStatus | `pending` |
| committeeStatus | `none` |
| bountyStatus | `candidate_only` |
| settlementStatus | `prohibited_before_acceptance` |
| calculatedRate | 63.25 |
| decision | `repair_candidate` |

动作建议：

1. 形成第三方来源补证任务。
2. 可生成 `BAC-HBLC-FEA-202606-0001` 的悬赏准备建议，但不得发布。
3. 人工确认前不得发布 Brain 页面或写入正式 SOP。
4. 不进入经营强引用。

### 5.2 行业权威来源样例

| 字段 | 虚拟填报 |
|---|---|
| linkedTask | `MCT-HBLC-IND-202606-0001` |
| executionState | `source_submitted_candidate` |
| sourceReceiptStatus | `metadata_received` |
| waesRecordStatus | `planned` |
| humanReviewStatus | `pending` |
| committeeStatus | `not_required` |
| bountyStatus | `candidate_only` |
| settlementStatus | `prohibited_before_acceptance` |
| calculatedRate | 75.25 |
| decision | `limited_report_candidate` |

动作建议：

1. 可进入有限报告候选，但必须标注待人工可信层级确认。
2. RAG 强引用仍需 `canonical`、证据等级、敏感信息和 `rag_include` 门禁。
3. 未确认前不得升级为高可信政策或标准适用结论。
4. 若适用范围发生争议，再触发 `CTC-HBLC-IND-202606-0001`。

### 5.3 订单线索样例

| 字段 | 虚拟填报 |
|---|---|
| linkedTask | `MCT-HBLC-ORD-202606-0001` |
| executionState | `returned` |
| sourceReceiptStatus | `returned` |
| waesRecordStatus | `blocked` |
| humanReviewStatus | `returned` |
| committeeStatus | `none` |
| bountyStatus | `candidate_only` |
| settlementStatus | `prohibited_before_acceptance` |
| calculatedRate | 47.75 |
| decision | `blocked_or_invalid` |

动作建议：

1. 退回补客户匿名编号、责任主体、需求时间和收益边界。
2. 只可作为知识缺口或线索缺口候选，不可作为订单事实。
3. 不得进入潜在产值池正式贡献，只能保留为潜在产值候选。
4. 不得进入 GFIS 主账、正式收入、正式产值或收益分配。

### 5.4 越权收入样例

| 字段 | 虚拟填报 |
|---|---|
| linkedTask | `MCT-HBLC-ORD-202606-0002` |
| executionState | `blocked` |
| sourceReceiptStatus | `blocked` |
| waesRecordStatus | `blocked` |
| humanReviewStatus | `blocked` |
| committeeStatus | `decision_planned` |
| bountyStatus | `withdrawn` |
| settlementStatus | `prohibited_before_acceptance` |
| calculatedRate | 34.50 |
| decision | `blocked_or_invalid` |

动作建议：

1. 触发 `CTC-HBLC-ORD-202606-0002` 的违规评议候选。
2. 立即撤回相关悬赏候选，不冻结或发放任何积分、收益或 AI 额度。
3. 一般违规酌情溯源扣除；重大违规按事实比例或全部扣除，由委员会机制处理。
4. 用户只保留规则治理权和急停权，不替代委员会日常裁决。

## 6. 缺口写回候选

| writebackCandidateId | linkedSampleId | gapType | proposedTarget | requiredHumanAction | status |
|---|---|---|---|---|---|
| `WBC-HBLC-FEA-202606-0001` | `VRS-HBLC-FEA-202606-0001` | missing_third_party_source | `MER-HBLC-FEA-202606-0001.evidenceSlot` | 项目组补第三方来源或说明不适用 | candidate_only |
| `WBC-HBLC-IND-202606-0001` | `VRS-HBLC-IND-202606-0001` | missing_trust_level_confirmation | `MER-HBLC-IND-202606-0001.humanReviewStatus` | 行业资料责任方和 WAES 规则复核人确认可信层级 | candidate_only |
| `WBC-HBLC-ORD-202606-0001` | `VRS-HBLC-ORD-202606-0001` | missing_order_lead_boundary | `MER-HBLC-ORD-202606-0001.evidenceSlot` | 销售或渠道责任方补匿名编号、责任人和收益边界 | candidate_only |
| `WBC-HBLC-ORD-202606-0002` | `VRS-HBLC-ORD-202606-0002` | invalid_revenue_claim | `CER-HBLC-ORD-202606-0002.evidenceSlot` | 委员会机制备案或裁决，用户可急停越权写回 | candidate_only |

## 7. 悬赏候选处理

| linkedSampleId | bountyCandidate | action | boundary |
|---|---|---|---|
| `VRS-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | 可准备补源悬赏草案 | 不发布、不冻结资源、不结算积分 |
| `VRS-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | 暂不发布，先走人工可信层级确认 | 不以 AI 判断替代来源确认 |
| `VRS-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | 退回补源后再评估 | 无到账不得确认正式产值 |
| `VRS-HBLC-ORD-202606-0002` | `BAC-HBLC-ORD-202606-0002` | 撤回候选并触发违规评议候选 | 不冻结、不结算、不分配 |

## 8. RAG 与指挥舱边界

| 样例 | RAG 强引用 | 有限报告 | 指挥舱强引用 | 原因 |
|---|---|---|---|---|
| `VRS-HBLC-FEA-202606-0001` | no | no | no | 缺第三方来源和人工确认 |
| `VRS-HBLC-IND-202606-0001` | no | candidate | no | 来源较完整，但可信层级未确认 |
| `VRS-HBLC-ORD-202606-0001` | no | no | no | 订单线索边界缺失 |
| `VRS-HBLC-ORD-202606-0002` | no | no | no | 一票否决，误写正式收入 |

## 9. 演练结论

1. “底座可用知识闭环率”可以把状态覆盖与事实成熟、证据、台账一致性、自动化和写回闭环分开判断。
2. 状态覆盖率高不等于事实可用；缺证据、缺人工确认或缺写回闭环时仍必须保持候选状态。
3. 有限报告候选仍不等于 RAG 强引用或经营强引用。
4. 越权收入、正式订单、主账写回等错误必须直接硬停止，并触发委员会机制候选。
5. AI 可以生成写回候选、补源建议和风险提示，但不得关闭缺口、发布悬赏、结算积分、分配收益或写业务主账。

## 10. DKS-041 建议

下一轮建议建立“底座可用知识闭环率计算样表与字段字典”，把本文虚拟样例中的六个评分维度拆成可复用字段、评分来源、证据要求和一票否决规则，供葛化、湖北磷材及后续工厂复制线共用。
