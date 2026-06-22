---
doc_id: GPCF-DOC-E5F419F29C
title: Brain PKC Revenue Attribution Read Model No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/brain-pkc-revenue-attribution-read-model-policy.md
source_path: docs/gc-knowledge-fabric/brain-pkc-revenue-attribution-read-model-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Brain PKC Revenue Attribution Read Model No-write 规则

本文件定义 DKS-099 Brain/PKC 收益归因只读模型。该模型用于展示收益/贡献归因包、收益口径、贡献候选、WAES/KWE 状态、委员会/冻结提示和可见性，不确认积分，不分配收益，不暴露未授权单位明细。

## 一、定位

Brain 视图用于治理、指挥舱、委员会和收益/贡献中心聚合查看。

PKC 视图用于个人、团队或项目成员查看自己被授权的归因、贡献、候选收益、争议和待办。

Read model 不做：

- 不确认 contribution score。
- 不分配 revenue。
- 不把 potential revenue 转 formal revenue。
- 不修改 KDS lifecycle。
- 不写 KWE work item。
- 不落 WAES gate result。
- 不写 GFIS/GPC/ERP/MES。
- 不调用外部 API。

## 二、必要字段

每个 read model 必须包含：

- `viewId`
- `surface`
- `tenantId`
- `viewerId`
- `projectId`
- `scope`
- `attributionPacketRefs`
- `visibleRevenueRefs`
- `visibleContributionRefs`
- `maskedContributionRefs`
- `waesGateRefs`
- `kweWorkpackRefs`
- `committeeRefs`
- `freezeRefs`
- `visibility`
- `displayMode`
- `blockedActions`
- `noWrite`

## 三、Surface 与 Scope

允许的 surface：

- `brain`
- `pkc`

允许的 scope：

- `governance_overview`
- `project_revenue_contribution`
- `my_revenue_candidates`
- `my_contributions`
- `committee_review`

Brain 可展示聚合、项目级、治理级和委员会审查视图，但跨单位明细必须按 ACL 掩码。

PKC 默认只能展示 viewer 自己或被授权项目内的贡献和候选收益，不默认展示其他单位明细。

## 四、Visibility 与 Display Mode

可见性：

- `own_only`
- `project_authorized`
- `governance_aggregate`
- `committee_authorized`

展示模式：

- `summary_only`
- `metadata_only`
- `authorized_detail`
- `masked_cross_unit`

跨单位争议、收益池争议、潜在收益、渠道机会和敏感财务证据默认不得直接展示其他单位明细。

## 五、Blocked Actions

Brain/PKC read model 必须显式阻断：

- `confirm_score`
- `distribute_revenue`
- `promote_potential_revenue`
- `override_waes_gate`
- `complete_committee_decision`
- `write_business_system`
- `mutate_kds_lifecycle`
- `call_external_api`

## 六、验收口径

DKS-099 dry-run 至少覆盖：

- Brain 治理聚合视图。
- Brain 委员会授权视图。
- PKC 我的贡献与候选收益视图。
- PKC 跨单位争议 masked 视图。

所有视图必须保持 no-write，且不得出现未授权跨单位明细泄露。
