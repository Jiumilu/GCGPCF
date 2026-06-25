---
doc_id: GPCF-DOC-5D0159ED7D
title: evidence-index
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/evidence-index.md
source_path: docs/harness/evidence/evidence-index.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

GPCF 证据索引

## GPCF-COGNEE-P1-RECALL-001 COGNEE P1 recall 对照试点

- Cognee 评估方案：`02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md`
- Cognee P1 policy: `loop/context/cognee/policy.yaml`
- Cognee MCP 接口：`loop/context/cognee/mcp.json`
- Cognee marker gate：`loop/context/cognee/waes/cognee-marker-gate.yaml`
- Cognee write gate：`loop/context/cognee/waes/cognee-write-gate.yaml`
- Cognee evidence schema：`loop/context/cognee/harness/evidence.schema.yaml`
- P1 召回对照模板：`fixtures/cognee/cognee-p1-recall-comparison-template.json`
- P1 召回对照 runner：`loop/context/cognee/scripts/run-cognee-p1-recall-comparison.py`
- P1 召回对照 validator：`loop/context/cognee/scripts/validate-cognee-p1-recall-output.py`
- Cognee P1 evidence.md：`docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.md`
- Cognee P1 evidence.json：`docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json`
- COGNEE P1 recall pilot evidence 输出：`cognee_p1_recall_output=hold record_count=5 mean_retrieval_precision=0.73619 marker_coverage=1.0 unauthorized_write_block_rate=1.0 pilot_gate_pass=false`

## GPCF-COGNEE-P2-WRITE-PREVIEW-001 COGNEE P2 写入预览受控试点

- Cognee 评估方案：`02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md`
- Cognee P2 policy：`loop/context/cognee/policy.yaml`
- P2 写入预览模板：`loop/context/cognee/harness/p2-write-preview-template.md`
- P2 写入预览 fixture：`fixtures/cognee/cognee-p2-write-preview-template.json`
- P2 写入预览 runner：`loop/context/cognee/scripts/run-cognee-p2-write-preview.py`
- P2 写入预览 validator：`loop/context/cognee/scripts/validate-cognee-p2-write-preview-output.py`
- P2 写入预览 evidence schema：`loop/context/cognee/harness/evidence-p2.schema.yaml`
- Cognee P2 evidence.md：`docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.md`
- Cognee P2 evidence.json：`docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json`
- COGNEE P2 preview pilot evidence 输出：`cognee_p2_write_preview_output=pass record_count=5 requested_write_count=5 pilot_gate_pass=True preview_block_rate=1.0`

## GPCF-COGNEE-P3-WRITE-PREVIEW-ROLLBACK-001 COGNEE P3 写入预览回滚演练

- Cognee 评估方案：`02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md`
- Cognee P3 policy：`loop/context/cognee/policy.yaml`
- P3 回滚演练 template：`fixtures/cognee/cognee-p3-write-preview-rollback-template.json`
- P3 回滚演练 runner：`loop/context/cognee/scripts/run-cognee-p3-write-preview-rollback.py`
- P3 回滚演练 validator：`loop/context/cognee/scripts/validate-cognee-p3-write-preview-rollback.py`
- P3 回滚演练 evidence schema：`loop/context/cognee/harness/evidence-p3.schema.yaml`
- Cognee P3 evidence.md：`docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.md`
- Cognee P3 evidence.json：`docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json`
- COGNEE P3 preview rollback evidence 输出：`cognee_p3_write_preview_rollback_output=pass record_count=4 requested_write_count=4 rollback_block_rate=1.0`

## GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-001 COGNEE P4 真实写入前置预检

