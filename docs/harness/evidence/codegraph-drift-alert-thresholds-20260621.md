---
doc_id: GPCF-DOC-43BA653EFB
title: CodeGraph Drift Alert Thresholds Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.md
source_path: docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Drift Alert Thresholds Evidence

本轮执行 `GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008`，建立下一阶段 CodeGraph 漂移告警阈值，并用当前 14 仓状态执行一次阈值判定。

当前状态：`drift_alert_thresholds_ready`。

## 阈值

| 对象 | green | watch | action_required | critical |
|---|---|---|---|---|
| normal_repo | pending_total=0 | 1-5 | >=6 | `.codegraph` 进 Git 或 removed>0 |
| gfis_policy_exception | pending_total=0 | pending_total=0 或 added=1 且 modified=0 且 removed=0 | >=2 或 modified>0 或 removed>0 | `.codegraph` 进 Git |
| brain_or_studio_sync_only | pending_total=0 | 1-5 | >=6 | 未授权 sync、业务开发或 `.codegraph` 进 Git |

## 当前阈值判定

| repo | pending | threshold_result | 处置 |
|---|---|---|---|
| GlobalCloud GFIS | added=0 / modified=0 / removed=0 | watch | 维持 policy exception watch |
| GlobalCloud Brain | added=0 / modified=0 / removed=0 | green | 维持 monitor-only |
| GlobalCloud Studio | added=1 / modified=2 / removed=0 | watch | 继续 watch，不进入 sync-only closure |

14 仓仍全部 initialized，`.codegraph` Git status entries 仍为 0。Studio 达到 action_required 不等于允许自动 sync，本轮不进入业务开发、不提交、不推送、不部署。Brain 当前回到 zero pending，仍仅作 monitor-only 观察。

## Impact Gate 采样

| 命令 | 当前结果 |
|---|---|
| `codegraph query codegraph_impact_regression_watch --json` | 4 results，top result 是 `validate_codegraph_impact_regression_watch.py` |
| `codegraph node tools/kds-sync/validate_codegraph_impact_regression_watch.py` | 155 lines / 11 symbols / 0 dependents |
| `codegraph affected tools/kds-sync/validate_codegraph_impact_regression_watch.py --json` | 0 affected tests / 0 traversed dependents |
| `codegraph impact main --depth 2` | 101 affected symbols，仍不可用于门禁 |
| `rg` 文本扫描 | 13 files / 30 lines |

## 决策

- CodeGraph 项目群状态保持 `review_required`。
- Brain 维持 monitor-only，Studio 达到 `action_required`，但本轮不执行 sync-only closure。
- GFIS 保持 policy exception watch，不作为业务失败。
- `.codegraph` 进 Git 或 removed>0 为 critical，阻断任何状态升级。
- 下一轮进入 `GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`，继续监控 Brain / KDS / GFIS / Studio 的 watch 状态。

## 下一轮

`GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009`
