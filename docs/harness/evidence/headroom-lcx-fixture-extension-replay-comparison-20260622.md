---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622
title: Headroom LCX 夹具扩展回放对比证据
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md
source_path: docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 夹具扩展回放对比证据

## 摘要

- evidence_id: `HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622`
- status: `fixture_extension_replay_comparison_pass_no_measurement`
- scope: `sanitized_fixture_metadata_replay_comparison_only`
- fixture: `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- project_count: `5`
- scenario_count: `3`
- entry_count: `15`
- replay_record_count: `15`
- comparison_count: `15`

## 门禁

| Gate | Value |
|---|---|
| fixture_extension_replay_comparison_gate | true |
| metadata_replay_gate | true |
| marker_retrieval_miss_comparison_gate | true |
| metadata_only | true |
| check_only | true |
| raw_text_compared | false |
| production_tokens_compared | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| production_sdk_enabled | false |
| production_external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |
| saving_rate | not_calculated |
| tokens_saved | not_calculated |

## 非声明边界

- 本次回放和对比只使用已脱敏的夹具元数据。
- 本次不读取原始提示词、原始补全、客户合同、POD、财务凭证、密钥、生产凭据或供应商密钥。
- 本次不计算真实生产 token 节省量。
- 本次不将 Headroom 标记为 accepted、integrated 或 production_ready。