- Cognee 评估方案：`02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md`
- Cognee P4 policy：`loop/context/cognee/policy.yaml`
- P4 前置预检 template：`fixtures/cognee/cognee-p4-real-writeback-precheck-template.json`
- P4 前置预检修复 template（20260624）：`fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json`
- P4 前置预检 runner：`loop/context/cognee/scripts/run-cognee-p4-real-writeback-precheck.py`
- P4 前置预检 validator：`loop/context/cognee/scripts/validate-cognee-p4-real-writeback-precheck.py`
- P4 前置预检 evidence schema：`loop/context/cognee/harness/evidence-p4.schema.yaml`
- Cognee P4 evidence.md：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260623.md`
- Cognee P4 evidence.json：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260623.json`
- COGNEE P4 real writeback precheck 输出：`cognee_p4_real_writeback_precheck_output=pass record_count=5 requested_write_count=5 precheck_pass_rate=0.8`
- Cognee P4 复测 evidence.md：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- Cognee P4 复测 evidence.json：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.json`
- COGNEE P4 real writeback precheck 复测输出：`cognee_p4_real_writeback_precheck_output=pass record_count=5 requested_write_count=5 precheck_pass_rate=1.0`

## GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001 Cognee P4 真实写入运行演练 001

- Cognee P4 live writeback runner：`loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py`
- Cognee P4 live writeback validator：`loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py`
- Cognee P4 live writeback evidence schema：`loop/context/cognee/harness/evidence-p4-live.schema.yaml`
- Cognee P4 live writeback evidence.md：`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`
- Cognee P4 live writeback evidence.json：`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json`
- Cognee P4 live 授权签核包（待签）：`docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md`
- COGNEE P4 real writeback live 演练输出：`cognee_p4_real_writeback_live_output=pass record_count=5 requested_write_count=5 execution_count=5 live_execution_ready_rate=1.0`

## GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001 Headroom project-group cost dry-run

- Headroom admission evidence: `docs/harness/evidence/headroom-project-group-admission-20260621.md`
- Headroom L2 dry-run evidence: `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md`
- Headroom L2 dry-run JSON: `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json`
- Headroom L2 generator: `tools/kds-sync/generate_headroom_l2_project_group_dry_run.py`
- Headroom L2 validator: `tools/kds-sync/validate_headroom_l2_project_group_dry_run.py`
- Validator output: `headroom_l2_project_group_dry_run=pass project_count=15 saving_rate=0.989506 all_admission_gates_pass=true compressor_mode=structured_surrogate_no_headroom_runtime headroom_runtime_used=false measured_production_tokens=false`
- Headroom runtime probe evidence: `docs/harness/evidence/headroom-runtime-probe-20260621.md`
- Headroom runtime probe JSON: `docs/harness/evidence/headroom-runtime-probe-20260621.json`
- Headroom runtime probe validator: `tools/kds-sync/validate_headroom_runtime_probe.py`
- Runtime probe output: `headroom_runtime_probe=pass runtime_imported=true version=0.26.0 project_count=15 runtime_saving_rate=0.0 runtime_admission_gate=false measured_production_tokens=false`
- Headroom runtime adapter dry-run evidence: `docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.md`
- Headroom runtime adapter dry-run JSON: `docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json`
- Headroom runtime adapter dry-run validator: `tools/kds-sync/validate_headroom_runtime_adapter_dry_run.py`
- Runtime adapter output: `headroom_runtime_adapter_dry_run=pass runtime_imported=true version=0.26.0 project_count=15 runtime_adapter_saving_rate=0.022083 runtime_adapter_admission_gate=false measured_production_tokens=false`
- Headroom runtime scenario matrix evidence: `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.md`
- Headroom runtime scenario matrix JSON: `docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json`
- Headroom runtime scenario matrix validator: `tools/kds-sync/validate_headroom_runtime_scenario_matrix.py`
- Runtime scenario matrix output: `headroom_runtime_scenario_matrix=pass scenario_count=4 scenario_gate_pass_count=1 saving_rate=0.15017 runtime_matrix_admission_gate=false measured_production_tokens=false`
- HeadroomCostMeasurement output evidence: `docs/harness/evidence/headroom-cost-measurement-output-20260621.md`
- HeadroomCostMeasurement output JSON: `docs/harness/evidence/headroom-cost-measurement-output-20260621.json`
- Marker preservation policy evidence: `docs/harness/evidence/headroom-marker-preservation-policy-20260621.md`
- Marker preservation policy JSON: `docs/harness/evidence/headroom-marker-preservation-policy-20260621.json`
- Controlled metric pilot evidence: `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.md`
- Controlled metric pilot JSON: `docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json`
- Loop cost observation evidence: `docs/harness/evidence/headroom-loop-cost-observation-20260621.md`
- Loop cost observation JSON: `docs/harness/evidence/headroom-loop-cost-observation-20260621.json`
- Loop cost observation series evidence: `docs/harness/evidence/headroom-loop-cost-observation-series-20260621.md`
- Loop cost observation series JSON: `docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json`
- Independent LOOP round replay evidence: `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.md`
- Independent LOOP round replay JSON: `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json`
- Production token intake gate evidence: `docs/harness/evidence/headroom-production-token-intake-gate-20260621.md`
- Production token intake gate JSON: `docs/harness/evidence/headroom-production-token-intake-gate-20260621.json`
- Production token ledger template: `fixtures/headroom/headroom-production-token-ledger-template.json`
- Production token ledger template validator: `tools/kds-sync/validate_headroom_production_token_ledger_template.py`
- Production token ledger evaluator: `tools/kds-sync/evaluate_headroom_production_token_ledger.py`
- Production token ledger negative fixtures: `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json`
- Production token ledger negative validator: `tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py`
- Production token authorization package evidence: `docs/harness/evidence/headroom-production-token-authorization-package-20260621.md`
- Production token authorization package JSON: `docs/harness/evidence/headroom-production-token-authorization-package-20260621.json`
- Production token authorization action queue evidence: `docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md`
- Production token authorization action queue JSON: `docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json`
- Project-group application router evidence: `docs/harness/evidence/headroom-project-group-application-router-20260621.md`
- Project-group application router JSON: `docs/harness/evidence/headroom-project-group-application-router-20260621.json`
- Project application coverage matrix evidence: `docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md`
- Project application coverage matrix JSON: `docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json`
- Cost sensitivity model evidence: `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md`
- Cost sensitivity model JSON: `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json`
- Headroom LCX full implementation plan: `02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md`
- Headroom LCX full implementation Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001.md`
- Headroom LCX controlled package evidence: `docs/harness/evidence/headroom-lcx-controlled-package-20260621.md`
- Headroom LCX controlled package JSON: `docs/harness/evidence/headroom-lcx-controlled-package-20260621.json`
- Headroom LCX controlled package validator: `tools/kds-sync/validate_headroom_lcx_controlled_package.py`
- Headroom LCX controlled package Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-CONTROLLED-PACKAGE-001.md`
- Headroom LCX P0 runtime replay evidence: `docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md`
- Headroom LCX P0 runtime replay JSON: `docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json`
- Headroom LCX P0 runtime replay runner: `tools/kds-sync/run_headroom_lcx_p0_runtime_replay.py`
- Headroom LCX P0 runtime replay validator: `tools/kds-sync/validate_headroom_lcx_p0_runtime_replay.py`
- Headroom LCX P0 runtime replay Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001.md`
- Headroom LCX P1 proxy dry-run smoke evidence: `docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md`
- Headroom LCX P1 proxy dry-run smoke JSON: `docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json`
- Headroom LCX P1 proxy dry-run smoke runner: `tools/kds-sync/run_headroom_lcx_p1_proxy_dry_run_smoke.py`
- Headroom LCX P1 proxy dry-run smoke validator: `tools/kds-sync/validate_headroom_lcx_p1_proxy_dry_run_smoke.py`
- Headroom LCX P1 proxy dry-run smoke Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001.md`
- Headroom LCX P2 MCP/SDK dry-run smoke evidence: `docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md`
- Headroom LCX P2 MCP/SDK dry-run smoke JSON: `docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json`
- Headroom LCX P2 MCP/SDK dry-run smoke runner: `tools/kds-sync/run_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py`
- Headroom LCX P2 MCP/SDK dry-run smoke validator: `tools/kds-sync/validate_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py`
- Headroom LCX P2 MCP/SDK dry-run smoke Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001.md`
- Headroom LCX P3 learn preview working memory gate 证据：`docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md`
- Headroom LCX P3 learn preview working memory gate JSON: `docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json`
- Headroom LCX P3 学习预览工作记忆门禁运行器：`tools/kds-sync/run_headroom_lcx_p3_learn_preview_working_memory_gate.py`
- Headroom LCX P3 学习预览工作记忆门禁校验器：`tools/kds-sync/validate_headroom_lcx_p3_learn_preview_working_memory_gate.py`
- Headroom LCX P3 学习预览工作记忆门禁 Loop round：`docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001.md`
- Headroom LCX P4 output shaper profile gate evidence: `docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.md`
- Headroom LCX P4 output shaper profile gate JSON: `docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.json`
- Headroom LCX P4 output shaper profile gate runner: `tools/kds-sync/run_headroom_lcx_p4_output_shaper_profile_gate.py`
- Headroom LCX P4 output shaper profile gate validator: `tools/kds-sync/validate_headroom_lcx_p4_output_shaper_profile_gate.py`
- Headroom LCX P4 output shaper profile gate Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001.md`
- Headroom LCX P5 production admission package evidence: `docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.md`
- Headroom LCX P5 production admission package JSON: `docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json`
- Headroom LCX P5 production admission package runner: `tools/kds-sync/run_headroom_lcx_p5_production_admission_package.py`
- Headroom LCX P5 production admission package validator: `tools/kds-sync/validate_headroom_lcx_p5_production_admission_package.py`
- Headroom LCX P5 production admission package Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001.md`
- Headroom LCX authorization boundary review evidence: `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.md`
- Headroom LCX authorization boundary review JSON: `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json`
- Headroom LCX authorization boundary review runner: `tools/kds-sync/run_headroom_lcx_authorization_boundary_review.py`
- Headroom LCX authorization boundary review validator: `tools/kds-sync/validate_headroom_lcx_authorization_boundary_review.py`
- Headroom LCX authorization boundary review Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001.md`
- Headroom LCX authorized measurement precheck evidence: `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.md`
- Headroom LCX authorized measurement precheck JSON: `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json`
- Headroom LCX authorized measurement precheck runner: `tools/kds-sync/run_headroom_lcx_authorized_measurement_precheck.py`
- Headroom LCX authorized measurement precheck validator: `tools/kds-sync/validate_headroom_lcx_authorized_measurement_precheck.py`
- Headroom LCX authorized measurement precheck Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-001.md`
- Headroom LCX next-stage real measurement authorization package evidence: `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md`
- Headroom LCX next-stage real measurement authorization package JSON: `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json`
- Headroom LCX next-stage real measurement authorization package runner: `tools/kds-sync/build_headroom_lcx_real_measurement_next_stage_authorization_package.py`
- Headroom LCX next-stage real measurement authorization package validator: `tools/kds-sync/validate_headroom_lcx_real_measurement_next_stage_authorization_package.py`
- Headroom LCX next-stage real measurement authorization package Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001.md`
- Headroom LCX next-stage real measurement authorization package output: `headroom_lcx_real_measurement_next_stage_authorization_package=generated real_measurement_window_requested=true real_measurement_window_granted=true real_measurement_open=false production_branch_blocked=true production_token_measurement_allowed=false measured_production_tokens=false accepted=false integrated=false production_ready=false`
- Headroom LCX authorized measurement authorization template evidence: `docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md`
- Headroom LCX authorized measurement authorization template JSON: `docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.json`
- Headroom LCX authorized measurement authorization template fixture: `fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json`
- Headroom LCX authorized measurement authorization template runner: `tools/kds-sync/build_headroom_lcx_authorized_measurement_authorization_template.py`
- Headroom LCX authorized measurement authorization template validator: `tools/kds-sync/validate_headroom_lcx_authorized_measurement_authorization_template.py`
- Headroom LCX authorized measurement authorization template Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001.md`
- Headroom LCX authorization negative fixtures evidence: `docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md`
- Headroom LCX authorization negative fixtures JSON: `docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.json`
- Headroom LCX authorization negative fixtures fixture: `fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json`
- Headroom LCX authorization negative fixtures runner: `tools/kds-sync/build_headroom_lcx_authorization_negative_fixtures.py`
- Headroom LCX authorization negative fixtures validator: `tools/kds-sync/validate_headroom_lcx_authorization_negative_fixtures.py`
- Headroom LCX authorization negative fixtures Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001.md`
- Headroom LCX authorization schema approval package evidence: `docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md`
- Headroom LCX authorization schema approval package JSON: `docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json`
- Headroom LCX authorization schema fixture: `fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json`
- Headroom LCX human approval package template: `fixtures/headroom/headroom-lcx-human-approval-package-template.json`
- Headroom LCX authorization schema approval package runner: `tools/kds-sync/build_headroom_lcx_authorization_schema_approval_package.py`
- Headroom LCX authorization schema approval package validator: `tools/kds-sync/validate_headroom_lcx_authorization_schema_approval_package.py`
- Headroom LCX authorization schema approval package Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001.md`
- Headroom LCX approval instance precheck evidence: `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md`
- Headroom LCX approval instance precheck JSON: `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json`
- Headroom LCX approval instance pending fixture: `fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json`
- Headroom LCX approval instance negative fixtures: `fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json`
- Headroom LCX approval instance precheck runner: `tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py`
- Headroom LCX approval instance precheck validator: `tools/kds-sync/validate_headroom_lcx_approval_instance_precheck.py`
- Headroom LCX approval instance precheck Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md`
- Headroom LCX session summary declaration boundary evidence: `docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.md`
- Headroom LCX session summary declaration boundary JSON: `docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.json`
- Headroom LCX session summary declaration boundary validator: `tools/kds-sync/validate_headroom_lcx_session_summary_declaration_boundary.py`
- Headroom LCX session summary declaration boundary Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SESSION-SUMMARY-DECLARATION-BOUNDARY-001.md`
- Headroom LCX completion audit evidence: `docs/harness/evidence/headroom-lcx-completion-audit-20260623.md`
- Headroom LCX completion audit JSON: `docs/harness/evidence/headroom-lcx-completion-audit-20260623.json`
- Headroom LCX completion audit validator: `tools/kds-sync/validate_headroom_lcx_completion_audit.py`
- Headroom LCX completion audit Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COMPLETION-AUDIT-001.md`
- Headroom LCX objective coverage matrix evidence: `docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.md`
- Headroom LCX objective coverage matrix JSON: `docs/harness/evidence/headroom-lcx-objective-coverage-matrix-20260623.json`
- Headroom LCX objective coverage matrix validator: `tools/kds-sync/validate_headroom_lcx_objective_coverage_matrix.py`
- Headroom LCX objective coverage matrix Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-OBJECTIVE-COVERAGE-MATRIX-001.md`
- Headroom LCX measurement admission request evidence: `docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md`
- Headroom LCX measurement admission request JSON: `docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json`
- Headroom LCX measurement admission request runner: `tools/kds-sync/run_headroom_lcx_measurement_admission_request.py`
- Headroom LCX measurement admission request validator: `tools/kds-sync/validate_headroom_lcx_measurement_admission_request.py`
- Headroom LCX measurement admission request Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001.md`
- Headroom LCX WAES/Harness admission decision checklist evidence: `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md`
- Headroom LCX WAES/Harness admission decision checklist JSON: `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json`
- Headroom LCX WAES/Harness admission decision fixtures: `fixtures/headroom/headroom-lcx-waes-harness-admission-decision-fixtures-20260622.json`
- Headroom LCX WAES/Harness admission decision checklist runner: `tools/kds-sync/build_headroom_lcx_waes_harness_admission_decision_checklist.py`
- Headroom LCX WAES/Harness admission decision checklist validator: `tools/kds-sync/validate_headroom_lcx_waes_harness_admission_decision_checklist.py`
- Headroom LCX WAES/Harness admission decision checklist Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001.md`
- Headroom LCX WAES/Harness admitted decision evidence: `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.md`
- Headroom LCX WAES/Harness admitted decision JSON: `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.json`
- Headroom LCX sanitized measurement dry-run evidence: `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md`
- Headroom LCX sanitized measurement dry-run JSON: `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json`
- Headroom LCX sanitized measurement dry-run runner: `tools/kds-sync/run_headroom_lcx_sanitized_measurement_dry_run.py`
- Headroom LCX sanitized measurement dry-run validator: `tools/kds-sync/validate_headroom_lcx_sanitized_measurement_dry_run.py`
- Headroom LCX sanitized measurement dry-run Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md`
- Headroom LCX metadata replay check evidence: `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md`
- Headroom LCX metadata replay check JSON: `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`
- Headroom LCX metadata replay check runner: `tools/kds-sync/run_headroom_lcx_metadata_replay_check.py`
- Headroom LCX metadata replay check validator: `tools/kds-sync/validate_headroom_lcx_metadata_replay_check.py`
- Headroom LCX metadata replay check Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md`
- Headroom LCX marker/retrieval miss comparison gate evidence: `docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md`
- Headroom LCX marker/retrieval miss comparison gate JSON: `docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.json`
- Headroom LCX marker/retrieval miss comparison gate runner: `tools/kds-sync/run_headroom_lcx_marker_retrieval_miss_comparison_gate.py`
- Headroom LCX marker/retrieval miss comparison gate validator: `tools/kds-sync/validate_headroom_lcx_marker_retrieval_miss_comparison_gate.py`
- Headroom LCX marker/retrieval miss comparison gate Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-001.md`
- Headroom LCX sanitized token fixture extension fixture: `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- Headroom LCX sanitized token fixture extension evidence: `docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.md`
- Headroom LCX sanitized token fixture extension JSON: `docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- Headroom LCX sanitized token fixture extension runner: `tools/kds-sync/build_headroom_lcx_sanitized_token_fixture_extension.py`
- Headroom LCX sanitized token fixture extension validator: `tools/kds-sync/validate_headroom_lcx_sanitized_token_fixture_extension.py`
- Headroom LCX sanitized token fixture extension Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-001.md`
- Headroom LCX fixture extension replay comparison evidence: `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md`
- Headroom LCX fixture extension replay comparison JSON: `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json`
- Headroom LCX fixture extension replay comparison runner: `tools/kds-sync/run_headroom_lcx_fixture_extension_replay_comparison.py`
- Headroom LCX fixture extension replay comparison validator: `tools/kds-sync/validate_headroom_lcx_fixture_extension_replay_comparison.py`
- Headroom LCX fixture extension replay comparison Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001.md`
- Headroom LCX fixture extension negative fixtures: `fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json`
- Headroom LCX fixture extension negative gate evidence: `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md`
- Headroom LCX fixture extension negative gate JSON: `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json`
- Headroom LCX fixture extension negative gate runner: `tools/kds-sync/build_headroom_lcx_fixture_extension_negative_gate.py`
- Headroom LCX fixture extension negative gate validator: `tools/kds-sync/validate_headroom_lcx_fixture_extension_negative_gate.py`
- Headroom LCX fixture extension negative gate Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001.md`
- Headroom LCX fixture stability gate evidence: `docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md`
- Headroom LCX fixture stability gate JSON: `docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.json`
- Headroom LCX fixture stability gate runner: `tools/kds-sync/run_headroom_lcx_fixture_stability_gate.py`
- Headroom LCX fixture stability gate validator: `tools/kds-sync/validate_headroom_lcx_fixture_stability_gate.py`
- Headroom LCX fixture stability gate Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-STABILITY-GATE-001.md`
- Headroom LCX project group sanitized fixture: `fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- Headroom LCX project group sanitized fixture evidence: `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.md`
- Headroom LCX project group sanitized fixture JSON: `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- Headroom LCX project group sanitized fixture runner: `tools/kds-sync/build_headroom_lcx_project_group_sanitized_fixture.py`
- Headroom LCX project group sanitized fixture validator: `tools/kds-sync/validate_headroom_lcx_project_group_sanitized_fixture.py`
- Headroom LCX project group sanitized fixture Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001.md`
- Headroom LCX project group replay stability evidence: `docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md`
- Headroom LCX project group replay stability JSON: `docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json`
- Headroom LCX project group replay stability runner: `tools/kds-sync/run_headroom_lcx_project_group_replay_stability.py`
- Headroom LCX project group replay stability validator: `tools/kds-sync/validate_headroom_lcx_project_group_replay_stability.py`
- Headroom LCX project group replay stability Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-001.md`
- Marker-preserving adapter pilot evidence: `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.md`
- Marker-preserving adapter pilot JSON: `docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json`
- Cost measurement output: `headroom_cost_measurement_output=pass record_count=15 saving_rate=0.625378 output_gate=true measured_production_tokens=false`
- Marker policy output: `headroom_marker_preservation_policy=pass allowed=3 rejected=3 log_and_search=adapter_only measured_production_tokens=false`
- Controlled pilot output: `headroom_controlled_metric_pilot=pass allowed_applied=2 rejected_blocked=3 saving_rate=0.636619 production_admission_gate=false measured_production_tokens=false`
- Loop cost observation output: `headroom_loop_cost_observation=pass runtime_included=3 runtime_saving_rate=0.274346 production_admission_gate=false measured_production_tokens=false`
- Loop cost observation series output: `headroom_loop_cost_observation_series=pass window_count=3 max_drift=0.0 stability_gate=true production_admission_gate=false measured_production_tokens=false`
- Independent LOOP round replay output: `headroom_independent_loop_round_replay=pass runtime_entry_count=3 runtime_saving_rate=0.274346 saving_rate_drift=0.0 independent_round_gate=true production_admission_gate=false measured_production_tokens=false`
- Production token intake gate output: `headroom_production_token_intake_gate=pass production_token_intake_gate=false measured_production_tokens=false production_admission_gate=false`
- Production token ledger template output: `headroom_production_token_ledger_template=pass entries=1 measured_production_tokens=false admission_gate=false production_admission_gate=false`
- Production token ledger negative fixtures output: `headroom_production_token_ledger_negative_fixtures=pass case_count=5 rejected=5 production_admission_gate=false`
- Production token authorization package output: `headroom_production_token_authorization_package=pass authorization_status=pending authorization_package_gate=false production_admission_gate=false measured_production_tokens=false`
- Production token authorization action queue output: `headroom_production_token_authorization_action_queue=pass action_count=6 authorization_action_queue_gate=false production_admission_gate=false measured_production_tokens=false`
- Project-group application router output: `headroom_project_group_application_router=pass allowed_routes=3 blocked_routes=3 dry_run_application_gate=true production_admission_gate=false measured_production_tokens=false`
- Project application coverage matrix output: `headroom_project_application_coverage_matrix=pass project_count=15 dry_run_routes=3 blocked_routes=3 production_admission_gate=false measured_production_tokens=false`
- Cost sensitivity model output: `headroom_cost_sensitivity_model=pass profile_count=3 min_saving_rate=0.989505 max_saving_rate=0.989506 production_admission_gate=false measured_production_tokens=false`
- Headroom LCX controlled package output: `headroom_lcx_controlled_package=pass project_route_count=15 proxy=true sdk=true mcp=true agent_wrap=true ccr_retrieve_gate=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P0 runtime replay output: `headroom_lcx_p0_runtime_replay=pass project_count=15 runtime_replay_gate=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P1 proxy dry-run smoke output: `headroom_lcx_p1_proxy_dry_run_smoke=pass project_count=15 proxy_dry_run_gate=true production_proxy_refused=true dry_run_livez_pass=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P2 MCP/SDK dry-run smoke output: `headroom_lcx_p2_mcp_sdk_dry_run_smoke=pass project_count=15 p2_mcp_sdk_dry_run_gate=true sdk_smoke_gate=true mcp_cli_gate=true retrieve_gate_configured=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P3 学习预览工作记忆门禁输出：`headroom_lcx_p3_learn_preview_working_memory_gate=pass project_count=15 learn_preview_gate=true apply_guard_gate=true memory_governance_gate=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P4 output shaper profile gate output: `headroom_lcx_p4_output_shaper_profile_gate=pass project_count=15 forbidden_context_pass_count=4 allowed_context_pass_count=5 production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX P5 production admission package output: `headroom_lcx_p5_production_admission_package=pass project_count=15 pending_action_count=6 request_package_generated=true production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX authorization boundary review 输出：`headroom_lcx_authorization_boundary_review=pass project_count=15 authorization_signal_present=true authorization_complete=false missing_required_field_count=6 production_admission_gate=false accepted=false integrated=false production_ready=false`（approval instance 完成前的历史 boundary review）
- Headroom LCX authorized measurement precheck output: `headroom_lcx_authorized_measurement_precheck=pass_precheck_only project_count=15 authorization_signal_present=true authorization_complete=true missing_required_field_count=0 waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX authorized measurement authorization template output: `headroom_lcx_authorized_measurement_authorization_template=pass project_count=15 required_field_count=6 authorization_complete=false production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX authorization negative fixtures output: `headroom_lcx_authorization_negative_fixtures=pass project_count=15 case_count=7 rejected=7 accepted=0 production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX authorization schema approval package output: `headroom_lcx_authorization_schema_approval_package=pass project_count=15 required_field_count=6 human_attestation_count=7 authorization_complete=false production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX approval instance precheck output: `headroom_lcx_approval_instance_precheck=pass_precheck_only project_count=15 negative_case_count=7 rejected=7 approval_instance_precheck_gate=true authorization_complete=true waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX session summary declaration boundary output: `headroom_lcx_session_summary_declaration_boundary=pass project_count=15 declaration_boundary_gate=true authorization_complete=true waes_harness_admitted=true production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX measurement admission request output: `headroom_lcx_measurement_admission_request=pass project_count=15 current_waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck waes_harness_admitted=true production_token_measurement_allowed=false accepted=false integrated=false production_ready=false`
- Headroom LCX WAES/Harness admission decision checklist output: `headroom_lcx_waes_harness_admission_decision_checklist=pass project_count=15 positive_case_count=1 negative_case_count=7 current_waes_harness_admission_decision=blocked waes_harness_admitted=false production_token_measurement_allowed=false accepted=false integrated=false production_ready=false`
- Headroom LCX sanitized measurement dry-run output: `headroom_lcx_sanitized_measurement_dry_run=pass_check_only project_count=15 entry_count=1 check_only=true saving_rate=not_calculated measured_production_tokens=false production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX metadata replay check output: `headroom_lcx_metadata_replay_check=pass_check_only project_count=15 entry_count=1 replay_record_count=1 check_only=true saving_rate=not_calculated measured_production_tokens=false production_token_measurement_allowed=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX marker/retrieval miss comparison gate output: `headroom_lcx_marker_retrieval_miss_comparison_gate=pass_check_only project_count=15 entry_count=1 comparison_count=1 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX sanitized token fixture extension output: `headroom_lcx_sanitized_token_fixture_extension=pass_check_only project_count=5 scenario_count=3 entry_count=15 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX fixture extension replay comparison output: `headroom_lcx_fixture_extension_replay_comparison=pass_check_only project_count=5 scenario_count=3 entry_count=15 replay_record_count=15 comparison_count=15 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX fixture extension negative gate output: `headroom_lcx_fixture_extension_negative_gate=pass_check_only case_count=9 rejected=9 accepted=0 production_admission_gate=false measured_production_tokens=false accepted=false integrated=false production_ready=false`
- Headroom LCX fixture stability gate output: `headroom_lcx_fixture_stability_gate=pass_check_only round_count=3 project_count=5 scenario_count=3 entry_count=15 stable_hash_count=1 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX project group sanitized fixture output: `headroom_lcx_project_group_sanitized_fixture=pass_check_only project_count=15 scenario_count=3 entry_count=45 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX project group replay stability output: `headroom_lcx_project_group_replay_stability=pass_check_only round_count=3 project_count=15 scenario_count=3 entry_count=45 stable_hash_count=1 metadata_only=true saving_rate=not_calculated measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX readiness pilot authorization package evidence: `docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.md`
- Headroom LCX readiness pilot authorization package JSON: `docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json`
- Headroom LCX readiness pilot authorization package builder: `tools/kds-sync/build_headroom_lcx_readiness_pilot_authorization_package.py`
- Headroom LCX readiness pilot authorization package validator: `tools/kds-sync/validate_headroom_lcx_readiness_pilot_authorization_package.py`
- Headroom LCX readiness pilot authorization package Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-001.md`
- Headroom LCX readiness pilot authorization package output: `headroom_lcx_readiness_pilot_authorization_package=pass_check_only recommended_next_authorization=L3.5_controlled_sanitized_pilot project_count=15 evidence_chain_count=23 l4_candidate=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX real measurement authorization request evidence: `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md`
- Headroom LCX real measurement authorization request JSON: `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json`
- Headroom LCX real measurement authorization request builder: `tools/kds-sync/build_headroom_lcx_real_measurement_authorization_request.py`
- Headroom LCX real measurement authorization request validator: `tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_request.py`
- Headroom LCX real measurement authorization request Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md`
- Headroom LCX real measurement authorization request output: `headroom_lcx_real_measurement_authorization_request=pass_check_only project_count=15 requested_future_decision=open_real_measurement_window production_token_measurement_allowed=false accepted=false integrated=false production_ready=false`
- Headroom LCX production runtime graph evidence: `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.md`
- Headroom LCX production runtime graph JSON: `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json`
- Headroom LCX production runtime graph validator: `tools/kds-sync/validate_headroom_lcx_production_runtime_graph.py`
- Headroom LCX production runtime graph Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-001.md`
- Headroom LCX production runtime graph output: `headroom_lcx_production_runtime_graph=pass project_count=15 production_branch_blocked=true production_token_measurement_allowed=false measured_production_tokens=false accepted=false integrated=false production_ready=false`
- Headroom LCX cost bridge evidence: `docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md`
- Headroom LCX cost bridge JSON: `docs/harness/evidence/headroom-lcx-cost-bridge-20260623.json`
- Headroom LCX cost bridge runner: `tools/kds-sync/build_headroom_lcx_cost_bridge.py`
- Headroom LCX cost bridge validator: `tools/kds-sync/validate_headroom_lcx_cost_bridge.py`
- Headroom LCX cost bridge Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md`
- Headroom LCX cost bridge output: `headroom_lcx_cost_bridge=pass project_count=15 bridge_mode=replay_only production_token_measurement_allowed=false measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX L3.5 controlled sanitized pilot window evidence: `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md`
- Headroom LCX L3.5 controlled sanitized pilot window JSON: `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json`
- Headroom LCX L3.5 controlled sanitized pilot window runner: `tools/kds-sync/run_headroom_lcx_l35_controlled_sanitized_pilot_window.py`
- Headroom LCX L3.5 controlled sanitized pilot window validator: `tools/kds-sync/validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py`
- Headroom LCX L3.5 controlled sanitized pilot window Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001.md`
- Headroom LCX L3.5 controlled sanitized pilot window output: `headroom_lcx_l35_controlled_sanitized_pilot_window=pass_check_only authorized_window_id=HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001 project_count=15 pilot_smoke_record_count=45 l4_candidate=false measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX L3.5 multi-window stability evidence: `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md`
- Headroom LCX L3.5 multi-window stability JSON: `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json`
- Headroom LCX L3.5 multi-window stability runner: `tools/kds-sync/run_headroom_lcx_l35_multi_window_stability.py`
- Headroom LCX L3.5 multi-window stability validator: `tools/kds-sync/validate_headroom_lcx_l35_multi_window_stability.py`
- Headroom LCX L3.5 multi-window stability Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001.md`
- Headroom LCX L3.5 multi-window stability output: `headroom_lcx_l35_multi_window_stability=pass_check_only window_count=5 project_count=15 record_count_per_window=45 stable_hash_count=1 substantive_rounds=1 l4_candidate=false measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Headroom LCX L3.5 answer equivalence synthetic gate evidence: `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.md`
- Headroom LCX L3.5 answer equivalence synthetic gate JSON: `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json`
- Headroom LCX L3.5 answer equivalence synthetic gate runner: `tools/kds-sync/run_headroom_lcx_l35_answer_equivalence_synthetic_gate.py`
- Headroom LCX L3.5 answer equivalence synthetic gate validator: `tools/kds-sync/validate_headroom_lcx_l35_answer_equivalence_synthetic_gate.py`
- Headroom LCX L3.5 answer equivalence synthetic gate Loop round: `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-001.md`
- Headroom LCX L3.5 answer equivalence synthetic gate output: `headroom_lcx_l35_answer_equivalence_synthetic_gate=pass_check_only project_count=15 scenario_count=3 sample_count=45 answer_equivalence_gate=true business_answer_equivalence_proven=false l4_candidate=false measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false`
- Marker-preserving adapter pilot output: `headroom_marker_preserving_adapter_pilot=pass scenario_count=2 adapter_gate_pass_count=2 saving_rate=0.640676 production_admission_gate=false measured_production_tokens=false`
- 范围说明：该证据证明的是项目群样本 token/cost measurement、structured surrogate、受控 metric-and-adapter pilot、三窗口 LOOP cost observation、一次无 production token 的独立 LOOP replay、production token intake blocking gate、sanitized ledger 模板与负例、待授权包与动作队列、dry-run 项目群路由、15 项目覆盖矩阵、三档 cost sensitivity model、marker-preserving adapter pilot、P1 本地 proxy dry-run smoke、P2 MCP/SDK dry-run smoke、P3 学习预览/工作记忆门禁 smoke、P4 output shaper profile gate、P5 production admission request package、authorization boundary review、admitted-for-sanitized-precheck 授权预检、authorization template/negative fixtures/schema approval package、precheck-only approval instance、session declaration boundary、WAES/Harness measurement admission request package、WAES/Harness decision checklist、check-only sanitized measurement dry-run skeleton、check-only metadata replay、check-only marker/retrieval miss comparison gate、5 项目域/3 场景 sanitized token fixture extension、15 条扩展 fixture replay/comparison、9 类负向边界拒绝门禁、3 轮稳定性门禁、15 项目域 sanitized fixture、15 项目域 replay/stability、L3.5 受控脱敏试点授权建议包、L3.5 受控脱敏试点窗口、L3.5 多窗口脱敏稳定性和 L3.5 synthetic answer/citation/marker 等价门禁；它不证明 full runtime admission、production token savings、真实业务答案等价、L4/L5、accepted、integrated 或 production_ready。

