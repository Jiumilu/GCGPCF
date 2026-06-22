---
doc_id: GPCF-DOC-DCD5E4AA37
title: CodeGraph Impact Regression Watch Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-impact-regression-watch-20260621.md
source_path: docs/harness/evidence/codegraph-impact-regression-watch-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph Impact Regression Watch Evidence

本轮执行 `GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007`，建立并执行下一阶段目标：用 006 的 impact metrics baseline 持续监控 CodeGraph 是否退化、是否继续降低 Loop 扫描成本、是否继续提供结构化影响证据。

当前状态：`impact_regression_watch_active`。

## 下一阶段目标

| 目标 | Definition of Done | 当前结果 |
|---|---|---|
| coverage_regression_watch | 14 仓保持 CodeGraph initialized，`.codegraph` 不进入 Git | pass |
| impact_precision_watch | targeted query / node / affected 继续给出目标、符号、依赖、测试影响 | pass |
| noise_control_watch | 宽泛 impact 查询继续被识别为噪声负例 | pass |
| active_drift_watch | Brain/GFIS/Studio pending 状态被观察和分类，不越权 sync | watch_required |
| loop_input_generation | 从回归信号生成下一轮 Loop 输入 | pass |

## 回归采样

| 指标 | 当前采样 | 判定 |
|---|---|---|
| repo_count | 14 | pass |
| initialized_repo_count | 14 | pass |
| git_protected_repo_count | 14 | pass |
| `.codegraph` Git status entries | 0 | pass |
| up_to_date_repo_count_at_sample | 11 | watch_required |
| GFIS pending | added=1 / modified=0 / removed=0 | policy_exception_watch |
| Brain pending | added=3 / modified=3 / removed=0 | active_drift_watch |
| Studio pending | added=0 / modified=4 / removed=0 | active_drift_regression_watch |

## Impact 指标回归

| 命令 | 当前结果 | 回归 |
|---|---|---|
| `codegraph query codegraph_impact_metrics_baseline --json` | 4 results，top result 是 `validate_codegraph_impact_metrics_baseline.py` | false |
| `codegraph node tools/kds-sync/validate_codegraph_impact_metrics_baseline.py` | 144 lines / 10 symbols / 0 dependents | false |
| `codegraph affected tools/kds-sync/validate_codegraph_impact_metrics_baseline.py --json` | 0 affected tests / 0 traversed dependents | false |
| `codegraph impact main --depth 2` | 101 affected symbols，仍不可用于门禁 | false |
| `rg` 文本扫描 | 13 files / 31 lines | false |

## 决策

- CodeGraph 项目群状态保持 `review_required`。
- 不自动升级 accepted / integrated / production_ready。
- 不进入业务开发，不提交、不推送、不部署。
- 本轮不对 Brain 或 Studio 执行 sync-only closure；Studio modified=4 登记为 active drift regression watch。
- 下一轮建立 drift alert thresholds 与 owner/action 阈值。

## 下一轮

`GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008`
