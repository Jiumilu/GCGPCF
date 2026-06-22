---
doc_id: GPCF-DOC-1946E4144B
title: WAES Precheck Bundle Read Model No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/waes-precheck-bundle-read-model-policy.md
source_path: docs/gc-knowledge-fabric/waes-precheck-bundle-read-model-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAES Precheck Bundle Read Model No-write 规则

## 1. 定位

WAES Precheck Bundle Read Model 是 DKS-106 `WAES Action Gate Precheck` 之后的只读聚合视图。

它把多个 precheck 候选聚合给 Brain、KWE、GFIS Assistant 使用，帮助不同入口展示：

- 候选 gate 类型；
- precheck 状态分布；
- reason code 摘要；
- required action 摘要；
- reviewer requirement；
- blocked action；
- evidence requirement；
- no-write 边界。

## 2. 入口范围

本轮只覆盖三类只读入口：

- Brain governance / review 视图；
- KWE validation queue 视图；
- GFIS Assistant writeback guidance 视图。

## 3. No-write 边界

Read Model 不得直接执行以下动作：

- 写入 `waes_gate_results`；
- 创建真实 KWE WorkItem；
- 修改 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 4. 最小字段

每个 bundle 必须包含：

- `bundleId`
- `surface`
- `tenantId`
- `projectId`
- `scope`
- `precheckRefs`
- `routeRefs`
- `gateSummary`
- `reasonCodeSummary`
- `requiredActions`
- `reviewerRequirements`
- `blockedActions`
- `canCreateWaesGateResult`
- `canCreateKweWorkItem`
- `canPromoteLifecycle`
- `noWrite`

## 5. 只读动作规则

允许展示：

- view_precheck_summary；
- view_required_actions；
- view_reason_codes；
- view_reviewer_requirement；
- view_harness_evidence_hint。

必须阻断：

- create_waes_gate_result；
- create_kwe_work_item；
- promote_lifecycle；
- write_business_system；
- complete_committee_decision；
- confirm_revenue_or_score。

## 6. 与 WAES / KWE 的关系

WAES Precheck Bundle Read Model 不是 WAES Gate Result，也不是 KWE WorkItem。

它只让 Brain、KWE 和 GFIS Assistant 安全读取 precheck 聚合状态。任何真实 gate result、task、lifecycle 或业务写回都必须进入后续受控流程。
