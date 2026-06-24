---
doc_id: GPCF-DOC-5916BC5419
title: Brain PKC KWE Queue Read Model No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/brain-pkc-kwe-queue-read-model-policy.md
source_path: docs/gc-knowledge-fabric/brain-pkc-kwe-queue-read-model-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Brain PKC KWE Queue Read Model No-write 规则

## 1. 定位

Brain PKC KWE Queue Read Model 是 KWE 审批路由包的多入口只读视图。

它承接 DKS-102 KWE Approval Route Packet，把 human queue、committee queue、metadata-only queue、repair queue、blocked queue 转换为 Brain、PKC、GFIS Assistant 可读的队列视图。

它只展示队列摘要、授权可见项、阻断原因、敏感处理状态和后续动作，不创建 KWE WorkItem，不执行审批，不改变 KDS 状态，不写 GFIS/GPC/ERP/MES。

## 2. Surface

允许的 surface：

- `brain`
- `pkc`
- `gfis_assistant`

Brain 可以展示项目级与治理级聚合。

PKC 默认只能展示 viewer 自己或被授权项目内的 KWE 队列项。

GFIS Assistant 只能展示与 GFIS 写回候选相关的审批路径提示，不能输出正式审批结论。

## 3. Scope

允许的 scope：

- `kwe_queue_overview`
- `my_kwe_tasks`
- `gfis_writeback_queue`
- `committee_queue`
- `blocked_queue`

## 4. 必要字段

每个 read model 必须包含：

- viewId
- surface
- tenantId
- viewerId
- projectId
- scope
- routePacketRefs
- visibleRouteRefs
- maskedRouteRefs
- queueSummary
- filter
- visibility
- displayMode
- blockedActions
- noWrite

## 5. 阻断动作

Read model 必须显式阻断：

- create_kwe_work_item
- complete_approval
- complete_committee_decision
- approve_gfis_writeback
- mutate_kds_lifecycle
- write_waes_gate_result
- write_business_system
- call_external_api

## 6. No-write 边界

Read model 不得：

- 创建真实 KWE WorkItem。
- 完成人工确认或委员会决议。
- 写 KDS lifecycle / fact / accepted fact。
- 写 WAES Gate Result。
- 写 GFIS/GPC/ERP/MES。
- 写 target receipt。
- 确认收益、积分、额度或悬赏。
- 调用外部 API。

## 7. 验收口径

DKS-103 dry-run 至少覆盖：

- Brain 项目队列聚合视图。
- Brain 委员会队列视图。
- PKC 我的 KWE 待办视图。
- GFIS Assistant 写回审批提示视图。
- blocked queue 只读视图。

所有视图必须保持 no-write，且不得出现未授权跨单位 route 明细泄露。
