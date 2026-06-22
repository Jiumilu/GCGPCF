---
doc_id: GPCF-DOC-EBE9E75E8B
title: Revenue Contribution Attribution Packet 归因包规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/revenue-contribution-attribution-packet-policy.md
source_path: docs/gc-knowledge-fabric/revenue-contribution-attribution-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Revenue Contribution Attribution Packet 归因包规则

本文件定义 DKS-096 收益/贡献归因包的最小受控边界。归因包只用于把 `RevenueRecord`、`ContributionRecord`、evidence、WAES gate、KWE/委员会触发原因组织成可审查候选，不代表收益分配、积分确认、额度转移、悬赏结算或业务系统写回完成。

## 一、定位

归因包解决的问题是：

- 说明某笔收益或机会与哪些贡献候选相关。
- 说明归因依据来自到账、开票、合同、机会、渠道或知识价值估算中的哪一种。
- 说明是否具备进入收益分配候选审查的最低条件。
- 说明是否需要补证、人工确认、委员会审查或冻结。
- 为 Brain/PKC/治理台账展示提供只读审查材料。

归因包不做：

- 不确认贡献积分。
- 不分配收益。
- 不把潜在收益转正式收益。
- 不把开票收入当作已到账收入。
- 不转移 AI 额度。
- 不结算悬赏。
- 不写 GFIS/GPC/ERP/MES/KDS 正式事实。
- 不调用外部 API。

## 二、对象字段

每个归因包必须包含：

- `id`：归因包编号。
- `tenantId`：租户编号。
- `projectId`：项目编号。
- `revenueRef`：关联 `RevenueRecord`。
- `contributionRefs`：关联 `ContributionRecord` 列表。
- `revenueType`：收益类型。
- `revenueBasis`：收益依据。
- `attributionBasis`：归因依据。
- `evidenceRefs`：证据引用。
- `waesGateRefs`：门禁记录引用。
- `confidence`：候选置信度。
- `attributionStatus`：归因状态。
- `committeeRequired`：是否需要委员会。
- `freezeRecommended`：是否建议冻结。
- `distributionCandidateOnly`：是否仅为收益分配候选材料。
- `noWrite`：所有写入计数必须为 0。

## 三、正式收益候选条件

只有同时满足以下条件，归因包才能标记为 `distribution_candidate`：

- `revenueType = formal_revenue`。
- `revenueBasis = cash_received`。
- 至少有一条 `evidenceRefs`。
- 至少有一条 `waesGateRefs`。
- 关联贡献中至少一条已由人工或委员会确认。
- 无冻结建议。
- `noWrite.writesRevenueDistribution = 0`。

`distribution_candidate` 仍然只是候选材料。正式分配必须进入 KWE/委员会或授权流程，并形成 Harness evidence。

## 四、开票、潜在、渠道与知识价值边界

开票收入：

- 可作为财务统计。
- 不得作为正式收益分配依据。
- 不得绕过到账证据进入 `distribution_candidate`。

潜在收益：

- 只能记录机会或合同参考。
- 不得自动升为正式收益。
- 涉及潜在转正式时必须触发委员会或授权审查。

渠道机会：

- 可记录渠道贡献。
- 可进入渠道积分候选。
- 不得直接进入正式收益分配。

知识潜在价值：

- 可记录知识贡献和潜在价值说明。
- 不得作为正式收益或产值分配依据。

## 五、委员会与冻结触发

以下情况必须触发委员会或冻结建议：

- 潜在收益申请转正式收益。
- 跨单位贡献比例争议。
- 收益池规则争议。
- 贡献主体边界不清。
- 重大违规或恶意违规。
- evidence 与收益依据不一致。
- WAES Revenue Gate 或 Contribution Gate 返回 `committee_required`、`freeze_required`、`blocked`。

委员会可形成 `DecisionRecord`、建议、冻结或解冻意见，但不能在归因包内直接完成收益分配或积分确认。

## 六、Dry-run 验收口径

DKS-096 验收只允许读取本地 OKF、fixture、shared type 和 validator：

- 至少覆盖正式收益、开票收入、潜在收益、渠道机会、争议冻结 5 类样例。
- 正式收益候选数必须可统计。
- 开票收入必须为统计口径。
- 潜在收益不得自动转正式。
- 渠道机会不得直接分配。
- 冻结建议必须可统计。
- `scoreConfirmations = 0`。
- `revenueDistributions = 0`。
- `quotaTransfers = 0`。
- `bountySettlements = 0`。
- `businessWrites = 0`。
- `externalApiWrites = 0`。

## 七、底线

归因包是审查材料，不是裁决结果。任何正式收益、积分、额度、悬赏或业务状态变化，都必须另走 WAES、KWE、人工/委员会、Harness evidence 和业务系统授权链路。
