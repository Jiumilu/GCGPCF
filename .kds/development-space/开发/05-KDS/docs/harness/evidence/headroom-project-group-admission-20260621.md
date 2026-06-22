---
doc_id: GPCF-DOC-E839C7F5A4
title: Headroom Project Group Admission Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-project-group-admission-20260621.md
source_path: docs/harness/evidence/headroom-project-group-admission-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Project Group Admission Evidence

## Evidence ID

`HEADROOM-PROJECT-GROUP-ADMISSION-20260621`

## 结论

Headroom 已进入 GPCF 项目群治理准入与成本模型定义阶段，角色为 `ai_context_compression_infrastructure_candidate`。

本 evidence 证明：项目群接入边界、应用矩阵、Loop 纳入对象和成本评估公式已建立，并具备 L2 本地 dry-run 的准备条件。

本 evidence 不证明：Headroom 已成为生产代理、已接入所有项目运行时、已产生全项目实测节省、已通过 L3.5/L4/L5 授权、已 accepted、已 integrated 或已 production_ready。

## 受控产物

| 产物 | 路径 |
|---|---|
| 接入方案 | `02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md` |
| Evidence JSON | `docs/harness/evidence/headroom-project-group-admission-20260621.json` |
| Loop round | `docs/harness/loops/loop-round-GPCF-HEADROOM-ADMISSION-001.md` |
| Validator | `tools/kds-sync/validate_headroom_project_group_admission.py` |
| Cost calculator | `tools/kds-sync/calculate_headroom_cost_model.py` |
| Measurement template | `fixtures/headroom/headroom-cost-measurement-template.json` |
| L2 project-group dry-run | `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json` |
| Runtime probe | `docs/harness/evidence/headroom-runtime-probe-20260621.json` |
| Runtime adapter dry-run | `docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json` |
| Runtime scenario matrix | `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json` |
| HeadroomCostMeasurement output | `docs/harness/evidence/headroom-cost-measurement-output-20260621.json` |
| Marker preservation policy | `docs/harness/evidence/headroom-marker-preservation-policy-20260621.json` |
| Controlled metric pilot | `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json` |
| Loop cost observation | `docs/harness/evidence/headroom-loop-cost-observation-20260621.json` |
| Loop cost observation series | `docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json` |
| Marker-preserving adapter pilot | `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json` |
| Independent LOOP round replay | `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json` |
| Production token intake gate | `docs/harness/evidence/headroom-production-token-intake-gate-20260621.json` |
| Production token ledger template | `fixtures/headroom/headroom-production-token-ledger-template.json` |
| Production token ledger template validator | `tools/kds-sync/validate_headroom_production_token_ledger_template.py` |
| Production token ledger evaluator | `tools/kds-sync/evaluate_headroom_production_token_ledger.py` |
| Production token ledger negative fixtures | `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json` |
| Production token ledger negative validator | `tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py` |
| Production token authorization package | `docs/harness/evidence/headroom-production-token-authorization-package-20260621.json` |
| Production token authorization action queue | `docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json` |
| Production token authorization package validator | `tools/kds-sync/validate_headroom_production_token_authorization_package.py` |
| Project-group application router | `docs/harness/evidence/headroom-project-group-application-router-20260621.json` |
| Project-group application router validator | `tools/kds-sync/validate_headroom_project_group_application_router.py` |
| Project application coverage matrix | `docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json` |
| Project application coverage matrix validator | `tools/kds-sync/validate_headroom_project_application_coverage_matrix.py` |
| Cost sensitivity model | `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json` |
| Cost sensitivity model validator | `tools/kds-sync/validate_headroom_cost_sensitivity_model.py` |

## 项目群覆盖

| 字段 | 值 |
|---|---|
| projects_covered | GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS |
| admission_level | `L1_governance_defined_L2_dry_run_ready` |
| telemetry_required_default | `off` |
| cross_project_memory | `disabled_first_round` |
| headroom_learn_apply | `disabled` |
| accepted | false |
| integrated | false |
| production_ready | false |

## 成本模型

```text
baseline_cost =
  input_tokens_before * P_in
  + output_tokens_before * P_out
  + cache_write_tokens_before * P_cache_write
  + cache_read_tokens_before * P_cache_read

headroom_cost =
  input_tokens_after * P_in
  + output_tokens_after * P_out
  + cache_write_tokens_after * P_cache_write
  + cache_read_tokens_after * P_cache_read
  + P_runtime

saving_rate = (baseline_cost - headroom_cost) / baseline_cost
```

## 门禁

| 门禁 | 当前状态 |
|---|---|
| Telemetry off required | pass_defined |
| KDS Token not written | pass_defined |
| Authorization headers not logged | pass_defined |
| Cross-project memory disabled first round | pass_defined |
| Sensitive originals metadata-only | pass_defined |
| Local cost calculator smoke | pass_defined |
| Project-group L2 sample measurement | pass_structured_surrogate |
| Real Headroom runtime probe | completed_noop_blocked |
| Runtime adapter dry-run | measured_below_l2_threshold |
| Runtime scenario matrix | partial_one_scenario_passed |
| HeadroomCostMeasurement output | pass_structured_metric_tool_output_only |
| Marker preservation policy | pass_adapter_only_policy |
| Controlled metric pilot | pass_metric_and_adapter_applied_rejected_blocked |
| Loop cost observation | pass_metric_output_cost_observation_only |
| Loop cost observation series | done_normalized_three_window_stability_gate_pass |
| Marker-preserving adapter pilot | pass_log_search_marker_preserved |
| Independent LOOP round replay | pass_production_token_free |
| Production token intake gate | blocked_until_authorized_sanitized_usage_ledger |
| Production token ledger template | pass_template_admission_gate_false |
| Production token ledger negative fixtures | pass_risk_ledgers_rejected |
| Production token authorization package | pending_authorization_gate_false |
| Project-group application router | pass_dry_run_routes_only |
| Project application coverage matrix | pass_15_projects_dry_run_routes_only |
| Cost sensitivity model | pass_three_price_profiles |
| Real Headroom runtime answer equivalence gate | defined_not_measured |
| Project group production token measurements | not_done |

## 非声明

- 不生产写入。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不部署。
- 不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。
