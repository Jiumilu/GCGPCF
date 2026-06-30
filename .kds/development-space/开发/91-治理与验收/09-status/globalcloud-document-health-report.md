---
doc_id: GPCF-DOC-C436DDB0F6
title: GlobalCloud 文档健康报告
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-document-health-report.md
source_path: 09-status/globalcloud-document-health-report.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 文档健康报告

本报告用于记录项目群文档门禁、镜像覆盖、状态分布和命令证据的当前健康状态。文中的英文项目名、脚本名、字段名和命令输出均为机器可回放证据，不代表业务事实完成、状态升级、客户验收、生产发布或真实外部写入。当前报告只作为受控治理快照，所有 accepted、integrated、production_ready、customer_accepted 等状态仍必须等待人工确认、真实 source-of-record 或等效正式确认文件、人工业务核验、运行层主键、review queue、runtime intake、WAES review 和 verified artifact 全部满足后才能重新评估。

生成时间：2026-06-28T22:23:34.391958+00:00

Loop 文档门禁：`rework_required`

## 总览

- 仓库 Markdown：3096
- KDS 镜像 Markdown：3110
- KDS 本地镜像流水：3096
- KDS 本地镜像唯一文档：3096
- KDS API 同步流水：141
- 元数据缺失：0
- README 缺失目录：0
- 中文本地化债务：False
- 固定 doc_id 漂移：False
- 门禁原因：hard_failure:project_group_live_status_snapshot

## 状态分布

- archive: 85
- controlled: 2838
- draft: 13
- okf_derived: 99

## 项目分布

- Brain: 11
- GFIS: 110
- GPC: 49
- GPCF: 1800
- KDS: 816
- MMC: 9
- PKC: 7
- PVAOS: 10
- Studio: 2
- WAES: 163
- XGD: 7
- XiaoC: 43
- XiaoG: 8

## 命令结果

### loop_engineering_five_direction

```text
loop_engineering_five_direction_implementation=pass run=implemented stop=implemented verify=implemented recover=implemented debug=implemented status_ceiling=partial_repair real_business_lane=repair_required runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_allowed=false integrated_allowed=false production_ready_allowed=false gfis_status_ceiling=repair_required
```

### loop_v11_slimming_delivery_recovery

```text
loop_v11_slimming_delivery_recovery=pass delivery_loop=enabled governance_loop=stage_or_risk_triggered gate_levels=P0,P1,P2,P3 gfis_min_slice=registered gfis_dev_completion_slice=registered gfis_dev_completion_multi_agent=registered gfis_dev_completion_evidence=registered gfis_dev_completion_governance_summary=registered fixture_e2e_passed=true contract_validator_passed=true development_lane=continue_allowed real_business_validation_lane=pending_source_of_record gfis_status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false status_promotion_allowed=false kds_sensitive_blocker=resolved_not_in_git_status kds_safe_to_auto_commit=false governance_drift=pass gfis_authorization_boundary=pass
```

### loop_engineering_master_plan

```text
loop_engineering_master_plan=pass baseline=v1.0 authority=master_implementation_plan roadmap=P0,P1,P2,P3,P4,P5 status_ceiling=repair_required accepted_allowed=false integrated_allowed=false runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 gfis_status_ceiling=repair_required
```

### loop_capability_registry

```text
loop_capability_registry=pass pools=skill,tool,method statuses=fast_admitted,candidate,pilot,controlled,default_enabled,downgraded,disabled,deprecated,superseded default_enable=risk_tiered pilot_plus_evidence=required core_methods=CodeGraph,external_search,RAG,multi_agent_parallel capability_families=CodeGraph,Agent-Reach,Ontology,WAS,Headroom,OKF_ODF,LCX,WAES_KDS_RAG_writeback gfis_status_ceiling=repair_required
```

### codegraph_loop_schema

```text
codegraph_loop_schema=pass templates=3 required_fields=38 automatic_status_upgrade=false karpathy_gate=enabled
```

### loop_ui_quality_baseline

