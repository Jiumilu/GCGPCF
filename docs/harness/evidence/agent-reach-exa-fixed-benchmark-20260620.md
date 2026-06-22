---
doc_id: GPCF-DOC-901EC6A452
title: Agent-Reach Exa固定查询集benchmark evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.md
source_path: docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Exa固定查询集benchmark evidence

## 结论

`GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001` 结论为 `pass`，但只证明 Exa 在 5 个固定公开查询上的候选搜索质量可评估。

本轮仍使用临时 npm prefix 和临时 HOME；未执行全局 npm 安装，未修改项目依赖，未配置 Cookie，未写生产系统，未写 KDS canonical。所有查询结果默认 `RAG Admission=limited`，不得转成强引用、KDS canonical 或 GFIS source-of-record。

## 指标

| 指标 | 值 |
|---|---:|
| query_count | 5 |
| success_count | 5 |
| exa_search_test_success_rate | 1.0 |
| latency_p50_seconds | 3.889 |
| latency_p95_seconds | 4.633 |
| source_provenance_rate | 1.0 |
| production_write_count | 0 |
| kds_canonical_write_count | 0 |
| credential_leakage_count | 0 |
| rollback_verified | true |

## 查询集

| id | result | first_url | RAG Admission |
|---|---|---|---|
| knowledge_provenance_rag | pass | https://gautierdorval.com/en/frameworks/rag-governance-retrieval-and-inference-control/ | limited |
| green_supply_chain_policy | pass | https://www.chinesestandard.net/PDF/English.aspx/GBT39256-2020 | limited |
| factory_execution_traceability | pass | https://sgsystemsglobal.com/glossary/mes-manufacturing-execution-system/ | limited |
| ai_agent_evidence_gate | pass | https://github.com/undercurrentai/aegis-mcp | limited |
| agent_reach_capability | pass | https://github.com/Panniantong/Agent-Reach | limited |

## 回滚

| 项 | 结果 |
|---|---|
| `/tmp/agent-reach-mcporter` | removed |
| `/tmp/agent-reach-exa-home` | removed |
| mcporter_still_available_after_rollback | false |

## 非声明

- 本 evidence 不证明 Agent-Reach 已生产集成。
- 本 evidence 不配置 Cookie 或登录态平台。
- 本 evidence 不写 KDS canonical Markdown。
- 本 evidence 不创建 GFIS source-of-record。
- 本 evidence 不授权生产写入。
- 本 evidence 不把 Exa 搜索结果升级为强引用。
- 本 evidence 不升级任何项目状态。

## 下一步

可以进入 `GPCF-AGENT-REACH-CANDIDATE-SEARCH-REVIEW-001`：把零配置渠道和 Exa benchmark 作为候选搜索能力提交 WAES/KDS review，而不是直接进入生产集成。
