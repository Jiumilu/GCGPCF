---
doc_id: GPCF-DOC-61F5839244
title: CodeGraph watchlist post-Studio 监控证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.md
source_path: docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph watchlist post-Studio 监控证据

本证据对应 `GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`。

## 结论

本轮只读监控 Studio sync-only precheck 后状态，以及 Brain、GFIS、KDS 未授权 watchlist 状态。本轮不执行任何 watchlist 仓 `codegraph sync`，不执行 clean reindex，不进入业务开发，不提交、不推送、不部署。

结论为 `watch_required`：

- Brain：CodeGraph pending 已归零，Git dirty=0，继续监控即可。
- GFIS：CodeGraph pending 已归零，Git dirty=0，继续监控即可。
- Studio：CodeGraph pending 已归零，Git dirty=0，sync-only 已收口。
- KDS：CodeGraph pending 为 modified=2，仍有 17 个 Git dirty，下一轮应优先做 KDS mirror / WorkWiki scope review 授权包。
- `review_rework_count=0`，沿用稳态监控基线；本轮未进入业务开发，因此没有新增 review 返工。

## 监控表

| repo | CodeGraph pending | Git dirty | 状态 | 决策 |
| --- | --- | ---: | --- | --- |
| Brain | added=0, modified=0, removed=0 | 0 | codegraph_clean_and_git_clean | monitor_only |
| GFIS | added=0, modified=0, removed=0 | 0 | codegraph_clean_and_git_clean | monitor_only |
| KDS | added=0, modified=2, removed=0 | 17 | git_dirty_growth_watch | authorization_required |
| Studio | added=0, modified=0, removed=0 | 0 | clean_after_sync | monitor_only |

## 五方向

### run

只读监控 Studio sync-only 后状态，以及 Brain/GFIS/KDS 未授权 watchlist 状态。

### stop

`stop_type=watch_required`。Brain/GFIS/Studio 已收口，KDS 仍需独立授权，不能自动执行 sync 或 clean reindex。

### verify

回放：

```bash
python3 tools/kds-sync/validate_codegraph_watchlist_post_studio_monitor.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

### recover

若 KDS 继续增长，进入 KDS mirror scope review 授权包；若 Brain/GFIS/Studio 再次出现 dirty，则回到对应只读监控。

### debug

KDS dirty 仍是下一轮最明确的治理风险；GFIS clean reindex 仍不授权。

## 非声明

- 不声明任何业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 Brain、GFIS、KDS sync-only closure 完成。
- 不声明 Studio 业务闭合。
- 不声明 GFIS clean reindex 已执行或已授权。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`
