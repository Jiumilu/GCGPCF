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
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph watchlist post-Studio 监控证据

本证据对应 `GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`。

## 结论

本轮只读监控 Studio sync-only precheck 后状态，以及 Brain、GFIS、KDS 未授权 watchlist 状态。本轮不执行任何 watchlist 仓 `codegraph sync`，不执行 clean reindex，不进入业务开发，不提交、不推送、不部署。

结论为 `pass_with_watch`：

- Studio：residual pending 为 added=0、modified=7、removed=0，仍低于授权前 modified=9 上限，保持 residual watch。
- Brain：pending 未变，仍需独立授权。
- GFIS：pending 未变，GFIS clean reindex 仍不授权。
- KDS：dirty total 从授权包基线 1652 增长到 1659，下一轮应优先做 KDS mirror / WorkWiki scope review 授权包。

## 监控表

| repo | CodeGraph pending | Git dirty | 状态 | 决策 |
| --- | --- | ---: | --- | --- |
| Brain | added=4, modified=54, removed=0 | 203 | unchanged_authorization_boundary | authorization_required |
| GFIS | added=1, modified=2, removed=0 | 239 | unchanged_policy_exception_boundary | authorization_required_without_clean_reindex |
| KDS | added=0, modified=1, removed=0 | 1659 | active_mirror_workwiki_drift_growth | authorization_required |
| Studio | added=0, modified=7, removed=0 | 12 | residual_within_authorized_ceiling | sync_only_precheck_completed_with_residual_watch |

## 五方向

### run

只读监控 Studio sync-only 后状态，以及 Brain/GFIS/KDS 未授权 watchlist 状态。

### stop

`stop_type=pass_with_watch`。Studio residual 未超过授权上限，Brain/GFIS/KDS 仍需独立授权，不能自动执行 sync 或 clean reindex。

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

若 Studio residual 超过 modified=9 或出现 added/removed，则回到 Studio 专项授权；若 KDS 继续增长，进入 KDS mirror scope review 授权包。

### debug

KDS dirty 持续增长，是下一轮最明确的治理风险；GFIS clean reindex 仍不授权。

## 非声明

- 不声明任何业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 Brain、GFIS、KDS sync-only closure 完成。
- 不声明 Studio 业务闭合。
- 不声明 GFIS clean reindex 已执行或已授权。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`
