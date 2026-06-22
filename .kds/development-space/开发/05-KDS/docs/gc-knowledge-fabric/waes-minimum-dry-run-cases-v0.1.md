---
doc_id: GPCF-DOC-19D7F0C3F0
title: GC-Knowledge Fabric WAES 最小门禁 Dry-run 样例 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/waes-minimum-dry-run-cases-v0.1.md
source_path: docs/gc-knowledge-fabric/waes-minimum-dry-run-cases-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric WAES 最小门禁 Dry-run 样例 v0.1

## 1. 定位

本文件定义 P0-D4 的 WAES 最小门禁 dry-run 样例，用于后续实现 `POST /api/v2/waes/gates/run`、RAG 准入检查、写回检查、收益检查和贡献检查时的输入输出基线。

本文件只定义候选检查，不写入正式 WAES Gate Result，不升级 KDS lifecycle，不写 GFIS/GPC/ERP/MES，不确认收益、积分、悬赏或委员会决议。

## 2. 覆盖范围

P0 最小 dry-run 覆盖六类门禁：

| Gate | 目的 | P0 输出 |
|---|---|---|
| `source_gate` | 检查来源等级、来源范围、时间戳 | `passed` / `repair_required` |
| `evidence_gate` | 检查 evidence 引用、哈希、受控原件指针 | `passed` / `repair_required` / `blocked` |
| `rag_gate` | 检查 trust、RAG admission、敏感性、确认状态 | `passed` / `blocked` / `repair_required` / `metadata_only` |
| `writeback_gate` | 检查目标系统、字段、证据、负责人确认 | `passed` / `human_required` / `blocked` |
| `contribution_gate` | 检查贡献主体、对象引用、重复主张、确认状态 | `passed` / `human_required` / `committee_required` |
| `revenue_gate` | 检查收入类型、依据、金额、证据 | `passed` / `repair_required` / `committee_required` |

## 3. 最小样例

| caseId | 场景 | Gate | 期望结果 | 说明 |
|---|---|---|---|---|
| `waes-p0-source-authoritative-policy` | 权威政策来源 | `source_gate` | `passed` | T1 来源，范围和时间戳明确 |
| `waes-p0-evidence-missing-pod` | POD 缺证 | `evidence_gate` | `repair_required` | 有来源但缺 evidence hash 和受控原件指针 |
| `waes-p0-rag-ai-candidate` | AI 候选事实 | `rag_gate` | `blocked` | T5 只能作为候选，不能 RAG 强引用 |
| `waes-p0-sensitive-finance` | 金融凭证 | `rag_gate` / `sensitive_data_gate` | `metadata_only` | 原件受控，RAG 只能用元数据 |
| `waes-p0-writeback-human` | GFIS 写回候选 | `writeback_gate` | `human_required` | 字段和证据齐备，但缺业务负责人确认 |
| `waes-p0-contribution-duplicate` | 重复贡献主张 | `contribution_gate` | `committee_required` | 跨单位重复主张必须进入委员会 |
| `waes-p0-revenue-formal` | 已到账收入 | `revenue_gate` | `passed` | cash received + evidence + confirmed contribution refs |
| `waes-p0-revenue-potential` | 潜在收益转正式收益 | `revenue_gate` | `committee_required` | 机会或合同不能自动进入正式分配 |

## 4. 输出字段

每个 dry-run gate case 必须输出：

- `caseId`
- `gateType`
- `inputObjectRef`
- `expectedStatus`
- `reasonCodes`
- `requiredActions`
- `reviewerRequirement`
- `harnessEvidenceRequired`
- `noWrite`

## 5. No-write 断言

每个 case 必须显式声明：

- `writesWaesGateResult = 0`
- `writesKdsLifecycle = 0`
- `writesKdsFact = 0`
- `writesBusinessSystem = 0`
- `writesRevenueDistribution = 0`
- `writesContributionScoreConfirmation = 0`
- `writesCommitteeDecision = 0`
- `writesExternalApi = 0`

## 6. Fixture

机器可读 fixture：

- `fixtures/waes/gckf-p0-waes-minimum-dry-run-cases-v0.1.json`

该 fixture 是后续 validator 和 API dry-run 的输入，不是正式 gate result。
