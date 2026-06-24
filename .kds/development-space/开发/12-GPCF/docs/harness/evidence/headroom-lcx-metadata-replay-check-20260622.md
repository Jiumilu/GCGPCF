---
doc_id: GPCF-DOC-1F18B14E93
title: Headroom LCX Metadata Replay Check Evidence 20260622
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md
source_path: docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Metadata Replay Check Evidence 20260622

## Evidence ID

`HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622`

## 结论

本轮只执行 `--check-only` 元数据 replay 校验。已验证脱敏台账字段映射、项目标记、gate marker 和 evidence schema；未计算真实生产 token 节省，未读取原文，未启动 proxy。

## 门禁

| 项 | 当前值 |
|---|---|
| metadata_replay_gate | true |
| field_mapping_gate | true |
| project_marker_gate | true |
| evidence_schema_gate | true |
| check_only | true |
| entry_count | 1 |
| replay_record_count | 1 |
| saving_rate | not_calculated |
| tokens_saved | not_calculated |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一步

下一轮可建立 marker/retrieval miss 对比门禁，但仍不得读取原文、不得计算真实生产节省、不得启动生产代理。
