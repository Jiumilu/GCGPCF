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

- Studio：residual pending 为 added=0、modified=18、removed=0，已超过授权前 modified=9 上限，需要重新收口 watch 边界。
- Brain：CodeGraph pending 已归零，但仍有 1 个 Git dirty，继续保持授权边界。
- GFIS：CodeGraph pending 已归零，但仍有 1 个 Git dirty，GFIS clean reindex 仍不授权。
- KDS：CodeGraph pending 已归零，但仍有 31 个 Git dirty，下一轮应优先做 KDS mirror / WorkWiki scope review 授权包。
- `review_rework_count=0`，沿用稳态监控基线；本轮未进入业务开发，因此没有新增 review 返工。

## 监控表

| repo | CodeGraph pending | Git dirty | 状态 | 决策 |
| --- | --- | ---: | --- | --- |
| Brain | added=0, modified=0, removed=0 | 1 | codegraph_clean_but_git_dirty | authorization_required |
| GFIS | added=0, modified=0, removed=0 | 1 | codegraph_clean_but_git_dirty | authorization_required_without_clean_reindex |
| KDS | added=0, modified=0, removed=0 | 31 | git_dirty_growth_watch | authorization_required |
| Studio | added=0, modified=18, removed=0 | 20 | residual_exceeds_authorized_ceiling | sync_only_precheck_completed_with_residual_watch |

## 五方向

### run

只读监控 Studio sync-only 后状态，以及 Brain/GFIS/KDS 未授权 watchlist 状态。

### stop

`stop_type=watch_required`。Studio residual 已超过授权上限，Brain/GFIS/KDS 仍需独立授权，不能自动执行 sync 或 clean reindex。

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

若 Studio residual 继续增长或出现 added/removed，则回到 Studio 专项授权；若 KDS 继续增长，进入 KDS mirror scope review 授权包。

### debug

Studio residual 已超过授权上限；KDS dirty 仍是下一轮最明确的治理风险；GFIS clean reindex 仍不授权。

## 非声明

- 不声明任何业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 Brain、GFIS、KDS sync-only closure 完成。
- 不声明 Studio 业务闭合。
- 不声明 GFIS clean reindex 已执行或已授权。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`
