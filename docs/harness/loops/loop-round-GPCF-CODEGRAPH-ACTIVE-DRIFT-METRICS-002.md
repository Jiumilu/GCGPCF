---
doc_id: GPCF-DOC-A1A8006738
title: GPCF CodeGraph Active Drift Metrics 002
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Active Drift Metrics 002

## 输入

- 用户要求建立下一阶段目标并执行。
- 上一轮输出为 `GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002`。
- 上一数据点显示 Brain `modified=39`，Studio `added=2, modified=5`。
- 本轮仍不进入项目内部开发任务。

## 动作

- 读取 Loop 技能、文档治理技能和上一轮 Active Drift Monitor。
- 只读采样 Brain、Studio、GFIS、GPCF 的 `codegraph status --json`。
- 记录第二个 metrics window。
- 判断 Brain/Studio sync-only closure 是否可自动执行。
- 新增 metrics evidence 与 validator。

## 输出

- 新增 `docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_active_drift_metrics.py`。
- Brain 从 `modified=39` 增至 `modified=56`。
- Studio 保持 `added=2, modified=5`。
- GFIS 保持 `added=1` 受控 residual。
- 下一轮输入为 `GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003`。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_active_drift_metrics.py`
- `python3 tools/kds-sync/validate_loop_codegraph_active_drift_monitor.py`
- `python3 tools/kds-sync/validate_loop_codegraph_impact_assessment.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

第二个 metrics 数据点证明 CodeGraph 的作用已经从“发现漂移”进入“量化漂移趋势”：Brain drift 在 119 分钟窗口内继续增长，Studio drift 持续未闭合。

本轮结论不是执行同步，而是建立授权边界：Brain/Studio `codegraph sync` 属于 sync-only closure，需要用户明确授权；未授权前继续 read-only metrics sampling。
