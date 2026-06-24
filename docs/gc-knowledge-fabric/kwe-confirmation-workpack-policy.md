---
doc_id: GPCF-DOC-92B1885FB3
title: GC-Knowledge Fabric KWE Confirmation Workpack 引用完整性规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-confirmation-workpack-policy.md
source_path: docs/gc-knowledge-fabric/kwe-confirmation-workpack-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KWE Confirmation Workpack 引用完整性规则

## 1. 定位

KWE confirmation workpack 是候选事实、候选 SOP、候选写回、贡献候选和收益候选进入人工确认或委员会审查前的最小确认包。

它不替代 KDS 存储，不替代 WAES 门禁，不替代 Harness evidence，不替代人工或委员会确认，也不直接写 GFIS/GPC/ERP/MES。

本规则只定义本地契约与 dry-run 校验，确保一个确认包在进入人工/委员会视图前，具备可审计的对象、来源、证据、门禁、责任、缺口、敏感处理和后续动作边界。

## 2. 必要字段

| 字段 | 要求 |
|---|---|
| `id` | 确认包编号 |
| `tenantId` | 租户隔离字段 |
| `workItemId` | 对应 KWE work item |
| `targetObjectId` | 待确认对象 |
| `targetObjectType` | fact_candidate / sop_candidate / writeback_candidate / contribution_candidate / revenue_candidate |
| `poolRefs` | 至少一个 KDS 十一池挂接 |
| `sourceRefs` | 至少一个来源引用 |
| `evidenceRefs` | 至少一个 evidence 引用，敏感对象可使用 metadata-only evidence |
| `waesGateRefs` | 至少一个 WAES gate 结果引用 |
| `reviewerType` | human / committee |
| `reviewerRefs` | reviewerType 对应的人员、角色或委员会引用 |
| `decisionOptions` | allow_accept / request_repair / reject / escalate_committee / freeze |
| `requiredActions` | 当前必须执行的补证、脱敏、确认或升级动作 |
| `sensitiveHandling` | none / redaction_required / metadata_only / controlled_original |
| `harnessEvidenceRefs` | 现有治理 evidence 或后续 evidence 占位 |
| `noWrite` | 必须为 true |

## 3. 引用完整性

Confirmation workpack 必须满足：

1. `targetObjectId` 与 `workItemId` 必须存在双向引用。
2. `sourceRefs`、`evidenceRefs`、`waesGateRefs` 不得为空。
3. 如果 `sensitiveHandling` 为 `metadata_only` 或 `controlled_original`，确认包不得包含 raw content。
4. 如果 `reviewerType=human`，不得直接输出委员会裁决结果。
5. 如果 `reviewerType=committee`，必须包含委员会触发原因。
6. 如果存在 missing evidence，`decisionOptions` 不得包含直接 accept 作为唯一选项。
7. 如果 WAES gate 为 blocked、freeze_required 或 committee_required，human-only workpack 不得标记可通过。
8. Workpack pass 只表示确认包结构完整，不表示事实已确认。

## 4. 决策边界

| 结果 | 含义 | 后续 |
|---|---|---|
| `ready_for_human_review` | 确认包完整，等待人工确认 | KWE 保持 reviewing |
| `ready_for_committee_review` | 确认包完整，等待委员会 | KWE 创建 committee review |
| `repair_required` | 来源、证据、WAES、ACL 或敏感处理缺口 | KWE 创建/更新 gap |
| `blocked` | 触发硬阻断或冻结 | WAES / governance 处理 |

任何结果都不能直接形成：

- KDS accepted fact
- GFIS/GPC 正式写回
- 正式收益分配
- 正式积分确认
- Quota transfer
- Bounty settlement
- Committee decision completion
- 外部 API 写入

## 5. DKS-094 dry-run 验收

本轮 dry-run 必须证明：

- 至少覆盖 human review、committee review、repair required、blocked 四类确认包。
- 引用完整性字段完整。
- metadata-only 包不暴露 raw content。
- blocked gate 和 committee-required gate 不会被 human-only 确认包放行。
- 所有真实写入计数为 0。
