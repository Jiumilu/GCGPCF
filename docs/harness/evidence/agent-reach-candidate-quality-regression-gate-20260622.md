---
doc_id: GPCF-DOC-AGENT-REACH-QUALITY-REGRESSION-20260622
title: Agent-Reach Candidate Quality Regression Gate 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.md
source_path: docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach Candidate Quality Regression Gate 2026-06-22

本轮执行 `GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001`，结论为 `candidate_quality_regression_gate_ready`。

## 执行边界

本轮只定义回归门禁，不调用 live external search，不调用 Agent-Reach runtime，不写 KDS canonical Markdown，不创建 GFIS source-of-record，不写 production configuration，不升级 accepted / integrated / production_ready。

## 回归门禁

| gate_id | metric | operator | threshold | baseline | failure_action |
| --- | --- | --- | ---: | ---: | --- |
| search_success_rate_gate | search_success_rate | >= | `0.8` | `1.0` | block_candidate_use_and_require_replay_investigation |
| source_provenance_rate_gate | source_provenance_rate | == | `1.0` | `1.0` | block_candidate_admission |
| duplicate_rate_gate | duplicate_rate | <= | `0.2` | `0.0` | require_deduplication_before_review |
| latency_p50_gate | latency_p50_seconds | <= | `10` | `3.889` | mark_efficiency_regression_and_require_benchmark_replay |
| latency_p95_gate | latency_p95_seconds | <= | `30` | `4.633` | mark_tail_latency_regression_and_require_benchmark_replay |
| canonical_write_gate | canonical_write_count | == | `0` | `0` | block_run_and_require_explicit_canonical_write_authorization |
| production_write_gate | production_write_count | == | `0` | `0` | block_run_and_require_explicit_production_authorization |
| limited_admission_gate | kds_admission | == | `limited_candidate_only` | `limited_candidate_only` | block_status_upgrade |

## 负向夹具

| fixture_id | mutated_metric | mutated_value | expected_gate | expected_result |
| --- | --- | ---: | --- | --- |
| missing_source_provenance | source_provenance_rate | `0.8` | source_provenance_rate_gate | fail |
| duplicate_rate_regression | duplicate_rate | `0.4` | duplicate_rate_gate | fail |
| canonical_write_attempt | canonical_write_count | `1` | canonical_write_gate | fail |
| production_write_attempt | production_write_count | `1` | production_write_gate | fail |
| unauthorized_status_upgrade | kds_admission | `canonical_candidate` | limited_admission_gate | fail |

## 质量状态

| item | value |
| --- | --- |
| regression_gate_count | `8` |
| negative_fixture_count | `5` |
| positive_baseline_expected_result | `pass` |
| all_negative_fixtures_must_fail | `true` |
| status_upgrade_allowed | `false` |
| production_integration_allowed | `false` |

## 下一轮

进入 `GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-FIXTURE-REPLAY-001`：用正向基线和 5 条负向夹具实际回放门禁。
