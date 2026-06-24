---
doc_id: GPCF-DOC-AGENT-REACH-P1-ISOLATED-INSTALL-20260622
title: Agent-Reach P1 隔离安装证据 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p1-isolated-install-20260622.md
source_path: docs/harness/evidence/agent-reach-p1-isolated-install-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach P1 隔离安装证据 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001`，结论为 `isolated_install_ready`。当前准入仍为 `limited_candidate_only`。

## 安装事实

| 项 | 值 |
| --- | --- |
| 上游 HEAD | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| 包版本 | `1.5.0` |
| 默认 Python 尝试 | `3.9.6`，被 `>=3.10` 要求拦截 |
| 隔离 Python | `3.12.13` |
| 临时 HOME | `/tmp/gpcf-agent-reach-p1-home` |
| 临时 venv | `/tmp/gpcf-agent-reach-p1-venv` |
| 临时源码 | `/tmp/agent-reach-p1-source` |
| 项目内安装 | `false` |
| 全局安装 | `false` |

## 检查结果

| 检查 | 结果 |
| --- | --- |
| `import agent_reach` | `pass` |
| `from agent_reach.core import AgentReach` | `pass` |
| `agent-reach --help` | `pass` |
| `agent-reach --version` | `Agent Reach v1.5.0` |
| `agent-reach doctor --json` | `pass_with_probe` |
| 临时 `config.yaml` | `absent` |

## Doctor 摘要

`doctor --json` 会进行健康探测，因此本轮将其登记为 `doctor_health_probe_invoked=true`。该探测不等于搜索调用，不等于搜索质量验收。

| 状态 | 通道 |
| --- | --- |
| ok | `web`, `rss`, `bilibili` |
| warn | `github`, `twitter`, `youtube`, `v2ex`, `xueqiu` |
| off | `reddit`, `xiaohongshu`, `linkedin`, `xiaoyuzhou`, `exa_search` |

## 安全边界

| control | value |
| --- | --- |
| package_installed_in_isolated_venv | `true` |
| package_installed_in_project | `false` |
| package_installed_globally | `false` |
| doctor_health_probe_invoked | `true` |
| live_external_search_invoked | `false` |
| agent_reach_search_command_invoked | `false` |
| credential_written | `false` |
| browser_cookie_extraction_invoked | `false` |
| temporary_config_directory_created | `true` |
| temporary_config_file_written | `false` |
| kds_canonical_write_allowed | `false` |
| gfis_source_of_record_write_allowed | `false` |
| production_config_write_allowed | `false` |
| global_mcp_config_write_allowed | `false` |
| production_integration_allowed | `false` |

## 非声明

- 不声明 Agent-Reach 已纳入项目群生产能力。
- 不声明 live external search 已调用。
- 不声明任一搜索通道已通过业务质量验收。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001`：建立受控 adapter skeleton、命令白名单、无凭据 dry-run fixture 和搜索结果候选结构。
