---
doc_id: GPCF-DOC-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622
title: Headroom LCX Project Group Replay Stability Evidence
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md
source_path: docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Project Group Replay Stability Evidence

## Summary

- evidence_id: `HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622`
- status: `project_group_replay_stability_pass_no_measurement`
- fixture: `fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- round_count: `3`
- project_count: `15`
- scenario_count: `3`
- entry_count: `45`
- stable_hash_count: `1`

## Gates

| Gate | Value |
|---|---|
| project_group_replay_stability_gate | true |
| metadata_replay_gate | true |
| marker_retrieval_miss_comparison_gate | true |
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

## Non-Claims

- This gate covers all 15 project domains with sanitized fixture metadata only.
- It does not read raw prompt, raw completion, customer contract, POD, financial voucher, key, production credential, or provider secret.
- It does not calculate real production token saving.
- It does not mark Headroom as accepted, integrated, or production_ready.
