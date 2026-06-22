---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001
title: LOOP Round GPCF-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001

## run

生成 P7 执行授权申请包，固定下一轮真实 dry-run 所需字段、授权文本和执行命令。本轮不创建 `limited-live-search-dry-run-authorization.local.json`。

## stop

停止类型：`authorization_boundary`。没有人工确认的 P7 本地授权文件时，runner 必须继续返回 `blocked_pending_execution_authorization`。

## verify

验证命令：

```bash
python3 tools/kds-sync/validate_agent_reach_p7_execution_authorization_request_package.py
```

预期结果：`p7_execution_authorization_request_package_ready`，并确认 `live_external_search_invoked=false`。

## recover

若误创建本地授权文件但未完成 P7 授权字段确认，删除或隔离 `fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json`，重跑 P7 授权申请包和 P7 授权预检。

## debug

当前阻塞仍是 P7 执行授权缺失。下一轮要进入真实 dry-run，必须先创建机器可校验的本地授权文件并通过 `validate_agent_reach_p7_authorization_precheck.py --authorization ...`。
