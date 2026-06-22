---
doc_id: GPCF-DOC-312B5F9215
title: GlobalCloud 湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则

日期：2026-06-17  
状态：`candidate_writeback_rule`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接《GlobalCloud 湖北磷材 Brain 知识页候选评审实例包与人工填报示例》，把 DKS-036 中三类虚拟评审样例转成可执行但未生效的 SOP 候选写回规则：

1. 拓厂项目知识页候选进入项目组评审候选。
2. 行业资料页候选退回补权威来源。
3. 订单线索页候选保留候选态并补收益边界。

本文只定义候选写回结构，不表示：

- 湖北磷材已提交真实资料；
- Brain 页面已正式发布；
- SOP 已正式生效；
- KDS、WAES、GFIS、GPC 或其他业务系统已发生真实写入；
- 订单、开票、到账收入、潜在产值、积分、收益或悬赏已确认；
- 项目、投资、建设、合作、采购、生产或发货事实已成立。

## 2. 总规则

| 规则项 | 要求 |
|---|---|
| 输入来源 | 仅限 DKS-036 虚拟脱敏评审样例和后续人工确认的候选评审记录 |
| 输出类型 | SOP 候选控制点、候选 KDS 字段、候选 WAES 规则记录、Brain 页面候选状态、知识缺口任务 |
| 生效条件 | 人工确认、WAES 规则记录、必要时委员会确认后，才可进入对应流程 |
| 写回层级 | 先写入 KDS / Brain 候选层；不得直接写入 GFIS 主账或生产系统 |
| KDS 挂接 | 每条候选写回必须挂接至少一个 KDS 11 池 |
| 增强账本 | SOP 账本、贡献账本、悬赏池、潜在产值池等不得游离，必须挂接 KDS 11 池 |
| 收益口径 | 正式收入按到账确认；开票只作为统计、财务和流程口径 |
| AI 作用 | 生成候选事实、候选 SOP 建议、候选字段、候选缺口和候选门禁建议 |
| 禁止动作 | 不得直接形成正式 SOP、正式订单、开票收入、到账收入、积分分配、收益分配或真实系统写入 |

## 3. SOPCandidateControlPoint

