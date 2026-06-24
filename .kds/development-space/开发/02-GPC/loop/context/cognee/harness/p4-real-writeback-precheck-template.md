---
doc_id: GPCF-DOC-8C7F2F5001
title: COGNEE P4 真实写入前置预检模板（最小字段）
project: GPC
related_projects: [GPC, GPCF]
domain: general
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/loop/context/cognee/harness/p4-real-writeback-precheck-template.md
source_path: loop/context/cognee/harness/p4-real-writeback-precheck-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# COGNEE P4 真实写入前置预检模板（最小字段）

> 用于 `cognee` 真实写回前置预检（precheck）验证，记录授权来源、依赖就绪和回滚可用性。

| task_id | round_id | project_id | scenario | operation | owner | payload_tier | precheck_passed | write_requested | write_allowed | owner_authorization_present | authorization_token_source | runtime_dependency_ok | rollback_plan_verified | expected_blocked_reason | token_before | token_after | latency_ms | marker_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `cognee-p4-task-001` | `loop-round-xxx` | `GPCF` | `writeback_precheck_live_gate` | `remember` | `GPCF` | `writeback_live` | `true` | `true` | `true` | `true` | `owner_jwt` | `true` | `true` | `none` | `1480` | `1368` | `94` | `pass` |

- `operation`: `remember` / `forget`
- `payload_tier`: `writeback_live`
- `authorization_token_source`: `none` | `owner_jwt` | `project_group_jwt` | `service_account` | `runtime_token` | `human_token`
- `precheck_passed`: `true` 表示本次写前置校验通过
- `runtime_dependency_ok`: 运行依赖可达时为 `true`
- `rollback_plan_verified`: 回滚计划可验证且可自动阻断时为 `true`
- `expected_blocked_reason`: 当 `write_allowed=false` 时必填；成功通过可填 `none`
- `write_allowed` 仅在 `precheck_passed + owner_authorization_present + runtime_dependency_ok + rollback_plan_verified + waes_decision=pass` 且未触发阻断时建议为 `true`
