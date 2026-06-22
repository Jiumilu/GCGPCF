---
doc_id: GPCF-DOC-DF923DE7E9
title: GPCF CodeGraph Project Group Monitor
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Project Group Monitor

## 输入

- 上一轮 `GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001` 已固化 GFIS 大文件 policy exception。
- 后续图谱化轮次已将项目群扩展为 14 仓，并纳入 Studio 与 WAS世界资产体系。
- 需要建立项目群 CodeGraph 轻量 monitor，检查 14 仓覆盖、`.codegraph` Git 保护、residual notice 与 policy exception。

## 动作

- 对 14 个本机项目仓执行 `codegraph status`。
- 对 14 个本机项目仓执行 `.codegraph` Git 状态检查。
- 检查 `.git/info/exclude` 是否包含 `.codegraph/`。
- 汇总 pending sync watchlist 与 GFIS policy exception。
- 对 Brain、Studio、GPCF 执行受控 `.codegraph` 同步复核。

## 输出

- 14 仓仍全部 indexed。
- 14 仓 `.codegraph/` Git 状态总数为 `0`。
- 11 仓 up-to-date。
- GPCF 普通 pending sync watchlist 已清空。
- Brain 同步后出现 `Modified: 32 files`，登记为活动仓 watchlist。
- Studio 同步后出现 `Added: 2 files; Modified: 2 files`，登记为活动仓 watchlist。
- GFIS 保持 policy exception。
- 新增 `docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_project_group_monitor.py`。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_project_group_monitor.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

CodeGraph 项目群监控已形成：14 仓覆盖和 Git 保护通过，GFIS policy exception 受控，GPCF 的普通 pending sync drift 已清空；Brain 同步后出现 `Modified: 32 files`，Studio 同步后出现 `Added: 2 files; Modified: 2 files`，均登记为活动仓 watchlist。下一轮进入 `GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`，只监控 Brain 与 Studio 活动漂移，不进入项目内部开发。
