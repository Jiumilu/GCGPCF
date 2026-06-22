---
doc_id: GPCF-DOC-E716105009
title: GC-Knowledge Fabric 统一状态机与状态提升规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/status-machine-policy.md
source_path: docs/gc-knowledge-fabric/status-machine-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 统一状态机与状态提升规则

## 1. 定位

本文件定义 GC-Knowledge Fabric P0 状态机硬规则，解决 KnowledgeObject、FactCandidate、SOPCandidate、WritebackCandidate、ContributionRecord、RevenueRecord、GapRecord、DecisionRecord 等对象在 KDS、WAES、KWE、Harness、Brain、PKC 和 GFIS/GPC 之间的统一状态语义。

本文件不是业务裁决记录，不把任何对象提升为正式事实，不触发 GFIS/GPC/ERP/MES 写回，不结算收益、积分、额度或悬赏。

## 2. 统一生命周期状态

| 状态 | 含义 | 可创建方 | 可提升方 | RAG 边界 | 写回边界 | 收益/积分边界 |
|---|---|---|---|---|---|---|
| `draft` | 草稿或未归集材料 | 用户、AI、系统、合作单位 | owner 或 KWE | 不可强引用 | 不可写回 | 不可计入 |
| `candidate` | 候选对象，已入 KDS 候选域但未确认 | 用户、AI、系统、合作单位 | KWE | 最多弱引用或缺口提示 | 不可写回 | 只能形成候选贡献 |
| `reviewing` | 已进入人工、KWE 或委员会审查 | KWE | 人工或委员会 | 视 WAES 结果 limited 或 blocked | 不可正式写回 | 只能形成候选记录 |
| `repair_required` | 来源、证据、权限、字段或责任边界缺口待补 | WAES、KWE | KWE | 不可做结论 | 不可写回 | 不可确认 |
| `evidence_ready` | 证据包已齐备，等待 WAES 或人工确认 | KWE、Harness | WAES、人工或委员会 | limited | 不可正式写回 | 可进入候选审查 |
| `verified` | 通过规则核验，但尚未完成业务验收 | KDS、WAES、KWE | 授权人或委员会 | limited 或 safe | 仅可进入写回候选 | 可进入候选积分/收益 |
| `accepted` | 授权人或委员会完成验收 | 授权人、委员会 | KDS | safe 或 limited | 可按规则进入正式写回 | 可按规则进入正式审查 |
| `published` | 已批准对外或跨域发布 | 授权发布人 | KDS | 按发布范围引用 | 不能反向改写业务主账 | 不作为新增收益事实 |
| `frozen` | 因争议、违规、权限或收益风险被冻结 | WAES、委员会、治理方 | 委员会或授权治理方 | blocked | 禁止写回 | 禁止结算 |
| `superseded` | 已被新版本、修订事实或后续决议替代 | KDS、委员会 | KDS | 不可作为当前事实强引用 | 禁止写回 | 不作为当前结算依据 |
| `archived` | 已归档，仅保留审计和追溯 | KDS | KDS | metadata 或 limited | 禁止写回 | 不作为当前结算依据 |

## 3. 状态提升硬规则

1. AI 只能创建 `draft`、`candidate` 或建议进入 `repair_required`，不能直接提升为 `verified`、`accepted`、`published`。
2. LOOP 只能记录 evidence 和下一步建议，不能自动完成 `accepted`、`published`、收益确认或业务写回。
3. 模板只能进入 `draft`、`candidate` 或 `published` 的模板资产；模板不能自动成为项目事实。
4. `candidate -> reviewing` 必须有来源登记、池挂接、责任主体和 KWE work item。
5. `reviewing -> repair_required` 必须有 WAES reason code、required actions 或 evidence gap。
6. `repair_required -> evidence_ready` 必须补齐 required actions，并绑定 evidence refs。
7. `evidence_ready -> verified` 必须通过 WAES 对应 gate，并保留 Harness evidence。
8. `verified -> accepted` 必须有人工确认或委员会确认，不能由 Agent、LOOP、dashboard 或普通 assistant 自动完成。
9. `accepted -> published` 必须通过 redaction、external share、ACL 和发布审批。
10. 任意状态均可因重大争议、违规、权限不明或收益争议进入 `frozen`。
11. `frozen` 只能由委员会或授权治理方解除，不能由 AI、普通用户或自动化脚本解除。
12. `superseded` 与 `archived` 为终态，不得再进入写回、收益分配或 RAG 强引用链路。

## 4. 操作准入矩阵

| 状态 | 可检索 | 可 RAG 强引用 | 可写回候选 | 可正式写回 | 可贡献候选 | 可收益确认 |
|---|---|---|---|---|---|---|
| `draft` | owner 范围 | 否 | 否 | 否 | 否 | 否 |
| `candidate` | 授权范围 | 否 | 否 | 否 | 是 | 否 |
| `reviewing` | 授权范围 | 否 | 否 | 否 | 是 | 否 |
| `repair_required` | 授权范围 | 否 | 否 | 否 | 否 | 否 |
| `evidence_ready` | 授权范围 | 否 | 否 | 否 | 是 | 否 |
| `verified` | 授权范围 | 条件允许 | 是 | 否 | 是 | 候选 |
| `accepted` | 授权范围 | 条件允许 | 是 | 允许按业务门禁执行 | 是 | 条件允许 |
| `published` | 发布范围 | 条件允许 | 否 | 否 | 否 | 否 |
| `frozen` | governance 范围 | 否 | 否 | 否 | 否 | 否 |
| `superseded` | 审计范围 | 否 | 否 | 否 | 否 | 否 |
| `archived` | 审计范围 | 否 | 否 | 否 | 否 | 否 |

## 5. 与 WAES / KWE / Harness 的关系

- WAES 负责给出 gate status、reason codes、required actions、allowed operations 和 next state 建议。
- KWE 负责把候选对象编排成 work item、confirmation workpack、gap、bounty、redaction、publication、dispute 或 committee review。
- Harness 负责保存 evidence、acceptance、audit、committee decision、agent used knowledge 和 permission change record。
- KDS 负责持久化状态，不替代人工或委员会裁决。
- Brain/PKC 只能展示状态、入口和待办，不能强改 KDS 状态。

## 6. P0 验收条件

- OKF 中有独立状态机 policy。
- Shared Types 中有统一状态、状态提升 actor、allowed operations 和 no-write 断言。
- KnowledgeObject schema 的 lifecycle 枚举与状态机保持一致。
- Validator 能检查状态全集、终态、AI/LOOP 禁止提升边界、正式写回与收益结算边界。
- 本轮所有验证只使用本地文件和 fixture，不触达真实 KDS API、GFIS/GPC 业务系统或外部 API。
