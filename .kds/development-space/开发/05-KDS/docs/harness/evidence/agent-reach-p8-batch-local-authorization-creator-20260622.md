---
doc_id: GPCF-DOC-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-20260622
title: Agent-Reach P8 批次本地授权创建器证据 2026-06-22
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P8 批次本地授权创建器证据 2026-06-22

- status: `p8_batch_local_authorization_creator_ready`
- dry_run_status: `dry_run_valid`
- isolated_write_status: `local_authorization_files_written`
- negative_status: `rejected`
- local_authorization_files_created: `False`
- isolated_authorization_files_created: `True`
- live_external_search_invoked: `False`

## run

- 新增 `tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py`，将精确 P8 批次授权文本转换为可机检 `.local.json`。
- 默认 dry-run；只有显式 `--write-local-auth` 才允许写本地授权文件。

## stop

- 本轮停止在授权创建器就绪，不执行真实搜索。
- 未收到三批 P8 执行授权时，不创建 `.local.json`。

## verify

- 正向 dry-run 覆盖三个 P8 batch。
- 隔离写入模式在临时目录生成三份授权文件，并通过 runner 授权校验。
- 负向用错误授权文本确认拒绝。
- 验证期间未写默认 fixtures 本地授权文件。

## recover

- 如误写授权文件，删除 `fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json` 后重新运行本验证器。

## debug

- 下一步仍需人工逐批授权 P8 Batch 1、Batch 2、Batch 3，才可执行 pipeline。

## 非声明

- 本证据仅为候选证据。
- 本证据不声明 accepted / integrated / production_ready 状态。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
- 本证据不持久化 raw provider payload。
