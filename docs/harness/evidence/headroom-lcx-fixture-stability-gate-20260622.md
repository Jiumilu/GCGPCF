---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622
title: Headroom LCX 脱敏夹具稳定性门禁证据
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md
source_path: docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 脱敏夹具稳定性门禁证据

## 摘要

- evidence_id: `HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622`
- status: `fixture_stability_gate_pass_no_measurement`
- scope: `sanitized_fixture_metadata_stability_only`
- fixture: `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- round_count: `3`
- entry_count: `15`
- stable_hash_count: `1`

## 门禁

| 门禁项 | 当前值 |
|---|---|
| fixture_stability_gate | true |
| multi_round_stability_gate | true |
| project_coverage_gate | true |
| scenario_coverage_gate | true |
| entry_count_gate | true |
| metadata_only | true |
| check_only | true |
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

## 非声明

- 本门禁只比对脱敏后的元数据摘要。
- 本门禁不读取原始提示词、原始完成内容、客户合同、签收凭证、财务凭证、密钥、生产凭证或供应商密钥。
- 本门禁不计算真实生产令牌节省。
- 本门禁不把 Headroom 标记为已验收、已集成或生产就绪。
