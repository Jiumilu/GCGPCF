---
doc_id: GPCF-DOC-03FE63E1D0
title: Headroom Controlled Metric Pilot Evidence
project: KDS
related_projects: [KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-controlled-metric-pilot-20260621.md
source_path: docs/harness/evidence/headroom-controlled-metric-pilot-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom Controlled Metric Pilot Evidence

## Evidence ID

`HEADROOM-CONTROLLED-METRIC-PILOT-20260621`

## 结论

本轮执行受控 pilot：读取 marker preservation policy，应用 `headroom_cost_measurement_output` 与 `marker_preserving_log_search_adapter_output`，并继续阻断未经 adapter 的 rejected scenario。

`controlled_metric_pilot_gate | true`，`production_admission_gate | false`。该结果证明 Headroom 已在项目群 LOOP 中形成一个最小可复放应用闭环，但仍不是生产接入，不升级 accepted、integrated 或 production_ready。

## pilot 摘要

| 字段 | 当前值 |
|---|---:|
| pilot_scope | structured_metric_and_marker_preserving_adapter_outputs |
| project_count | 15 |
| allowed_application_count | 2 |
| rejected_application_count | 3 |
| tokens_before | 2496 |
| tokens_after | 907 |
| tokens_saved | 1589 |
| saving_rate | 0.636619 |
| all_allowed_applications_applied | true |
| all_rejected_applications_blocked | true |
| all_marker_gates_pass | true |
| controlled_metric_pilot_gate | true |
| production_admission_gate | false |

## 应用与阻断

| scenario_id | policy_decision | applied |
|---|---|---|
| headroom_cost_measurement_output | allow | true |
| marker_preserving_log_search_adapter_output | allow | true |
| project_group_evidence_json | reject | false |
| loop_validation_log | reject | false |
| rg_marker_search_output | reject | false |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不启用跨项目 memory。
- 不保存敏感原文。
- 不升级 accepted、integrated 或 production_ready。
