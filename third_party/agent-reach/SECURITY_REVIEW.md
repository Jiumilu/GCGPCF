---
doc_id: GPCF-DOC-AGENT-REACH-SECURITY-REVIEW-20260622
title: Agent-Reach 安全审查
project: GPC
related_projects: [GPC, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/third_party/agent-reach/SECURITY_REVIEW.md
source_path: third_party/agent-reach/SECURITY_REVIEW.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach 安全审查

## 安全面

| surface | observed upstream behavior | P0 decision |
| --- | --- | --- |
| local config | `~/.agent-reach/config.yaml` may store token/cookie/proxy values | isolated install only in P1 |
| config permissions | code attempts `0600` on config save | verify in P1 |
| browser cookies | optional extraction from browser via cookie helpers | blocked until explicit credential authorization |
| xhs cookie file | may write `~/.agent-reach/xhs-cookies.json` | blocked until explicit credential authorization |
| mcporter config | install/uninstall may add/remove MCP entries | blocked in P0 |
| system package install | installer may call package managers or npm | blocked in P0 |
| subprocess execution | installer and channel probes execute external tools | isolated HOME / PATH required in P1 |
| external network | channels may call Jina, Exa, platform APIs, public sites | no live external search in P0 |
| transcribe provider | Groq/OpenAI keys may be used for Whisper | blocked until explicit key authorization |

## 凭据边界

P0 forbids storing or printing:

- KDS token.
- GitHub token.
- Twitter/X auth token or ct0.
- Xiaohongshu cookie.
- Xueqiu cookie.
- Reddit cookie.
- Groq/OpenAI API key.
- Proxy credential.

任何后续 credential test 在适用时必须使用专用 low-risk account，必须可撤销，并且只能产出 redacted evidence。

## P1 必需控制项

| control | requirement |
| --- | --- |
| temporary HOME | required |
| temporary venv | required |
| temporary npm prefix | required when npm is used |
| dry-run first | required |
| uninstall dry-run | required |
| config leakage scan | required |
| global MCP diff | required |
| rollback evidence | required |

## 安全结论

P0 仅按 source-lock 口径通过。

当前不批准 production 或 login-enabled channel。下一项安全动作是 `GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001`，不是 production integration。
