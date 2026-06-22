---
doc_id: GPCF-DOC-3620016ACE
title: KWE Approval Route Packet No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-approval-route-packet-policy.md
source_path: docs/gc-knowledge-fabric/kwe-approval-route-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# KWE Approval Route Packet No-write 规则

## 1. 定位

KWE Approval Route Packet 是 KWE 审批路径的只读路由包。

它承接 GFIS Writeback Approval Preflight Checklist，把每条候选写回映射到 KWE 展示队列：

- human_queue
- committee_queue
- metadata_only_queue
- repair_queue
- blocked_queue

它只生成路由建议和队列视图，不创建真实 KWE WorkItem，不改变 KDS 状态，不写 WAES Gate Result，不写 GFIS/GPC/ERP/MES，不确认收益或积分。

## 2. 输入

每个 route item 必须绑定：

- preflightRef
- candidateId
- targetSystem
- targetEntityType
- targetEntityId
- preflightStatus
- reviewerRequirement
- sensitiveHandling
- evidenceRefs
- waesGateRefs
- lifecycleAuditRefs
- requiredActions
- blockedReasons

## 3. 路由队列

| Preflight 状态 | Route Queue | Route Status |
|---|---|---|
| human_required | human_queue | route_ready |
| committee_required | committee_queue | route_ready |
| metadata_only_required | metadata_only_queue | route_ready |
| repair_required | repair_queue | repair_required |
| blocked | blocked_queue | blocked |
| preflight_required | repair_queue | preflight_required |

## 4. 禁止行为

Route Packet 不得：

- 创建真实 KWE WorkItem。
- 写 KDS lifecycle。
- 写 KDS fact 或 accepted fact。
- 写 WAES Gate Result。
- 写 GFIS/GPC/ERP/MES。
- 生成 business write approval。
- 生成 target receipt。
- 完成委员会决议。
- 确认收益、积分、额度或悬赏。
- 调用外部 API。

## 5. 强制规则

1. `blocked` 必须进入 blocked_queue。
2. `committee_required` 必须进入 committee_queue。
3. `human_required` 必须进入 human_queue。
4. `metadata_only_required` 必须进入 metadata_only_queue，且不能携带 raw content。
5. `repair_required` 和 `preflight_required` 必须进入 repair_queue。
6. route_ready 只代表队列路由完整，不代表审批完成。
7. 所有 no-write 计数必须为 0。

## 6. 与 DKS-101 的关系

DKS-101 判断写回审批前置状态。

DKS-102 把前置状态转换成 KWE 审批队列建议，供 Brain、PKC、GFIS 助手和 KWE Work Queue 展示。它仍然只是 no-write read model。
