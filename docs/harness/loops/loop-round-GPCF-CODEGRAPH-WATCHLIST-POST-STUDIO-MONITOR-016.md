---
doc_id: GPCF-DOC-9D0EC80EB6
title: Loop Round - CodeGraph watchlist post-Studio 监控
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph watchlist post-Studio 监控

## run

- 输入：`GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015` 的 clean 收口结果。
- 范围：Brain、GFIS、KDS、Studio 四仓 watchlist。
- 动作：只读采集四仓 CodeGraph status 与 Git dirty，确认 Studio residual 和其他三仓授权边界。
- 输出：
  - `docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.json`
  - `docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.md`
  - `tools/kds-sync/validate_codegraph_watchlist_post_studio_monitor.py`

## stop

- stop_type：`watch_required`
- 停止证据：Brain/GFIS/Studio 已收口，KDS 仍有 Git dirty，需要下一轮授权包复核。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_watchlist_post_studio_monitor.py
```

同时保留：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`
- 可重试动作：重新只读采集 watchlist status。
- 不可重试动作：未授权 sync、clean reindex、业务开发、commit、push、deploy、生产写入、外部 API 写入。
- 恢复轮次：`GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`

## debug

- 当前阻塞：KDS mirror / WorkWiki dirty 仍需复核，Brain/GFIS/Studio 已收口。
- 下一轮：`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
