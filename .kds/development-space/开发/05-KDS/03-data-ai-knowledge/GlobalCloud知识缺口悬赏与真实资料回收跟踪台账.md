---
doc_id: GPCF-DOC-C60ECF8A71
title: GlobalCloud 知识缺口悬赏与真实资料回收跟踪台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md
source_path: 03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 知识缺口悬赏与真实资料回收跟踪台账

状态：`GPCF-KDS-DKS-025` 受控台账  
日期：2026-06-17  
适用范围：葛化物流预运营期订单、辽宁远航链路、湖北磷材拓厂项目、真实脱敏资料回收、知识缺口积分、悬赏候选、KDS 11 个底座资源池、增强治理账本、WAES 规则门禁、人工确认和委员会备案。

## 1. 定位

本文是 `GPCF-KDS-DKS-025` 的正式交付，用于把 `GPCF-KDS-DKS-024` 中 `returned_for_evidence` 的人工审核演练结果，转成可治理、可追踪、可悬赏候选化的知识缺口和真实脱敏资料回收任务。

本文只建立缺口台账、回收任务、候选悬赏、候选评分和状态机。本文不代表真实资料已经收到，不代表悬赏已经发布，不代表积分已经确认，不代表收益已经分配，不代表真实业务主账已经写入，不代表真实 KDS API 已同步，不代表 GFIS 运行层 SOP E2E 已完成。

## 2. 基本原则

1. 知识缺口、悬赏候选、回收任务、潜在产值、积分候选和 SOP 建议均为增强治理账本对象，必须挂接至少一个 KDS 11 底座资源池。
2. KDS 11 个底座资源池仍为订单池、运力池、产能池、资金池、政策池、装备池、数据池、能源池、原料池、人才池、场景池。
3. 积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本和贡献账本不新增底座，只作为增强治理账本挂接在 11 池之上。
4. AI 只能生成候选缺口、候选悬赏、候选评分、候选 SOP 和候选写回建议。
5. WAES 只确认规则、证据、权限、密级、边界和例外，不替代业务主账确认。
6. 人工确认负责接收、脱敏、来源、责任主体、业务适用性和退回补证判断。
7. 委员会负责积分、收益、悬赏、争议、重大违规、追溯扣减和分配参考事项。
8. 用户保留体系治理权、急停权和规则治理权，不承担日常裁决。
9. 合作单位自购 AI 额度先自用，不进入统一收益池或悬赏资源池。
10. 正式收入按到账确认，开票可作为统计、流程和财务口径记录。

## 3. 台账对象

| 对象 | 编号前缀 | 作用 | 生效边界 |
|---|---|---|---|
| KnowledgeGapRequest | `KGR` | 登记知识、证据、SOP、资料、订单、项目来源缺口 | 登记后仍为缺口，不等于悬赏发布 |
| RealSourceRecoveryTask | `RRT` | 跟踪真实脱敏来源回收、责任主体和审核状态 | 未收到资料前保持 `waiting_source` |
| KnowledgeGapBountyCandidate | `KGB` | 形成悬赏候选、可见范围、资源建议和验收标准 | 委员会或规则确认前不得发布 |
| CandidateScoringRecord | `CSR` | 对缺口紧急度、权威度、业务关联和可回收性评分 | 仅供排序，不确认积分 |
| GapClosureRecord | `GCR` | 缺口关闭、部分关闭、退回、争议和追溯记录 | 必须有来源、WAES 或人工证据 |

## 4. 必填字段

### 4.1 KnowledgeGapRequest

| 字段 | 含义 | 必填性 |
|---|---|---|
| requestId | 知识缺口编号 | 必填 |
| sourceRound | 来源 Loop 轮次 | 必填 |
| sourceCandidateRef | 来源候选对象 | 必填 |
| gapType | evidence / knowledge / sop / project_source / order_source / industry_source | 必填 |
| gapSummary | 缺口摘要 | 必填 |
| requester | 发起方，可为系统、人员或单位 | 必填 |
| ownerCandidate | 责任主体候选 | 必填 |
| kdsBasePools | KDS 11 底座资源池挂接 | 必填 |
| enhancedLedgerLinks | 增强治理账本挂接 | 必填 |
| visibility | public / semi_public / directed / private | 必填 |
| sensitivity | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 | 必填 |
| currentState | candidate / waiting_source / recovery_open / blocked / closed / disputed | 必填 |
| forbiddenClaims | 禁止声明 | 必填 |

### 4.2 RealSourceRecoveryTask