```text
loop_ui_quality_baseline=pass template_ui_section=present master_spec=present capability_status=pilot explicit_ui_scope_rounds=23 explicit_ui_scope_valid=23 historical_ui_signal_rounds_without_explicit_scope=585 baseline_evidence=present gfis_status_ceiling=repair_required
```

### loop_session_mainline_control

```text
loop_session_mainline_control=pass session_mainline=required handoff_evidence=required mainline_drift_detected=hard_pause write_without_handoff=false commit_push_deploy_status_promotion_allowed=false gfis_status_ceiling=repair_required
```

### current_session_mainline_declaration

```text
current_session_mainline_declaration=pass session_mainline=session-mainline-control-rollout handoff_required=false mainline_drift_detected=false status_ceiling=partial accepted=false integrated=false production_ready=false gfis_status_ceiling=repair_required
```

### loop_session_registry

```text
loop_session_registry=pass repo_recorded_loop_rounds=1221 orphan_session_family=0 live_codex_threads_covered=false auto_takeover_allowed=false GFIS_L4_repair_and_test_sync=296,KDS___DKS_governance=461,Ontology___WAS_governance=131,CodeGraph_governance=67,COGNEE_pilot___writeback=24,Agent-Reach_governance=49,Headroom___LCX_governance=81,OKF___ODF_governance=4,GPCF_CF___governance_rounds=47,XiaoG_evidence_repair=1,Project_group_phase_goals=22,LOOP_localization_governance=6,UI_governance_and_validation=27,Session_declaration_and_mainline=5 gfis_status_ceiling=repair_required
```

### session_mainline_preflight_enforcement

```text
session_mainline_preflight_enforcement=pass preflight_decision=continue_current_mainline_only mainline_drift_detected=false handoff_required=false authorization_required=false live_codex_threads_covered=false auto_takeover_allowed=false gfis_status_ceiling=repair_required
```

### session_mainline_drift_watch

```text
session_mainline_drift_watch=pass watch_mode=repo_recorded_governance_only positive_fixtures=2 negative_fixtures=4 live_codex_threads_covered=false auto_takeover_allowed=false
```

### session_mainline_handoff_request_gate

```text
session_mainline_handoff_request_gate=pass gate_mode=explicit_user_confirmation_required proposal_only_for_other_sessions=true live_codex_threads_covered=false auto_takeover_allowed=false gfis_status_ceiling=repair_required
```

### gfis_real_fact_entry_gate

```text
gfis_real_fact_entry_gate=pass strong_block=true read_only_verified=true development_lane=continue_allowed real_business_validation_lane=pending_source_of_record real_source_records_zero_is_not_dev_blocker=true real_business_validation_block=true status_promotion_block=true real_source_records=0 valid_source_records=0 formal_confirmation_files=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 manual_business_verification_pending=true real_business_lane=repair_required status_ceiling=repair_required next_required_input=real_source_record_or_equivalent_formal_confirmation accepted=false integrated=false production_ready=false customer_accepted=false
```

### gfis_real_fact_entry_coverage

```text
gfis_real_fact_entry_coverage=pass covered_entries=8 real_source_record=0 equivalent_formal_confirmation_file=0 manual_business_verification=pending runtime_primary_key=0 review_queue=0 runtime_intake=0 waes_review=0 verified_artifact=0 status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false
```

### gfis_real_fact_no_status_promotion

```text
gfis_real_fact_no_status_promotion=pass checked_docs=9 positive_status_claims=0 gfis_status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false strong_block=true
```

### loop_document_gate_gfis_coverage

```text
loop_document_gate_gfis_coverage=pass status_related_direct_validators=30 gfis_guarded_direct_validators=30 gfis_status_ceiling=repair_required customer_accepted_guard=covered
```

### project_group_external_loop_gate_delegates

```text
project_group_external_loop_gate_delegates=pass checked_repos=3 delegation_only=true gfis_status_ceiling=repair_required formal_confirmation_files=0
```

### gpcf_project_status_matrix_17_project_scope

