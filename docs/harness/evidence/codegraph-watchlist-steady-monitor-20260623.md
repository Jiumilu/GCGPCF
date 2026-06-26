---
doc_id: GPCF-DOC-4D7F2B9020
title: CodeGraph watchlist steady monitor 20260623
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.md
source_path: docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph watchlist steady monitor 20260623

本证据对应 `GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020`。

## 结论

本轮只读复核 14 仓 live CodeGraph / Git 状态，不进入项目业务开发，不对 watchlist 仓执行 `codegraph sync`，不执行 clean reindex，不提交、不推送、不部署。

结论为 `watch_required`：

- 14 仓 CodeGraph 均可读，`.codegraph/` 均未进入 Git 状态。
- Brain、GFIS 的 CodeGraph pending 已清零，且各自 Git dirty 也已清零，继续纳入稳态 watch。
- KDS Git dirty 仍为 18，CodeGraph pending 已清零，KDS mirror / WorkWiki 仍需授权边界。
- Studio CodeGraph pending 为 `added=1, modified=2, removed=0`，仍保持 residual watch。
- GPCF 当前 CodeGraph pending 为 `added=28, modified=4, removed=0`，工作树仍有 405 个 Git dirty，继续 watch。
- `review_rework_count=0`，继续作为稳态监控趋势基线。

## 14 仓矩阵

| repo | CodeGraph pending | Git dirty | 决策 |
| --- | --- | ---: | --- |
| Brain | added=0, modified=0, removed=0 | 0 | steady |
| GFIS | added=0, modified=0, removed=0 | 0 | monitor_only_without_clean_reindex |
| KDS | added=0, modified=0, removed=0 | 18 | mirror_scope_review_required_now |
| Studio | added=1, modified=2, removed=0 | 9 | residual_pending_watch |
| GPCF | added=28, modified=4, removed=0 | 405 | self_sync_pending_residual_and_git_dirty |
| GPC | added=0, modified=1, removed=0 | 3 | steady |
| PVAOS | added=0, modified=1, removed=0 | 3 | steady |
| WAES | added=0, modified=0, removed=0 | 0 | steady |
| PKC | added=0, modified=0, removed=0 | 0 | steady |
| XiaoC | added=0, modified=0, removed=0 | 0 | steady |
| XGD | added=0, modified=0, removed=0 | 0 | steady |
| XiaoG | added=0, modified=0, removed=0 | 0 | steady |
| MMC | added=0, modified=0, removed=0 | 0 | steady |
| WAS | added=0, modified=0, removed=0 | 1 | steady |

## watch items

| repo | 决策 | 原因 |
| --- | --- | --- |
| Brain | steady | CodeGraph clean and local git dirty remains 0. |
| GFIS | monitor_only_without_clean_reindex | CodeGraph clean; sync and clean reindex still not authorized. |
| KDS | mirror_scope_review_required_now | CodeGraph clean but KDS mirror / WorkWiki dirty persists at 18. |
| Studio | residual_pending_watch | Studio retains modified pending residual at 3. |
| GPCF | self_sync_pending_residual_and_git_dirty | 本仓 pending 仍为 30，local git dirty still high. |

## 五方向

### run

读取 14 仓 live CodeGraph 状态与 Git dirty，记录当前 watchlist 和本仓 self-sync 后收口。

### stop

`stop_type=watch_required`。Brain/GFIS/KDS 进入 monitor_only，Studio 保留 residual watch，GPCF 仅保留当前 watch，不执行非 GPCF sync 或 clean reindex。

### verify

本轮验证口径：

- `codegraph status --json .`
- `git status --short -- .codegraph`
- `python3 tools/kds-sync/validate_codegraph_watchlist_steady_monitor_20260623.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`

### recover

若 Brain/KDS/GFIS/Studio 再次出现新的 pending 增长，回到只读 watchlist recheck；非 GPCF sync 继续要求显式授权。

### debug

当前 KDS mirror / WorkWiki 仍有 Git dirty 18，Studio 仍有 CodeGraph modified residual 2，GPCF 当前仍有 32 项 CodeGraph pending 且本地工作树 dirty 405。

## 非声明

- 不声明任何业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 Brain、GFIS、KDS、Studio 已完成业务修复。
- 不声明 GFIS clean reindex 已执行或已授权。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`
