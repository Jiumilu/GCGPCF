---
doc_id: GPCF-DOC-147F80FD46
title: GC-Knowledge Fabric KDS Lifecycle Transition Audit Packet No-write 规则
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kds-lifecycle-transition-audit-packet-policy.md
source_path: docs/gc-knowledge-fabric/kds-lifecycle-transition-audit-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KDS Lifecycle Transition Audit Packet No-write 规则

## 1. 定位

KDS Lifecycle Transition Audit Packet 是 KDS 对象生命周期变化的只读审计包。

它用于记录一次状态流转是否具备来源、证据、WAES 门禁、KWE 工包、Harness evidence、人工或委员会确认、发布控制和冻结理由等条件。

它不是 KDS 生命周期写入接口，不是 KWE promotion 执行器，不是 WAES Gate Result 生成器，也不是业务系统写回凭证。

## 2. 适用范围

本规则覆盖以下状态流转审计：

| 流转 | 审计重点 | 允许输出 |
|---|---|---|
| candidate -> reviewing | 来源、KWE 工包、初始归集边界 | ready_for_review |
| reviewing -> repair_required | WAES 发现缺证、缺字段、缺权限或敏感处理要求 | repair_required |
| evidence_ready -> verified | Harness evidence 与 WAES 条件是否齐备 | waes_required / human_required |
| verified -> accepted | 是否具备人工或委员会确认条件 | human_required / committee_required |
| accepted -> published | 脱敏、外部共享、发布审批是否齐备 | publication_required |
| any -> frozen | 冻结原因、治理证据、权限边界 | freeze_required |
| archived / superseded -> any active state | 终态对象不得重新进入写回、收益或 RAG 强引用链 | blocked |

## 3. 标准字段

Audit Packet 必须包含：

- auditId
- tenantId
- targetObjectId
- targetObjectType
- fromLifecycle
- toLifecycle
- transitionActor
- promotionRequestRefs
- sourceRefs
- evidenceRefs
- waesGateRefs
- workpackRefs
- harnessEvidenceRefs
- decisionRefs
- reviewerRequirement
- auditStatus
- blockedReasons
- requiredActions
- noWrite

## 4. 审计状态

| 状态 | 含义 |
|---|---|
| ready_for_review | 条件足以进入人工或 KWE 复核，但尚未改变 KDS 状态 |
| repair_required | 存在证据、字段、来源、权限或敏感处理缺口 |
| waes_required | 需要 WAES 继续执行门禁判断 |
| human_required | 需要人工确认 |
| committee_required | 需要委员会确认 |
| publication_required | 需要发布、脱敏、外部共享控制 |
| freeze_required | 需要冻结或维持冻结 |
| blocked | 明确禁止该流转 |

## 5. No-write 边界

Audit Packet 必须保持以下计数为 0：

- writesKdsLifecycle
- writesAcceptedFact
- writesPublishedObject
- writesWaesGateResult
- writesKweWorkItem
- writesBusinessSystem
- writesRevenueOrScoreConfirmation
- writesExternalApi

审计通过不等于业务完成。审计包不得把对象状态写成 verified、accepted、published 或 frozen，也不得确认收益、积分、产值、写回结果或 RAG 强引用。

## 6. 强制门禁

1. AI 与 LOOP 不得把 verified、accepted、published 审计为已批准，只能形成 blocked 或 required 状态。
2. accepted 必须具备 human_required 或 committee_required 的 reviewerRequirement。
3. published 必须包含 redaction_gate、external_share_gate、publication_approval 三类动作。
4. frozen 必须有冻结原因或冻结动作。
5. archived、superseded 等终态对象不得重新进入 active 生命周期。
6. verified、accepted、published 等高信任流转必须绑定 Harness evidence。
7. Harness evidence 只能证明审计发生，不代表业务系统已写入或收益已分配。

## 7. 与 KWE Promotion Request 的关系

KWE Promotion Request 是状态提升申请材料。KDS Lifecycle Transition Audit Packet 是对该申请材料和上下游证据的只读审计结果。

两者都不能直接写 KDS lifecycle；真正状态变更必须由授权执行路径在 WAES、KWE、人工或委员会确认后另行执行，并进入 Harness evidence。
