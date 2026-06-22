---
doc_id: GPCF-DOC-1EC63249AE
title: CodeGraph 开发执行层 watchlist 漂移分诊证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-dev-execution-watchlist-drift-triage-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-watchlist-drift-triage-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph 开发执行层 watchlist 漂移分诊证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013`。

## 结论

本轮只读分诊 Brain、GFIS、KDS、Studio 的 CodeGraph 活动漂移，不进入任何项目业务开发，不对 watchlist 仓库执行 `codegraph sync`，不执行 clean reindex，不提交、不推送、不部署。

结论为 `triage_complete_authorization_boundary`：

- Brain：大范围活动开发漂移，含 openspec 删除项，需要独立授权。
- GFIS：运行层 SOP E2E 治理漂移，继续保留 GFIS policy exception，clean reindex 未授权。
- KDS：大范围 KDS mirror / WorkWiki 内容漂移，需要 KDS 镜像治理复核。
- Studio：相对可控的 session binding / KDS governance 漂移，可作为后续 sync-only precheck 候选，但本轮不发布、不部署。

## 分诊表

| repo | CodeGraph pending | Git dirty | 分类 | 决策 |
| --- | --- | ---: | --- | --- |
| Brain | added=4, modified=54, removed=0 | 203 | broad_active_development_drift_with_deleted_openspec_archive | authorization_required |
| GFIS | added=1, modified=2, removed=0 | 239 | broad_runtime_sop_e2e_governance_drift_with_policy_exception | authorization_required |
| KDS | added=0, modified=1, removed=0 | 1651 | broad_kds_mirror_workwiki_content_drift | authorization_required |
| Studio | added=2, modified=9, removed=0 | 12 | bounded_studio_session_binding_and_kds_governance_drift | precheck_candidate |

## 五方向

### run

只读采集 Brain/GFIS/KDS/Studio 的 `codegraph status --json .` 与 `git status --short`，生成漂移分类。

### stop

`stop_type=authorization_boundary`。watchlist 仓库存在大范围 dirty 或需专项授权，不能在本轮自动 sync-only closure。

### verify

回放：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py
python3 tools/kds-sync/validate_codegraph_dev_execution_steady_state_monitor.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

### recover

恢复点为 `GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012`。若后续授权不足，继续保持 `monitor_only`，不得自动处理 watchlist 仓。

### debug

当前阻塞在 Brain/GFIS/KDS/Studio 漂移授权边界。下一轮只能生成授权包，或将 Studio 作为低风险 sync-only precheck 候选；不得把分诊结果声明为业务完成。

## 非声明

- 不声明业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 watchlist sync-only closure 完成。
- 不声明 GFIS clean reindex 已执行。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014`
