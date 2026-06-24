---
doc_id: GPCF-DOC-79B503879D
title: GFIS Assistant WAES Guidance Packet No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-waes-guidance-packet-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-waes-guidance-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant WAES Guidance Packet No-write 规则

## 1. 定位

GFIS Assistant WAES Guidance Packet 是 DKS-107 `WAES Precheck Bundle Read Model` 之后的 GFIS 助手指导包。

它把 GFIS Assistant 可见的 WAES precheck bundle 转换为用户可理解的门禁解释、补证提示、metadata-only 提示和人工/委员会路径提示。

## 2. 能力边界

Guidance Packet 可以：

- 解释为什么当前不能正式写回；
- 展示需要补齐的 source / evidence / owner confirmation；
- 提示是否需要 metadata-only；
- 提示是否需要人工确认、委员会或治理负责人；
- 提示下一步候选动作。

Guidance Packet 不能：

- 批准 GFIS 正式写回；
- 写入 WAES Gate Result；
- 创建 KWE WorkItem；
- 改变 KDS lifecycle；
- 写入 GFIS / GPC / ERP / MES；
- 生成 target receipt；
- 完成人工确认或委员会裁决；
- 确认收益、积分、额度或悬赏；
- 调用外部 API。

## 3. 最小字段

每个 packet 必须包含：

- `packetId`
- `bundleRef`
- `tenantId`
- `projectId`
- `assistantSurface`
- `guidanceMode`
- `writebackExplanation`
- `repairPrompts`
- `metadataOnlyHints`
- `manualConfirmationPoints`
- `committeeTriggers`
- `blockedActions`
- `allowedAssistantActions`
- `approvedForBusinessWrite`
- `createsWaesGateResult`
- `createsKweWorkItem`
- `promotesLifecycle`
- `noWrite`

## 4. Guidance Mode

| mode | 说明 |
|---|---|
| writeback_blocked | 当前不得写回 |
| repair_guidance | 需要补证或补字段 |
| metadata_only_guidance | 只能使用 metadata / hash / summary |
| committee_guidance | 需要委员会路径 |
| freeze_guidance | 需要冻结候选路径 |

## 5. 只读助手动作

允许：

- explain_waes_gate；
- suggest_repair；
- show_metadata_boundary；
- show_manual_confirmation；
- show_committee_path；
- show_harness_evidence_hint。

阻断：

- approve_business_write；
- create_waes_gate_result；
- create_kwe_work_item；
- promote_lifecycle；
- complete_committee_decision；
- confirm_revenue_or_score。

## 6. 与 GFIS 的关系

Guidance Packet 不是 GFIS 写回批准，不是业务状态更新，也不是 target receipt。

它只让 GFIS Assistant 安全解释门禁与补证路径。任何真实写回必须经过 WAES、KWE、人工或委员会确认，并由授权业务系统执行。
