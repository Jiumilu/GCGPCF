---
doc_id: GPCF-DOC-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-20260622
title: Agent-Reach P8 授权后执行 Driver 证据 2026-06-22
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P8 授权后执行 Driver 证据 2026-06-22

- status: `p8_post_authorization_driver_ready`
- dry_run_status: `authorized_execution_not_requested`
- cli_dry_run_status: `authorized_execution_not_requested`
- negative_status: `rejected_execute_requires_write_evidence`
- cli_negative_exit_code: `1`
- default_local_authorization_files_created: `False`
- live_external_search_invoked: `False`

## run

- 新增 P8 post-authorization driver，串联授权文本摄取、授权文件创建、pipeline、输出质量门禁与返工队列入口。
- 验证只使用临时授权文件和 pipeline dry-run，不执行真实搜索。

## stop

- 本轮停止在授权后执行 driver 就绪。
- 未收到正式授权前，不写默认授权文件，不执行 web/rss/bilibili 请求。

## verify

- dry-run 路径进入 `authorized_execution_not_requested`。
- CLI dry-run 路径进入 `authorized_execution_not_requested`。
- `--execute-live` 未配套 `--write-evidence` 时被拒绝。
- CLI 负向路径以非零退出码拒绝。
- 默认 fixtures 授权文件未创建。

## recover

- 删除本轮 driver、validator 和 evidence/loop 文档即可回滚。

## debug

- 正式执行仍需要 P8 三批授权文本、ISO 时间窗、`--write-local-auth --execute-live --write-evidence`。