| 字段 | 含义 | 必填性 |
|---|---|---|
| recoveryTaskId | 资料回收任务编号 | 必填 |
| requestId | 关联缺口编号 | 必填 |
| requiredSources | 需要回收的来源索引或资料类型 | 必填 |
| sourceOwner | 来源责任主体 | 必填 |
| submitter | 提交人 | 条件必填 |
| receiver | 接收人 | 条件必填 |
| redactionMode | none / partial / metadata_only | 必填 |
| waesRequirement | 需要的 WAES 规则记录 | 必填 |
| humanReviewRequirement | 需要的人工确认 | 必填 |
| committeeRequirement | none / filing / decision | 必填 |
| dueHint | 建议回收时点 | 可选 |
| currentState | waiting_source / source_received_private / redaction_checked / received_redacted_candidate / returned / blocked / closed | 必填 |

### 4.3 KnowledgeGapBountyCandidate

| 字段 | 含义 | 必填性 |
|---|---|---|
| bountyCandidateId | 悬赏候选编号 | 必填 |
| requestId | 关联缺口编号 | 必填 |
| sponsorCandidate | 发起主体候选 | 必填 |
| rewardMixCandidate | 积分、现金、AI 额度或服务权益建议 | 必填 |
| frozenResourceState | not_frozen / pending_freeze / frozen | 必填 |
| acceptanceRule | 验收规则 | 必填 |
| disputeRule | 争议规则 | 必填 |
| visibility | public / semi_public / directed / private | 必填 |
| currentState | candidate_only / ready_for_committee / published / withdrawn / closed | 必填 |

## 5. 知识缺口总表

| requestId | 来源 | gapType | 缺口摘要 | 责任主体候选 | KDS 底座资源池 | 增强账本 | visibility | currentState |
|---|---|---|---|---|---|---|---|---|
| `KGR-GH-ORD-202606-0001` | `RHR-GH-ORD-202606-0001` | order_source / evidence / sop | 葛化预运营期订单候选缺真实来源索引、来源责任主体、目标工厂和 OEM 承接方责任拆分 | 葛化项目负责人 / 订单来源责任方 / OEM 承接方 | 订单池、资金池、产能池、数据池、场景池 | 潜在产值池、贡献账本、SOP 账本、悬赏池、争议池 | directed | candidate |
| `KGR-HBLC-FEA-202606-0001` | `RHR-HBLC-FEA-202606-0001` | project_source / knowledge / sop | 湖北磷材拓厂候选缺真实脱敏项目来源、区域资料、政策来源索引和项目负责人确认 | 湖北磷材项目负责人 / 区域来源责任方 | 装备池、产能池、政策池、数据池、场景池 | 贡献账本、积分池、悬赏池、SOP 账本、争议池 | directed | candidate |
| `KGR-GH-LY-202606-0001` | 辽宁远航链路既有缺口 | evidence / order_source | 辽宁远航链路缺客户确认、样箱反馈、POD、真实回执、KDS 回执和 WAES confirmation | 葛化项目负责人 / 订单责任方 / 相关承接方 | 订单池、运力池、资金池、数据池、场景池 | 潜在产值池、贡献账本、悬赏池、争议池 | directed | recovery_open |

## 6. 真实脱敏资料回收任务

### 6.1 葛化预运营期订单

| 字段 | 值 |
|---|---|
| recoveryTaskId | `RRT-GH-ORD-202606-0001` |
| requestId | `KGR-GH-ORD-202606-0001` |
| requiredSources | 电话纪要、会议纪要、邮件、平台线索、合作单位文件、目标工厂责任说明、OEM 承接方责任说明 |
| sourceOwner | `TBD` |
| redactionMode | partial |
| waesRequirement | 证据规则、密级规则、边界规则 |
| humanReviewRequirement | 来源责任主体、目标工厂、OEM 承接方和责任拆分人工确认 |
| committeeRequirement | filing_if_points_or_bounty |
| currentState | waiting_source |
| forbiddenClaims | 正式订单、到账、收益、质量放行、GFIS 主账写入、SOP 生效 |

### 6.2 湖北磷材拓厂项目来源

| 字段 | 值 |
|---|---|
| recoveryTaskId | `RRT-HBLC-FEA-202606-0001` |
| requestId | `KGR-HBLC-FEA-202606-0001` |
| requiredSources | 拓厂项目来源索引、区域资料、政策来源、第三方来源、装备或产能线索、项目负责人确认 |
| sourceOwner | `TBD` |
| redactionMode | partial / metadata_only |
| waesRequirement | 证据规则、密级规则、权威来源规则、边界规则 |
| humanReviewRequirement | 项目来源、政策来源和项目负责人确认 |
| committeeRequirement | filing_if_points_or_bounty |
| currentState | waiting_source |
| forbiddenClaims | 投资通过、合作确认、收益确认、GFIS 接入完成、新工厂模板正式生效 |

