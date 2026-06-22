---
doc_id: GPCF-DOC-AGENT-REACH-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-20260622
title: Agent-Reach 项目群全量真实搜索覆盖输出质量门禁 2026-06-22
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.md
source_path: docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach 项目群全量真实搜索覆盖输出质量门禁 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001`。结论为 `full_project_group_live_coverage_output_quality_gate_ready`。本轮只建立 14 项目全量真实搜索结果验收器，不执行真实搜索。

## 输出

| 项 | 路径 |
| --- | --- |
| P8 全量输出质量 validator | `tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py` |
| P8 输出质量 evidence JSON | `docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.json` |
| P8 输出质量 evidence Markdown | `docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.md` |
| P8 输出质量 Loop 轮次 | `docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001.md` |

## 验收范围

- runtime evidence 必须为 `full_project_group_live_coverage_completed`。
- `execution_requested=true`。
- `live_external_search_invoked=true`，但不得出现凭据写入、cookie 提取、KDS canonical 写入、GFIS source-of-record 写入、生产配置写入、全局 MCP 配置写入或生产集成。
- 候选记录必须覆盖候选 schema 全字段，并且每个 query 的结果数不得超过授权上限。
- 候选 `url` 必须为 `http` 或 `https`，且 `source_domain` 必须与 URL host 一致。
- 候选 `retrieved_at` 必须为带时区的 ISO 8601 时间。
- 候选 `snippet_redacted` 不得为空。
- `project_coverage` 必须为 `1.0`，覆盖 14 项目：GPCF、KDS、WAES、Brain、GFIS、GPC、PVAOS、PKC、XiaoC、XGD、XiaoG、MMC、Studio、WAS。
- `query_candidate_coverage` 必须为 `1.0`。
- `channel_candidate_coverage` 必须为 `1.0`，覆盖 `web`、`rss`、`bilibili`。
- `query_error_count` 必须为 `0`。
- `duplicate_url_count` 必须为 `0`。
- `average_overall_score` 必须不低于 `0.65`。
- `minimum_candidate_overall_score` 必须不低于 `0.5`。
- `minimum_traceability_score` 必须为 `1.0`。
- 每条候选的 `relevance_score`、`authority_score`、`freshness_score`、`traceability_score` 与 `overall_score` 必须在 `0` 到 `1` 范围内。
- `credential_leak_count` 必须为 `0`。
- `forbidden_claim_count` 必须为 `0`。
- evidence 中不得持久化 raw provider payload。

## 自测

已执行：

```bash
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --self-test
```

预期结果：

```text
agent_reach_project_group_full_live_coverage_output=pass status=self_test candidate_count=14 project_coverage=1.0
```

## 负向自测

已覆盖：

```bash
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test missing-project
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test duplicate-url
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test query-error
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test raw-payload
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test credential-leak
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test forbidden-claim
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test missing-channel
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test low-score
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test bad-url-scheme
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test domain-mismatch
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py --negative-test bad-retrieved-at
```

预期阻断点：

| case | expected |
| --- | --- |
| missing-project | `project_coverage_missing` |
| duplicate-url | `duplicate_candidate_url` |
| query-error | `query_errors_present` |
| raw-payload | `raw_provider_payload_persisted` |
| credential-leak | `candidate_credential_leak` |
| forbidden-claim | `candidate_forbidden_claim` |
| missing-channel | `candidate_channel_mismatch` |
| low-score | `quality_below_requirement:minimum_candidate_overall_score` |
| bad-url-scheme | `candidate_url_scheme_invalid` |
| domain-mismatch | `candidate_source_domain_mismatch` |
| bad-retrieved-at | `candidate_retrieved_at_missing_timezone` |

## 安全边界

| control | value |
| --- | --- |
| live_external_search_invoked | `false` |
| agent_reach_binary_invoked | `false` |
| credential_written | `false` |
| browser_cookie_extraction_invoked | `false` |
| kds_canonical_write_allowed | `false` |
| gfis_source_of_record_write_allowed | `false` |
| production_config_write_allowed | `false` |
| global_mcp_config_write_allowed | `false` |
| production_integration_allowed | `false` |

## 非声明

- 不执行真实搜索。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`。执行真实搜索前仍需独立 P8 batch 授权。
