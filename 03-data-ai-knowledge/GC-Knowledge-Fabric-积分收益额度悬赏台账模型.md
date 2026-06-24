---
doc_id: GPCF-DOC-0C9C673398
title: GC-Knowledge Fabric 积分收益额度悬赏台账模型
project: KDS
related_projects: [WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-积分收益额度悬赏台账模型.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-积分收益额度悬赏台账模型.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 积分收益额度悬赏台账模型

## 1. 定位

本模型定义 Contribution、Revenue、Quota、Bounty 四类台账的 P0 口径。四类台账都必须区分候选、确认、冻结和证据状态。

## 2. Contribution 台账

| 字段 | 说明 |
|---|---|
| contributorType / contributorId | 贡献主体 |
| contributionType | 知识、证据、SOP、纠错、渠道、订单、验收、争议处理 |
| relatedObjectRefs | 关联知识对象 |
| poolRefs | 挂接十一池 |
| candidateScore | 候选积分 |
| confirmedScore | 确认积分 |
| confirmationStatus | candidate / human_confirmed / committee_confirmed / rejected / frozen |
| revenueRelated | 是否关联收益 |

## 3. Revenue 台账

| revenueType | 口径 |
|---|---|
| formal_revenue | 已到账收入，可作为正式收益依据 |
| invoiced_revenue | 已开票收入，可作财务统计 |
| potential_revenue | 未到账但可追踪机会 |
| channel_opportunity | 渠道机会 |
| knowledge_potential_value | 知识潜在价值 |

正式收益必须以到账为准。潜在收益、渠道机会和知识潜在价值不得自动转为正式收益分配依据。

## 4. Quota 台账

| quotaType | 口径 |
|---|---|
| platform_quota | 平台统一提供 |
| self_purchased_quota | 合作单位自购，先自用，不进入统一收益池 |
| contributed_quota | 合作单位贡献给体系 |
| shared_quota | 项目或单位共享额度 |
| reward_quota | 积分兑换或激励额度 |

## 5. Bounty 台账

悬赏必须绑定 GapRecord，并记录发布方、提交方、验收结果、争议期、结算方式和 evidence。AI 初审只能形成建议，不能直接结算。

## 6. 冻结规则

发生重大违规、恶意污染、跨权限使用、收益争议或委员会触发事项时，相关积分、收益、额度、悬赏可进入 `frozen`，并写入 governance evidence。
