---
doc_id: GPCF-DOC-AGENT-REACH-QUALITY-TREND-20260622
title: Agent-Reach Candidate Quality Trend Baseline 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.md
source_path: docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach Candidate Quality Trend Baseline 2026-06-22

本轮执行 `GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001`，结论为 `candidate_quality_trend_baseline_ready`。

## 执行边界

本轮只建立质量趋势基线，不调用 live external search，不调用 Agent-Reach runtime，不写 KDS canonical Markdown，不创建 GFIS source-of-record，不写 production configuration，不升级 accepted / integrated / production_ready。

## 搜索回放基线

| metric | baseline |
| --- | ---: |
| entry_count | `5` |
| successful_entry_count | `5` |
| search_success_rate | `1.0` |
| source_provenance_rate | `1.0` |
| duplicate_rate | `0.0` |
| latency_p50_seconds | `3.889` |
| latency_p95_seconds | `4.633` |
| review_status | `pending_waes_kds_review` |

## 候选摄取 dry-run 基线

| metric | baseline |
| --- | ---: |
| candidate_count | `4` |
| rejected_count | `1` |
| accepted_limited_rate | `0.8` |
| rejected_records_ingested | `0` |
| all_candidates_have_source_provenance | `true` |
| all_candidates_have_review_status | `true` |
| all_candidates_keep_limited_admission | `true` |
| canonical_write_count | `0` |
| production_write_count | `0` |
| credential_leakage_count | `0` |

## 趋势门禁

| metric | guardrail |
| --- | --- |
| search_success_rate | candidate use 不低于 `0.8` |
| source_provenance_rate | candidate admission 必须保持 `1.0` |
| duplicate_rate | 不高于 `0.2` |
| latency_p50_seconds | 不高于 `10` 秒 |
| latency_p95_seconds | 不高于 `30` 秒 |
| accepted_limited_rate | 仅作候选接受率，不授权强 RAG 或 canonical write |
| canonical_write_count | 未单独授权时必须保持 `0` |
| production_write_count | 未单独授权时必须保持 `0` |

## 持续进化控制

- 任何质量趋势升级前，必须重复 fixed-query replay 或经过授权的 Agent-Reach benchmark。
- source provenance rate 必须保持 `1.0`。
- canonical 和 production write count 未经单独授权必须保持 `0`。
- human 或 WAES/KDS review decision 必须独立记录，不能由 search success 自动替代。
- `accept_limited` 只代表候选元数据，不代表强 RAG 或 canonical knowledge。

## 下一轮

进入 `GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001`：定义回归门禁，确保未来搜索质量、来源追溯和候选摄取不会退化。
