---
doc_id: GPCF-DOC-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-20260622
title: Agent-Reach P8 授权文本摄取证据 2026-06-22
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach P8 授权文本摄取证据 2026-06-22

- status: `p8_authorization_text_intake_ready`
- dry_run_status: `dry_run_valid`
- isolated_write_status: `local_authorization_files_written`
- negative_status: `rejected`
- default_local_authorization_files_created: `False`
- live_external_search_invoked: `False`

## run

- 新增授权文本摄取脚本，支持从一段文本抽取授权人、有效期和三条 P8 batch 授权文本。
- 默认 dry-run；只有显式 `--write-local-auth` 才会委托创建 `.local.json`。

## stop

- 本轮不执行真实搜索，不写默认授权文件。
- 缺少任一批次授权文本、授权人、有效期、渠道或禁止边界时拒绝。

## verify

- 完整文本 dry-run 通过。
- 完整文本在临时目录隔离写入通过。
- 缺少 Batch 3 的负向文本被拒绝。
- 默认 fixtures 授权文件未创建。

## recover

- 摄取脚本不写生产配置，不写 KDS canonical，不写 GFIS source-of-record。
- 如误写默认授权文件，删除 `fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json` 后重新运行验证器。

## debug

下一步仍需正式 P8 三批授权文本与具体 ISO 起止时间窗口。
