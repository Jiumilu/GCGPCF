---
doc_id: GPCF-DOC-1978124720
title: KWE Action Validation Workpack No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-action-validation-workpack-policy.md
source_path: docs/gc-knowledge-fabric/kwe-action-validation-workpack-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# KWE Action Validation Workpack No-write 规则

## 1. 定位

KWE Action Validation Workpack 是 DKS-104 `KWE Queue Action Intake Request` 之后的本地 dry-run 校验工包。

它负责把 Brain、PKC、GFIS Assistant 提交的 action request 转为可审查的 validation workpack 候选，用于检查：

- actor 是否具备动作权限；
- route 与 source view 是否一致；
- payload / evidence 是否满足动作最低要求；
- metadata-only 请求是否没有原文或敏感正文；
- blocked request 是否带有 blocked reasons；
- committee / freeze 请求是否仍停留在候选态；
- 后续 required followups 是否完整。

## 2. No-write 边界

Validation Workpack 只能作为校验候选，不得直接执行以下动作：

- 创建真实 KWE WorkItem；
- 修改 KDS lifecycle；
- 写入 KDS fact 或 accepted fact；
- 写入 WAES Gate Result；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 3. 输入

每个 validation workpack 必须引用一个 DKS-104 action request。

最低输入：

- `requestRef`
- `routeRef`
- `sourceViewRef`
- `surface`
- `actorId`
- `actionType`
- `payloadRefs`
- `evidenceRefs`
- `blockedReasons`
- `requiredFollowups`

## 4. 校验项

| check | 说明 |
|---|---|
| actor_permission | actor 是否允许在该 surface 发起动作 |
| route_consistency | request route 是否与来源队列视图一致 |
| payload_integrity | payload refs 是否存在且不是原文泄露 |
| evidence_presence | 动作是否满足 evidence 最低要求 |
| metadata_only_boundary | metadata-only 请求是否只引用元数据、哈希、摘要 |
| blocked_reason_presence | blocked / freeze 请求是否保留阻断原因 |
| no_write_guard | 是否保持所有写入计数为 0 |

## 5. 校验状态

| status | 说明 |
|---|---|
| validation_passed | 可进入下一步候选审查，但仍不创建任务 |
| repair_required | 缺少 payload / evidence / followup，需要补齐 |
| committee_review_candidate | 可进入委员会审查候选，不代表决议完成 |
| freeze_review_candidate | 可进入冻结审查候选，不代表冻结执行 |
| blocked | 阻断保持，不允许审批或写回 |

## 6. 产出

Validation Workpack 产出只包含：

- 校验状态；
- 校验项明细；
- accepted payload / evidence refs；
- rejected refs；
- required followups；
- validation notes；
- no-write 计数。

## 7. 与 KWE 的关系

Validation Workpack 不是 KWE WorkItem。

只有后续经过 WAES、KWE、人工或委员会确认，并由明确 API / 流程授权后，才可能创建真实 KWE WorkItem。本规则不授权任何真实写入。
