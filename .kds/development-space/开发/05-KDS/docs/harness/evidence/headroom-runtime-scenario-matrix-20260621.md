---
doc_id: GPCF-DOC-9BB94B0126
title: Headroom Runtime Scenario Matrix Evidence
project: KDS
related_projects: [GFIS, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.md
source_path: docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom Runtime Scenario Matrix Evidence

## Evidence ID

`HEADROOM-RUNTIME-SCENARIO-MATRIX-20260621`

## 结论

本轮把真实 `headroom-ai==0.26.0` runtime 扩展到 4 类项目群 LOOP 输出场景，形成应用矩阵。结果为 partial：`headroom_metric_json_array` 场景通过 L2 阈值和 marker gate；`loop_validation_log` 与 `rg_marker_search_output` 虽然压缩率较高，但丢失部分项目 marker；`project_group_evidence_json` 未形成有效节省。

因此 `runtime_matrix_admission_gate | false`。当前只能建议后续围绕指标 JSON array 类 tool output 做受控试点；log/search 类必须先解决 marker 保真，不得升级 accepted、integrated 或 production_ready。

## 聚合摘要

| 字段 | 当前值 |
|---|---:|
| scenario_count | 4 |
| scenario_gate_pass_count | 1 |
| tokens_before | 9103 |
| tokens_after | 7736 |
| tokens_saved | 1367 |
| saving_rate | 0.15017 |
| all_marker_gates_pass | false |
| all_scenario_gates_pass | false |
| runtime_matrix_admission_gate | false |

## 场景矩阵

| scenario_id | strategy | tokens_before | tokens_after | saving_rate | marker_gate | scenario_gate |
|---|---|---:|---:|---:|---|---|
| project_group_evidence_json | mixed | 6322 | 6690 | 0.0 | true | false |
| headroom_metric_json_array | smart_crusher | 728 | 356 | 0.510989 | true | true |
| loop_validation_log | search | 774 | 100 | 0.870801 | false | false |
| rg_marker_search_output | mixed | 1279 | 590 | 0.538702 | false | false |

## 应用边界

- 可继续试点：`headroom_metric_json_array`，用于 Headroom 成本、token、门禁类结构化指标输出。
- 暂不试点：`loop_validation_log`，原因是压缩后缺失多个项目 marker。
- 暂不试点：`rg_marker_search_output`，原因是压缩后缺失 `Edge`、`WAS` marker。
- 暂不试点：`project_group_evidence_json`，原因是压缩后 token 不降反升，被 runtime 拒绝为有效节省。

## 安全边界

- `HEADROOM_TELEMETRY=off`。
- 不保存原始敏感文本。
- 不启用跨项目 memory。
- 不写真实 KDS。
- 不执行真实外部 API 写入。
- 不生产代理、不部署、不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。

## 下一步

下一轮应将 `headroom_metric_json_array` 封装为最小可复用的 HeadroomCostMeasurement 输出类，并对 log/search 类增加 marker-preserving adapter 或强制拒绝策略。只有所有拟纳入场景同时满足 saving_rate、marker gate 和安全门禁后，才可申请 L3.5/L4 试点授权。
