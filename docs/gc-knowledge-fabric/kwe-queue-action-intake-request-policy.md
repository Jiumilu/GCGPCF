---
doc_id: GPCF-DOC-9181F60312
title: KWE Queue Action Intake Request No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-queue-action-intake-request-policy.md
source_path: docs/gc-knowledge-fabric/kwe-queue-action-intake-request-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# KWE Queue Action Intake Request No-write 规则

## 1. 定位

KWE Queue Action Intake Request 是 Brain、PKC、GFIS Assistant 队列视图中的用户动作请求包。

它承接 DKS-103 KWE Queue Read Model，把用户点击、补证、提交说明、请求修复、转委员会、冻结建议等输入记录为 request-only 材料。

它不创建真实 KWE WorkItem，不更新队列状态，不执行审批，不改变 KDS lifecycle，不写 GFIS/GPC/ERP/MES。

## 2. 支持动作

允许的 actionType：

- `submit_evidence`
- `request_repair`
- `escalate_committee`
- `request_freeze`
- `add_comment`
- `metadata_only_review`
- `acknowledge_blocked`

## 3. 必要字段

每个 action request 必须包含：

- requestId
- tenantId
- projectId
- sourceViewRef
- routeRef
- surface
- actorId
- actionType
- actionStatus
- payloadRefs
- evidenceRefs
- requiredFollowups
- blockedReasons
- createsKweWorkItem
- noWrite

## 4. Action 状态

| 状态 | 含义 |
|---|---|
| intake_received | 已接收输入，但未写任何系统 |
| validation_required | 需要补齐字段、权限、证据或 WAES 条件 |
| committee_request_candidate | 仅为委员会请求候选 |
| freeze_request_candidate | 仅为冻结请求候选 |
| blocked | 输入被阻断 |

## 5. 禁止行为

Action Intake Request 不得：

- 创建真实 KWE WorkItem。
- 写 KDS lifecycle / fact / accepted fact。
- 写 WAES Gate Result。
- 写 GFIS/GPC/ERP/MES。
- 完成人工确认或委员会决议。
- 生成 target receipt。
- 确认收益、积分、额度或悬赏。
- 调用外部 API。

## 6. 强制规则

1. committee queue 的转委员会动作只能形成 `committee_request_candidate`。
2. blocked queue 只能形成 acknowledge 或 freeze candidate，不得变成 approval。
3. submit evidence 必须至少有 evidenceRefs 或 payloadRefs。
4. metadata-only review 不得携带 raw content。
5. 所有 action request 的 createsKweWorkItem 必须为 false。
6. 所有 no-write 计数必须为 0。

## 7. 与 DKS-103 的关系

DKS-103 负责展示 KWE 队列视图。

DKS-104 负责记录用户从这些视图发起的动作意图。它是后续真实 KWE 工单创建前的输入材料，不是执行结果。
