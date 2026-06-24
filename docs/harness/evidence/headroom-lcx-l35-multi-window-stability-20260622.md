---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622
title: Headroom LCX L3.5 多窗口脱敏稳定性证据
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md
source_path: docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX L3.5 多窗口脱敏稳定性证据

## 摘要

- evidence_id: `HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622`
- status: `l3_5_multi_window_stability_pass_check_only`
- scope: `l3_5_multi_window_sanitized_fixture_stability_only`
- window_count: `5`
- total_record_count: `225`
- stable_hash_count: `1`

## 连续运行边界

| Field | Value |
|---|---|
| mode | L3.5 |
| declared_rounds | 5 |
| substantive_rounds | 1 |
| generated_items | 5 |
| batch_generated | true |
| substance_gate | pass_as_single_substantive_round |
| stop_type | authorization_boundary |
| stop_evidence | L3.5 multi-window stability complete; L4/L5/production requires separate authorization. |

## 门禁

| Gate | Value |
|---|---|
| l3_5_multi_window_stability_gate | true |
| source_l35_window_gate | true |
| window_count_gate | true |
| record_count_gate | true |
| project_coverage_gate | true |
| multi_window_hash_stability_gate | true |
| metadata_only | true |
| check_only | true |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| production_sdk_enabled | false |
| production_external_api_write | false |
| kds_api_write | false |
| headroom_learn_apply_executed | false |
| l4_candidate | false |
| l5_candidate | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 禁止声明

- 本证据仅证明 L3.5 脱敏 fixture 多窗口 replay hash 稳定。
- 本证据不计算 token 节省，不测量 production tokens，也不证明生产成本收益。
- 本证据不授权 production proxy、external API write、KDS API write 或 `headroom learn --apply`。
- 本证据不得将 Headroom LCX 标记为 accepted、integrated 或 production_ready。
