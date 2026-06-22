---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622
title: Headroom LCX fixture 扩展负向门禁证据
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md
source_path: docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX fixture 扩展负向门禁证据

## 摘要

- evidence_id: `HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622`
- status: `negative_gate_pass_no_measurement`
- scope: `fixture_extension_negative_boundary_cases`
- negative_fixture: `fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json`
- case_count: `9`
- rejected: `9`
- accepted_count: `0`

## 门禁

| 门禁项 | 值 |
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

## 非声明

- 负向 fixture 只使用占位标记表示被禁止的原始字段或敏感字段。
- 本证据不保存真实客户材料、供应商密钥、KDS token、授权头、生产凭证或生产 token 台账。
- 本证据不授权 accepted、integrated、production_ready、生产代理、真实 KDS API 写入或外部 API 写入。
