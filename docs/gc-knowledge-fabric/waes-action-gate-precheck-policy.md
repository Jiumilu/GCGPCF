---
doc_id: GPCF-DOC-56866C0959
title: WAES Action Gate Precheck No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/waes-action-gate-precheck-policy.md
source_path: docs/gc-knowledge-fabric/waes-action-gate-precheck-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAES Action Gate Precheck No-write 规则

## 1. 定位

WAES Action Gate Precheck 是 DKS-105 `KWE Action Validation Workpack` 之后的本地 dry-run 前置门禁候选。

它负责把 validation workpack 转为 WAES gate precheck 候选，用于提前判断后续可能需要哪些 WAES Gate，但不生成正式 WAES Gate Result。

## 2. 适用范围

本规则覆盖以下前置检查：

- source gate precheck；
- evidence gate precheck；
- permission / DSR gate precheck；
- sensitive data gate precheck；
- writeback gate precheck；
- committee gate precheck；
- freeze gate precheck。

## 3. No-write 边界

Precheck 只能产生本地候选结论，不得直接执行以下动作：

- 写入 `waes_gate_results`；
- 创建真实 KWE WorkItem；
- 修改 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 4. 输入

每个 precheck 必须引用一个 DKS-105 validation workpack。

最低输入：

- `precheckId`
- `workpackRef`
- `tenantId`
- `projectId`
- `routeRef`
- `actionType`
- `requestedGateTypes`
- `precheckStatus`
- `reasonCodes`
- `requiredActions`
- `reviewerRequirement`
- `harnessEvidenceRequired`
- `createsWaesGateResult`
- `createsKweWorkItem`
- `promotesLifecycle`
- `noWrite`

## 5. 状态

| status | 说明 |
|---|---|
| precheck_passed | 可进入下一步 gate 候选审查，不代表 gate 通过 |
| repair_required | 缺少来源、证据、权限或 metadata-only 边界确认 |
| human_required | 需要人工确认 |
| committee_required | 需要委员会候选审查 |
| freeze_required | 需要冻结候选审查 |
| blocked | 阻断保持，不允许审批或写回 |

## 6. 输出

Precheck 输出只包含：

- 候选 gate 类型；
- 前置状态；
- reason codes；
- required actions；
- reviewer requirement；
- harness evidence requirement；
- no-write 计数。

## 7. 与 WAES 的关系

WAES Action Gate Precheck 不是正式 WAES Gate Result。

只有后续经过 WAES API / KWE 流程 / 人工或委员会授权后，才可能形成真实 `waes_gate_results`。本规则不授权任何真实写入。
