---
doc_id: GPCF-DOC-531DC02EE0
title: GC-Knowledge Fabric KDS 状态候选更新 Dry-run 样例 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kds-state-candidate-update-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/kds-state-candidate-update-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KDS 状态候选更新 Dry-run 样例 v0.1

## 1. 定位

本文件定义 P0-D6 的 KDS 状态候选更新 dry-run，用于验证候选事实从 WAES dry-run、KWE confirmation workpack 到 KDS lifecycle 候选更新的受控链路。

本文件不执行真实 lifecycle mutation，不写 KDS Fact，不写 accepted fact，不写 published object，不写 GFIS/GPC/ERP/MES，不确认收益、积分或责任归因。

## 2. 强制边界

以下状态不可由 AI、WAES dry-run、KWE dry-run 或 LOOP 直接写入：

- `verified`
- `accepted`
- `published`
- `written_back`

P0 dry-run 只能生成：

- `PromotionRequestCandidate`
- `LifecycleAuditCandidate`
- `RequiredAction`
- `BlockedReason`
- `HarnessEvidenceRequirement`

## 3. 候选状态链路

| 输入 | 允许 dry-run 输出 | 禁止输出 |
|---|---|---|
| AI 候选事实 | `candidate` / `repair_required` 建议 | `verified` / `accepted` |
| WAES `repair_required` | `repair_required` 审计候选 | `accepted` |
| KWE 人工确认包候选 | `human_required` promotion 候选 | 直接 `accepted` |
| KWE 委员会审查包候选 | `committee_required` promotion 候选 | 直接 `accepted` / `published` |
| publication 候选 | `publication_required` 审计候选 | 直接 `published` |

## 4. Fixture

机器可读 fixture：

- `fixtures/kds/gckf-p0-kds-state-candidate-update-dry-run-v0.1.json`

该 fixture 是后续 validator 和 API dry-run 输入，不是正式 KDS 状态变更记录。