```text
{
  "gate": "gpcf_project_status_matrix_17_project_scope",
  "status": "pass",
  "projects_checked": 17,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates status matrix coverage only; it does not upgrade project status or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_status_control_surface_17_scope

```text
{
  "gate": "project_group_status_control_surface_17_scope",
  "status": "pass",
  "files_checked": 5,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates control-surface consistency only; it does not execute project tasks or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_full_project_baseline

```text
{
  "gate": "project_group_full_project_baseline",
  "status": "pass",
  "projects_checked": 17,
  "baseline": "controlled",
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates 17-project baseline coverage only; it does not grant accepted, integrated, production, customer acceptance, commit, or push authority."
  ]
}
```

### project_group_current_state_baseline_refresh

```text
{
  "gate": "project_group_current_state_baseline_refresh_20260626",
  "status": "pass",
  "project_count": 17,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates current-state baseline refresh evidence only; it does not execute tasks, clean repos, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_dev_task_queue

```text
{
  "gate": "project_group_dev_task_queue_20260626",
  "status": "pass",
  "project_count": 17,
  "binding_row_count": 17,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates dev-task queue control only; it does not execute project tasks or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_real_execution_metadata_coverage

```text
{
  "gate": "project_group_real_execution_metadata_coverage_20260626",
  "status": "pass",
  "key_doc_count": 36,
  "expected_project_count": 17,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates frontmatter related_projects coverage only; it does not execute tasks, grant authorization, stage, commit, push, deploy, release, sync KDS API, or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_live_status_snapshot

```text
{
  "gate": "project_group_live_status_snapshot_20260626",
  "status": "fail",
  "checked_repo_count": 17,
  "dirty_repo_count": 4,
  "dirty_repos": [
    "GlobalCloud Brain",
    "GlobalCoud GPCF",
    "GlobalCloud KDS",
    "GlobalCloud SOP"
  ],
  "stable_dirty_repos": [
    "GlobalCloud Brain",
    "GlobalCloud SOP"
  ],
  "optional_volatile_dirty_repos": [
    "GlobalCoud GPCF"
  ],
  "ahead_repos": [],
  "live_dirty_counts": {
    "GlobalCloud AAAS": 0,
    "GlobalCloud Brain": 1,
    "WAS世界资产体系": 0,
    "GlobalCloud XiaoC": 0,
    "GlobalCloud WAES": 0,
    "GlobalCloud GPC": 0,
    "GlobalCloud Studio": 0,
    "GlobalCoud GPCF": 295,
    "GlobalCloud XWAIL": 0,
    "GlobalCloud GFIS": 0,
    "GlobalCloud MMC": 0,
    "GlobalCloud KDS": 61,
    "GlobalCloud XiaoG": 0,
    "GlobalCloud PVAOS": 0,
    "GlobalCloud SOP": 43,
    "GlobalCloud PKC": 0,
    "GlobalCloud XGD": 0
  },
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [
    "dirty repo set drifted: required=['GlobalCloud Brain', 'GlobalCloud SOP'], optional_volatile=['GlobalCoud GPCF'], actual=['GlobalCloud Brain', 'GlobalCoud GPCF', 'GlobalCloud KDS', 'GlobalCloud SOP']"
  ],
  "warnings": [
    "This validates the live status snapshot only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status."
  ]
}
```

### project_group_real_execution_governance_board

```text
{
  "gate": "project_group_real_execution_governance_board",
  "status": "pass",
  "projects_checked": 17,
  "full_baseline_projects_checked": 17,
  "tasks_checked": 52,
  "dependencies_checked": 5,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This gate validates the governance board structure and boundary wording; it does not execute project repositories."
  ]
}
```

### project_group_status_advancement_matrix

```text
{
  "gate": "project_group_status_advancement_matrix",
  "status": "pass",
  "project_status_rule_count": 17,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates advancement criteria only; it does not execute tasks or grant accepted, integrated, production, customer acceptance, commit, push, deploy, or release authority."
  ]
}
```

### project_group_ready_for_review_advancement_queue

```text
{
  "gate": "project_group_ready_for_review_advancement_queue_20260626",
  "status": "pass",
  "project_count": 17,
  "auto_ready_for_review_upgrade": false,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates advancement queue control only; it does not upgrade project status or grant accepted/integrated/customer acceptance."
  ]
}
```

### project_group_authorization_pre_execution_command_pack

```text
{
  "gate": "project_group_authorization_pre_execution_command_pack_20260626",
  "status": "pass",
  "command_pack_count": 7,
  "receipt_record_count": 0,
  "authorization_granted_count": 0,
  "action_executed_count": 0,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates command-pack control only; it does not grant authorization or execute project actions."
  ]
}
```

### project_group_authorization_pre_execution_environment_readiness

```text
{
  "gate": "project_group_authorization_pre_execution_environment_readiness_20260626",
  "status": "pass",
  "repo_path_check_pass": 7,
  "repo_path_check_count": 7,
  "package_script_check_pass": 6,
  "package_script_check_count": 6,
  "target_file_check_pass": 4,
  "target_file_check_count": 4,
  "gpcf_validator_check_pass": 11,
  "gpcf_validator_check_count": 11,
  "authorization_granted_count": 0,
  "action_executed_count": 0,
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "This validates read-only environment readiness only; it does not execute authorization command packs."
  ]
}
```

### project_group_delivery_readiness

```text
{
  "gate": "project_group_delivery_readiness",
  "status": "pass",
  "readiness": "partial",
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "delivery readiness remains partial because business implementation and customer delivery are outside document-governance completion"
  ]
}
```

### project_runtime_readiness

```text
{
  "gate": "project_runtime_readiness",
  "status": "pass",
  "readiness": "phase_3_all_project_plans_controlled",
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "phase 3 does not assert any project runtime is live"
  ]
}
```

### project_integration_readiness

```text
{
  "gate": "project_integration_readiness",
  "status": "pass",
  "readiness": "phase_3_all_project_plans_controlled",
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "phase 3 does not assert any cross-project integration is verified"
  ]
}
```

### customer_acceptance_readiness

```text
{
  "gate": "customer_acceptance_readiness",
  "status": "pass",
  "readiness": "phase_3_all_project_plans_controlled",
  "gfis_real_fact_entry": {
    "gfis_real_fact_entry_gate": "pass",
    "strong_block": "true",
    "read_only_verified": "true",
    "development_lane": "continue_allowed",
    "real_business_validation_lane": "pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker": "true",
    "real_business_validation_block": "true",
    "status_promotion_block": "true",
    "real_source_records": "0",
    "valid_source_records": "0",
    "formal_confirmation_files": "0",
    "runtime_primary_key_ready": "0",
    "review_queue": "0",
    "runtime_intake": "0",
    "waes_review": "0",
    "verified": "0",
    "manual_business_verification_pending": "true",
    "real_business_lane": "repair_required",
    "status_ceiling": "repair_required",
    "next_required_input": "real_source_record_or_equivalent_formal_confirmation",
    "accepted": "false",
    "integrated": "false",
    "production_ready": "false",
    "customer_accepted": "false"
  },
  "failures": [],
  "warnings": [
    "phase 3 does not assert customer acceptance"
  ]
}
```

### document_pollution

```text
document_pollution=pass
```

### fixed_doc_id_preservation

```text
gckf_p0_document_control_preserves_fixed_doc_id=pass
frontmatter_doc_id_preservation=covered
old_short_doc_ids_present=0
fixed_doc_ids_present=16
execution_mode=read_only_validation
```

### chinese_localization

```text
localization_gate=pass
docs_checked=856
software_files_checked=240
findings=0
```

### kds_token

```text
kds_token=pass fingerprint=bfd9553d
```

### project_group_gate_readiness

```text
attempt=1 code=0 output=project_group_gate_readiness=pass checked_repos=17 passed=17 failed=0 gfis_status_ceiling=repair_required reasons=none
```
