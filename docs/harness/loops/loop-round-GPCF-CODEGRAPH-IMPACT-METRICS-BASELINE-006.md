---
doc_id: GPCF-DOC-8055ED77AE
title: GPCF CodeGraph Impact Metrics Baseline 006
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Impact Metrics Baseline 006

## 输入

- 上一轮输出：`GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006`。
- 已有证据：CodeGraph impact report dry-run 已通过。
- 本轮目标：建立可持续衡量 CodeGraph 降本提效和质量收益的指标基线。

## 动作

- 复核 14 仓 CodeGraph 覆盖与 `.codegraph` Git 隔离。
- 对上一轮 validator 执行 `codegraph query`、`codegraph node`、`codegraph affected`。
- 使用 `codegraph impact main --depth 2` 作为宽泛查询噪声负例。
- 使用 `rg` 做文本扫描对照。
- 生成 metrics baseline evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.json`
- `docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.md`
- `tools/kds-sync/validate_codegraph_impact_metrics_baseline.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_impact_metrics_baseline.py`
- `python3 tools/kds-sync/validate_codegraph_impact_report_dry_run.py`
- `python3 tools/kds-sync/validate_codegraph_project_group_full_coverage.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

CodeGraph impact metrics baseline 已建立，当前状态为 `impact_metrics_baseline_ready`。该基线把 CodeGraph 的实际作用拆成 coverage、query_precision、impact_precision、noise_control、manual_scan_reduction、gate_replayability 六类指标。仍不进入业务开发、不提交、不推送、不部署、不升级 accepted/integrated/production_ready。下一轮进入 `GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007`。
