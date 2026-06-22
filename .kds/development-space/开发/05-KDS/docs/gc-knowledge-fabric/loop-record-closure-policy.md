---
doc_id: GPCF-DOC-2E5699ED35
title: LOOP Record Schema 与 Next-action Closure Gate
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/loop-record-closure-policy.md
source_path: docs/gc-knowledge-fabric/loop-record-closure-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Record Schema 与 Next-action Closure Gate

## 1. 定位

LOOP record 是 GC-Knowledge Fabric 每轮受控推进的最小治理证据。

它不负责自动把对象提升为完成状态，也不替代 Harness 验收、WAES 门禁、KWE 流程或人工/委员会确认。它只记录：

- 本轮目标。
- 输入资料。
- 新增对象。
- 新增缺口。
- 候选事实 / 候选 SOP。
- WAES 门禁结果。
- 人工确认事项。
- 委员会事项。
- 风险与阻塞。
- 下一轮动作。
- 本轮验证证据。

## 2. 最小字段

每条 LOOP record 至少包含：

- loopId
- tenantId
- projectId
- roundId
- goal
- inputRefs
- newObjectRefs
- newGapRefs
- candidateFactRefs
- candidateSopRefs
- waesResultRefs
- confirmationRefs
- committeeRefs
- riskRefs
- validationRefs
- nextActions
- closureGate
- createdBy
- createdAt

## 3. Next-action 最小字段

每条 next action 至少包含：

- actionId
- title
- priority
- ownerType
- ownerId
- requiredEvidenceRefs
- requiredGateRefs
- blockedByRefs
- status
- closeCondition

## 4. Closure Gate 规则

LOOP record 可以标记为 `closed_for_round` 的条件：

- 本轮验证项都有 evidence 或明确的 not_applicable 原因。
- P0/P1 next action 不得处于 open 或 blocked 且没有责任人。
- blocked next action 必须有 blocker reference 和下一步处理路径。
- 任何 accepted、integrated、生产就绪判定、正式写回、正式收益或积分确认均不得由 LOOP 自动生成。
- 若存在人工确认或委员会确认要求，LOOP 只能记录 `human_required` 或 `committee_required`，不能直接确认完成。

## 5. 禁止自动提升

LOOP record 不能自动执行：

- accepted 状态提升。
- integrated 状态提升。
- production ready 判定。
- GFIS/GPC/ERP/MES 正式写回。
- 收益分配。
- 积分确认。
- 额度划拨。
- 悬赏结算。
- 委员会裁决。
- 真实外部 API 写入。

## 6. 输出状态

Closure gate 只允许输出：

- open
- blocked
- repair_required
- evidence_ready
- closed_for_round

`closed_for_round` 只表示本轮工程记录完整，不表示业务完成或验收完成。

## 7. 本地验证边界

本规则当前只通过本地 OKF、shared type、fixture 和 validator 验证。

不得把本规则写成：

- LOOP 已替代 Harness 验收。
- LOOP 已替代 WAES/KWE。
- 业务事实、写回、收益、积分或委员会裁决已经完成。
- 真实接口同步已经完成。
