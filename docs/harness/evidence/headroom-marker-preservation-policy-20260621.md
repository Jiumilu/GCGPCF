---
doc_id: GPCF-DOC-BEAC22ACA5
title: Headroom Marker Preservation Policy Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-marker-preservation-policy-20260621.md
source_path: docs/harness/evidence/headroom-marker-preservation-policy-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Marker Preservation Policy Evidence

## Evidence ID

`HEADROOM-MARKER-PRESERVATION-POLICY-20260621`

## 结论

本轮将真实 runtime 场景矩阵转为应用策略：默认 `reject_unless_saving_and_marker_gates_pass`。marker loss 是硬阻断，低于 saving 阈值也是硬阻断。

`log_and_search_runtime_application | adapter_only`。当前允许结构化指标输出类和 marker-preserving adapter 输出进入下一轮受控试点；未经 adapter 的原始 log/search 类仍不得自动应用 Headroom。

## 策略摘要

| 字段 | 当前值 |
|---|---|
| default | reject_unless_saving_and_marker_gates_pass |
| runtime_application_scope | structured_metric_and_marker_preserving_adapter_outputs |
| marker_loss_is_hard_block | true |
| below_saving_threshold_is_hard_block | true |
| log_and_search_runtime_application | adapter_only |

## allow/reject

| scenario_id | 判定 | 原因 |
|---|---|---|
| headroom_metric_json_array | allow | saving 和 marker gate 均通过 |
| headroom_cost_measurement_output | allow | output gate 通过 |
| marker_preserving_log_search_adapter_output | allow | adapter gate 通过 |
| project_group_evidence_json | reject | rejected_not_smaller、below_saving_threshold |
| loop_validation_log | reject | marker_loss |
| rg_marker_search_output | reject | marker_loss |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不启用跨项目 memory。
- 不保存敏感原文。
- 不升级 accepted、integrated 或 production_ready。
