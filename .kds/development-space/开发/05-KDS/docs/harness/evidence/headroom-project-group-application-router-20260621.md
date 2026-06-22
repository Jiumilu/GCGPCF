---
doc_id: GPCF-DOC-1C0104FCC9
title: Headroom Project Group Application Router Evidence
project: KDS
related_projects: [KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-project-group-application-router-20260621.md
source_path: docs/harness/evidence/headroom-project-group-application-router-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom Project Group Application Router Evidence

## Evidence ID

`HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-20260621`

## 结论

本轮将 Headroom marker policy、controlled pilot 和 LOOP cost observation series 固化为项目群应用路由注册表。

`application_router_gate | true`，`dry_run_application_gate | true`，`production_admission_gate | false`，`measured_production_tokens | false`。

当前路由只允许 dry-run 应用到通过 marker 与 saving 门禁的结构化输出；生产应用、真实 KDS 写入和真实外部 API 写入全部保持 false。

## 路由表

| scenario_id | content_type | route_mode | dry_run | production | saving_rate |
|---|---|---|---|---|---:|
| project_group_evidence_json | json_tool_output | blocked | false | false | 0.0 |
| headroom_metric_json_array | metric_json_array | dry_run_apply | true | false | 0.510989 |
| loop_validation_log | loop_log_output | blocked | false | false | 0.870801 |
| rg_marker_search_output | search_output | blocked | false | false | 0.538702 |
| headroom_cost_measurement_output | structured_metric_tool_output | dry_run_apply | true | false | 0.625378 |
| marker_preserving_log_search_adapter_output | marker_preserving_adapter_output | adapter_only_dry_run_apply | true | false | 0.640676 |

## 路由边界

- `project_count`: 15
- `allowed_route_count`: 3
- `blocked_route_count`: 3
- `production_route_count`: 0
- `authorized_window_present`: false
- `authorization_action_queue_gate`: false
