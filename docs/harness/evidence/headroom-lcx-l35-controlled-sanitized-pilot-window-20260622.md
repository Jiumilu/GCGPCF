---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622
title: Headroom LCX L3.5 受控脱敏试点窗口
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md
source_path: docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX L3.5 受控脱敏试点窗口

## 摘要

- evidence_id: `HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622`
- status: `l3_5_controlled_sanitized_pilot_window_pass_check_only`
- scope: `l3_5_controlled_sanitized_fixture_replay_only`
- authorized_window_id: `HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001`
- project_count: `15`
- pilot_smoke_record_count: `45`

## 授权

| Field | Value |
|---|---|
| authorized_window_id | HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001 |
| authorized_by | user_current_codex_session |
| authorized_at | 2026-06-22T21:48:40+08:00 |
| authorization_signal | 用户回复：批准 |
| authorization_scope | L3.5_controlled_sanitized_pilot_only |
| sanitized_production_token_ledger | fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json |
| rollback_plan_id | HEADROOM-LCX-ROLLBACK-PLAN-20260622-001 |
| waes_harness_admission_decision | admitted_for_l3_5_sanitized_pilot_only |
| authorization_complete_for_l3_5 | true |
| authorization_complete_for_l4_l5_or_production | false |

## 门禁

| Gate | Value |
|---|---|
| l3_5_pilot_window_generated | true |
| authorization_complete_for_l3_5 | true |
| authorization_complete_for_l4_l5_or_production | false |
| readiness_gate | true |
| negative_gate_pass | true |
| replay_stability_gate | true |
| project_coverage_gate | true |
| pilot_smoke_gate | true |
| telemetry_off | true |
| metadata_only | true |
| check_only | true |
| raw_prompt_storage | false |
| raw_completion_storage | false |
| unredacted_sensitive_material_processed | false |
| headroom_learn_apply_executed | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| production_sdk_enabled | false |
| production_external_api_write | false |
| kds_api_write | false |
| database_migration | false |
| permission_change | false |
| l4_candidate | false |
| l5_candidate | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 禁止声明

- 本 L3.5 试点窗口仅限本机脱敏 fixture replay 和 evidence 生成。
- 本窗口不授权 L4、L5、production proxy、production SDK、external API write、KDS API write、database migration、permission change 或 `headroom learn --apply`。
- 本窗口不测量 production tokens，也不证明 production token savings。
- 本窗口不得将 Headroom LCX 标记为 accepted、integrated 或 production_ready。