### 6.3 葛化辽宁远航链路

| 字段 | 值 |
|---|---|
| recoveryTaskId | `RRT-GH-LY-202606-0001` |
| requestId | `KGR-GH-LY-202606-0001` |
| requiredSources | 客户确认、样箱签收或反馈、POD、真实回执、KDS 回执、WAES confirmation、现代精工过渡责任材料 |
| sourceOwner | `TBD` |
| redactionMode | partial / metadata_only |
| waesRequirement | 证据规则、真实回执规则、密级规则、边界规则 |
| humanReviewRequirement | 客户链路、样箱链路、承接方链路和回执链路人工确认 |
| committeeRequirement | filing_if_points_bounty_or_potential_value |
| currentState | recovery_open |
| forbiddenClaims | 客户确认已取得、POD 已取得、KDS 回执已取得、WAES confirmation 已取得、GFIS verified artifact 已形成 |

## 7. 悬赏候选表

| bountyCandidateId | requestId | sponsorCandidate | rewardMixCandidate | frozenResourceState | acceptanceRule | disputeRule | visibility | currentState |
|---|---|---|---|---|---|---|---|---|
| `KGB-GH-ORD-202606-0001` | `KGR-GH-ORD-202606-0001` | 葛化项目组 / 平台激励池候选 | 知识积分候选 + SOP 贡献候选；不含自购 AI 额度 | not_frozen | 提交真实脱敏来源索引、责任拆分和 WAES 记录后，人工审核通过 | 一般争议先项目组协商，重大争议进委员会多数决 | directed | candidate_only |
| `KGB-HBLC-FEA-202606-0001` | `KGR-HBLC-FEA-202606-0001` | 湖北磷材项目组 / 平台激励池候选 | 知识积分候选 + 新工厂复制模板贡献候选；不含自购 AI 额度 | not_frozen | 提交拓厂来源索引、政策或第三方来源、项目负责人确认和 WAES 记录后，人工审核通过 | 一般争议先项目组协商，重大争议进委员会多数决 | directed | candidate_only |
| `KGB-GH-LY-202606-0001` | `KGR-GH-LY-202606-0001` | 葛化项目组 / 平台激励池候选 | 知识积分候选 + 潜在产值贡献候选；不含自购 AI 额度 | not_frozen | 提交客户确认、样箱反馈、POD 或真实回执之一并通过 WAES / 人工审核 | 涉及潜在产值或责任争议时进委员会备案或裁决 | directed | candidate_only |

## 8. 候选评分规则

候选评分只用于排序和资源建议，不确认正式积分。

| 维度 | 说明 | 建议分值 |
|---|---|---:|
| urgency | 是否阻断 GFIS SOP、订单运行母版、拓厂复制或资料入库 | 0-30 |
| sourceAuthority | 来源是否为责任主体、权威网站、政策标准、业务系统或第三方可信资料 | 0-25 |
| businessRelevance | 是否直接关联订单、产能、原料、拓厂、收入、POD 或质量门禁 | 0-25 |
| recoverability | 在当前阶段是否可由合作单位、项目组或责任主体补齐 | 0-15 |
| governanceClarity | 密级、权限、脱敏、验收和争议路径是否清晰 | 0-5 |
| confidentialityRisk | 涉密、隐私、合同和金融风险；该项为扣分或阻断项 | 0 到 -30 |

候选评分建议：

| requestId | urgency | sourceAuthority | businessRelevance | recoverability | governanceClarity | confidentialityRisk | candidateScore | 排序 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `KGR-GH-LY-202606-0001` | 30 | 20 | 25 | 10 | 4 | -10 | 79 | P0 |
| `KGR-GH-ORD-202606-0001` | 28 | 18 | 24 | 12 | 4 | -8 | 78 | P0 |
| `KGR-HBLC-FEA-202606-0001` | 22 | 18 | 21 | 12 | 4 | -6 | 71 | P1 |

## 9. 状态机

```text
gap_identified
  -> recovery_task_open
  -> redacted_source_received
  -> waes_rule_recorded
  -> human_review_pending
  -> committee_if_needed
  -> closed
```

退回和争议分支：

```text
returned_for_evidence
  -> recovery_task_open
blocked_by_classification
  -> metadata_only_required
disputed
  -> committee_decision
withdrawn
  -> archived
```

状态边界：

