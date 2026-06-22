---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P1-ISOLATED-INSTALL-001
title: Agent-Reach P1 隔离安装 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P1 隔离安装 Loop 记录

## 输入

- `GPCF-AGENT-REACH-P0-SOURCE-LOCK-001` 已完成，下一轮为 `GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001`。
- 上游锁定为 `22d7f03a59401b5740b380c3ad43e3ff7a9dc373`，包版本为 `1.5.0`。
- 本轮不得写入 KDS canonical、GFIS source-of-record、生产配置或全局 MCP 配置。

## 动作

- 使用 `/tmp/gpcf-agent-reach-p1-home` 作为临时 HOME。
- 使用 `/tmp/gpcf-agent-reach-p1-venv` 作为临时 Python venv。
- 先用默认 Python 尝试安装并记录 `3.9.6` 被 `>=3.10` 要求拦截。
- 改用 Python `3.12.13` 完成隔离安装。
- 执行 CLI 帮助、版本、Python import 和 `doctor --json` 健康探测。

## 输出

- `third_party/agent-reach/ISOLATED_INSTALL_REVIEW.md`
- `docs/harness/evidence/agent-reach-p1-isolated-install-20260622.json`
- `docs/harness/evidence/agent-reach-p1-isolated-install-20260622.md`
- `tools/kds-sync/validate_agent_reach_p1_isolated_install.py`

## 检查

- `import agent_reach`：通过。
- `from agent_reach.core import AgentReach`：通过。
- `agent-reach --help`：通过。
- `agent-reach --version`：`Agent Reach v1.5.0`。
- `doctor --json`：通过但发生健康探测，结论仅用于安装健康，不用于搜索质量验收。
- 临时 `config.yaml`：未写入。

## 反馈

- P1 隔离安装可继续推进，但仍只能作为候选能力。
- `doctor` 的健康探测会触达部分公开平台状态检查，后续 validator 必须区分 `doctor_health_probe_invoked` 与 `live_external_search_invoked`。
- `exa_search`、`reddit`、`xiaohongshu`、`linkedin`、`xiaoyuzhou` 仍为 off，不能声明全量搜索能力可用。

## 下一轮

进入 `GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001`：建立受控 adapter skeleton、命令白名单、无凭据 dry-run fixture 和搜索结果候选结构，不调用真实搜索、不写 KDS canonical、不写 GFIS source-of-record。
