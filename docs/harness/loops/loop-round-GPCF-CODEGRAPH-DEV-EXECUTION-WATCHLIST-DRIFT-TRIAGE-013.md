---
doc_id: GPCF-DOC-F5BC0C93DF
title: Loop Round - CodeGraph watchlist 漂移分诊
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph watchlist 漂移分诊

## run

- 输入：`GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012` 的 watchlist。
- 范围：Brain、GFIS、KDS、Studio 四个活动漂移仓。
- 动作：只读采集 CodeGraph status 与 Git dirty 计数，生成分诊分类。
- 输出：
  - `docs/harness/evidence/codegraph-dev-execution-watchlist-drift-triage-20260622.json`
  - `docs/harness/evidence/codegraph-dev-execution-watchlist-drift-triage-20260622.md`
  - `tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py`

## stop

- stop_type：`authorization_boundary`
- 停止证据：Brain/GFIS/KDS 存在大范围 dirty；GFIS clean reindex 未授权；Studio 虽较小但仍需专项 sync-only precheck 授权。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py
```

同时保留：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_steady_state_monitor.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012`
- 可重试动作：重新只读采集 watchlist status。
- 不可重试动作：未授权 sync-only closure、clean reindex、commit、push、deploy、生产写入、外部 API 写入。
- 恢复轮次：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013`

## debug

- 当前阻塞：watchlist 漂移需要授权包或专项 precheck。
- 下一授权：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
