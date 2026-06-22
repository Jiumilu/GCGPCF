---
doc_id: GPCF-DOC-85B4EB50A3
title: GPCF CodeGraph Sync Drift Closure
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-DRIFT-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-DRIFT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Sync Drift Closure

## 输入

- 上一轮 `LOOP-CODEGRAPH-INTEGRATION-CLOSURE-AUDIT-20260621` 登记 4 个 pending-sync 仓：Brain、GFIS、KDS、Studio。
- 用户要求只推进 CodeGraph 项目群集成，不进入项目内部开发任务。

## 动作

- 对 Brain、GFIS、KDS、Studio 执行 `codegraph sync`。
- 对 GFIS 追加一次 `codegraph sync` 复核残留提示。
- 对新增 GPCF 证据与 validator 产生的本仓 CodeGraph drift 执行 `codegraph sync`。
- 检查同步后 `codegraph status`。
- 检查 `.codegraph/` Git 状态。

## 输出

- Brain、KDS、Studio、GPCF 同步为 up-to-date。
- GFIS 保留 `residual_pending_notice`：重复 sync 后仍提示 `Added: 1 files`，但 sync 输出为 `Added: 1 - 0 nodes`。
- 新增 `docs/harness/evidence/loop-codegraph-sync-drift-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-sync-drift-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_sync_drift.py`。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_sync_drift.py`
- `git status --short -- .codegraph`

## 反馈

CodeGraph 项目群集成已从 4 仓 sync drift 收敛到 1 个 GFIS 残留提示，且 GPCF 本仓证据变更已同步进 CodeGraph。下一轮输入为 `GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001`，只在集成层调查 GFIS `Added: 1 files / 0 nodes` 残留提示，不进入 GFIS 业务开发。
