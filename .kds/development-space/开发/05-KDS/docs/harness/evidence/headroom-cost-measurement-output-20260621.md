---
doc_id: GPCF-DOC-78C4270FD2
title: Headroom Cost Measurement Output Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-cost-measurement-output-20260621.md
source_path: docs/harness/evidence/headroom-cost-measurement-output-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Cost Measurement Output Evidence

## Evidence ID

`HEADROOM-COST-MEASUREMENT-OUTPUT-20260621`

## 结论

本轮将已通过的指标 JSON 场景固化为 `HeadroomCostMeasurement` 输出类。该输出类只用于 `structured_metric_tool_output_only`：每条记录保留 `project`、`source_path`、压缩前后 token、saving rate、marker gate 和 raw-text 安全标记；完整成本明细仍以 L2 evidence JSON 为来源。

真实 `headroom-ai==0.26.0` runtime 对该输出类执行 `smart_crusher`，`output_gate | true`。该结果证明它可作为下一轮受控试点对象，但不升级 accepted、integrated 或 production_ready。

## 测量摘要

| 字段 | 当前值 |
|---|---:|
| record_count | 15 |
| tokens_before | 662 |
| tokens_after | 248 |
| tokens_saved | 414 |
| saving_rate | 0.625378 |
| minimum_saving_rate | 0.2 |
| marker_gate | true |
| output_gate | true |

## 输出类边界

| 字段 | 当前值 |
|---|---|
| schema | HeadroomCostMeasurement |
| allowed_application | structured_metric_tool_output_only |
| full_cost_detail_source | `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json` |
| telemetry | off |
| raw_text_stored | false |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不启用跨项目 memory。
- 不保存敏感原文。
- 不升级 accepted、integrated 或 production_ready。
