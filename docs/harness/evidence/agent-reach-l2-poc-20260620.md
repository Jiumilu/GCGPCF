---
doc_id: GPCF-DOC-22516238C0
title: Agent-Reach L2 隔离PoC evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoC, XGD, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-l2-poc-20260620.md
source_path: docs/harness/evidence/agent-reach-l2-poc-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach L2 隔离PoC evidence

## 结论

本轮为 `GPCF-AGENT-REACH-L2-001` 隔离 PoC，结论为 `partial`。

Agent-Reach 可以在本机临时环境安装并运行 doctor，但当前可用渠道不足以进入 L3 连续搜索能力提升。语义搜索需要 `mcporter + Exa MCP`，属于 MCP 或全局 npm 配置变更，必须单独授权。Jina Reader 在本机复测公开网页时返回 403，因此 web 渠道在本轮不得作为可用能力声明。

## 执行边界

| 项 | 值 |
|---|---|
| 安装范围 | `/tmp/agent-reach-poc-venv` |
| 源码范围 | `/tmp/agent-reach-readonly` |
| 项目依赖修改 | 否 |
| Cookie 配置 | 否 |
| MCP 配置修改 | 否 |
| 生产写入 | 0 |
| KDS canonical 写入 | 0 |
| 外部平台写入 | 0 |
| 凭据泄露 | 0 |

## Doctor 摘要

| 指标 | 值 |
|---|---:|
| doctor_ok_channels | 4 |
| doctor_total_channels | 13 |
| doctor_available_channel_rate | 0.3077 |

可用渠道：`github`、`bilibili`、`rss`、`web`。

警告或不可用渠道：`twitter`、`youtube`、`reddit`、`xiaohongshu`、`linkedin`、`xiaoyuzhou`、`v2ex`、`xueqiu`、`exa_search`。

## Benchmark 摘要

| case | channel | result | latency_seconds | RAG Admission | 说明 |
|---|---|---|---:|---|---|
| read_agent_reach_github_page_via_jina | web | failed | 0.666 | repair_required | Jina Reader 返回 403 |
| github_repo_view_agent_reach | github | passed | 1.337 | limited | `gh repo view Panniantong/Agent-Reach` 成功 |
| rss_python_peps_feed | rss | passed | 0.753 | limited | Python PEP RSS 可读取 |
| semantic_search_exa_doctor_gate | exa_search | failed | 0.0 | repair_required | mcporter + Exa MCP 未配置 |

| 指标 | 值 |
|---|---:|
| benchmark_case_count | 4 |
| benchmark_success_count | 2 |
| search_success_rate | 0.5 |
| citation_validity_rate | 1.0 |
| source_provenance_rate | 1.0 |
| duplicate_rate | 0.0 |
| latency_p50_seconds | 0.753 |
| latency_p95_seconds | 1.337 |

## 阻塞项

1. `exa_search` 需要 `mcporter + Exa MCP`。这会涉及 MCP 或全局 npm 工具配置，当前未授权。
2. `web` 渠道虽然 doctor 标记为 ok，但 Jina Reader 对普通公开网页和 GitHub 页面复测返回 403，本轮只能记为 `repair_required`。
3. Twitter、Reddit、小红书等登录态平台没有 Cookie 授权，也不应使用主账号。
4. YouTube 当前 doctor 显示 `yt-dlp` 未安装，本轮未扩大安装范围。

## 非声明

本 evidence 不声明：

- Agent-Reach 已生产集成。
- Agent-Reach 已配置 Cookie 或登录态平台。
- Agent-Reach 已写入 KDS canonical Markdown。
- Agent-Reach 已创建 GFIS source-of-record。
- GPCF、GFIS、KDS、Brain、WAES、GPC、PKC、XiaoC 或 XGD 状态可升级。

## 下一步

若继续推进，下一轮应先选择授权边界：

| 选项 | 动作 | 风险 |
|---|---|---|
| A | 仅修复零配置渠道：YouTube、Jina Reader 备选读取路径 | 低 |
| B | 授权临时安装 mcporter 并配置 Exa MCP | 中，需要 MCP 回滚 |
| C | 授权专用小号 Cookie 平台测试 | 高，存在平台风控和封号风险 |

推荐先走 A，再决定是否进入 B。
