---
doc_id: GPCF-DOC-F240247924
title: Headroom Marker Preserving Adapter Pilot Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.md
source_path: docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom Marker Preserving Adapter Pilot Evidence

## Evidence ID

`HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-20260621`

## 结论

本轮针对原先因 marker loss 被阻断的 `loop_validation_log` 与 `rg_marker_search_output` 执行 marker-preserving adapter 试点。adapter 采用 `compressed_payload_plus_project_marker_index`，只追加项目 marker index，不保存原始文本。

`marker_preserving_adapter_pilot_gate | true`，`production_admission_gate | false`。该结果证明 log/search 类输出存在受控 adapter 路径，但仍不代表生产代理、真实外部 API 写入、真实 KDS 写入、accepted、integrated 或 production_ready。

## 试点范围

| 字段 | 当前值 |
|---|---|
| adapter_scope | log_and_search_outputs_only |
| adapter | compressed_payload_plus_project_marker_index |
| headroom_runtime_used | true |
| telemetry | off |
| raw_text_stored | false |

## 结果

| scenario_id | tokens_before | tokens_after | tokens_saved | saving_rate | marker_gate | adapter_gate |
|---|---:|---:|---:|---:|---|---|
| loop_validation_log | 774 | 111 | 663 | 0.856589 | true | true |
| rg_marker_search_output | 1060 | 548 | 512 | 0.483019 | true | true |

## 汇总

| 字段 | 当前值 |
|---|---:|
| scenario_count | 2 |
| adapter_gate_pass_count | 2 |
| tokens_before | 1834 |
| tokens_after | 659 |
| tokens_saved | 1175 |
| saving_rate | 0.640676 |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不启用跨项目 memory。
- 不保存敏感原文。
- 不升级 accepted、integrated 或 production_ready。
