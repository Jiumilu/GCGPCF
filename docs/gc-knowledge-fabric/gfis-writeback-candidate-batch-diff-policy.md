---
doc_id: GPCF-DOC-23F8320542
title: GFIS Writeback Candidate Batch Diff No-write 规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-writeback-candidate-batch-diff-policy.md
source_path: docs/gc-knowledge-fabric/gfis-writeback-candidate-batch-diff-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Writeback Candidate Batch Diff No-write 规则

本文件定义 DKS-098 GFIS Writeback Candidate Batch Diff 的最小契约。Batch diff 只用于批量展示候选写回字段差异、WAES gate 结果、KWE 后续动作和敏感处理要求，不代表 GFIS/GPC/ERP/MES 主账写回完成。

## 一、定位

Batch diff 解决的问题：

- 将多个 `WritebackCandidate` 组织成一批 GFIS 写回候选。
- 对每条候选展示目标实体、目标字段、当前值、建议值和 diff reason。
- 对每条候选给出 WAES gate 状态、KWE 后续动作和是否需要人工/委员会。
- 对敏感字段只允许 metadata-only 或 controlled-original 引用。
- 为 Brain/GFIS 助手展示 no-write 候选差异提供结构化材料。

Batch diff 不做：

- 不写 GFIS/GPC/ERP/MES。
- 不写 KDS accepted fact。
- 不落库 WAES gate result。
- 不创建真实 KWE work item。
- 不确认收益或积分。
- 不调用外部 API。
- 不把 `accepted`、`approved`、`passed` 写成目标系统 receipt。

## 二、必要字段

批次必须包含：

- `batchId`
- `tenantId`
- `projectId`
- `targetSystem`
- `createdBy`
- `dryRun`
- `items`
- `batchNoWrite`

每条 item 必须包含：

- `candidateId`
- `targetEntityType`
- `targetEntityId`
- `fieldDiffs`
- `basedOnObjectRefs`
- `evidenceRefs`
- `poolRefs`
- `waesGateStatus`
- `writebackStatus`
- `diffAction`
- `sensitiveHandling`
- `kweNextAction`
- `approvedForBusinessWrite`
- `targetReceiptRefs`
- `noWrite`

## 三、字段级 Diff 规则

每个 `fieldDiffs` 条目必须包含：

- `fieldPath`
- `currentValue`
- `proposedValue`
- `diffReason`
- `riskLevel`

风险等级：

- `low`
- `medium`
- `high`
- `critical`

高风险或敏感字段必须进入 `human_required`、`committee_required`、`repair_required` 或 `blocked`，不得直接写回。

## 四、Diff Action

允许的 diff action：

- `candidate_only`
- `return_for_repair`
- `block_writeback`
- `escalate_human`
- `escalate_committee`
- `metadata_only`

任何 action 都不能直接变成正式写回。

## 五、Hard Boundaries

- `dryRun` 必须为 `true`。
- `approvedForBusinessWrite` 必须为 `false`。
- `targetReceiptRefs` 必须为空。
- `writebackStatus=written_back` 在 batch diff 中禁止出现。
- `waesGateStatus=passed` 也只能进入候选，不代表写回完成。
- 缺 evidence、缺 business owner、敏感原文、POD/金融/质量争议必须阻断或升级。
- 所有 no-write 计数必须为 0。

## 六、验收口径

DKS-098 dry-run 至少覆盖：

- 普通订单字段候选差异。
- POD metadata-only 候选差异。
- 金融凭证 controlled-original 候选差异。
- 质量争议 blocked。
- OEM 责任边界 committee required。

`pass` 只证明 batch diff 结构完整和 no-write 边界可机检，不表示任何写回已完成。