## GPCF-L4-GFIS-TEST-SCENARIO-SYNC-001 GFIS test data scenario coverage sync

- GFIS test-data scenario coverage validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_scenario_coverage.py`
- GFIS scenario coverage matrix: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/scenario-coverage/gfis-runtime-sop-e2e.test-scenario-coverage.json`
- GFIS mutation guard: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/scenario-coverage/gfis-runtime-sop-e2e.test-mutation-guard.json`
- GFIS scenario evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-scenario-coverage-evidence.json`
- GFIS validator output: `gfis_test_data_scenario_coverage=pass test_data_mutation_guard=pass positive_scenario_count=12 boundary_scenario_count=6 covered_stage_count=12 runtime_object_count=15 waes_evidence_candidate_count=15 kds_backlink_candidate_count=15 mutation_attempt_count=8 rejected_mutation_count=8 accepted_mutation_count=0 test_data_12_stage_replay_harness=pass test_data_runtime_object_contract=pass test_data_lane=pass real_business_lane=repair_required runtime_sop_e2e=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF 自纠偏 validator 当前报告 `test_data_scenario_coverage=pass` 与 `test_data_mutation_guard=pass`，同时继续保持 `project_group_score=78` / `repair_required`；GPCF L4 聚合 validator 仍因缺失 XiaoG 外部 retrieval evidence 而失败，不能按通过计。

## GPCF-L4-GFIS-TEST-REPLAY-SYNC-001 GFIS 测试数据运行层回放 harness 同步

- GFIS test-data runtime replay validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_runtime_replay_harness.py`
- GFIS test-data replay input: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/replay/gfis-runtime-sop-e2e.test-replay-input.json`
- GFIS runtime object contract: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/replay/gfis-runtime-sop-e2e.test-runtime-object-contract.json`
- GFIS test-data replay evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-replay-evidence.json`
- GFIS validator output: `gfis_test_data_runtime_replay_harness=pass test_data_12_stage_replay_harness=pass test_data_runtime_object_contract=pass replay_stage_count=12 runtime_object_count=15 replay_transition_count=11 negative_attempt_count=10 rejected_attempt_count=10 accepted_attempt_count=0 test_data_lane=pass real_business_lane=repair_required runtime_sop_e2e=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_data_12_stage_replay_harness=pass` and `test_data_runtime_object_contract=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-TEST-12STAGE-NEGATIVE-SYNC-001 GFIS 测试数据 12 阶段负向流转门禁同步

