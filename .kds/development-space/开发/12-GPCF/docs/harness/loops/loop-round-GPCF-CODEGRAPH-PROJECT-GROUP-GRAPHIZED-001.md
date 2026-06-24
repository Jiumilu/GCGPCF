---
doc_id: GPCF-DOC-222DA884C1
title: GPCF CodeGraph Project Group Graphized
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-GRAPHIZED-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-GRAPHIZED-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Project Group Graphized

## 输入

- 目标：完成整个项目群的图谱化。
- 上一轮 `GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001` 已建立 Brain、Studio、GPCF 的同步授权门。
- 当前控制板显示项目群 CodeGraph 范围已扩展到 14 仓，新增 WAS世界资产体系。
- Brain 曾按用户指令临时跳过；本轮复核后仅同步 `.codegraph`，但最终复核仍出现活动漂移。

## 动作

- 复核 14 仓 CodeGraph 当前状态。
- 对 Brain、KDS、Studio、GFIS、GPCF 执行受控 `codegraph sync`，仅更新 `.codegraph/`。
- 复核 14 仓 `.codegraph/` Git 保护。
- 固化项目群图谱化 evidence。
- 不进入项目内部开发，不修改业务代码。

## 输出

- 14 仓均已纳入 CodeGraph 本地图谱。
- 11 仓 up-to-date。
- Brain 已执行受控 `.codegraph` 同步复核，但后续复核出现 `Modified: 32 files` 活动漂移；不改业务文件，不杀进程。
- Studio 已执行受控 `.codegraph` 同步复核，但后续复核出现 `Added: 2 files; Modified: 2 files` 活动漂移；不改业务文件，不杀进程。
- GFIS 保持受控 residual：`Added: 1 files` / `Added: 1 - 0 nodes`。
- Studio 与 WAS世界资产体系均纳入项目群图谱和 Loop 证据。
- 新增 `docs/harness/evidence/loop-codegraph-project-group-graphized-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-project-group-graphized-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_project_group_graphized.py`。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_project_group_graphized.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

项目群 CodeGraph 图谱化覆盖已在本机治理边界内建立：14 仓覆盖、11 仓 up-to-date、Brain 与 Studio active watchlist、GFIS residual 受控、`.codegraph/` 不入 Git。下一轮进入 `GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`，持续监控 Brain 与 Studio 活动漂移，不进入项目业务开发。
