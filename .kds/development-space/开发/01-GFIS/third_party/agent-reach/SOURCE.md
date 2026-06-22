---
doc_id: GPCF-DOC-AGENT-REACH-SOURCE-20260622
title: Agent-Reach Source Lock
project: GFIS
related_projects: [GFIS, KDS]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/third_party/agent-reach/SOURCE.md
source_path: third_party/agent-reach/SOURCE.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach Source Lock

## 上游源

| item | value |
| --- | --- |
| repository | `https://github.com/Panniantong/Agent-Reach.git` |
| verified_head | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| latest_commit_time | `2026-06-16T20:45:57+08:00` |
| latest_commit_subject | `Merge pull request #385 from Panniantong/codex/english-readme-browseract-trendshift` |
| package_name | `agent-reach` |
| package_version | `1.5.0` |
| python_requirement | `>=3.10` |
| license | `MIT` |
| source_file_count | `89` |
| source_archive_copied | `false` |

## 入口

| entry | value |
| --- | --- |
| CLI | `agent-reach = agent_reach.cli:main` |
| Python API | `agent_reach.core.AgentReach` |
| health command | `agent-reach doctor --json` |
| config path | `~/.agent-reach/config.yaml` |
| config file mode | `0600` intended |

## 核心模块

| module | purpose |
| --- | --- |
| `agent_reach/cli.py` | install、doctor、configure、uninstall、skill、watch、transcribe |
| `agent_reach/config.py` | 本机配置和凭据键读取/写入 |
| `agent_reach/doctor.py` | 通道健康检查聚合 |
| `agent_reach/channels/*` | 多通道后端探测与 active backend 选择 |
| `agent_reach/cookie_extract.py` | 浏览器 cookie 读取和本机配置写入 |
| `agent_reach/transcribe.py` | 音频转写入口 |
| `agent_reach/skill/*` | 智能体使用指南候选 |
| `agent_reach/integrations/mcp_server.py` | 可选 MCP server skeleton |

## 支持通道

| channel | upstream backend |
| --- | --- |
| web | Jina Reader |
| exa_search | Exa via mcporter |
| github | gh CLI |
| youtube | yt-dlp |
| rss | feedparser |
| bilibili | bili-cli / OpenCLI |
| v2ex | V2EX public API |
| xueqiu | Xueqiu cookie-aware HTTP |
| twitter | twitter-cli / OpenCLI / bird |
| reddit | OpenCLI / rdt-cli |
| xiaohongshu | OpenCLI / xiaohongshu-mcp / xhs-cli |
| linkedin | linkedin-scraper-mcp / Jina Reader |
| xiaoyuzhou | Groq/OpenAI Whisper with ffmpeg |

## P0 结论

Source lock 完成，但只证明上游源可识别、版本可锁定、入口和风险面可列举。

该结论不证明：

- Agent-Reach 已安装。
- 任一通道在本机可用。
- live external search 已调用。
- KDS canonical Markdown 可写。
- GFIS source-of-record 可创建。
- production integration 可启用。
