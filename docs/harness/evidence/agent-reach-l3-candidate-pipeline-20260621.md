---
doc_id: GPCF-DOC-23C9EEDF9B
title: Agent-Reach L3 Candidate Pipeline Evidence 20260621
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.md
source_path: docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach L3 Candidate Pipeline Evidence 20260621

## 结论

`GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001` 已建立为只读候选搜索流水线目标，执行模式为 `read_only_replay_plan`。本轮未调用新的外部搜索，未写 KDS canonical，未生产集成，未升级任何项目状态。

## 流水线

| 阶段 | 输出 | 门禁 |
|---|---|---|
| P0 Source Intake | candidate_source_batch | provenance present |
| P1 Normalize | normalized_candidate_set | duplicate_rate <= 20% |
| P2 Score | scored_candidate_set | source_provenance_rate = 1.0 |
| P3 Admit | limited_admission_ledger | no strong citation |
| P4 Review | waes_kds_review_queue_item | no auto accept |

## 当前证据

| 证据 | 作用 |
|---|---|
| `agent-reach-zero-config-repair-20260620.json` | 公开通道 zero-config 可用性 |
| `agent-reach-exa-local-pilot-20260620.json` | Exa 临时配置、查询、回滚 |
| `agent-reach-exa-fixed-benchmark-20260620.json` | 固定查询质量与效率指标 |
| `agent-reach-candidate-search-review-20260620.json` | WAES/KDS 候选评审准入 |

## 当前指标

| 指标 | 值 |
|---|---|
| exa_fixed_query_count | 5 |
| exa_fixed_success_count | 5 |
| exa_fixed_query_success_rate | 1.0 |
| source_provenance_rate | 1.0 |
| latency_p50_seconds | 3.889 |
| latency_p95_seconds | 4.633 |
| rollback_verified | true |

## 准入判定

| 字段 | 判定 |
|---|---|
| waes_review_status | `ready_for_review` |
| kds_admission | `limited_candidate_only` |
| rag_admission | `limited` |
| status_upgrade_allowed | false |
| production_integration_allowed | false |
| accepted_or_integrated_claim_allowed | false |

## 持续进化

下一阶段必须生成 `candidate_search_replay_ledger`，持续记录：

- `search_success_rate`
- `source_provenance_rate`
- `duplicate_rate`
- `latency_p50_seconds`
- `latency_p95_seconds`
- `review_acceptance_rate`

## 非声明

- 不证明 Agent-Reach 已生产集成。
- 不写 KDS canonical Markdown。
- 不创建 GFIS source-of-record。
- 不升级 GPCF accepted/integrated/production_ready 状态。
- 不把 Agent-Reach 结果转成强 RAG 引用。
- 不授权 Cookie 或登录态平台。
