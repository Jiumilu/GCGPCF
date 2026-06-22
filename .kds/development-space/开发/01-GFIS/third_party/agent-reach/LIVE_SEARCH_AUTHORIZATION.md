---
doc_id: GPCF-DOC-AGENT-REACH-LIVE-SEARCH-AUTHORIZATION-20260622
title: Agent-Reach Live Search Authorization Boundary
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md
source_path: third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach Live Search Authorization Boundary

本文件定义 `GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001` 的真实搜索授权边界。当前结论是授权包已建立，但尚未获得真人授权；因此不得执行真实搜索。

## 当前状态

| 项 | 值 |
| --- | --- |
| current_admission | `limited_candidate_only` |
| authorization_status | `pending_human_authorization` |
| live_search_authorized | `false` |
| template | `fixtures/agent-reach/live-search-authorization-pack.template.json` |
| negative_fixtures | `fixtures/agent-reach/live-search-authorization-negative-fixtures.json` |

## 必填授权字段

| 字段 | 要求 |
| --- | --- |
| authorization_id | 唯一授权编号 |
| authorized_by | 真人授权人，不接受空值或系统占位 |
| authorized_at | ISO-8601 授权时间 |
| expires_at | ISO-8601 过期时间，必须晚于授权时间 |
| allowed_channels | 明确列出本轮允许通道 |
| allowed_actions | 仅限读取公开外部内容、生成候选记录、写入 harness evidence |
| forbidden_actions | 必须包含凭据写入、浏览器 cookie 提取、KDS canonical 写入、GFIS source-of-record 写入、生产配置写入、全局 MCP 配置写入、生产集成 |
| logging_redaction | 必须开启 token、cookie、authorization header、个人数据脱敏 |
| rollback_plan | 必须说明关闭真实搜索、删除本轮候选证据、维持准入边界的方法 |

## 允许通道边界

初始候选通道只能来自 P1 doctor 结果中的可用通道：`web`、`rss`、`bilibili`。在授权状态仍为 `pending_human_authorization` 时，这些通道只是授权模板中的候选项，不代表已经启用。

## 禁止动作

- 不得写入凭据或 `.env`。
- 不得提取浏览器 cookie。
- 不得写入 KDS canonical Markdown。
- 不得写入 GFIS source-of-record。
- 不得修改生产配置。
- 不得修改全局 MCP 配置。
- 不得声明 accepted、integrated 或 production_ready。

## 非声明

- 不声明真实搜索已授权。
- 不声明真实搜索已调用。
- 不声明真实搜索质量已验收。
- 不声明 KDS canonical、GFIS source-of-record、生产配置或全局 MCP 配置已写入。
- 不声明 accepted、integrated 或 production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001`：只在收到完整授权包后执行授权前检查；未通过前仍不得执行真实搜索。
