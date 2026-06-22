---
doc_id: GPCF-DOC-69EFF16571
title: LOOP Round GPCF Headroom Controlled Metric Pilot 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-CONTROLLED-METRIC-PILOT-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-CONTROLLED-METRIC-PILOT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Controlled Metric Pilot 001

## 输入

- `docs/harness/evidence/headroom-marker-preservation-policy-20260621.json`
- `docs/harness/evidence/headroom-cost-measurement-output-20260621.json`
- `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json`
- `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json`

## 动作

1. 执行 `python3 tools/kds-sync/run_headroom_controlled_metric_pilot.py`。
2. 应用 allowlist 中的 `headroom_cost_measurement_output` 与 `marker_preserving_log_search_adapter_output`。
3. 阻断未经 adapter 的 rejected scenarios。
4. 执行 `python3 tools/kds-sync/validate_headroom_controlled_metric_pilot.py`。

## 输出

- `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json`
- `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.md`
- `tools/kds-sync/run_headroom_controlled_metric_pilot.py`
- `tools/kds-sync/validate_headroom_controlled_metric_pilot.py`

## 检查

| 检查项 | 结果 |
|---|---|
| allowed application applied | true |
| rejected applications blocked | true |
| saving_rate | 0.636619 |
| marker gate | true |
| controlled_metric_pilot_gate | true |
| production_admission_gate | false |

## 反馈

Headroom 现在具备一个可复放的受控应用闭环：结构化指标 tool output 与 marker-preserving adapter output。下一轮应重算连续 LOOP 成本观测，但不得扩大到未经 adapter 的 log/search 或生产代理。
