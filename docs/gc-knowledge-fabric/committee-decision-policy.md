---
doc_id: GPCF-DOC-391D3222B0
title: GC-Knowledge Fabric 委员会 DecisionRecord 输入输出与争议冻结规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/committee-decision-policy.md
source_path: docs/gc-knowledge-fabric/committee-decision-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 委员会 DecisionRecord 输入输出与争议冻结规则

## 1. 定位

本文件定义委员会处理积分确认、收益分配争议、重大违规、悬赏结算、潜在产值转正式产值、跨单位贡献争议、第三方池子分配、项目组内部争议、重大 RAG 强引用争议和收益池规则争议时的 DecisionRecord 输入输出契约。

委员会只生成治理域 DecisionRecord、冻结建议和后续动作，不直接写 GFIS/GPC/ERP/MES，不直接分配收益，不直接确认积分，不绕过 WAES/KWE/Harness。

## 2. Decision 输入契约

每个委员会决策请求至少必须包含：

- `decisionId`
- `tenantId`
- `issueRef`
- `decisionType`
- `triggerReason`
- `relatedObjectRefs`
- `evidenceRefs`
- `participants`
- `votingMethod`
- `requestedBy`
- `requiresFreezeReview`

## 3. Decision 输出契约

每个委员会决策输出至少必须包含：

- `decisionId`
- `result`
- `reasonCodes`
- `requiredActions`
- `freezeScope`
- `visibilityScope`
- `harnessEvidenceRef`
- `effectiveState`
- `writesBusinessSystem`
- `writesRevenueDistribution`
- `writesScoreConfirmation`
- `writesExternalApi`

## 4. 冻结范围

| 冻结范围 | 含义 |
|---|---|
| `object` | 冻结争议知识对象或候选对象 |
| `rag_admission` | 冻结 RAG 强引用或引用强度 |
| `contribution_score` | 冻结贡献积分确认 |
| `revenue_distribution` | 冻结收益分配 |
| `quota_transfer` | 冻结额度划拨 |
| `bounty_settlement` | 冻结悬赏结算 |
| `external_share` | 冻结外部共享 |

## 5. 硬边界

1. 委员会 DecisionRecord 必须位于 governance domain。
2. 委员会不能替代 WAES gate，只能引用 gate result 或要求重跑 gate。
3. 委员会不能直接写业务系统。
4. 委员会不能直接分配收益或确认积分；只能输出分配/确认建议和所需后续动作。
5. 重大争议、重大违规、收益分配争议、跨单位贡献争议必须允许冻结相关对象和台账。
6. 决策必须绑定 evidence refs 与 Harness evidence。
7. 外部账号默认只能看到授权视图，不能看到其他单位明细。

## 6. P0/P1 验收条件

- OKF 中有委员会 DecisionRecord IO policy。
- Shared Types 中有 decision input、decision output、freeze scope、reason code 和 no-write 断言。
- Validator 能检查输入输出字段、10 类委员会触发事项、7 类冻结范围、governance domain、WAES 不被替代和 no-write 断言。
