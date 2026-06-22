---
doc_id: GPCF-DOC-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-20260622
title: Agent-Reach P4 Live Search Authorization Pack 证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.md
source_path: docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P4 Live Search Authorization Pack 证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001`，结论为 `live_search_authorization_pack_ready`。当前准入仍为 `limited_candidate_only`。

## 输入

| 项 | 值 |
| --- | --- |
| P3 结论 | `quality_replay_harness_ready` |
| 当前准入 | `limited_candidate_only` |
| 授权状态 | `pending_human_authorization` |
| live_search_authorized | `false` |

## 输出

| 项 | 路径 |
| --- | --- |
| 授权模板 | `fixtures/agent-reach/live-search-authorization-pack.template.json` |
| 负向用例 | `fixtures/agent-reach/live-search-authorization-negative-fixtures.json` |
| 授权边界文档 | `third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md` |
| 验证器 | `tools/kds-sync/validate_agent_reach_p4_live_search_authorization_pack.py` |

## 授权要求

| 字段 | 要求 |
| --- | --- |
| authorized_by | 必填真人授权人 |
| authorized_at / expires_at | 必填 ISO-8601 时间窗，且过期时间晚于授权时间 |
| allowed_channels | 仅允许明确列出的通道 |
| forbidden_actions | 必须包含凭据写入、浏览器 cookie 提取、KDS canonical 写入、GFIS source-of-record 写入、生产配置写入、全局 MCP 配置写入、生产集成 |
| logging_redaction | 必须开启 token、cookie、authorization header、个人数据脱敏 |
| rollback_plan | 必须定义关闭真实搜索和证据清理办法 |

## 负向用例

| 指标 | 值 |
| --- | --- |
| negative_fixture_count | `8` |
| expected_decision | `all_rejected` |
| rejected_negative_fixtures | `8` |

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

- 不声明真实搜索已授权。
- 不声明真实搜索已调用。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001`：只有在收到完整授权包后，才检查授权字段、时间窗、通道、日志脱敏、回滚和证据路径；未通过前仍不得执行真实搜索。