- GFIS test-data 12-stage negative transition validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_12_stage_negative_transition_guard.py`
- GFIS test-data 12-stage negative transition matrix: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/12-stage/gfis-runtime-sop-e2e.test-12-stage-negative-transition-matrix.json`
- GFIS test-data 12-stage negative evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-12-stage-negative-transition-guard.json`
- GFIS validator output: `gfis_test_data_12_stage_negative_transition_guard=pass negative_attempt_count=10 rejected_attempt_count=10 accepted_attempt_count=0 test_data_12_stage_transition_gate=pass test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_data_12_stage_negative_transition_guard=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-TEST-12STAGE-TRANSITION-SYNC-001 GFIS 测试数据 12 阶段流转门禁同步

- GFIS test-data 12-stage transition validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_12_stage_transition_gate.py`
- GFIS test-data 12-stage transition matrix: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/12-stage/gfis-runtime-sop-e2e.test-12-stage-transition-matrix.json`
- GFIS test-data 12-stage transition evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-12-stage-transition-gate.json`
- GFIS validator output: `gfis_test_data_12_stage_transition_gate=pass test_stage_count=12 transition_count=11 boundary_count=12 manual_gate_count=2 test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_data_12_stage_transition_gate=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-TEST-12STAGE-SYNC-001 GFIS 测试数据 12 阶段 SOP E2E 同步

