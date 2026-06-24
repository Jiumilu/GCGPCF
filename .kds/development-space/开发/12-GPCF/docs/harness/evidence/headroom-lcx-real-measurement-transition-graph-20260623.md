---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623
title: Headroom LCX Real Measurement Transition Graph Evidence
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement Transition Graph Evidence

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-TRANSITION-GRAPH-20260623`

## 结论

当前图谱已经稳定地停留在受控态，真实测量转移图已明确所有需要跨越的条件，但 production branch 仍然 blocked。
status: transition_graph_defined_blocked_real_measurement

## 授权窗口

- real_measurement_authorization_window_status: `granted_precheck_only`
- real_measurement_authorization_window_granted_precheck_only: `true`
- real_measurement_window_granted: `true`
- real_measurement_window_grant_evidence: `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623`
- real_measurement_signed_approval_bundle: `recorded_precheck_only`
- authorization_boundary_review: `recorded_precheck_only`

## 节点

| node_id | status | evidence |
|---|---|---|
| current_controlled_graph | controlled | `HEADROOM-LCX-GRAPH-MANIFEST-20260623` |
| real_measurement_gap_matrix | blocked | `HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623` |
| real_measurement_authorization_request_package | precheck_only | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623` |
| real_measurement_authorization_window_request_package | requested_not_granted | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623` |
| rollback_runbook | controlled_no_production | `HEADROOM-LCX-ROLLBACK-PLAN-20260622-001` |
| sanitized_precheck | admitted_for_sanitized_measurement_precheck | `HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621` |
| real_measurement_authorization_window | granted_precheck_only | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623` |
| real_measurement_signed_approval_bundle | recorded_precheck_only | `HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623` |
| authorization_boundary_review | recorded_precheck_only | `HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623` |
| waes_harness_decision | precheck_only | `admitted_for_sanitized_measurement_precheck` |
| sanitized_token_ledger | present | `fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json` |
| production_proxy_enablement | blocked | `production_proxy_and_sdk_flags_remain_false` |
| real_business_equivalence_measurement | synthetic_only | `HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622` |
| production_branch | blocked | `HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621` |

## 边

| from | to | relation | allowed |
|---|---|---|---|
| current_controlled_graph | real_measurement_gap_matrix | current_graph_exposes_real_measurement_gaps | `true` |
| real_measurement_gap_matrix | real_measurement_authorization_request_package | gap_matrix_creates_precheck_only_request_package | `true` |
| real_measurement_authorization_request_package | real_measurement_authorization_window_request_package | request_package_records_window_request_only | `true` |
| real_measurement_authorization_window_request_package | sanitized_precheck | window_request_remains_sanitized_only | `true` |
| sanitized_precheck | real_measurement_authorization_window | requires_authorized_window | `true` |
| real_measurement_authorization_window | waes_harness_decision | requires_waes_harness_admission | `false` |
| waes_harness_decision | sanitized_token_ledger | may_reference_sanitized_ledger_only | `true` |
| sanitized_token_ledger | production_proxy_enablement | production_proxy_remains_blocked_until_future_authorization | `false` |
| production_proxy_enablement | real_business_equivalence_measurement | real_measurement_requires_non_synthetic_equivalence | `false` |
| real_business_equivalence_measurement | production_branch | production_branch_requires_real_business_equivalence_and_authorized_measurement | `false` |
| rollback_runbook | production_branch | rollback_runbook_guards_not_opens_production | `false` |

## 转移要求

| requirement_id | current_value | future_value | maps_to |
|---|---|---|---|
| requested_window_id | LCX-MEASURE-20260622-001 | requested_only_not_granted | real_measurement_authorization_window_request_package |
| requested_by | lujunxiang / GPCF owner | requested_only_not_granted | real_measurement_authorization_window_request_package |
| requested_at | 2026-06-22T08:42:06+08:00 | requested_only_not_granted | real_measurement_authorization_window_request_package |
| authorized_window_id | None | granted_precheck_only | real_measurement_authorization_window |
| authorized_by | None | granted_precheck_only | real_measurement_authorization_window |
| authorized_at | None | granted_precheck_only | real_measurement_authorization_window |
| sanitized_production_token_ledger | present_sanitized_only | authorized_for_read_only_measurement_metadata | sanitized_token_ledger |
| rollback_plan_id | present | required | rollback_runbook |
| waes_harness_admission_decision | admitted_for_sanitized_measurement_precheck | future_admitted_for_real_measurement_only_if_authorized | waes_harness_decision |
| real_business_equivalence_measurement | synthetic_only | real_business_equivalence_proven | real_business_equivalence_measurement |

## 当前状态

- real_measurement_gap_present: `true`
- production_branch_blocked: `true`
- production_branch_open: `false`
- real_business_equivalence_measurement_allowed: `false`
- production_token_measurement_allowed: `false`
- measured_production_tokens: `false`
- production_admission_gate: `false`
- accepted: `false`
- integrated: `false`
- production_ready: `false`

## 非声明

- 本证据不表示真实测量已执行。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产分支已打开。
- 本证据不表示 accepted、integrated 或 production_ready。
