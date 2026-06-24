---
doc_id: GPCF-DOC-AGENT-REACH-P8-OPERATOR-HANDOFF-20260623
title: Agent-Reach P8 Operator Handoff 2026-06-23
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.md
source_path: docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach P8 Operator Handoff 2026-06-23

- status: `p8_operator_handoff_ready_pending_authorization`
- readiness_status: `p8_live_execution_ready_pending_human_authorization`
- current_admission: `limited_candidate_only`
- live_external_search_invoked: `False`

## run

本轮固化 P8 授权后执行交接清单，只生成本地 evidence，不执行真实搜索。

## stop

停止类型为 `authorization_boundary`。未收到正式 P8 三批授权前，不得执行真实 web/rss/bilibili 搜索。

## verify

### Required Authorization Text

```text
授权执行 Agent-Reach P8 Project Group Full Live Search Batch 1
授权执行 Agent-Reach P8 Project Group Full Live Search Batch 2
授权执行 Agent-Reach P8 Project Group Full Live Search Batch 3
授权人：lujunxiang
有效期：<start-iso8601> 至 <end-iso8601>
仅允许 web/rss/bilibili 公开内容读取，Batch 1/2 最多 5 个 query，Batch 3 最多 4 个 query，每个 query 最多 10 条结果。
禁止写凭据、提取 cookie、写 KDS canonical、写 GFIS source-of-record、改生产配置、改全局 MCP 配置、生产集成或声明 accepted/integrated/production_ready。
```

### Local Authorization Files

- `fixtures/agent-reach/project-group-full-live-search-batch-1-authorization.local.json` exists=`False`
- `fixtures/agent-reach/project-group-full-live-search-batch-2-authorization.local.json` exists=`False`
- `fixtures/agent-reach/project-group-full-live-search-batch-3-authorization.local.json` exists=`False`

### Command Recipe

| step | command | expected |
|---|---|---|
| authorization_text_dry_run | `python3 tools/kds-sync/ingest_agent_reach_p8_authorization_text.py --authorization-text-file <authorization-text-file>` | status=dry_run_valid |
| authorization_text_write_local_auth | `python3 tools/kds-sync/ingest_agent_reach_p8_authorization_text.py --authorization-text-file <authorization-text-file> --write-local-auth` | writes fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json only after valid authorization |
| local_authorization_window_audit | `python3 tools/kds-sync/validate_agent_reach_p8_local_authorization_window_audit.py` | blocks missing, future, expired, and wrong-batch local authorization files without network access |
| pre_execution_readiness | `python3 tools/kds-sync/validate_agent_reach_p8_live_execution_readiness_matrix.py` | status=p8_live_execution_ready_pending_human_authorization before local auth, or no readiness regression after local auth |
| execute_live_with_evidence | `python3 tools/kds-sync/run_agent_reach_p8_post_authorization_driver.py --authorization-text-file <authorization-text-file> --write-local-auth --execute-live --write-evidence --report docs/harness/evidence/agent-reach-p8-post-authorization-driver-live-20260623.json` | requires --write-evidence with --execute-live |
| output_quality_gate | `python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py` | all project/query/channel coverage, no duplicate URLs, no query errors, required field coverage 1.0 |
| document_governance | `python3 tools/kds-sync/document_control.py && python3 tools/kds-sync/check_document_pollution.py && python3 tools/kds-sync/validate_kds_token.py && python3 tools/kds-sync/loop_document_gate.py` | controlled evidence, pollution pass, KDS token pass, loop document gate pass |

## recover

删除本轮 evidence、loop 文档和 validator 即可回滚；本轮不创建 `.local.json` 授权文件。

## debug

- 下一步仍是 `GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`。
- 执行后必须跑 output quality gate 与文档治理门禁。

## 非声明

- 本证据不声明全量真实搜索已完成。
- 本证据不声明 accepted / integrated / production_ready。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