| controlPointId | linkedReviewId | candidateSopSegment | controlPoint | kdsPoolRefs | enhancedLedgerRefs | requiredConfirmation | status |
|---|---|---|---|---|---|---|---|
| `SCP-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | 拓厂项目评审前控制点 | 来源完整、脱敏通过、KDS 池挂接、人工评分不低于 85、红线通过后，才可进入项目组评审候选；不得写成投资、合作或建设事实 | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | SOP 账本 / 贡献账本 / 悬赏池 | 人工确认 / WAES 记录 / 项目组确认 | candidate |
| `SCP-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | 行业资料可信来源补证控制点 | 行业资料缺权威来源、检索时间或适用范围时必须退回；不得升级为高可信政策或标准结论 | 政策池 / 数据池 / 场景池 | 贡献账本 / 悬赏池 | 人工确认 / WAES 记录 | candidate |
| `SCP-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | 订单线索收益边界控制点 | 电话、会议、邮件等需求起点只能形成订单线索候选；未取得正式订单、开票和到账材料前，不得写成正式收入 | 订单池 / 产能池 / 资金池 / 数据池 | 潜在产值池 / 贡献账本 / 悬赏池 | 人工确认 / 委员会条件触发 / WAES 记录 | candidate |

## 4. CandidateKdsFieldWriteback

| writebackId | linkedControlPointId | targetLayer | candidateFields | confirmationRequired | forbiddenUpgrade |
|---|---|---|---|---|---|
| `CKW-HBLC-FEA-202606-0001` | `SCP-HBLC-FEA-202606-0001` | KDS / Brain 候选层 | `pageStatus=project_review_candidate`; `sourceIndexStatus=complete`; `redactionStatus=pass`; `kdsPoolCheck=pass`; `manualScore=88`; `publishSuggestion=project_review` | 人工确认 / WAES 记录 / 项目组确认 | 不升级为 `investment_confirmed`、`construction_started`、`cooperation_confirmed` |
| `CKW-HBLC-IND-202606-0001` | `SCP-HBLC-IND-202606-0001` | KDS / Brain 候选层 | `pageStatus=returned`; `trustedSourceStatus=source_required`; `returnReason=missing_authoritative_source`; `publishSuggestion=keep_candidate` | 人工确认 / WAES 记录 | 不升级为 `trusted_standard_confirmed`、`policy_applicability_confirmed`、`T3_passed` |
| `CKW-HBLC-ORD-202606-0001` | `SCP-HBLC-ORD-202606-0001` | KDS / Brain 候选层 | `pageStatus=reviewing_candidate`; `sourceType=phone_or_meeting_or_email_lead`; `revenueBoundary=lead_only`; `potentialValueStatus=candidate_only`; `publishSuggestion=keep_candidate` | 人工确认 / 必要时委员会确认 / WAES 记录 | 不升级为 `official_order`、`invoice_revenue`、`cash_received_revenue`、`gfis_runtime_primary_key` |

## 5. CandidateWaesRuleWriteback

| waesRuleId | linkedControlPointId | gateType | candidateRule | ruleEffect | status |
|---|---|---|---|---|---|
| `CWR-HBLC-FEA-202606-0001` | `SCP-HBLC-FEA-202606-0001` | publish_boundary | 拓厂项目页达到来源、脱敏、KDS 挂接、人工评分和红线要求时，只能进入项目组评审候选 | 记录规则，不放行投资、合作或建设事实 | candidate |
| `CWR-HBLC-IND-202606-0001` | `SCP-HBLC-IND-202606-0001` | trusted_source | 行业资料缺权威来源、检索时间或适用范围时，必须退回补源 | 退回规则候选，不形成可信结论 | candidate |
| `CWR-HBLC-ORD-202606-0001` | `SCP-HBLC-ORD-202606-0001` | revenue_boundary | 电话、会议、邮件需求只形成订单线索候选；正式收入必须以到账为最终确认口径 | 记录边界，不形成正式订单或收入事实 | candidate |

## 6. BrainPageStatusCandidate

| statusCandidateId | linkedReviewId | currentStatus | nextCandidateStatus | allowedUserView | requiredEvidence |
|---|---|---|---|---|---|
| `BSC-HBLC-FEA-202606-0001` | `BPR-HBLC-FEA-202606-EX01` | reviewing | project_review_candidate | 项目组内可见；跨单位可见需权限确认 | 来源索引、脱敏记录、KDS 池挂接、人工评分、WAES 记录 |
| `BSC-HBLC-IND-202606-0001` | `BPR-HBLC-IND-202606-EX01` | returned | returned_source_required | 责任方和发起方可见；可发起知识缺口悬赏 | 权威来源链接、检索时间、适用范围 |
| `BSC-HBLC-ORD-202606-0001` | `BPR-HBLC-ORD-202606-EX01` | reviewing | lead_candidate_reviewing | 销售、渠道、项目组和授权人员可见 | 客户匿名编号、来源记录、需求时间、收益边界、潜在产值候选说明 |

## 7. ForbiddenWritebackList

| forbiddenId | 场景 | 禁止写回内容 | 原因 |
|---|---|---|---|
| `FWL-HBLC-202606-0001` | 所有场景 | 真实 KDS API 写入完成 | 本轮只做本地受控文档和候选规则，不做真实 API 写入 |
| `FWL-HBLC-202606-0002` | 所有场景 | WAES 已放行或规则已生效 | 本轮只形成候选规则和记录建议 |
| `FWL-HBLC-202606-0003` | 拓厂项目 | 投资确认、建设启动、合作确认、产线确定 | 缺真实项目确认和人工授权 |
| `FWL-HBLC-202606-0004` | 行业资料 | 权威政策结论、标准适用结论、高可信层级通过 | 缺权威来源、检索时间和适用范围 |
| `FWL-HBLC-202606-0005` | 订单线索 | 正式订单、开票收入、到账收入、GFIS 主账、运行层主键 | 电话、会议或邮件需求不等同正式订单和收入 |
| `FWL-HBLC-202606-0006` | 积分收益 | 正式积分、收益分配、悬赏成交、潜在产值确认 | 需要委员会、人工确认或收入到账证据 |
| `FWL-HBLC-202606-0007` | 权限发布 | 跨单位公开、外部发布、不可撤回发布 | 需要权限、脱敏、来源和发布门禁确认 |

## 8. HumanConfirmationChecklist

| checklistId | checkItem | passCondition | triggerRole |
|---|---|---|---|
| `HCC-HBLC-202606-0001` | 来源确认 | 有来源类型、时间、责任方、原始材料或可追溯索引 | 资料责任方 |
| `HCC-HBLC-202606-0002` | 脱敏确认 | 不含客户实名、敏感价格、未授权合同原文、个人信息或不可公开字段 | 项目组 / 治理方 |
| `HCC-HBLC-202606-0003` | KDS 池挂接 | 至少挂接一个 KDS 11 池，增强账本不得游离 | KDS 管理责任方 |
| `HCC-HBLC-202606-0004` | WAES 规则记录 | 发布、可信、收益边界等规则均有候选记录 | WAES 规则责任方 |
| `HCC-HBLC-202606-0005` | 积分收益边界 | 涉及积分、收益、潜在产值、悬赏或争议时，进入委员会或人工确认机制 | 委员会 / 治理方 |
| `HCC-HBLC-202606-0006` | 权限确认 | 页面可见范围、跨单位共享、第三方可见均有授权边界 | 平台治理方 |

## 9. 回撤与重评规则

| rollbackId | 触发条件 | 处理动作 | 保留证据 |
|---|---|---|---|
| `RR-HBLC-202606-0001` | 来源被证明不完整或不真实 | 页面降级为 returned 或 withdrawn_candidate | 原候选记录、退回原因、责任方、时间 |
| `RR-HBLC-202606-0002` | 脱敏或权限违规 | 立即暂停发布建议，必要时进入重大违规评议 | 原页面状态、访问范围、违规字段摘要 |
| `RR-HBLC-202606-0003` | 收益或订单边界误写 | 删除正式化表述，回退为线索候选或潜在产值候选 | 原写回建议、修正记录、委员会或人工意见 |
| `RR-HBLC-202606-0004` | WAES 规则不适用 | 回退规则候选，进入重新评审 | 规则版本、适用范围、退回说明 |

## 10. 完成定义

本文完成条件：

1. DKS-036 三类虚拟评审样例均转成 SOP 候选控制点。
2. 每个控制点均给出候选 KDS 字段、候选 WAES 规则和 Brain 页面候选状态。
3. 明确禁止把候选规则写成真实 SOP、真实订单、真实收入、真实 KDS API 写入或 WAES 放行。
4. 明确积分、收益、悬赏、潜在产值等增强账本必须挂接 KDS 11 池，并经人工或委员会确认。
5. 明确正式收入按到账确认，开票只作为统计、财务和流程口径。
6. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 11. DKS-038 建议

下一轮建议建立“湖北磷材 SOP 候选写回规则到缺口悬赏与人工确认任务包”，把本文候选规则进一步拆成可分派的人工确认任务、知识缺口悬赏任务、委员会触发条件和候选关闭标准。
