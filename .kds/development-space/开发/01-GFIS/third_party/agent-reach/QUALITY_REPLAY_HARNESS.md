---
doc_id: GPCF-DOC-AGENT-REACH-QUALITY-REPLAY-HARNESS-20260622
title: Agent-Reach 离线质量 Replay Harness
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/third_party/agent-reach/QUALITY_REPLAY_HARNESS.md
source_path: third_party/agent-reach/QUALITY_REPLAY_HARNESS.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach 离线质量 Replay Harness

本文件定义 `GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001` 的质量回归口径。当前 harness 只使用离线 fixture，不调用真实搜索、不调用 Agent-Reach binary。

## 固定输入

| 项 | 值 |
| --- | --- |
| fixture | `fixtures/agent-reach/quality-replay-harness.json` |
| runner | `tools/kds-sync/run_agent_reach_quality_replay_harness.py` |
| 模式 | `offline_replay_only` |
| 当前准入 | `limited_candidate_only` |

## 阈值

| 指标 | 阈值 |
| --- | --- |
| minimum_query_count | `3` |
| minimum_candidate_count | `5` |
| minimum_average_score | `0.78` |
| minimum_precision_at_1 | `0.66` |
| minimum_required_field_coverage | `1.0` |
| maximum_forbidden_claim_count | `0` |

## 评分字段

| 字段 | 权重 |
| --- | --- |
| relevance_score | `0.4` |
| freshness_score | `0.2` |
| authority_score | `0.2` |
| traceability_score | `0.2` |

## 本轮结果

| 指标 | 结果 |
| --- | --- |
| query_count | `3` |
| candidate_count | `5` |
| average_score | `0.882` |
| precision_at_1 | `1.0` |
| required_field_coverage | `1.0` |
| forbidden_claim_count | `0` |
| threshold_pass | `true` |

## 非声明

- 不声明真实搜索已调用。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical、GFIS source-of-record、生产配置或全局 MCP 配置已写入。
- 不声明 accepted、integrated 或 production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001`：建立真实搜索授权包、允许通道、时间窗、凭据边界、日志脱敏、回滚和验收指标；未授权前仍不得执行真实搜索。
