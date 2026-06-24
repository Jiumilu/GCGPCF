---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622
title: Headroom LCX Fixture Extension Negative Gate Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md
source_path: docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Fixture Extension Negative Gate Evidence

## Summary

- evidence_id: `HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622`
- status: `negative_gate_pass_no_measurement`
- scope: `fixture_extension_negative_boundary_cases`
- negative_fixture: `fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json`
- case_count: `9`
- rejected: `9`
- accepted_count: `0`

## Gates

| Gate | Value |
|---|---|
| negative_fixture_gate | true |
| raw_prompt_rejected | true |
| raw_completion_rejected | true |
| sensitive_material_rejected | true |
| production_measurement_rejected | true |
| kds_api_write_rejected | true |
| production_proxy_rejected | true |
| status_upgrade_rejected | true |
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

## Non-Claims

- Negative fixtures use placeholder-only markers for forbidden raw or sensitive fields.
- No real customer material, provider secret, KDS token, authorization header, production credential, or production token ledger is stored.
- This evidence does not authorize accepted, integrated, production_ready, production proxy, real KDS API write, or external API write.
