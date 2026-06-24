---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001
title: LOOP Round GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001

## run

- 输入：P7 查询计划、P7 runner、P7 output quality gate。
- 动作：新增并执行本地 runtime dependency precheck。
- 输出：dependency precheck script、evidence、Loop 轮次文档。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：P7 runtime dependency 已就绪；本轮未收到 P7 live dry-run 授权，不执行真实搜索。

## verify

- `check_agent_reach_p7_runtime_dependencies.py` 扫描 5 个 P7 查询计划。
- `python3` 可用，覆盖 web 通道的 `duckduckgo_html_via_python_stdlib` backend。
- `curl` 可用，覆盖 RSS 和 Bilibili 通道。
- `missing_binaries=[]`。
- 本轮未执行真实搜索，`live_external_search_invoked=false`。

## recover

- 若后续 backend 变化，重新运行 dependency precheck。
- 若授权文件错误，删除本地授权文件并重新生成。
- 若 P7 live dry-run 失败，删除 P7 runtime evidence，保留本轮 precheck evidence。

## debug

- 当前阻塞：缺少 P7 live dry-run 授权。
- 下一轮：`GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001`
