---
doc_id: GPCF-DOC-D3B37861BD
title: GPCF CodeGraph Watchlist Sync Plan 001
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Watchlist Sync Plan 001

## 输入

- 上一轮输出：`GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001`。
- 上一轮证据：`docs/harness/evidence/codegraph-project-group-steady-state-recheck-20260621.json`。
- 当前 live watch：Brain `modified=12`，Studio `modified=5`，GFIS `added=1`，GPCF pending=0。

## 动作

- 对 Brain/Studio/GFIS/GPCF 执行只读 `codegraph status --json .`。
- 对 Brain/Studio/GFIS/GPCF 执行只读 `.codegraph` Git 隔离检查。
- 建立 owner / threshold / action watchlist 矩阵。
- 明确 Brain/Studio 再次 sync 的授权口令。
- 生成 evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.json`
- `docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.md`
- `tools/kds-sync/validate_codegraph_watchlist_sync_plan.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_watchlist_sync_plan.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

Brain/Studio active drift 已从“发现”转成可执行 watchlist 计划，但未获得新授权前不执行 sync。GFIS 继续保持 policy exception watch；GPCF 继续允许治理证据生成后的 self-sync。本轮不进入业务开发，不提交、不推送、不部署，不升级 accepted / integrated / production_ready。

下一轮进入 `GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002`。
