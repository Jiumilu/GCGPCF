---
doc_id: GPCF-DOC-951520EA69
title: LOOP Round GPCF Headroom Cost Measurement Output 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-COST-MEASUREMENT-OUTPUT-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-COST-MEASUREMENT-OUTPUT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Cost Measurement Output 001

## 输入

- `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json`
- `headroom-ai==0.26.0`
- `HEADROOM_TELEMETRY=off`

## 动作

1. 执行 `HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/build_headroom_cost_measurement_output.py`。
2. 生成 `HeadroomCostMeasurement` 结构化指标数组。
3. 调用真实 Headroom runtime 压缩。
4. 执行 `python3 tools/kds-sync/validate_headroom_cost_measurement_output.py`。

## 输出

- `docs/harness/evidence/headroom-cost-measurement-output-20260621.json`
- `docs/harness/evidence/headroom-cost-measurement-output-20260621.md`
- `tools/kds-sync/build_headroom_cost_measurement_output.py`
- `tools/kds-sync/validate_headroom_cost_measurement_output.py`

## 检查

| 检查项 | 结果 |
|---|---|
| saving_rate >= 0.2 | pass |
| marker_gate | pass |
| output_gate | true |
| raw_text_stored | false |
| telemetry | off |

## 反馈

`HeadroomCostMeasurement` 可作为下一轮受控试点对象，但仍不得升级 accepted、integrated 或 production_ready。
