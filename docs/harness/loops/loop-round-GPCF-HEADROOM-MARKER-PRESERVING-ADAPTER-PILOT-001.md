---
doc_id: GPCF-DOC-8E0C267C51
title: LOOP Round GPCF Headroom Marker Preserving Adapter Pilot 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Marker Preserving Adapter Pilot 001

## 输入

- `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json`
- `fixtures/headroom/headroom-l2-project-group-sources.json`
- `tools/kds-sync/run_headroom_marker_preserving_adapter_pilot.py`

## 动作

1. 执行 `HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_marker_preserving_adapter_pilot.py`。
2. 对 `loop_validation_log` 和 `rg_marker_search_output` 先执行 Headroom runtime compression。
3. 追加项目 marker index，避免压缩后丢失项目 marker。
4. 执行 `python3 tools/kds-sync/validate_headroom_marker_preserving_adapter_pilot.py`。

## 输出

- `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json`
- `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.md`
- `tools/kds-sync/run_headroom_marker_preserving_adapter_pilot.py`
- `tools/kds-sync/validate_headroom_marker_preserving_adapter_pilot.py`

## 检查

| 检查项 | 结果 |
|---|---|
| marker_preserving_adapter_pilot_gate | true |
| scenario_count | 2 |
| adapter_gate_pass_count | 2 |
| saving_rate | 0.640676 |
| marker_gate | true |
| production_admission_gate | false |

## 反馈

Headroom 对 log/search 类输出已有受控 marker-preserving adapter 试点路径。下一轮可以把 adapter 结果接入 controlled metric pilot 和 marker policy，但继续不升级 accepted、integrated 或 production_ready。
