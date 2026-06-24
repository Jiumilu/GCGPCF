---
doc_id: GPCF-DOC-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622
title: Headroom LCX Marker Retrieval Miss Comparison Gate Evidence
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md
source_path: docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Marker Retrieval Miss Comparison Gate Evidence

## Summary

- evidence_id: `HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622`
- status: `marker_retrieval_miss_comparison_gate_pass_no_measurement`
- scope: `sanitized_metadata_comparison_only`
- source_replay: `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`
- project_count: `15`
- entry_count: `1`
- comparison_count: `1`

## Allowed Compare Fields

- `marker_gate`
- `sensitive_redaction_gate`
- `ccr_retrieval_miss_count`
- `answer_equivalence`

## Gates

| Gate | Value |
|---|---|
| marker_retrieval_miss_comparison_gate | true |
| metadata_only | true |
| raw_text_compared | false |
| production_tokens_compared | false |
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

## Non-Claims

- This evidence does not compare raw prompt, raw completion, customer contract text, POD, financial voucher, key, production credential, or provider secret.
- This evidence does not calculate real production token saving.
- This evidence does not start Headroom production proxy or enable production SDK.
- This evidence does not mark Headroom as accepted, integrated, or production_ready.