- GFIS test-data 12-stage SOP E2E validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_12_stage_sop_e2e.py`
- GFIS test-data 12-stage fixture: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/12-stage/gfis-runtime-sop-e2e.test-12-stage.json`
- GFIS test-data 12-stage evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-12-stage.json`
- GFIS validator output: `gfis_test_data_12_stage_sop_e2e=pass test_stage_count=12 test_runtime_primary_keys=12 test_review_queue_items=12 test_runtime_intake_items=12 test_waes_evidence_candidates=12 test_verified_artifacts=12 test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_data_12_stage_sop_e2e=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-TEST-MCL-SYNC-001 GFIS test data minimum SOP E2E sync

- GFIS test-data minimum SOP E2E validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_test_data_minimum_sop_e2e.py`
- GFIS test-data minimum closed-loop fixture: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/customer-requirement-platform-order/minimum-closed-loop/customer-requirement-platform-order.test-minimum-closed-loop.json`
- GFIS test-data minimum evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-test-data-minimum-sop-e2e.json`
- GFIS validator output: `gfis_test_data_minimum_sop_e2e=pass test_source_records=1 test_runtime_primary_keys=1 test_review_queue_items=1 test_runtime_intake_items=1 test_waes_evidence_candidates=1 test_verified_artifacts=1 test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_data_minimum_sop_e2e=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-TEST-SR-SYNC-001 GFIS test source-record submission gate sync

- GFIS test source-record validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_customer_requirement_test_source_record_submission.py`
- GFIS test data directory: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/customer-requirement-platform-order/`
- GFIS test gate evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-test-source-record-submission-gate.json`
- GFIS validator output: `gfis_customer_requirement_test_source_record_submission=pass test_source_records=1 test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_source_record_submission_gate=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-DEV-READY-SYNC-001 GFIS development_ready goal audit sync

- GFIS development-ready validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_development_ready_goal.py`
- GFIS development-ready loop round: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-DEV-READY-001.md`
- GFIS validator output: `gfis_development_ready_goal=pass development_ready=pass synthetic_dev_lane=dev_closed synthetic_e2e_pass=1 synthetic_stage_count=12 synthetic_verified_artifacts=12 runtime_subject=GFIS运行层 demo_e2e=pass_demo_only real_business_lane=repair_required business_verification_pending=true real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `development_ready=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-007 GFIS verified artifact admission gate sync

- GFIS REAL-007 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/verified-artifact/README.md`
- GFIS REAL-007 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/verified-artifact/customer-requirement-platform-order-verified-artifact-gate.json`
- GFIS REAL-007 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_verified_artifact_gate.py`
- GFIS real-lane validator now reports `verified_artifact_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `verified_artifact_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-006 GFIS WAES review admission gate sync

- GFIS REAL-006 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/waes-review/README.md`
- GFIS REAL-006 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/waes-review/customer-requirement-platform-order-waes-review-gate.json`
- GFIS REAL-006 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_waes_review_gate.py`
- GFIS real-lane validator now reports `waes_review_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `waes_review_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-005 GFIS runtime intake admission gate sync

- GFIS REAL-005 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-intake/README.md`
- GFIS REAL-005 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-intake/customer-requirement-platform-order-runtime-intake-gate.json`
- GFIS REAL-005 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_intake_gate.py`
- GFIS real-lane validator now reports `runtime_intake_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `runtime_intake_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-003 GFIS runtime primary key gate sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-003 README | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-primary-key/README.md` | `CustomerRequirementOrPlatformOrder` runtime primary key gate 已定义；缺 valid source record 和人工业务核验时不得创建运行层主键 | controlled |
| GFIS REAL-003 gate JSON | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-primary-key/customer-requirement-platform-order-runtime-primary-key-gate.json` | `valid_source_records=0`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0` | repair_required |
| GFIS REAL-003 validator | `python3 scripts/validate_gfis_runtime_primary_key_gate.py` in GFIS | `gfis_runtime_primary_key_gate=pass`；KDS 候选、报价、合同链、用户口述、Demo、mock、fixture、synthetic 均不能打开运行层主键 | pass |
| GFIS REAL-002 validator | `python3 scripts/validate_gfis_pending_business_verification.py` in GFIS | `gfis_pending_business_verification=pass`；pending 机制可机检，但真实提交仍为 0 | pass |
| GFIS REAL-001 validator | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass` 且真实业务计数仍为 0 | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 runtime_primary_key_gate=pass real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-003.md` | 总控同步 GFIS REAL-003，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=completed`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实 source-of-record 进入 pending_business_verification、通过人工业务核验并生成运行层主键后，推进 review queue gate。

## GPCF-L4-GFIS-REAL-SYNC-002 GFIS pending_business_verification sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-002 README | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/README.md` | `CustomerRequirementOrPlatformOrder` pending_business_verification 顶层接收入口已定义；禁止报价单-only、合同审阅稿-only、KDS candidate-only、用户口述-only、Loop 文档-only、GFIS Demo、mock、fixture、synthetic/dev-only 直接进入真实业务链路 | controlled |
| GFIS REAL-002 schema | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/customer-requirement-platform-order.schema.json` | 12 个必填字段、5 类待人工核验等效来源、2 类最终有效来源；强制 manual verification before release | controlled |
| GFIS REAL-002 precheck | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/customer-requirement-platform-order-precheck.json` | `real_business_lane=repair_required`、`business_verification_pending=true`、`valid_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | repair_required |
| GFIS REAL-002 validator | `python3 scripts/validate_gfis_pending_business_verification.py` in GFIS | `gfis_pending_business_verification=pass`；KDS 候选可作为 pending 线索，弱凭证不会进入真实业务链路 | pass |
| GFIS REAL-001 gate | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass` 且真实业务计数仍为 0 | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-002.md` | 总控同步 GFIS REAL-002，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=completed`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实客户订单、平台订单回执、采购订单、客户确认、客户签样或等效正式确认进入 pending_business_verification 并通过人工核验后推进 `REAL-003`。

