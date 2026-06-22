---
doc_id: GPCF-DOC-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-20260622
title: Agent-Reach P6 最小真实搜索 Dry-run 准备证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.md
source_path: docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P6 最小真实搜索 Dry-run 准备证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001`。结论为 `limited_live_search_dry_run_preparation_ready`，当前准入仍为 `limited_candidate_only`。

## 输入

| 项 | 值 |
| --- | --- |
| P5B 结论 | `live_search_precheck_pass_with_watch` |
| 本轮模式 | `preparation_only` |
| query_count | `5` |
| allowed_channels | `web` / `rss` / `bilibili` |
| max_results_per_query | `10` |

## Query 清单

| query_id | project | channel | query |
| --- | --- | --- | --- |
| q1 | GPCF | web | `GlobalCloud GPCF LOOP evidence search integration` |
| q2 | GFIS | web | `GlobalCloud GFIS source record search evidence` |
| q3 | KDS | rss | `KDS knowledge fabric controlled document search` |
| q4 | WAES | web | `WAES governance evidence search quality gate` |
| q5 | GPC | bilibili | `GlobalCloud project governance search quality` |

## 输出契约

候选记录必须包含 `candidate_id`、`query_id`、`project`、`channel`、`title`、`url`、`source_domain`、`retrieved_at`、`snippet_redacted`、`relevance_score`、`authority_score`、`freshness_score`、`traceability_score`、`overall_score`、`non_claims`。

## 质量阈值

| 指标 | 阈值 |
| --- | --- |
| minimum_query_count | `1` |
| maximum_query_count | `5` |
| minimum_candidate_count | `1` |
| minimum_required_field_coverage | `1.0` |
| minimum_average_score | `0.7` |
| minimum_traceability_score | `0.6` |
| maximum_forbidden_claim_count | `0` |
| maximum_credential_leak_count | `0` |

## 日志与回滚

- 只允许持久化脱敏 snippet，不保存 provider 原始载荷。
- 必须脱敏 token、cookie、authorization header、查询中的个人数据。
- 若 P7 dry-run 异常，删除 P7 输出证据，P6 准备证据保留。
- P7 执行前必须收到明确 `授权执行 Agent-Reach P7 Limited Live Search Dry Run`。

## 安全边界

| control | value |
| --- | --- |
| agent_reach_binary_invoked | `false` |
| live_external_search_invoked | `false` |
| doctor_health_probe_invoked | `false` |
| credential_written | `false` |
| browser_cookie_extraction_invoked | `false` |
| kds_canonical_write_allowed | `false` |
| gfis_source_of_record_write_allowed | `false` |
| production_config_write_allowed | `false` |
| global_mcp_config_write_allowed | `false` |
| production_integration_allowed | `false` |

## 非声明

- 不声明真实搜索已调用。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001`。P7 需要单独执行授权，且授权必须明确是否允许调用 Agent-Reach binary；未授权前不得执行真实搜索。
