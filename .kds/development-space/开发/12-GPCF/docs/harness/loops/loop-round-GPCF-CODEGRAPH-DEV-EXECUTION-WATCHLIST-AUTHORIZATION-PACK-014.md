---
doc_id: GPCF-DOC-E17EF2D241
title: Loop Round - CodeGraph watchlist 授权包
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph watchlist 授权包

## run

- 输入：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013` 的四仓分诊结果。
- 范围：Brain、GFIS、KDS、Studio 的 CodeGraph watchlist 授权问题。
- 动作：生成问答式授权包，明确建议授权项、暂缓项、禁止项和下一轮候选。
- 输出：
  - `docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.json`
  - `docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.md`
  - `tools/kds-sync/validate_codegraph_dev_execution_watchlist_authorization_pack.py`

## stop

- stop_type：`authorization_boundary`
- 停止证据：本轮只生成授权包；未获得明确授权前不得对 Brain、GFIS、KDS、Studio 执行 sync-only closure、clean reindex、commit、push、deploy 或业务开发。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_authorization_pack.py
```

同时保留：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013`
- 可重试动作：重新只读刷新四仓 status 并重新生成授权问答。
- 不可重试动作：未授权 watchlist sync、clean reindex、commit、push、deploy、生产写入、外部 API 写入、业务开发。
- 恢复轮次：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014`

## debug

- 当前阻塞：缺少用户对具体仓与具体动作的显式授权。
- 下一授权：优先建议 `GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`。
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
