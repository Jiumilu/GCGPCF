---
doc_id: GPCF-DOC-B7F62C3EA4
title: GC-Knowledge Fabric KWE 最小流程 Dry-run 样例 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kwe-minimum-workflow-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/kwe-minimum-workflow-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KWE 最小流程 Dry-run 样例 v0.1

## 1. 定位

本文件定义 P0-D5 的 KWE 最小流程 dry-run 样例，用于把 P0-D4 的 WAES dry-run 输出转成 KWE 候选流程输入。

本文件只生成候选 WorkItem、Gap、Bounty、Confirmation Workpack 和后续动作建议，不创建真实 KWE 工单，不升级 KDS lifecycle，不写 WAES Gate Result，不写 GFIS/GPC/ERP/MES，不确认收益、积分、悬赏或委员会决议。

## 2. 覆盖范围

| 对象 | 目的 | P0 输出 |
|---|---|---|
| `KnowledgeWorkItem` | 承接 WAES 输出并形成候选流程任务 | `candidate_only` |
| `GapRecord` | 承接缺来源、缺证据、缺字段、缺责任边界 | `open_candidate` |
| `BountyWorkItem` | 将高优先级缺口转为悬赏候选 | `bounty_candidate` |
| `ConfirmationWorkpack` | 将候选事实、候选写回、贡献争议送人工或委员会 | `ready_for_human_review` / `ready_for_committee_review` |
| `KweNextAction` | 给 Brain、PKC、GFIS Assistant 展示下一步候选动作 | `read_model_only` |

## 3. WAES 到 KWE 映射

| WAES case | Gate status | KWE 候选动作 |
|---|---|---|
| `waes-p0-evidence-missing-pod` | `repair_required` | 创建 Evidence Gap 候选和补证 WorkItem 候选 |
| `waes-p0-rag-ai-candidate` | `blocked` | 创建 Source/Evidence 绑定 WorkItem 候选，不允许 promotion |
| `waes-p0-sensitive-finance` | `metadata_only` | 创建 metadata-only review workpack 候选 |
| `waes-p0-writeback-human` | `human_required` | 创建业务负责人确认包候选 |
| `waes-p0-contribution-duplicate` | `committee_required` | 创建委员会审查包候选并冻结候选积分 |
| `waes-p0-revenue-potential` | `committee_required` | 创建潜在收益转正式收益委员会审查候选 |

## 4. No-write 断言

每个 KWE dry-run case 必须显式声明：

- `createsKweWorkItem = false`
- `writesKdsLifecycle = 0`
- `writesKdsFact = 0`
- `writesWaesGateResult = 0`
- `writesBusinessSystem = 0`
- `writesRevenueOrScoreConfirmation = 0`
- `writesBountySettlement = 0`
- `writesCommitteeDecisionCompletion = 0`
- `writesExternalApi = 0`

## 5. Fixture

机器可读 fixture：

- `fixtures/kwe/gckf-p0-kwe-minimum-workflow-dry-run-v0.1.json`

该 fixture 是后续 validator 和 API dry-run 的输入，不是正式 KWE 工单、正式确认包或正式决议。