## GPCF-L4-GFIS-REAL-SYNC-001 GFIS real source-of-record intake gate sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-001 gate doc | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/gfis-real-source-record-intake-gate.md` | `CustomerRequirementOrPlatformOrder` 真实 source-of-record intake gate 已定义；禁止 synthetic/dev-only/mock/demo/fixture/KDS candidate-only/Loop document-only/口述-only 替代真实 source-of-record | controlled |
| GFIS REAL-001 evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-real-source-record-intake-gate.json` | `source_record_files_found=0`、`pending_business_verification_files_found=0`、`valid_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | repair_required |
| GFIS REAL-001 validator | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0 real_business_lane=repair_required business_verification_pending=true stop_type=completed` | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | 先因 Playwright webServer 15 秒启动超时失败；手动按同一配置启动 `python3 -m http.server 4173 --bind 127.0.0.1` 后复跑 `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-001.md` | 总控同步 GFIS REAL-001，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=4`、`batch_generated=false`、`substance_gate=pass`、`stop_type=blocked_missing_real_source_record`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实客户订单、平台订单回执、采购订单、客户确认或等效正式确认进入 `pending_business_verification` 后推进 REAL-002。

## GPCF-L4-GFIS-DEV-SYNC-001 GFIS dual-lane dev sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS DEV-001 synthetic master | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/synthetic-fixtures/synthetic-gehu-sop-e2e-master.json` | 覆盖 12 个 GFIS SOP 阶段；标记 `synthetic=true`、`dev_only=true`、`dry_run=true`、`not_source_of_record=true`、`not_business_verified=true` | pass |
| GFIS DEV-002 dry-run | `python3 scripts/run_gfis_runtime_sop_e2e_dev_dry_run.py` in GFIS | `synthetic_dev_lane=dev_closed`、`synthetic_e2e=synthetic_e2e_pass`、`synthetic_stage_count=12`、`synthetic_verified_artifacts=12`、`real_business_lane=repair_required`、`business_verification_pending=true` | pass |
| GFIS DEV-003 dev validator | `python3 scripts/validate_gfis_runtime_sop_e2e_dev.py` in GFIS | `gfis_runtime_sop_e2e_dev=pass`、`synthetic_dev_lane=dev_closed`、`synthetic_e2e_pass=1`、`business_verification_pending=true`、`runtime_sop_e2e_real=repair_required` | pass |
| GFIS DEV-003 real validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required`、`synthetic_rejected_by_real_lane=1`、`synthetic_pollution_files=0`、`real_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | pass_as_repair_guard |
| GPCF control status | `GPCF-L4-GFIS-DEV-SYNC-001` | `synthetic_dev_lane=dev_closed`、`real_business_lane=repair_required`、`business_verification_pending=true`；不恢复 100/100，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=8`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 真正业务闭环仍等待真实 source-of-record：`real source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact`。

## GPCF-L4-GFIS-REPAIR-278 GFIS CustomerRequirementOrPlatformOrder 责任方提醒派发授权负例门禁同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 268 validator | `python3 scripts/validate_gfis_sop_e2e_268.py` in GFIS | `source_receiving_scan_items=1`、`negative_fixture_count=6`、`rejected_fixture_count=6`、`accepted_fixture_count=0`、`dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`kds_backlinks_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-268.md` | 记录 6 类弱派发授权声明均被拒收，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-278.md` | 总控同步 GFIS 268，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步进入 `GFIS-RUNTIME-SOP-E2E-269`，把缺有效派发授权转换为 post-scan hold/action queue。

## GPCF-L4-GFIS-REPAIR-277 GFIS CustomerRequirementOrPlatformOrder 责任方提醒派发授权接收扫描同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 267 validator | `python3 scripts/validate_gfis_sop_e2e_267.py` in GFIS | `source_dispatch_preflight_items=1`、`dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`invalid_dispatch_authorizations=0`、`missing_dispatch_authorizations=1`、`unexpected_files=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-267.md` | 记录派发授权接收目录为空，无有效授权、收件方确认或通道确认，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-277.md` | 总控同步 GFIS 267，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步进入 `GFIS-RUNTIME-SOP-E2E-268`，在授权接收目录仍为空时建立授权缺口 hold/action queue 或下一步受控补证机制。

## GPCF-L4-GFIS-REPAIR-276 GFIS CustomerRequirementOrPlatformOrder 责任方提醒派发授权预检同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 266 validator | `python3 scripts/validate_gfis_sop_e2e_266.py` in GFIS | `dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-266.md` | 记录派发授权预检已建立，但无人工授权、收件方确认或通道确认，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-276.md` | 总控同步 GFIS 266，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步扫描 owner reminder dispatch authorization 接收目录。

## GPCF-L4-GFIS-REPAIR-275 GFIS CustomerRequirementOrPlatformOrder 有效 source-record 索引责任方提醒升级动作包同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 265 validator | `python3 scripts/validate_gfis_sop_e2e_265.py` in GFIS | `owner_action_items=3`、`owner_reminders_prepared=3`、`owner_reminders_dispatched=0`、`dispatch_authorizations_found=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-265.md` | 记录三类责任方补证动作已准备但未派发，不能重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-275.md` | 总控同步 GFIS 265，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 owner 补证动作派发授权预检。

## GPCF-L4-GFIS-REPAIR-274 GFIS CustomerRequirementOrPlatformOrder 有效 source-record 索引变更监听同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 264 validator | `python3 scripts/validate_gfis_sop_e2e_264.py` in GFIS | `source_record_index_files_found=0`、`new_source_record_index_files=0`、`changed_source_record_index_files=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-264.md` | 记录 valid source-record index 接收目录无新增或变更文件，不能重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-274.md` | 总控同步 GFIS 264，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步继续监听真实 source-record index，并形成 owner 补证提醒/升级动作。

## GPCF-L4-GFIS-REPAIR-273 GFIS CustomerRequirementOrPlatformOrder 运行层主键负例 / 污染门禁同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 263 validator | `python3 scripts/validate_gfis_sop_e2e_263.py` in GFIS | `weak_primary_key_open_attempts=6`、`rejected_primary_key_open_attempts=6`、`accepted_primary_key_open_attempts=0`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-263.md` | 记录 GFIS Demo、KDS candidate-only、报价单、Loop 文档、口述事实、mock/fixture/培训资料均不能打开运行层主键门禁 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-273.md` | 总控同步 GFIS 263，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 valid source-record 接收目录的下一轮监听/变更检测。

## GPCF-L4-GFIS-REPAIR-272 GFIS CustomerRequirementOrPlatformOrder 运行层主键门禁同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 262 validator | `python3 scripts/validate_gfis_sop_e2e_262.py` in GFIS | `valid_source_records=0`、`runtime_primary_key_gate_blocked=1`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-262.md` | 记录缺 valid source record 时 runtime primary key gate 必须阻断 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-272.md` | 总控同步 GFIS 262，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 runtime primary key gate 的负例/污染拒收。

## GPCF-L4-GFIS-REPAIR-271 GFIS CustomerRequirementOrPlatformOrder 有效 source record 索引接收扫描同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 261 validator | `python3 scripts/validate_gfis_sop_e2e_261.py` in GFIS | `source_record_index_files_found=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-261.md` | 记录真实 source-of-record 脱敏索引接收目录为空，不能打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-271.md` | 总控同步 GFIS 261，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步只有在真实 source-record index 出现并通过校验后才允许打开 runtime primary key gate。

## GPCF-L4-GFIS-REPAIR-270 GFIS CustomerRequirementOrPlatformOrder 有效 source record 准入同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 260 validator | `python3 scripts/validate_gfis_sop_e2e_260.py` in GFIS | `pending_business_verification_candidates=1`、`formal_quotation_candidates=1`、`customer_confirmations=0`、`purchase_orders=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS KDS harvester | `python3 scripts/harvest_gfis_kds_gehu_inputs.py` in GFIS | categories `8/8`，missing live business inputs `5`，controlled missing sources `4` | partial |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-260.md` | 记录报价单与 KDS 受控数据只能进入 pending_business_verification，不能升级 valid source record | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-270.md` | 总控同步 GFIS 260，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=4`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步必须接收真实客户确认、平台订单回执、采购订单或等效正式确认原件的脱敏索引。

## GPCF-L4-GFIS-REPAIR-269 GFIS CustomerRequirementOrPlatformOrder KDS candidate mapping sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 259 validator | `python3 scripts/validate_gfis_sop_e2e_259.py` in GFIS | `kds_candidate_sources=1`、`quotation_sources=1`、`customer_confirmations=0`、`purchase_orders=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增输出 `runtime_customer_requirement_platform_order_kds_candidate_source_record_mapping_gate=customer_requirement_platform_order_kds_candidate_mapped_customer_source_record_missing:...`；整体仍为 `gfis_runtime_sop_e2e=repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-259.md` | 记录报价单 KDS 候选只能作为 pending_business_verification 种子，不能升级 valid source record | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-269.md` | 总控同步 GFIS 259，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、dispatch confirmation、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；只有至少一个阶段打通 `source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact` 后才能进入闭环判定。

## GPCF-L4-GFIS-REPAIR-268 GFIS 运行层 12 阶段输入缺口收敛队列同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 12-stage queue validator | `python3 scripts/validate_gfis_sop_e2e_258.py` in GFIS | `runtime_sop_stages=12`、`kds_controlled_stages=12`、`blocked_stages=12`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增输出 `runtime_12_stage_input_gap_convergence_queue=runtime_12_stage_input_gap_convergence_queue_open_missing_real_inputs:...`；整体仍为 `gfis_runtime_sop_e2e=repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-258.md` | 记录 12 阶段均 blocked，review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-268.md` | 总控同步 GFIS 258，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、客户签样、转量产批准、生产订单、质检、库存、发货、POD、WAES review、KDS write receipt、运行层主键或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-259`：从 12 阶段队列中选择一个阶段建立真实输入接收门禁。

