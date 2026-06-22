---
doc_id: GPCF-DOC-F063780121
title: LOOP Round GPCF Headroom Project Group Application Router 001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Project Group Application Router 001

## 输入

- `docs/harness/evidence/headroom-marker-preservation-policy-20260621.json`
- `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json`
- `docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json`
- `docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json`

## 动作

1. 新增 `tools/kds-sync/build_headroom_project_group_application_router.py`。
2. 新增 `tools/kds-sync/validate_headroom_project_group_application_router.py`。
3. 将 marker policy 转为项目群应用路由注册表。
4. 校验 dry-run 允许路由、阻断路由、生产路由和授权边界。

## 输出

- `docs/harness/evidence/headroom-project-group-application-router-20260621.json`
- `docs/harness/evidence/headroom-project-group-application-router-20260621.md`
- `tools/kds-sync/build_headroom_project_group_application_router.py`
- `tools/kds-sync/validate_headroom_project_group_application_router.py`

## 检查

| 检查项 | 结果 |
|---|---|
| route_count | 6 |
| allowed_route_count | 3 |
| blocked_route_count | 3 |
| dry_run_application_gate | true |
| production_route_count | 0 |
| authorized_window_present | false |
| production_admission_gate | false |

## 反馈

Headroom 已具备项目群 dry-run 应用路由注册表。当前仍只允许结构化 metric/tool output 和 marker-preserving adapter output 进入 dry-run 应用；生产代理、真实 KDS 写入、真实外部 API 写入和状态升级仍全部阻断。