| 状态 | 可做事项 | 禁止事项 |
|---|---|---|
| gap_identified | 建立缺口候选 | 不发布悬赏，不计积分 |
| recovery_task_open | 指定补证任务和来源责任主体 | 不确认资料已收到 |
| redacted_source_received | 做脱敏候选审核 | 不进入业务主账 |
| waes_rule_recorded | 记录规则判断 | 不替代业务确认 |
| human_review_pending | 等待人工确认 | 不自动写回 |
| committee_if_needed | 进入积分、收益、悬赏或争议备案 | 不由 AI 裁决 |
| closed | 有证据关闭缺口 | 不追溯覆盖原始记录 |

## 10. 可见性与参与边界

1. 合作单位默认只能查看本单位资料、本单位贡献候选、本单位积分候选、本单位 AI 额度和本单位参与的悬赏事项。
2. 跨单位资料只有在公开规则、被邀请、被授权、参与悬赏或委员会必要审议时可见。
3. DSR-L2 资料默认只展示脱敏索引和摘要。
4. DSR-L3 资料默认只展示元数据，不进入普通 AI 问答。
5. 公开、半公开、定向、私密悬赏均需记录可见范围和验收规则。
6. 悬赏发布前必须冻结资源或形成明确资源来源备案。

## 11. SOP 写回建议

AI 可基于本台账向 GFIS 或其它业务系统生成候选事实和 SOP 建议，但必须区分以下类别：

| 类别 | 可生成内容 | 写回条件 | 当前状态 |
|---|---|---|---|
| 知识问答建议 | 缺口摘要、资料位置、补证路径 | KDS 可见范围内 | candidate |
| 使用助手建议 | 字段填写、责任拆分、流程提示 | 人工确认规则内 | candidate |
| 文档验收建议 | 缺字段、缺来源、缺脱敏、缺 WAES 记录 | 人工审核前 | candidate |
| SOP 建议 | 预运营期订单形成 SOP、拓厂来源评估 SOP、辽宁远航补证 SOP | WAES 规则记录 + 人工确认 | candidate |
| 业务系统候选事实 | 订单来源候选、项目来源候选、责任主体候选 | 不得自动进入主账；需人工确认和系统门禁 | blocked_until_confirmed |

## 12. 关闭条件

缺口关闭必须同时满足：

1. 回收任务中至少一个 requiredSources 已提交真实脱敏来源索引或元数据索引。
2. DSR 分级和脱敏检查完成。
3. WAES 规则记录完成或明确 pending 原因。
4. 人工审核作出 pass / partial / returned / blocked / disputed 决策。
5. 涉及积分、收益、悬赏、争议或重大违规时，完成委员会备案或裁决。
6. 关闭记录不包含正式订单、到账、收益、业务主账写入、POD、质量放行、accepted 或 integrated 的越权声明。

## 13. 本轮不处理范围

1. 不接收、保存或展示真实未脱敏资料正文。
2. 不发布真实悬赏，不冻结真实资源，不结算积分。
3. 不写 GFIS/GCFIS、GPC、PVAOS 或其它业务主账。
4. 不调用真实外部 API，不配置真实生产权限。
5. 不执行真实 KDS API 写入，不把本地镜像写成真实同步。
6. 不确认客户、供应商、价格、订单、合同、POD、到账、金融凭证、积分、收益、AI 额度或参数生效。

## 14. Definition of Done

| 检查项 | 状态 |
|---|---|
| 知识缺口对象字段 | done |
| 真实资料回收任务字段 | done |
| 悬赏候选字段 | done |
| 葛化预运营期订单缺口 | done |
| 湖北磷材拓厂项目来源缺口 | done |
| 辽宁远航链路缺口延续 | done |
| 候选评分规则 | done |
| 状态机和可见性边界 | done |
| SOP 写回建议边界 | done |
| LOOP evidence 待本轮记录纳入 | done |

本轮完成后，只证明知识缺口、真实资料回收任务和悬赏候选台账已经建立，不证明真实资料已收到、真实悬赏已发布、真实积分已确认、真实收益已分配、真实业务主账已写入或真实 KDS API 已同步。

## 15. 下一轮建议

`GPCF-KDS-DKS-026` 建议进入“首批资料回收包字段验收与候选 SOP 写回建议”：

1. 将 `RRT-GH-ORD-202606-0001`、`RRT-HBLC-FEA-202606-0001`、`RRT-GH-LY-202606-0001` 转成可填报回收包。
2. 形成字段级验收 checklist。
3. 输出候选 SOP 写回格式，但保持 `candidate` 和 `blocked_until_confirmed`。
4. 建立人工确认后的关闭记录模板。
