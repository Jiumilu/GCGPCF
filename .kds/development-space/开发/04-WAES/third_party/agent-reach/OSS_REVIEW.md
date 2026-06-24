---
doc_id: GPCF-DOC-AGENT-REACH-OSS-REVIEW-20260622
title: Agent-Reach OSS 审查
project: WAES
related_projects: [WAES, KDS]
domain: general
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/third_party/agent-reach/OSS_REVIEW.md
source_path: third_party/agent-reach/OSS_REVIEW.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach OSS 审查

## 许可证

| item | value |
| --- | --- |
| upstream license | `MIT` |
| copyright | `Copyright (c) 2025 Agent Eyes` |
| redistribution allowed | `yes` |
| attribution required | `yes` |
| warranty disclaimer required | `yes` |
| source modification in this repo | `none` |

## 包依赖

| dependency | scope |
| --- | --- |
| `requests>=2.28` | runtime |
| `feedparser>=6.0` | runtime |
| `python-dotenv>=1.0` | runtime |
| `loguru>=0.7` | runtime |
| `pyyaml>=6.0` | runtime |
| `rich>=13.0` | runtime |
| `yt-dlp>=2024.0` | runtime |
| `playwright>=1.40` | optional browser |
| `browser-cookie3>=0.19` | optional cookies |
| `mcp[cli]>=1.0` | optional all |
| `pytest>=8.0` | dev |
| `ruff>=0.8` | dev |
| `mypy>=1.12` | dev |

## 外部工具依赖

| tool | reason | GlobalCloud P0 decision |
| --- | --- | --- |
| `mcporter` | Exa and MCP routing | do not install in P0 |
| `gh` | GitHub channel | do not authenticate in P0 |
| `yt-dlp` | YouTube channel | do not run in P0 |
| `ffmpeg` | transcription | do not install in P0 |
| `OpenCLI` | login-session channels | gated pilot only |
| `twitter-cli` | Twitter/X channel | gated pilot only |
| `rdt-cli` | Reddit channel | gated pilot only |
| `bili-cli` | Bilibili channel | controlled pilot only |

## OSS 结论

在任何复制或分发包中保留 attribution 与 warranty text 的前提下，`MIT` license 与受控候选 pilot 兼容。

P0 不批准生产使用。生产准入仍需要 P1-P8 evidence、WAES/KDS review、credential safety、rollback、benchmark 与明确 approval。
