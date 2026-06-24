---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622
title: Headroom LCX Fixture Extension Replay Comparison Evidence
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md
source_path: docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Fixture Extension Replay Comparison Evidence

## Summary

- evidence_id: `HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622`
- status: `fixture_extension_replay_comparison_pass_no_measurement`
- scope: `sanitized_fixture_metadata_replay_comparison_only`
- fixture: `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- project_count: `5`
- scenario_count: `3`
- entry_count: `15`
- replay_record_count: `15`
- comparison_count: `15`

## Gates

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

## Non-Claims

- This replay/comparison uses sanitized fixture metadata only.
- It does not read raw prompt, raw completion, customer contract, POD, financial voucher, key, production credential, or provider secret.
- It does not calculate real production token saving.
- It does not mark Headroom as accepted, integrated, or production_ready.
