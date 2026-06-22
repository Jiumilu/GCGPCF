---
doc_id: GPCF-DOC-AGENT-REACH-P2-CONTROLLED-ADAPTER-20260622
title: Agent-Reach P2 受控 Adapter Skeleton 证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p2-controlled-adapter-skeleton-20260622.md
source_path: docs/harness/evidence/agent-reach-p2-controlled-adapter-skeleton-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach P2 受控 Adapter Skeleton 证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001`，结论为 `controlled_adapter_skeleton_ready`。当前准入仍为 `limited_candidate_only`。

## 输入

| 项 | 值 |
| --- | --- |
| P1 结论 | `isolated_install_ready` |
| 上游 HEAD | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| 包版本 | `1.5.0` |
| 本轮模式 | `dry_run_only` |
| fixture | `fixtures/agent-reach/controlled-adapter-dry-run.json` |

## Adapter 策略

| 项 | 值 |
| --- | --- |
| allowed_command_count | `3` |
| blocked_command_count | `6` |
| candidate_schema_field_count | `7` |
| candidate_count | `2` |
| allowed_commands | `agent-reach --help`, `agent-reach --version`, `agent-reach doctor --json` |
| blocked_command_kinds | `configuration`, `installer`, `update`, `watch`, `transcribe`, `live_search` |

## Policy Blocks

| block | 说明 |
| --- | --- |
| credential_required_channel | 需要 token、cookie、browser profile 或第三方账号时阻断 |
| production_write | 任何生产写入阻断 |
| kds_canonical_write | KDS canonical 写入阻断 |
| gfis_source_of_record_write | GFIS source-of-record 写入阻断 |
| global_mcp_config_write | 全局 MCP 配置写入阻断 |
| live_external_search_without_authorization | 未授权真实搜索阻断 |

## 候选结果结构

候选结果只来自 fixture，且只允许 `evidence_tier=fixture_only` 与 `admission_status=candidate_only`。

| 字段 | 必填 |
| --- | --- |
| candidate_id | yes |
| channel | yes |
| title | yes |
| source_url | yes |
| snippet | yes |
| evidence_tier | yes |
| admission_status | yes |

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
- 不声明搜索质量已验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001`：建立离线 replay harness、固定查询集、评分字段和质量回归门禁，仍不调用真实搜索。
