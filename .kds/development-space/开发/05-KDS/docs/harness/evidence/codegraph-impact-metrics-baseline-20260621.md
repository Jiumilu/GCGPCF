---
doc_id: GPCF-DOC-82A9FD6319
title: CodeGraph Impact Metrics Baseline Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.md
source_path: docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph Impact Metrics Baseline Evidence

本轮执行 `GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006`，建立 CodeGraph 对项目群持续发挥作用的指标基线。范围只包括 CodeGraph 项目群治理、Loop/Harness/WAES/KDS 证据与 validator，不进入项目业务开发。

当前状态：`impact_metrics_baseline_ready`。

## 项目群覆盖基线

| 指标 | 基线 |
|---|---|
| repo_count | 14 |
| indexed_repo_count | 14 |
| git_protected_repo_count | 14 |
| `.codegraph` Git status entries | 0 |
| Studio included | true |
| WAS included | true |
| up_to_date_repo_count_at_sample | 12 |
| controlled_exception_repos | GFIS policy exception / Brain active drift watchlist |

## Impact 命令基线

| 命令 | 结果 | 用途 |
|---|---|---|
| `codegraph query codegraph_impact_report_dry_run --json` | 4 results，top result 是 `validate_codegraph_impact_report_dry_run.py` | 定位目标 validator 和证据常量 |
| `codegraph node tools/kds-sync/validate_codegraph_impact_report_dry_run.py` | 108 lines / 9 symbols / 0 dependents | 判断文件、符号和依赖 |
| `codegraph affected tools/kds-sync/validate_codegraph_impact_report_dry_run.py --json` | 0 affected tests / 0 traversed dependents | 选择受影响测试 |
| `codegraph impact main --depth 2` | 101 affected symbols | 宽泛符号噪声负例，不能作为门禁证据 |

## 文本扫描对照

`rg` 对同一主题返回 13 个 matched files / 28 个 matched lines。该基线证明文本扫描适合发现引用，但不能给出符号、indexed dependents、affected tests 或噪声门禁判断。

## 可持续指标

| 指标 | 判定方法 | 当前基线 |
|---|---|---|
| coverage | 14 仓是否 initialized 且 `.codegraph` 不进 Git | 14/14 indexed，14/14 git-protected |
| query_precision | targeted query 的 top result 是否命中目标 | pass |
| impact_precision | affected tests 与 dependents 是否明确 | 0 tests / 0 dependents |
| noise_control | 宽泛符号是否被识别并拒绝 | `main` = 101 affected symbols，rejected |
| manual_scan_reduction | CodeGraph 结构化结果对照 rg 文本结果 | direct file/symbol/test set vs 13 files / 28 lines |
| gate_replayability | 是否有 validator 可重放 | `validate_codegraph_impact_metrics_baseline.py` |

## 边界

- 不进入业务开发。
- 不提交、不推送、不部署。
- 不写生产、不写外部 API。
- 不升级 accepted / integrated / production_ready。
- Brain drift 与 GFIS policy exception 继续作为受控观察对象，不在本轮修复。

## 下一轮

`GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007`
