---
doc_id: GPCF-DOC-AGENT-REACH-P8-BATCH-AUTHORIZATION-REQUEST-PACKAGE-20260622
title: Agent-Reach P8 批次真实搜索授权申请包 2026-06-22
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach P8 批次真实搜索授权申请包 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P8-BATCH-AUTHORIZATION-REQUEST-PACKAGE-001`。结论为 `p8_batch_authorization_request_package_ready`。本轮只生成 P8 三批次授权申请包，不执行真实搜索。

## 输出

| 项 | 路径 |
| --- | --- |
| P8 授权申请包 | `fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json` |
| P8 授权申请包 validator | `tools/kds-sync/validate_agent_reach_p8_batch_authorization_request_package.py` |
| P8 授权申请 evidence JSON | `docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.json` |
| P8 授权申请 evidence Markdown | `docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.md` |

## 授权文本

| batch | 授权文本 | 项目 |
| --- | --- | --- |
| p8-batch-1 | `授权执行 Agent-Reach P8 Project Group Full Live Search Batch 1` | GPCF、KDS、WAES、Brain、GFIS |
| p8-batch-2 | `授权执行 Agent-Reach P8 Project Group Full Live Search Batch 2` | GPC、PVAOS、PKC、XiaoC、XGD |
| p8-batch-3 | `授权执行 Agent-Reach P8 Project Group Full Live Search Batch 3` | XiaoG、MMC、Studio、WAS |

## 授权字段

每批授权必须包含：

- `authorization_status=approved_for_p8_project_group_full_live_search_batch`
- `authorized_by=lujunxiang`
- 具体 `authorized_at` 与 `expires_at`
- 对应 `batch_id`
- `allowed_channels=web/rss/bilibili`
- `max_queries` 等于该批 query 数量
- `max_results_per_query=10`
- `allow_agent_reach_binary_invocation=false`
- `allow_external_network=true`
- `allow_write_evidence_only=true`
- 保留所有禁止动作：credential 写入、cookie 提取、KDS canonical 写入、GFIS source-of-record 写入、生产配置写入、全局 MCP 配置写入、生产集成、accepted/integrated/production_ready 声明
- 启用 token、cookie、authorization header、query personal data 和 snippet 持久化脱敏

## 安全边界

| control | value |
| --- | --- |
| agent_reach_binary_invoked | `false` |
| live_external_search_invoked | `false` |
| credential_written | `false` |
| browser_cookie_extraction_invoked | `false` |
| kds_canonical_write_allowed | `false` |
| gfis_source_of_record_write_allowed | `false` |
| production_config_write_allowed | `false` |
| global_mcp_config_write_allowed | `false` |
| production_integration_allowed | `false` |

## 非声明

- 不执行真实搜索。
- 不声明 14 项目真实搜索覆盖已完成。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`。执行前仍需按批次生成 `.local.json` 授权文件，并先补齐 `tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py` 运行器。
