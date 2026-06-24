---
doc_id: GPCF-DOC-6CE82BFD9A
title: GFIS Writeback Approval Preflight No-write Checklist 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-writeback-approval-preflight-policy.md
source_path: docs/gc-knowledge-fabric/gfis-writeback-approval-preflight-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Writeback Approval Preflight No-write Checklist 规则

## 1. 定位

GFIS Writeback Approval Preflight Checklist 是 GFIS 候选写回进入人工或委员会审批前的只读检查清单。

它承接：

- GFIS Writeback Candidate Batch Diff。
- KDS Lifecycle Transition Audit Packet。
- WAES gate refs。
- Evidence / Harness evidence refs。
- KWE workpack 或 committee review refs。

它只判断写回候选下一步应进入 human_required、committee_required、metadata_only_required、repair_required 或 blocked，不产生正式 approval，不写业务系统。

## 2. 输入

每个 preflight item 必须绑定：

- batchDiffRef
- candidateId
- targetSystem
- targetEntityType
- targetEntityId
- lifecycleAuditRefs
- fieldPaths
- evidenceRefs
- waesGateRefs
- harnessEvidenceRefs
- sensitiveHandling
- waesGateStatus
- lifecycleAuditStatus
- reviewerRequirement

## 3. 输出状态

| 状态 | 含义 |
|---|---|
| preflight_required | 资料存在，但仍需进入审批前置队列 |
| human_required | 需要业务负责人或授权人工确认 |
| committee_required | 需要委员会确认 |
| metadata_only_required | 只能写入元数据引用或受控原件位置，不能暴露原文 |
| repair_required | 缺少来源、证据、字段、Harness evidence 或 WAES 条件 |
| blocked | 明确禁止进入写回审批 |

## 4. 禁止行为

Preflight Checklist 不得：

- 把 `approvalEligible` 设为 true。
- 把 `businessWriteAllowed` 设为 true。
- 写 GFIS/GPC/ERP/MES。
- 写 KDS accepted fact。
- 写 KDS lifecycle。
- 写 WAES Gate Result。
- 创建真实 KWE WorkItem。
- 生成目标系统 receipt。
- 确认收益或积分。
- 调用外部 API。

## 5. 强制规则

1. `waesGateStatus=blocked` 必须输出 `blocked`。
2. `waesGateStatus=committee_required` 必须输出 `committee_required`。
3. `waesGateStatus=human_required` 且非敏感 metadata-only 场景，必须输出 `human_required`。
4. `sensitiveHandling=metadata_only` 必须输出 `metadata_only_required` 或 blocked。
5. `sensitiveHandling=controlled_original` 必须有 evidenceRefs，不得暴露原文。
6. lifecycle audit 为 `blocked` 时必须输出 `blocked`。
7. 缺 evidenceRefs 或缺 lifecycleAuditRefs 时必须输出 `repair_required` 或 `blocked`。
8. preflight 通过只代表可以进入审批路径，不代表写回批准、业务完成、收益确认或积分确认。

## 6. 与 DKS-098 / DKS-100 的关系

DKS-098 负责展示候选写回字段差异。

DKS-100 负责展示 KDS 生命周期流转是否具备审计条件。

DKS-101 只把两者组合成写回审批前置检查清单，用于 Brain、GFIS 助手、KWE 审批队列展示，不写任何正式系统。
