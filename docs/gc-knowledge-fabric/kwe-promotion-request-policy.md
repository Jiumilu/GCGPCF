---
doc_id: GPCF-DOC-3BD549C1C1
title: KWE Promotion Request No-write 规则
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-promotion-request-policy.md
source_path: docs/gc-knowledge-fabric/kwe-promotion-request-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# KWE Promotion Request No-write 规则

本文件定义 DKS-097 KWE Promotion Request 的最小契约。Promotion Request 是状态提升申请包，只能表达“建议从当前 lifecycle 进入目标 lifecycle 的审查请求”，不能直接修改 KDS lifecycle、不能形成正式事实、不能完成业务写回、不能确认收益或积分。

## 一、定位

Promotion Request 用于以下场景：

- `candidate -> reviewing`
- `reviewing -> repair_required`
- `repair_required -> evidence_ready`
- `evidence_ready -> verified`
- `verified -> accepted`
- `accepted -> published`
- `any -> frozen`

它负责把目标对象、当前状态、目标状态、来源、证据、WAES gate、KWE confirmation workpack、Harness evidence 和 reviewer requirement 放入一个可审查包。

## 二、必要字段

每个 Promotion Request 必须包含：

- `id`
- `tenantId`
- `targetObjectId`
- `targetObjectType`
- `currentLifecycle`
- `requestedLifecycle`
- `requestedBy`
- `requestActor`
- `sourceRefs`
- `evidenceRefs`
- `waesGateRefs`
- `workpackRefs`
- `harnessEvidenceRefs`
- `reviewerRequirement`
- `promotionStatus`
- `blockedReasons`
- `requiredActions`
- `noWrite`

## 三、状态提升边界

Promotion Request 必须遵守统一状态机：

- AI 只能申请 `draft`、`candidate`、`repair_required`，不能申请 `verified`、`accepted`、`published`。
- LOOP 不能申请 `verified`、`accepted`、`published`。
- `candidate -> reviewing` 必须有 source refs、pool/owner 边界和 KWE work item 或 workpack。
- `repair_required -> evidence_ready` 必须完成 required actions 并绑定 evidence。
- `evidence_ready -> verified` 必须有 WAES gate passed 和 Harness evidence。
- `verified -> accepted` 必须要求 human 或 committee，不得自动完成。
- `accepted -> published` 必须要求 redaction、external share、ACL 和 publication approval。
- `any -> frozen` 必须保留 freeze reason，且解冻不在本申请包内完成。

## 四、Promotion Status

允许状态：

- `draft_request`
- `ready_for_kwe_review`
- `repair_required`
- `waes_required`
- `human_required`
- `committee_required`
- `freeze_required`
- `blocked`

这些状态只描述申请包本身，不改变目标对象 lifecycle。

## 五、No-write 断言

Promotion Request validator 必须证明：

- `writesKdsLifecycle = 0`
- `writesAcceptedFact = 0`
- `writesPublishedObject = 0`
- `writesWaesGateResult = 0`
- `writesKweWorkItem = 0`
- `writesBusinessSystem = 0`
- `writesRevenueOrScoreConfirmation = 0`
- `writesExternalApi = 0`

## 六、验收口径

DKS-097 dry-run 至少覆盖：

- 可进入 KWE review 的候选对象。
- 证据缺口导致 repair required。
- evidence ready 到 verified 的 WAES required/human required。
- verified 到 accepted 必须 human/committee required。
- accepted 到 published 必须 redaction/external share/ACL 审查。
- AI 或 LOOP 越权申请 accepted/published 必须 blocked。
- 冻结申请必须 freeze required。

`pass` 只表示申请包结构和 no-write 边界可机检，不表示目标对象已经提升状态。
