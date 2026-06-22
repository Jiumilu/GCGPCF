---
doc_id: GPCF-DOC-75314D153A
title: GPCF CodeGraph Impact Regression Watch 007
project: GPCF
related_projects: [GPC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Impact Regression Watch 007

## 输入

- 用户要求：建立下一阶段目标并执行。
- 上一轮输出：`GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007`。
- 基线来源：`docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.json`。

## 动作

- 建立下一阶段 CodeGraph 目标：coverage、impact precision、noise control、active drift watch、Loop input generation。
- 复核 14 仓 CodeGraph initialized 与 `.codegraph` Git 隔离。
- 执行 `codegraph query`、`codegraph node`、`codegraph affected` 和 `codegraph impact main --depth 2`。
- 执行 `rg` 文本扫描对照。
- 生成 regression watch evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-impact-regression-watch-20260621.json`
- `docs/harness/evidence/codegraph-impact-regression-watch-20260621.md`
- `tools/kds-sync/validate_codegraph_impact_regression_watch.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_impact_regression_watch.py`
- `python3 tools/kds-sync/validate_codegraph_impact_metrics_baseline.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

下一阶段目标已建立并执行。CodeGraph coverage 与 impact precision 未退化，宽泛 `main` 仍为 101 affected symbols 的噪声负例；Studio 出现 modified=4，被登记为 `active_drift_regression_watch`，本轮不越权 sync。下一轮进入 `GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008`。
