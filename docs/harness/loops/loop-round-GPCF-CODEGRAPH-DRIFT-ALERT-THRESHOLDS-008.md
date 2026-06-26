---
doc_id: GPCF-DOC-33EED81A10
title: GPCF CodeGraph Drift Alert Thresholds 008
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Drift Alert Thresholds 008

## 输入

- 用户要求：建立下一阶段目标并执行。
- 上一轮输出：`GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008`。
- 基线来源：`docs/harness/evidence/codegraph-impact-regression-watch-20260621.json`。

## 动作

- 建立 CodeGraph drift alert thresholds。
- 复核 14 仓 CodeGraph initialized 与 `.codegraph` Git 隔离。
- 对 GFIS、Brain、Studio 当前 pending 状态执行阈值判定。
- 执行 `codegraph query`、`codegraph node`、`codegraph affected`、`codegraph impact main --depth 2`。
- 执行 `rg` 文本扫描对照。
- 生成 thresholds evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.json`
- `docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.md`
- `tools/kds-sync/validate_codegraph_drift_alert_thresholds.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_drift_alert_thresholds.py`
- `python3 tools/kds-sync/validate_codegraph_impact_regression_watch.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

下一阶段目标已建立并执行。Brain 当前回到 `green` / monitor-only，Studio 维持 `watch`，本轮未执行 sync-only closure；GFIS 保持 policy exception watch。下一轮进入 `GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`。
