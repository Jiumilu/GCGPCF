---
doc_id: GPCF-DOC-LOOP-ROUND-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001
title: Loop Round GPCF-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001

## run

建立 Agent-Reach P7 live search dry-run 的授权预检门禁。新增 `tools/kds-sync/validate_agent_reach_p7_authorization_precheck.py`，验证 P7 授权文件必须满足 approved 状态、具体 ISO8601 时间窗、`web/rss/bilibili` 范围、5 个 query、每 query 10 条结果、只写 evidence、保留禁用项和日志脱敏。

## stop

停止类型：`authorization_boundary`。默认 `fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json` 不存在时必须阻断，不能执行真实搜索。

## verify

验证命令：

```bash
python3 tools/kds-sync/validate_agent_reach_p7_authorization_precheck.py --self-test
python3 tools/kds-sync/validate_agent_reach_p7_authorization_precheck.py
```

预期结果：正例授权通过；`missing-status`、`placeholder-time`、`out-of-scope-channel`、`too-many-results`、`binary-allowed` 负例被拒绝；默认无本地 P7 授权时 `authorization_file_missing`，且 `live_external_search_invoked=false`。

## recover

若误生成 P7 本地授权文件，先删除或隔离 `fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json`，再重跑授权预检和 P7 execution harness guard，确认默认阻断恢复。

## debug

当前仍未执行真实外部搜索。下一轮若要真实 dry-run，需要提供 P7 授权文件或等价授权文本，并明确 `authorization_status=approved_for_p7_limited_live_search_dry_run`、授权时间窗、执行范围和 `allow_agent_reach_binary_invocation=false`。
