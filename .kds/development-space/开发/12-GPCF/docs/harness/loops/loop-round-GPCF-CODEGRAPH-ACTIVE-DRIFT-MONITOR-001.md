---
doc_id: GPCF-DOC-8CB660E132
title: GPCF CodeGraph Active Drift Monitor
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Active Drift Monitor

## 输入

- 用户要求建立下一阶段目标并执行。
- 上一轮输入为 `GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`。
- 前序 impact assessment 已证明 CodeGraph 达到 `28 / 30`，但 Brain 与 Studio 仍为 active watchlist。
- 本轮边界是不进入任何项目内部开发任务。

## 动作

- 读取 Loop 控制板、自治策略、AGENTS.md 和上一轮 CodeGraph impact assessment。
- 执行 Loop 编排器、Git 门禁和运行门禁。
- 只读采样 Brain、Studio、GFIS、GPCF 的 `codegraph status --json`。
- 固化 Active Drift Monitor evidence。
- 新增可回放 validator。

## 输出

- 新增 `docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_active_drift_monitor.py`。
- Brain 当前 drift：`modified=36`。
- Studio 当前 drift：`added=2, modified=2`。
- GFIS residual 继续为 `added=1` policy-controlled。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_active_drift_monitor.py`
- `python3 tools/kds-sync/validate_loop_codegraph_impact_assessment.py`
- `python3 tools/kds-sync/validate_loop_codegraph_project_group_graphized.py`
- `python3 tools/kds-sync/validate_loop_codegraph_project_group_monitor.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

下一阶段目标已从“证明 CodeGraph 有用”推进为“持续量化 CodeGraph 监控价值”。

本轮已经获得第一个 active drift metrics 数据点：Brain drift 增长，Studio drift 持续，GFIS residual 保持受控。由于 Git gate 为 partial、operational gates 为 blocked，本轮不做状态升级、不提交、不推送、不部署。

下一轮进入 `GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002`：继续只读采样 Brain 与 Studio drift，收集第二个 MTTD/MTTR 数据点，并判断是否需要用户授权执行 sync-only closure。
