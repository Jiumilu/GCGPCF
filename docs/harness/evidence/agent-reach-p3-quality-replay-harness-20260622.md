---
doc_id: GPCF-DOC-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-20260622
title: Agent-Reach P3 离线质量 Replay Harness 证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.md
source_path: docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach P3 离线质量 Replay Harness 证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001`，结论为 `quality_replay_harness_ready`。当前准入仍为 `limited_candidate_only`。

## 输入

| 项 | 值 |
| --- | --- |
| P2 结论 | `controlled_adapter_skeleton_ready` |
| 上游 HEAD | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| 包版本 | `1.5.0` |
| 本轮模式 | `offline_replay_only` |
| fixture | `fixtures/agent-reach/quality-replay-harness.json` |

## 质量指标

| 指标 | 结果 | 阈值 |
| --- | --- | --- |
| query_count | `3` | `>=3` |
| candidate_count | `5` | `>=5` |
| average_score | `0.882` | `>=0.78` |
| precision_at_1 | `1.0` | `>=0.66` |
| required_field_coverage | `1.0` | `>=1.0` |
| forbidden_claim_count | `0` | `<=0` |
| threshold_pass | `true` | `true` |

## 评分字段

| 字段 | 权重 |
| --- | --- |
| relevance_score | `0.4` |
| freshness_score | `0.2` |
| authority_score | `0.2` |
| traceability_score | `0.2` |

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

进入 `GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001`：建立真实搜索授权包、允许通道、时间窗、凭据边界、日志脱敏、回滚和验收指标；未授权前仍不得执行真实搜索。
