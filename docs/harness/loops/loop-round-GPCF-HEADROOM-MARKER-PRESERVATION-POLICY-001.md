---
doc_id: GPCF-DOC-2F2B13445C
title: LOOP Round GPCF Headroom Marker Preservation Policy 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVATION-POLICY-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVATION-POLICY-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Marker Preservation Policy 001

## 输入

- `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json`
- `docs/harness/evidence/headroom-cost-measurement-output-20260621.json`
- `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json`

## 动作

1. 执行 `python3 tools/kds-sync/build_headroom_marker_preservation_policy.py`。
2. 从场景矩阵生成 allow/reject 策略。
3. 执行 `python3 tools/kds-sync/validate_headroom_marker_preservation_policy.py`。

## 输出

- `docs/harness/evidence/headroom-marker-preservation-policy-20260621.json`
- `docs/harness/evidence/headroom-marker-preservation-policy-20260621.md`
- `tools/kds-sync/build_headroom_marker_preservation_policy.py`
- `tools/kds-sync/validate_headroom_marker_preservation_policy.py`

## 检查

| 检查项 | 结果 |
|---|---|
| marker_loss_is_hard_block | true |
| below_saving_threshold_is_hard_block | true |
| allowed scenarios | headroom_metric_json_array, headroom_cost_measurement_output, marker_preserving_log_search_adapter_output |
| rejected scenarios | project_group_evidence_json, loop_validation_log, rg_marker_search_output |

## 反馈

未经 adapter 的 log/search 类输出继续 blocked；marker-preserving adapter output 可以进入受控试点。下一轮只允许推进受控 metric+adapter 输出，不得生产代理化。
