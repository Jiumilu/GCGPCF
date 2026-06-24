---
doc_id: GPCF-DOC-CGFSR019
title: Loop Round - CodeGraph GFIS 只读 Scope Review
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph GFIS 只读 Scope Review

## run

- 输入：用户授权“允许对 GFIS 做只读 CodeGraph/Git scope review；不包含 sync、clean reindex 或业务开发”。
- 范围：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS`。
- 动作：只读运行 `git status --short`、`codegraph status --json .`、`.codegraph` Git 隔离检查。
- 输出：
  - `docs/harness/evidence/codegraph-gfis-scope-review-20260623.json`
  - `docs/harness/evidence/codegraph-gfis-scope-review-20260623.md`
  - `tools/kds-sync/validate_codegraph_gfis_scope_review.py`

## stop

- stop_type：`clean_current_state`
- 停止证据：GFIS Git dirty=0，CodeGraph pending added=0、modified=0、removed=0。
- 状态上限：`partial_evidence_only`，不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_gfis_scope_review.py
```

同时保留：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：GFIS clean current state。
- 可重试动作：重新只读采集 GFIS Git 与 CodeGraph status。
- 不可重试动作：未授权 GFIS sync、clean reindex、业务开发、commit、push、deploy。
- 恢复轮次：`GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019`

## debug

- 上一轮记录的 GFIS pending=3/dirty=239 已在本轮只读复核时变为 clean。
- 本轮未执行 GFIS `codegraph sync`。
- 下一轮：`GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020`
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
