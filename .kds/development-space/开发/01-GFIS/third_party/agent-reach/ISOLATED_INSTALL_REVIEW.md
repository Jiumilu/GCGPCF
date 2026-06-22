---
doc_id: GPCF-DOC-AGENT-REACH-ISOLATED-INSTALL-20260622
title: Agent-Reach 隔离安装审查
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/third_party/agent-reach/ISOLATED_INSTALL_REVIEW.md
source_path: third_party/agent-reach/ISOLATED_INSTALL_REVIEW.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach 隔离安装审查

本文件记录 `GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001` 的隔离安装结论。该结论只覆盖 `/tmp` 临时目录、临时 `HOME` 和临时 Python venv，不代表项目仓、用户全局环境或生产环境已安装。

## 安装边界

| 项 | 结论 |
| --- | --- |
| 上游锁定 | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| 包版本 | `1.5.0` |
| 初始默认 Python | `3.9.6`，被 `>=3.10` 要求拦截 |
| 实际隔离 Python | `3.12.13` |
| 安装位置 | `/tmp/gpcf-agent-reach-p1-venv` |
| 临时 HOME | `/tmp/gpcf-agent-reach-p1-home` |
| 项目内安装 | `false` |
| 全局安装 | `false` |
| 生产配置写入 | `false` |

## 本地可运行检查

| 检查 | 结果 |
| --- | --- |
| `import agent_reach` | `pass` |
| `from agent_reach.core import AgentReach` | `pass` |
| `agent-reach --help` | `pass` |
| `agent-reach --version` | `Agent Reach v1.5.0` |
| `agent-reach doctor --json` | `pass_with_probe` |

## Doctor 结果摘要

本轮 doctor 只作为安装健康探测使用，不作为搜索结果、不作为业务证据。

| 状态 | 通道 |
| --- | --- |
| ok | `web`, `rss`, `bilibili` |
| warn | `github`, `twitter`, `youtube`, `v2ex`, `xueqiu` |
| off | `reddit`, `xiaohongshu`, `linkedin`, `xiaoyuzhou`, `exa_search` |

## 配置与凭据

| 项 | 结论 |
| --- | --- |
| 临时 `.agent-reach/` 目录 | 已由只读配置对象初始化创建 |
| 临时 `config.yaml` | `false`，未写入 |
| 用户真实 `~/.agent-reach` | 未写入、未清理、未声明状态 |
| token / key / cookie | 未写入 |
| browser cookie 抽取 | 未执行 |
| `configure` | 未执行 |
| `install --channels` | 未执行 |

## 非声明

- 不声明 Agent-Reach 已纳入项目群生产能力。
- 不声明任一搜索通道已完成业务验证。
- 不声明 Exa、Reddit、小红书、LinkedIn 或小宇宙可用。
- 不声明 KDS canonical Markdown、GFIS source-of-record、生产配置或全局 MCP 配置已写入。
- 不声明 accepted、integrated 或 production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001`：建立受控 adapter skeleton、命令白名单、无凭据 dry-run fixture 和搜索结果候选结构，不调用真实搜索、不写 KDS canonical、不写 GFIS source-of-record。