## GPCF-L4-GFIS-REPAIR-267 GFIS source owner response release remediation evidence 接收扫描同步

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS remediation evidence intake scanner validator | `python3 scripts/validate_gfis_sop_e2e_257.py` in GFIS | `remediation_evidence_intake_scanner_items=1`、`remediation_evidence_files_found=0`、`valid_remediation_evidence_files=0`、`missing_remediation_evidence_files=1`、`remediation_evidence_intake_blocked=1`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；`gfis_runtime_sop_e2e=repair_required`、`missing_inputs=5 missing_kds_source_paths=2` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-257.md` | 记录真实补证材料接收目录为空，release/review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-267.md` | 总控同步 GFIS 257，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=7`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 remediation evidence、source-of-record、pending submission、人工核验完成、有效 release-ready package、有效 dispatch confirmation、运行层主键、review/runtime/WAES 或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-258`：继续收敛完整 12 阶段 SOP 的 KDS/GFIS 输入差距。

## GPCF-L4-GFIS-REPAIR-266 GFIS remediation action recheck sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS remediation action recheck validator | `python3 scripts/validate_gfis_sop_e2e_256.py` in GFIS | `remediation_action_recheck_items=1`、`remediation_actions_required=8`、`remediation_actions_satisfied=0`、`remediation_actions_unsatisfied=8`、`remediation_recheck_blocked=1`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；GFIS 运行层仍为 `repair_required`，未形成真实业务闭环 | repair_required |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-256.md` | 记录 8 项 remediation action 均未满足，release/dispatch/review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-266.md` | 总控同步 GFIS 256，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=7`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、pending submission、人工核验完成、有效 release-ready package、有效 dispatch confirmation、运行层主键、review/runtime/WAES 或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-257`：建立 source owner response release remediation evidence intake scanner。

## Base Knowledge / ODF Evidence Registry

## GPCF-L4-GFIS-REAL-SYNC-004 GFIS review queue admission gate sync

- GFIS REAL-004 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/review-queue/README.md`
- GFIS REAL-004 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/review-queue/customer-requirement-platform-order-review-queue-admission-gate.json`
- GFIS REAL-004 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_review_queue_admission_gate.py`
- GFIS real-lane validator now reports `review_queue_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF validators: `tools/kds-sync/validate_loop_self_correction_gate.py` and `tools/kds-sync/validate_l4_minimum_closed_loop.py`
- Truth counts: `declared_rounds=1/15`, `substantive_rounds=1/15`, `generated_items=5`, `batch_generated=false`, `substance_gate=pass`, `stop_type=completed`.
- Non-claim：本证据不创建 source record、runtime primary key、review queue、runtime intake、WAES review、KDS/WAES write receipt、verified artifact，也不形成 accepted、integrated、production write、external API write、schema sync、bench migrate、deployment 或 permission change。

本注册表把 `docs/harness/evidence/README.md` 中已列出的证据连接到主 evidence index。
它只用于可发现性登记，不声明 real KDS writeback、RAG admission、settlement、production write、
accepted 或 integrated 状态。

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| Base Knowledge closure score dry-run summary | `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md` | dry-run scoring evidence; uses fixtures and hard-stop checks only | dry_run_evidence_only |
| Base Knowledge writeback candidate ledger | `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md` | candidate ledger for controlled review; not a real writeback receipt | candidate_only |
| Base Knowledge committee review queue | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md` | committee review queue for human-controlled decisions | review_queue_only |
| Base Knowledge committee review schema | `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md` | schema for controlled committee review records | controlled_schema |
| Base Knowledge committee review template | `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md` | template for future committee review entries | controlled_template |
| Base Knowledge human confirmation queue | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md` | human confirmation queue; does not prove confirmation completed | confirmation_queue_only |
| Base Knowledge human confirmation schema | `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md` | schema for human confirmation records | controlled_schema |
| Base Knowledge human confirmation template | `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md` | template for future human confirmation entries | controlled_template |
| KDS MD/OKF/ODF full closure report | `docs/harness/evidence/kds-md-okf-odf-full-closure-report-20260619.md` | governance closure report; not a production KDS API write receipt | controlled_report |
| KDS Phase 10 backlog triage report | `docs/harness/evidence/kds-phase10-backlog-triage-20260619.md` | backlog triage report for continued KDS governance; not accepted/integrated proof | controlled_report |
| KDS Phase 10 self-refresh stabilization workpack | `docs/harness/evidence/kds-phase10-self-refresh-stabilization-workpack-20260619.md` | self-refresh stabilization workpack; not a production write or remote sync receipt | controlled_workpack |
| ODF phase 2 expansion closure report | `docs/harness/evidence/odf-phase2-closure-report-20260617.md` | closure evidence for phase 2 expanded sample governance | controlled_closure |
| ODF phase 2 sample ledger | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` | sample ledger for phase 2 ODF governance | controlled_ledger |
| ODF phase 3 schema gate evidence | `docs/harness/evidence/odf-phase3-schema-gate-20260617.md` | schema gate evidence for ODF governance | controlled_gate |
| ODF phase 4 small-batch closure | `docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` | closure evidence for phase 4 small-batch governance | controlled_closure |
| ODF phase 4 small-batch ledger | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` | small-batch ledger for phase 4 ODF governance | controlled_ledger |
| ODF phase 5 change request closure | `docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` | closure evidence for phase 5 change-request governance | controlled_closure |
| ODF phase 5 change request ledger | `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` | change-request ledger for phase 5 ODF governance | controlled_ledger |
| ODF phase 6 manual confirmation workbench | `docs/harness/evidence/odf-phase6-manual-confirmation-workbench-20260618.md` | manual confirmation workbench evidence; confirmation remains controlled by human review | controlled_workbench |
| ODF phase 6 manual confirmation closure | `docs/harness/evidence/odf-phase6-manual-confirmation-workbench-closure-20260618.md` | closure evidence for phase 6 governance workflow | controlled_closure |
| ODF phase 7 small-batch ledger | `docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.md` | small-batch governance ledger; not business completion evidence | controlled_ledger |
| ODF phase 7 small-batch closure | `docs/harness/evidence/odf-phase7-small-batch-closure-20260619.md` | closure evidence for phase 7 small-batch governance workflow | controlled_closure |
| ODF phase 8 drift monitoring report | `docs/harness/evidence/odf-phase8-drift-monitoring-report-20260619.md` | drift monitoring evidence; does not upgrade runtime business status | controlled_report |
| ODF phase 8 drift monitoring closure | `docs/harness/evidence/odf-phase8-drift-monitoring-closure-20260619.md` | closure evidence for phase 8 drift monitoring workflow | controlled_closure |
| ODF phase 9 dynamic source stabilization report | `docs/harness/evidence/odf-phase9-dynamic-source-stabilization-report-20260619.md` | dynamic source stabilization report; not a remote sync or accepted/integrated proof | controlled_report |
| ODF phase 9 dynamic source stabilization closure | `docs/harness/evidence/odf-phase9-dynamic-source-stabilization-closure-20260619.md` | closure evidence for phase 9 dynamic source stabilization workflow | controlled_closure |

### Non-Claims

- 本注册表不执行也不证明 real KDS API writeback。
- does not perform or prove real KDS API writeback
- 本注册表不把任何条目准入 production RAG、settlement、
  runtime business flow、accepted 或 integrated 状态。
- It does not place any entry into accepted, or integrated status.
- 本注册表不授权 production write、external API write、schema
  sync、bench migrate、deployment、commit 或 push。

## Current Control Gates

| 门禁 | 命令 | 当前结论 |
|---|---|---|
| KDS sync plan | `python3 tools/kds-sync/kds_sync_plan.py --allow-unconfigured-remote` | pass |
| KDS token guard | `python3 tools/kds-sync/validate_kds_token.py` | pass，token 未写入 Git 文档 |
| Loop document gate | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| Loop engineering integrity | `python3 tools/kds-sync/validate_loop_engineering_integrity.py` | pass，GFIS subject remains runtime layer |
| Loop self-correction gate | `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | expected blocked，GFIS runtime repair still required |
| L4 minimum closed loop | `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | repair，GFIS runtime SOP blocks final closure |

