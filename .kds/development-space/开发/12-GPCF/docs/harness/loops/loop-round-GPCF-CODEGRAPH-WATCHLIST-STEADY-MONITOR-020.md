---
doc_id: GPCF-DOC-8C1A3F9020
title: Loop Round - CodeGraph watchlist steady monitor 20260623
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph watchlist steady monitor 20260623

## run

- 输入：`GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019` 后的 14 仓 live 状态。
- 范围：Brain、GFIS、KDS、Studio、GPCF 与其余 9 仓的 current live CodeGraph / Git 状态。
- 目标：只读复核 14 仓 watchlist，确认本仓 self-sync 后的当前态，并保留 KDS / Studio / GPCF drift watch。

- 只读读取 14 仓 `codegraph status --json .`。
- 只读读取 14 仓 `git status --short` 与各仓 `.codegraph/` 隔离状态。
- 记录当前 watch items 和本仓 self-sync 后的收口状态。
- 生成 current-state evidence 与 validator。

## stop

- stop_type：`watch_required`
- 停止证据：Brain/GFIS/KDS/Studio/GPCF 进入只读 watchlist 维持；不进入业务开发，不执行 watchlist 仓 sync 或 clean reindex。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_watchlist_steady_monitor_20260623.py
```

同时保留：

```bash
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019`
- 可重试动作：重新只读采集 14 仓 live state 与 `.codegraph` 隔离状态。
- 不可重试动作：未授权 sync、clean reindex、业务开发、commit、push、deploy、生产写入、外部 API 写入。
- 恢复轮次：`GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`

## debug

- 当前阻塞：KDS mirror / WorkWiki 仍有 Git dirty，Studio 仍有 CodeGraph modified residual，GPCF 已 self-sync 清零 pending，但本地工作树仍 dirty。
- 下一轮：`GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。

## 输出

- `docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.json`
- `docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.md`
- `tools/kds-sync/validate_codegraph_watchlist_steady_monitor_20260623.py`
