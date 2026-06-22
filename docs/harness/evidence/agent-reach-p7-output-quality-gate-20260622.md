---
doc_id: GPCF-DOC-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-20260622
title: Agent-Reach P7 输出质量门禁证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.md
source_path: docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P7 输出质量门禁证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001`。结论为 `limited_live_search_output_quality_gate_ready`。本轮只建立 P7 live dry-run 输出验收器，不执行真实搜索。

## 输出

| 项 | 路径 |
| --- | --- |
| P7 输出质量 validator | `tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py` |
| P7 输出质量 evidence JSON | `docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.json` |
| P7 输出质量 evidence Markdown | `docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.md` |
| P7 输出质量 Loop 轮次 | `docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001.md` |

## 验收范围

- P7 runtime evidence 必须为 `limited_live_search_dry_run_completed`。
- `authorization_valid=true`，`execution_requested=true`。
- `live_external_search_invoked=true`，但不得出现凭据写入、cookie 提取、KDS canonical 写入、GFIS source-of-record 写入、生产配置写入、全局 MCP 配置写入或生产集成。
- 候选记录必须覆盖 P6 schema 全字段，并且 channel、query 数量、每 query 结果数量不超过授权范围。
- 质量报告必须通过 minimum candidate、全 query 候选覆盖率、query error count、字段覆盖率、平均分、traceability、禁用声明和凭据泄漏阈值。
- `query_candidate_coverage` 必须为 `1.0`。
- `channel_candidate_coverage` 必须为 `1.0`。
- `query_error_count` 必须为 `0`。
- `duplicate_url_count` 必须为 `0`。
- evidence 中不得持久化 raw provider payload。

## 自测

已执行：

```bash
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --self-test
```

结果：

```text
agent_reach_p7_limited_live_search_output=pass status=limited_live_search_dry_run_completed candidate_count=5 average_score=0.88 threshold_pass=True
```

## 负向自测

已执行：

```bash
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --negative-test missing-query
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --negative-test query-error
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --negative-test raw-payload
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --negative-test duplicate-url
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py --negative-test missing-channel
```

预期结果：

```text
missing-query -> query_coverage_missing
query-error -> query_errors_present
raw-payload -> raw_provider_payload_persisted
duplicate-url -> duplicate_candidate_url
missing-channel -> channel_coverage_missing
```

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

- 不声明真实搜索已调用。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001`。执行后必须运行：

```bash
python3 tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py
```
