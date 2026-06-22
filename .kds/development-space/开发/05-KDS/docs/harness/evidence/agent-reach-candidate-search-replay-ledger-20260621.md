---
doc_id: GPCF-DOC-FF1E624F1E
title: Agent-Reach Candidate Search Replay Ledger 20260621
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.md
source_path: docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Candidate Search Replay Ledger 20260621

## 结论

`GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001` 已建立。本轮只从既有 Exa fixed benchmark evidence 回放生成台账，`external_search_invoked=false`，不重新调用外部搜索，不写 KDS canonical，不生产集成，不升级任何项目状态。

## 汇总

| 指标 | 值 |
|---|---|
| entry_count | 5 |
| successful_entry_count | 5 |
| search_success_rate | 1.0 |
| source_provenance_rate | 1.0 |
| duplicate_rate | 0.0 |
| latency_p50_seconds | 3.889 |
| latency_p95_seconds | 4.633 |
| review_acceptance_rate | pending |
| review_status | pending_waes_kds_review |

## 台账条目

| id | channel | success | latency_seconds | first_url | rag_admission | review_status |
|---|---|---:|---:|---|---|---|
| knowledge_provenance_rag | exa_search | true | 3.889 | `https://gautierdorval.com/en/frameworks/rag-governance-retrieval-and-inference-control/` | limited | pending_waes_kds_review |
| green_supply_chain_policy | exa_search | true | 3.598 | `https://www.chinesestandard.net/PDF/English.aspx/GBT39256-2020` | limited | pending_waes_kds_review |
| factory_execution_traceability | exa_search | true | 4.633 | `https://sgsystemsglobal.com/glossary/mes-manufacturing-execution-system/` | limited | pending_waes_kds_review |
| ai_agent_evidence_gate | exa_search | true | 4.126 | `https://github.com/undercurrentai/aegis-mcp` | limited | pending_waes_kds_review |
| agent_reach_capability | exa_search | true | 3.545 | `https://github.com/Panniantong/Agent-Reach` | limited | pending_waes_kds_review |

## 准入判定

| 字段 | 判定 |
|---|---|
| kds_admission | `limited_candidate_only` |
| rag_admission | `limited` |
| waes_review_status | `pending_waes_kds_review` |
| status_upgrade_allowed | false |
| production_integration_allowed | false |
| accepted_or_integrated_claim_allowed | false |

## 安全

| 字段 | 值 |
|---|---|
| credential_leakage_count | 0 |
| production_write_count | 0 |
| kds_canonical_write_count | 0 |
| external_platform_write_count | 0 |

## 非声明

- 不证明 Agent-Reach 已生产集成。
- 不写 KDS canonical Markdown。
- 不创建 GFIS source-of-record。
- 不升级 GPCF accepted/integrated/production_ready 状态。
- 不把 Agent-Reach 结果转成强 RAG 引用。
- 不授权 Cookie 或登录态平台。

## 下一门禁

`waes_kds_candidate_review_queue`