## Governance Evidence Registry

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| Loop governance dashboard evidence | `docs/harness/evidence/loop-governance-dashboard-20260617.md` | 登记 `LOOP-GOV-DASHBOARD-20260617`，维持 `partial_repair` 状态上限、`repair_required` 业务事实和 accepted/integrated 禁止升级边界 | active_governance_dashboard |
| Loop governance current window disposition evidence | `docs/harness/evidence/loop-governance-current-window-disposition-20260619.md` | 登记 `LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619`，记录 `LEDB-001-RD-005` 与 `LEDB-002-RD-004`；区分 shell exceptions 与 targeted annotation candidates，不批量改写历史 | review_required |
| Loop governance current window review evidence | `docs/harness/evidence/loop-governance-current-window-review-20260619.md` | 登记 `LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619`，记录当前 audit window 的 `truth_records=25`、`five_segment_records=0`、duplicate/similarity review 信号，不批量改写历史 | review_required |
| Loop governance phase goal evidence | `docs/harness/evidence/loop-governance-phase-goal-20260617.md` | 登记 `LOOP-GOV-PHASE-20260617`，限定治理进程服务于实施主进程质量提升，维持 `partial_repair` 状态上限且不创建业务事实 | active_governance |
| Loop governance efficiency debt backlog evidence | `docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.md` | 登记 `LOOP-GOV-EFF-DEBT-20260617`，覆盖 `LEDB-001` 至 `LEDB-004` 的受控 review disposition 队列，不升级业务状态 | review_required |
| Loop governance efficiency debt locator evidence | `docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md` | 登记 `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`，用于定位 `LEDB-001` / `LEDB-002` 当前审计窗口债务，不批量改写历史 | review_required |
| Loop governance round review plan evidence | `docs/harness/evidence/loop-governance-round-review-plan-20260617.md` | 登记 `LOOP-GOV-ROUND-REVIEW-PLAN-20260617`，绑定 `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`，保持 `no_bulk_rewrite=true` 与 `business_status_impact=none` | review_required |
| Loop governance truth-field review evidence | `docs/harness/evidence/loop-governance-truth-field-review-20260617.md` | 登记 `LOOP-GOV-TRUTH-FIELD-REVIEW-20260617` 与 `LEDB-001-RD-003`，保留 shell 例外和已注释历史记录的区分 | review_required |
| Loop governance five-segment review evidence | `docs/harness/evidence/loop-governance-five-segment-review-20260617.md` | 登记 `LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617` 与 `LEDB-002-RD-002`，区分 targeted annotation candidate 与 index-level exception | review_required |
| Loop governance sequence checkpoint evidence | `docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.md` | 记录 `LEDB-003-RD-002`：每 25 个 `GPCF-L4-GFIS-REPAIR-*` 轮次做一次长序列 checkpoint，下一次到 sequence length 200 或 hard-window debt 复现时触发 | watch |
| Loop governance sequence checkpoint validator | `python3 tools/kds-sync/validate_loop_governance_sequence_checkpoint.py` | 校验 checkpoint cadence、hard-window 清洁、不批量改写历史和不升级业务状态 | pass |

## LOOP-GOV-DASHBOARD-20260617 Loop governance dashboard

- 仪表盘 evidence 已登记在上方治理证据登记表中。
- It links `LOOP-GOV-PHASE-20260617`, keeps `efficiency_risk=review_required`, and enforces `status_ceiling=partial_repair`.
- 这不证明 GFIS runtime SOP E2E 已通过，也不允许升级到 accepted/integrated 状态。

## LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619 Loop governance current window review

- 当前窗口 review evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-001-RD-004` 和 `LEDB-002-RD-003`，对应当前 live audit-window review 目标。
- 它保持 `no_bulk_rewrite=true`、`business_status_impact=none`，且不证明 GFIS runtime SOP E2E 已通过。

## LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619 Loop governance current window disposition

- 当前窗口 disposition evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-001-RD-005` 和 `LEDB-002-RD-004`，对应受影响记录 `252`、`254` 与 `269` 到 `273`。
- 它区分 index-level shell exceptions 与 targeted annotation candidates，保持 `no_bulk_rewrite=true`，且不证明 GFIS runtime SOP E2E 已通过。

## LOOP-GOV-PHASE-20260617 Loop governance phase goal

- 阶段目标 evidence 已登记在上方治理证据登记表中。
- 它保持 Loop governance 绑定在实施主流程的质量、效率与自我改进支撑范围内。
- 它不创建真实业务事实，也不允许升级到 accepted/integrated 状态。

## LOOP-GOV-EFF-DEBT-20260617 Loop governance efficiency debt backlog

- 效率债务 backlog evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-001`、`LEDB-002`、`LEDB-003` 与 `LEDB-004`；不会批量重写历史记录，也不会改变 GFIS/GPCF 业务状态。

## LOOP-GOV-ROUND-REVIEW-PLAN-20260617 Loop governance round review plan

- 轮次 review plan evidence 已登记在上方治理证据登记表中。
- 它将 review packages 绑定到 `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`，并保持 `no_bulk_rewrite=true`。
- 它保持 `business_status_impact=none`，且不证明 GFIS runtime SOP E2E 已通过。

## LOOP-GOV-TRUTH-FIELD-REVIEW-20260617 Loop governance truth-field review

- truth-field review evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-001-RD-003`；shell records 仍属于 index-level exceptions，除非另行授权独立的历史迁移方案。

## LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617 Loop governance five-segment review

- five-segment review evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-002-RD-002`；targeted annotation candidates 与 index-level exceptions 继续保持分离。

## LOOP-GOV-SEQUENCE-CHECKPOINT-20260619 Loop governance sequence checkpoint

- sequence checkpoint evidence 已登记在上方治理证据登记表中。
- 它记录 `LEDB-003-RD-002`；不会关闭 `LEDB-003`，不会批量重写历史记录，也不会改变 GFIS/GPCF 业务状态。

## CODEGRAPH-TASK-INTAKE-GATE-20260623 CodeGraph 任务 Intake 门禁证据

- 任务 Intake 门禁证据已登记在 `docs/harness/evidence/codegraph-task-intake-gate-20260623.md`。
- 它把 `query`、`target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`fallback_tests`、`fallback_reason` 和 `codegraph_evidence` 固化为任务开工前必填项。
- 它提供正负例回放，确保 `affected_tests=[]` 且无 fallback 时被阻断。
- 它不证明业务功能完成，也不升级 `accepted`、`integrated` 或 `production_ready`。

## CODEGRAPH-WATCHLIST-STEADY-MONITOR-20260623 CodeGraph watchlist steady monitor

- 监控 evidence 已登记在 `docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.md` 与 `docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.json`。
- 它记录 14 仓 live CodeGraph / Git 状态、`.codegraph/` Git 隔离、Brain/GFIS/KDS/Studio/GPCF drift watch 与 GPCF 本仓 self-sync 收口。
- 它明确 `watch_required` 上限，不进入业务开发，不执行 watchlist 仓 sync 或 clean reindex，不声明 accepted/integrated/production_ready。
- 对应 validator 为 `python3 tools/kds-sync/validate_codegraph_watchlist_steady_monitor_20260623.py`。

## CODEGRAPH-NORMALIZATION-CHECKLIST-20260623 CodeGraph 常态化归一清单证据

- 归一清单证据已登记在 `docs/harness/evidence/codegraph-normalization-checklist-20260623.md` 与 `docs/harness/evidence/codegraph-normalization-checklist-20260623.json`。
- 它把任务 Intake、验收证据、效率指标、14 仓稳态监控、`.codegraph/` Git 隔离和授权边界收束为长期受控清单。
- 它连接到现有项目群门禁与稳态监控链，不把 CodeGraph 当参考材料，而是当默认执行门禁。
- 对应 validator 为 `python3 tools/kds-sync/validate_codegraph_normalization_checklist.py`。

## GPCF-HEADROOM-LCX-REAL-MEASUREMENT-WINDOW-REQUEST-20260623 Headroom LCX real measurement window request

- 窗口请求 evidence 已登记在 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md` 与 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`。
- 它记录真实测量授权窗口仍为 `requested_not_granted`，并把窗口请求显式挂到 manifest、gap matrix、transition graph、objective coverage 和 completion audit 的受控引用链上。
- 它只表示 precheck-only 请求被结构化，不表示真实测量已打开，也不改变 `accepted=false`、`integrated=false`、`production_ready=false`。

## GPCF-HEADROOM-LCX-REAL-MEASUREMENT-WINDOW-GRANT-20260623 Headroom LCX real measurement window grant

- 窗口授予 evidence 已登记在 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md` 与 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json`。
- 它记录真实测量窗口已进入 `granted_precheck_only`，但 `real_measurement_open=false`，因此仍不能进入生产测量。
- 它把窗口授予显式挂到 transition graph、gap matrix、remaining blocker inventory 和 next-stage authorization package 的受控引用链上。
- 它只表示授权窗口被预检授予，不表示真实测量已打开，也不改变 `accepted=false`、`integrated=false`、`production_ready=false`。

## GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623 Headroom LCX real measurement authorization signoff template

- 授权签字模板 evidence 已登记在 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.md` 与 `docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.json`。
- 对应 validator 为 `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_signoff_template.py`。
- 它只提供 6 个必须签字字段与签署区占位，不表示授权完成，也不打开 real measurement window。
- 它要求签字后仍保持 `authorization_complete=false`、`real_measurement_window_open=false`、`production_token_measurement_allowed=false`、`accepted=false`、`integrated=false`、`production_ready=false`。

## GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260623 Headroom LCX authorization boundary review 20260623

- 授权边界审查 evidence 已登记在 `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.md` 与 `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json`。
- 对应 validator 为 `python3 tools/kds-sync/validate_headroom_lcx_authorization_boundary_review_20260623.py`。
- 它记录已签字审批 bundle，但仍不表示 production admission 已打开，也不表示 real measurement window 已打开。
- 它要求 `authorization_complete=true`，同时保持 `production_admission_gate=false`、`real_measurement_window_open=false`、`accepted=false`、`integrated=false`、`production_ready=false`。

## GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623 Headroom LCX remaining blocker inventory

- 剩余阻断清单 evidence 已登记在 `docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.md` 与 `docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.json`。
- 它把真实测量仍缺的授权窗口预检开放、WAES/Harness 决策、token ledger、proxy / SDK enablement 和真实业务等价测量固定成可校验清单。
- 它只说明当前仍 blocked，不表示真实测量、accepted、integrated 或 production_ready。

## GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260623 Headroom LCX next-stage real measurement authorization package

- 下一阶段授权桥接包已登记在 `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md` 与 `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json`。
- 它把授权前置完成、真实窗口已预检授予但仍未打开、production branch 仍 blocked 的状态收束到单一桥接入口。
- 它只表示 next-stage bridge boundary 已结构化，不表示真实测量已打开，也不改变 `accepted=false`、`integrated=false`、`production_ready=false`。
