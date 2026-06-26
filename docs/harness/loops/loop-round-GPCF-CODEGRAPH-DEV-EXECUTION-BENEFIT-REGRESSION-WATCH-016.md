---
doc_id: GPCF-DOC-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016
title: Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016

## run

- 输入：`GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-PROOF-015` 已通过。
- 目标：把 CodeGraph 开发态收益变成可回放 regression watch。
- 动作：建立收益阈值，读取 benefit proof，确认 manual scan reduction、scope control、fallback test selection、missed impact、review rework 和状态边界未退化。
- 边界：不进入新的业务代码开发，不提交、不推送、不部署、不生产写入、不外部 API 写入、不真实 KDS/WAES 写入。

## stop

- stop_type：`benefit_regression_watch_active`
- 停止证据：当前样本未出现收益回归，但 GFIS runtime SOP 与真实业务 source input 仍未闭合。
- 状态上限：`partial`

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_benefit_proof.py
python3 tools/kds-sync/validate_codegraph_dev_execution_benefit_regression_watch.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-PROOF-015`
- 可重试动作：刷新 benefit proof sample 并重跑 regression watch。
- 不可重试动作：未授权 commit、push、deploy、production write、external API write、real KDS write、real WAES write。

## debug

- 当前收益阈值：manual scan reduction 必须 >= 80.0%。
- 当前样本：97.5%，无收益回归。
- 当前质量阈值：changed files outside allowed scope、missed impact 和 review rework 必须为 0。
- 当前阻塞：GFIS runtime SOP 与真实业务 source input 仍未闭合。
- 下一轮：`GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017`

## 输出

- `docs/harness/evidence/codegraph-dev-execution-benefit-regression-watch-20260626.json`
- `docs/harness/evidence/codegraph-dev-execution-benefit-regression-watch-20260626.md`
- `tools/kds-sync/validate_codegraph_dev_execution_benefit_regression_watch.py`
