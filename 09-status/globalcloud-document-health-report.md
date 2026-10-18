---
doc_id: GPCF-DOC-C436DDB0F6
title: GlobalCloud 文档健康报告
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP, PQC, SpaceAI, SpaceAIStudio, World, GCMEM, WAE]
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

本报告用于记录项目群文档门禁、镜像覆盖、状态分布和命令证据的当前健康状态。文中的英文项目名、脚本名、字段名和命令输出均为机器可回放证据，不代表业务事实完成、状态升级、客户验收、生产发布或真实外部写入。当前报告只作为受控治理快照，所有 accepted、integrated、production_ready、customer_accepted 等状态仍必须等待人工确认、真实 source-of-record 或等效正式确认文件、人工业务核验、运行层主键、review queue、runtime intake、WAME review 和 verified artifact 全部满足后才能重新评估。

生成时间：2026-10-18T02:13:02.340691+00:00

Loop 文档门禁：`pass`

## 总览

- 仓库 Markdown：3543
- KDS 镜像 Markdown：3575
- KDS 本地镜像流水：3450
- KDS 本地镜像唯一文档：3450
- KDS API 同步流水：141
- 元数据缺失：0
- README 缺失目录：0
- 中文本地化债务：False
- 固定 doc_id 漂移：False
- 受控文档复核逾期（>90 天）：2824
- 受控文档复核日期缺失或无效：1
- 治理状态上限：partial
- 门禁原因：无

## 状态分布

- archive: 97
- controlled: 3134
- draft: 150
- okf_derived: 99

## 项目分布

- AAAS: 3
- Brain: 14
- GFIS: 117
- GPC: 54
- GPCF: 1852
- KDS: 1107
- MMC: 13
- PKC: 10
- PVAOS: 13
- SOP: 3
- Studio: 5
- WAME: 194
- WAS: 3
- XGD: 10
- XWAIL: 3
- XiaoC: 68
- XiaoG: 11

## 命令结果

### project_group_live_status_current

```text
{"status": "pass", "project_count": 24, "snapshot_fresh": true, "snapshot_matches": true}
[warn] GlobalCloud ICP: no upstream, ahead/behind treated as 0
```

### loop_engineering_five_direction

```text
loop_engineering_five_direction_implementation=pass run=implemented stop=implemented verify=implemented recover=implemented debug=implemented status_ceiling=partial_repair real_business_lane=repair_required runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 wame_review=0 verified=0 accepted_allowed=false integrated_allowed=false production_ready_allowed=false gfis_status_ceiling=repair_required
```

### loop_v11_slimming_delivery_recovery

```text
loop_v11_slimming_delivery_recovery=pass delivery_loop=enabled governance_loop=stage_or_risk_triggered gate_levels=P0,P1,P2,P3 gfis_min_slice=registered gfis_dev_completion_slice=registered gfis_dev_completion_multi_agent=registered gfis_dev_completion_evidence=registered gfis_dev_completion_governance_summary=registered fixture_e2e_passed=true contract_validator_passed=true development_lane=continue_allowed real_business_validation_lane=pending_source_of_record gfis_status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false status_promotion_allowed=false kds_sensitive_blocker=resolved_not_in_git_status kds_safe_to_auto_commit=false governance_drift=pass gfis_authorization_boundary=pass
```

### loop_engineering_master_plan

```text
loop_engineering_master_plan=pass baseline=v1.0 authority=master_implementation_plan roadmap=P0,P1,P2,P3,P4,P5 status_ceiling=repair_required accepted_allowed=false integrated_allowed=false runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 wame_review=0 verified=0 gfis_status_ceiling=repair_required
```

### loop_optional_commentary_policy

```text
loop_optional_commentary_policy=pass required_phrase='DO NOT send optional commentary' project_group_scope=17_projects skills=covered templates=covered
```

### loop_capability_registry

```text
loop_capability_registry=pass pools=skill,tool,method statuses=fast_admitted,candidate,pilot,controlled,default_enabled,downgraded,disabled,deprecated,superseded default_enable=risk_tiered pilot_plus_evidence=required core_methods=CodeGraph,external_search,RAG,multi_agent_parallel capability_families=CodeGraph,Agent-Reach,Ontology,WAS,Headroom,OKF_ODF,LCX,WAME_KDS_RAG_writeback gfis_status_ceiling=repair_required
```

### codegraph_loop_schema

```text
codegraph_loop_schema=pass templates=3 required_fields=38 automatic_status_upgrade=false karpathy_gate=enabled
```

### loop_ui_quality_baseline

```text
loop_ui_quality_baseline=pass template_ui_section=present master_spec=present capability_status=pilot explicit_ui_scope_rounds=23 explicit_ui_scope_valid=23 historical_ui_signal_rounds_without_explicit_scope=760 baseline_evidence=present gfis_status_ceiling=repair_required
```

### loop_delivery_efficiency_control

```text
loop_delivery_efficiency_control=pass project_group_scope_17_projects=true delivery_efficiency_gate=required product_delta=required user_visible_delta=required loop_cost_level=required substantive_round=required high_compliance_low_product_progress=blocked single_label_copy_tweak_heavy_loop_blocked=true status_promotion_allowed=false gfis_status_ceiling=repair_required
```

### gpcf_2_feature_workspace

```text
gpcf_2_feature_workspace=pass feature_delivery_center=true project_scope=24 new_feature_entry=enabled close_feature_exit=enabled status_promotion_allowed=false
```

### icp_project_registration

```text
icp_project_registration=pass
project_count=24 icp_status=candidate overall_status=partial confirmation_status=human_required
historical_project_count=17 historical_evidence_rewrite=false
```

### constitution_g00_inheritance

```text
constitution_g00=pass status=candidate domain_owner=ICP canonical_custodian=KDS authorization=human_required status_promotion=false
```

### loop_ui_product_first_control

```text
loop_ui_product_first_control=pass studio_control=governance_only product_first_ui_gate=required evidence_overexposure_gate=required debug_details_default_hidden=required task_flow_e2e_required=true human_operable_gate=required multi_user_usability_gate=required project_count=24 active_feature_coverage=18 status_promotion_allowed=false gfis_status_ceiling=repair_required
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
loop_session_registry=pass repo_recorded_loop_rounds=1269 orphan_session_family=0 live_codex_threads_covered=gke001_three_lane_only live_codex_thread_count=3 auto_takeover_allowed=false GFIS_L4_repair_and_test_sync=296,KDS___DKS_governance=462,Knowledge_engineering_governance=41,Ontology___WAS_governance=131,CodeGraph_governance=67,COGNEE_pilot___writeback=24,Agent-Reach_governance=49,Headroom___LCX_governance=81,OKF___ODF_governance=4,GPCF_CF___governance_rounds=47,XiaoG_evidence_repair=1,Project_group_phase_goals=22,LOOP_localization_governance=6,UI_governance_and_validation=27,Session_declaration_and_mainline=5,GPC_domain_registry_and_graph_extension=3,XWAIL___MMC_intake_governance=3 gfis_status_ceiling=repair_required
```

### gke001_three_lane_coordination

```text
gke001_three_lane_coordination=pass coordination_id=GKE-001-COORDINATION-20260803-001 lanes=3 unique_locks=3 brain_mode=a10c12_report_only_verified studio_mode=a10c12_report_only_verified kds_mode=a10c12_report_only_verified mmc_mode=a10c12_report_only_policy_admission_blocked active_product_lanes=0 governance_implementation_lanes=0 report_only_lanes=3 authorized_pending_receipt_lanes=0 review_pending_lanes=0 human_authorization_request_lanes=1 kds_external_role_view_excluded=true gfis_status_ceiling=repair_required studio_a4=GKE-001-COORDINATION-20260803-001-A4 studio_a4_sha256=c1c7963b0f66e5c66d471817c0f25219fe1653182362c5b4b3fe01010bfc6f3a studio_a5=GKE-001-COORDINATION-20260810-001-A5 studio_a5_sha256=8709a81b994eac6b91216d11cffb0e70115e450c776ac1081e5ac7972160a344 studio_a6=GKE-001-COORDINATION-20260810-002-A6 studio_a6_sha256=bba9f2f33a1c43066df551ba8b086bcaa5f3c2d655b2ca6af831aefb40ee8f3c minimal_parallel_a7=GKE-001-COORDINATION-20260811-001-A7 minimal_parallel_a7_sha256=04e27fd23e1a3fd32a10bd85aa4f387af56668d938c44943f575340d3b8f8668 a7_governance_cleanup_a8=GKE-001-COORDINATION-20260811-002-A8 a7_governance_cleanup_a8_sha256=1e8fcdd04dade89a76a27647189a374d70d67267ff19817a6d5e7ff6cce30a89 a9_read_admission=GKE-001-COORDINATION-20260811-003-A9 a9_read_admission_sha256=a3918471b8cde1eeb965c3ff5120be99944ee8fd24d0ffe1e87fe3b724435fc7 a9r1=GKE-001-COORDINATION-20260811-004-A9R1 a9r1_sha256=05bfb1c3cfae04b1f253afce5cb347fdd9306af606faade2129f1499b59f22f6 a10p0=GKE-001-COORDINATION-20260811-005-A10P0 a10p0_sha256=b9d4acdef872289afd5a2194a1430daf977bab028f9fc76ce6e937f39e8ecc96 a10p1=GKE-001-COORDINATION-20260811-006-A10P1 a10p1_sha256=264a50bb1020a97777761371fb331f6a6c05e6ed3698875d27107b0c79bfd1bb a10p2=GKE-001-COORDINATION-20260811-007-A10P2 a10p2_sha256=e2a0cb491bcb626bb29507be5e51612e4cb26ddf1427b94e70f7bd3f1b7f249e candidate_sha256=11e15a3448279c7ddcdc97ea25b80cfefbef17a332c08cd20f41efc97a6667f8 a10p3=GKE-001-COORDINATION-20260811-008-A10P3 a10p3_sha256=9a3fe20c87d269263e442b5a6899f6f75581319adc7a8800a27e0669abcd22e4 schema_sha256=48dfcb0967a894ee2bd760311d7f84023054b0bcc2bc578292d826e73fbc7c18 a10p3r1=GKE-001-COORDINATION-20260811-009-A10P3R1 a10p3r1_sha256=c8b76dcde4ffdee835fe426edbd44c33c975b6bcbd25dd60ad0dd827134f6060 corrected_schema_sha256=74b51affabf79d2ba4a908d2d9397671bdd0b07bc80814a0c36dd8d83faa7e14 a10p3r2=GKE-001-COORDINATION-20260811-010-A10P3R2 a10p3r2_sha256=d4b21c2ccfbc9d2878ce5c020c232f26c53b704b51313a92da6d8345748b12bc frozen_schema_sha256=cc5865ac5f76e82d7ea86891f020e196073a0a23cd5a4f6bb44a3a279b0b0de0 freeze_id=GKE-001-CONTRACT-FREEZE-20260811-001 freeze_sha256=a7dbdcf6a64a4f9b6c6cd11e4ae2fe02405624b29e4ad009a317510de557a23f a10i1=GKE-001-COORDINATION-20260811-011-A10I1 a10i1_sha256=8f4087ca09a4695a0cdec021d0d22270c4866ec9903dc86c0c8cbff8069d37c3 a10i1r1=GKE-001-COORDINATION-20260811-012-A10I1R1 a10i1r1_sha256=4c4a164e7e30186789d4f518ffeede6465dab28e10cc0206bb3c151b16958e7e a10i2=GKE-001-COORDINATION-20260811-013-A10I2 a10i2_sha256=8ab2dd88b45c33669a4d3a14dc8065765738e113ff1728965b1defaa3776aacf a10i2r1=GKE-001-COORDINATION-20260811-014-A10I2R1 a10i2r1_sha256=ef4065c374f5f2be480c170b3a4e60bef54a72b0d8ee40c3bd3c7fb5e12cbd2e a10i2r2=GKE-001-COORDINATION-20260811-015-A10I2R2 a10i2r2_sha256=bae892222772f306c41999631a5d1bf27cc9ea17f79e88cc42c1e9163a6b2d11 a10i3p0=GKE-001-COORDINATION-20260811-016-A10I3P0 a10i3p0_sha256=4a7de8561f2882940caea5b9ed55a790e53f9c44ea5cfb3c359e5ff9791b73df a10i3h1=GKE-001-COORDINATION-20260811-017-A10I3H1 a10i3h1_sha256=a3fc12a42b47e23d39a867719bcde0da10ec452751378d5a0128f38bb54cdbff a10i3h1r1=GKE-001-COORDINATION-20260811-018-A10I3H1R1 a10i3h1r1_sha256=8a5470cfa1adfdab1ff18307aad3739bc3af6fbd32b10c3353ff8e8545875850 a10i3h1r2=GKE-001-COORDINATION-20260811-019-A10I3H1R2 a10i3h1r2_sha256=880980dbd38462c58fa8da34ea67fca593c3e2bae2958e3410a6a74b1222c731 a10i3h1r2r0=GKE-001-COORDINATION-20260811-020-A10I3H1R2R0 a10i3h1r2r0_sha256=a40e54f14ff5bd1e7b9474097e466f6ac0f6dea854ac3c35f0c34f59d4e62152 a10i3h1r2r1=GKE-001-COORDINATION-20260812-001-A10I3H1R2R1 a10i3h1r2r1_sha256=3699642fde266e74a797d1515abd9d791da0526b7eef8c278f7cc2e098a35a3f brain_a10p1t3=GKE-001-COORDINATION-20260812-002-A10P1T3 brain_a10p1t3_sha256=d96472aee1af90b94ac0f5f24ca06f5d4dc07d83ee0ff44d5fd03f74879a03ad brain_a10p1t4=GKE-001-COORDINATION-20260812-008-A10P1T4 brain_a10p1t4_sha256=25349bb558c0ef8fed5233d080c20356789c4a89bfdf5ebd09ca07d2eab9322f brain_a10p1t4r1=GKE-001-COORDINATION-20260812-009-A10P1T4R1 brain_a10p1t4r1_sha256=d3a7dced8b559ff4d2cc543f7c04e5524af2902563cf6423496ce157f9a37e8c a10i3h1r2r2=GKE-001-COORDINATION-20260812-003-A10I3H1R2R2 a10i3h1r2r2_sha256=588691af5c5866a481fcc46886df0e9c3cd200a191bcca89295397f7cd0838c3 a10i3h1r2r3=GKE-001-COORDINATION-20260812-006-A10I3H1R2R3 a10i3h1r2r3_sha256=06a34a9b05078fe26897c15070315e919886b132e02c8006fcf50fce8f32e0ff studio_a10i1g1=GKE-001-COORDINATION-20260812-004-A10I1G1 studio_a10i1g1_sha256=f6f3ceeacda0fd8d6f969c164d9e9c481ddb87b8be0788c357f2b2734b79b8b9 studio_a10i1g1r1=GKE-001-COORDINATION-20260812-007-A10I1G1R1 studio_a10i1g1r1_sha256=2b228d7a89771c117b2fb91607e8f32f65cca4e079a644c58f43b5f129ffcd1b kds_dirty_isolation=GKE-001-COORDINATION-20260812-010-A10I1D1 kds_dirty_isolation_sha256=d14ef30b401284c833e16bc1f1add845fba7e34cb2f31a29cf85c52e6eec2840 kds_dependency_order=GKE-001-COORDINATION-20260812-011-A10I1D2 kds_dependency_order_sha256=a226a75e1d839678b79ea941def964b69e0e2876b7c49510b256882017ac6e5d kds_stageb_disposition=GKE-001-COORDINATION-20260812-012-A10I1D3 kds_stageb_disposition_sha256=44952b52497325a936deb68a6a2a986f4d6d287805818b8a8fce4cd5f5a13142 kds_stageb_authorization_request=GKE-001-COORDINATION-20260812-013-A10I1D4 kds_stageb_authorization_request_sha256=01685904e46c63e3997f6080716f8bb5ddddfe6ebe7588641870c905f9b23f76 kds_stageb_core_authorization_request=GKE-001-COORDINATION-20260812-014-A10I1D4R1 kds_stageb_core_authorization_request_sha256=d9dbe8ba24518beec10d4e5eefbcfddebeb22669d4195b084ae150ba6a433b3a kds_stageb_core_baseline_reconciliation=GKE-001-COORDINATION-20260812-015-A10I1D4R1B1 kds_stageb_core_baseline_reconciliation_sha256=989e77472642fdc7000799243bb5b68fd79e736c6b7bbb3e5e33ddd9dbe6e4e7 kds_stageb_core_diffcheck_rework=GKE-001-COORDINATION-20260812-016-A10I1D4R2 kds_stageb_core_diffcheck_rework_sha256=6f89ede57b739d374dd44b26bb2fad60a36b60e77333781d4cb2125382b6d7db kds_stageb_core_diffcheck_authorization=GKE-001-COORDINATION-20260812-017-A10I1D4R2A1 kds_stageb_core_diffcheck_authorization_sha256=c3bc86e0ae4aea6b2920d49daaf403bbec64cace11f3d8e93d2a615b5c659237 kds_stageb_core_local_commit_receipt=GKE-001-COORDINATION-20260812-018-A10I1D4R2A2 kds_stageb_core_local_commit_receipt_sha256=0921e27a7d3066e7c9a5691c4bd63b18211f7fceb20e083cc924a265631a11bb kds_stageb_regression_preflight=GKE-001-COORDINATION-20260812-019-A10I1D4R3 kds_stageb_regression_preflight_sha256=22c50de2ea3e5fbe2ed1d2a1e35efda1c44cdeb507abfb76abc1843db2f47d99 kds_stageb_regression_preflight_receipt=GKE-001-COORDINATION-20260812-020-A10I1D4R3R1 kds_stageb_regression_preflight_receipt_sha256=d8a746f5cf323211f94846193d92fe32ea7ac4293faede1b3f0b1caec031278d kds_stageb_regression_commit_authorization_request=GKE-001-COORDINATION-20260812-021-A10I1D4R4 kds_stageb_regression_commit_authorization_request_sha256=7107019c08ba37a61b0531f0dd6102d0b26dd16248365b9499c9b0e69174366e kds_stageb_regression_commit_authorization=GKE-001-COORDINATION-20260812-022-A10I1D4R4A1 kds_stageb_regression_commit_authorization_sha256=859e6eac3a4a792f6977d3dba87a3810439354410517704af9f88450ce2935a7 kds_stageb_regression_commit_receipt=GKE-001-COORDINATION-20260812-023-A10I1D4R4A2 kds_stageb_regression_commit_receipt_sha256=7973115f76b2cf671b2a68fceec3a7559096a3e26d531101082a64db8472a8e7 kds_stageb_openspec_preflight=GKE-001-COORDINATION-20260812-024-A10I1D4R5 kds_stageb_openspec_preflight_sha256=829f1a2eda39c89eefcb2374da62483e8294b27470feeb223532d1a42c6a2a4a kds_stageb_openspec_preflight_receipt=GKE-001-COORDINATION-20260812-025-A10I1D4R5R1 kds_stageb_openspec_preflight_receipt_sha256=5a96e5548c8ba05a3f598f85c480a2b763e2bf6af11e798957eac1be4c269492 kds_stageb_openspec_commit_request=GKE-001-COORDINATION-20260812-026-A10I1D4R6 kds_stageb_openspec_commit_request_sha256=6695349d631cf1084486456dd47e95d6f2f0f20381548757d1c163cfdff7b021 kds_stageb_openspec_commit_authorization=GKE-001-COORDINATION-20260812-027-A10I1D4R6A1 kds_stageb_openspec_commit_authorization_sha256=9f518d538a6471337fcfd390091baf14aecae39a20b0f852b8a6890bc9a20a0b kds_stageb_openspec_commit_receipt=GKE-001-COORDINATION-20260812-028-A10I1D4R6A2 kds_stageb_openspec_commit_receipt_sha256=54b4bced82937fba41fa890d36a5b12c9342ffa0445483fed1dfe7bccc136fb1 kds_stageb_run_handoff_preflight=GKE-001-COORDINATION-20260812-029-A10I1D4R7 kds_stageb_run_handoff_preflight_sha256=d04069ae437b0a2defcbad81b8f5c6feb3760c207675a44f8baac187dd9ea02d kds_stageb_run_handoff_preflight_receipt=GKE-001-COORDINATION-20260812-030-A10I1D4R7R1 kds_stageb_run_handoff_preflight_receipt_sha256=88c7b131aef332f6004ece1c1191932f0e93bbc05dab0e1f0674786dd80f0440 kds_stageb_run_handoff_eof_baseline=GKE-001-COORDINATION-20260813-033-A10I1D4R8B1 kds_stageb_run_handoff_eof_baseline_sha256=41ea87a447d40b17fae124cff74cbc1198882e89112e81b7178abc098118bbd6 kds_stageb_run_handoff_eof_execution=GKE-001-COORDINATION-20260813-034-A10I1D4R8A1 kds_stageb_run_handoff_eof_execution_sha256=7ea77e17fc0a72b433bc244903efcc633ddd992e7ff7823b50dbff3909f2f999 kds_stageb_run_handoff_eof_receipt=GKE-001-COORDINATION-20260813-035-A10I1D4R8A2 kds_stageb_run_handoff_eof_receipt_sha256=8f1aaa99ed58c4c26b79c53b5cac50c7a1f4fda9475a47ac9e58253c0a48038a kds_stageb_run_handoff_commit_request=GKE-001-COORDINATION-20260813-036-A10I1D4R9 kds_stageb_run_handoff_commit_request_sha256=f55627928263a30b0c29536778d71ffd428ee657e9109395ca770c15691752d8 kds_stageb_push_preflight=GKE-001-COORDINATION-20260813-039-A10I1D4R10 kds_stageb_push_preflight_sha256=6e25314b88b07cc6ca1bfc4bf589bfd574c0d9d9c4bc47c7cb4479ea9eeb05d8 kds_stageb_push_preflight_receipt=GKE-001-COORDINATION-20260813-040-A10I1D4R10R1 kds_stageb_push_preflight_receipt_sha256=bb5f388526767b23bb66efbeec1aa0222576a2654b1ec17486c92df25c2d191d kds_stageb_push_request=GKE-001-COORDINATION-20260813-041-A10I1D4R11 kds_stageb_push_request_sha256=3d292b13ca6910524dd3d30f0cc5088f6713dbc4befac0f7c78e65698886d47d kds_stageb_push_authorization=GKE-001-COORDINATION-20260813-042-A10I1D4R11A1 kds_stageb_push_authorization_sha256=29c54680a9c78dbc63e0abb9b3502482e1b50d119bc4250f12b5128d8f2d0abc kds_stageb_push_receipt=GKE-001-COORDINATION-20260813-043-A10I1D4R11A2 kds_stageb_push_receipt_sha256=5e2e604af4e26d7a6c6eedf7160c4da362387c0dcb1cd6beaa0e987a8fb67035 release0_current_state=GKE-001-COORDINATION-20260813-076-A10C12 release0_current_state_sha256=ac4c218ea1335b0275196d92af4ea66c62560cf9c53d96615ea0c079f844445c release0_current_state_handoff=GKE-001-COORDINATION-20260813-077-A10C12R1 release0_current_state_handoff_sha256=9ff607e7c56cf0aa9349d6e2f13112cd1ea18e3fb5a153cf035ae204c01f8b98 release0_current_state_review=GKE-001-COORDINATION-20260813-078-A10C12R2 release0_current_state_review_sha256=5fef27d8c380a0eb48d76f0e70e09108172c432dc7861442097a6d9a6f4c9fb1 release0_kds_commit_request=GKE-001-COORDINATION-20260813-079-A10C13 release0_kds_commit_request_sha256=88a6c2b201c9e3e949f955908831920fea89adf301ac0a380b559df6deb56001 localization_boundary_repair=GKE-001-COORDINATION-20260813-080-A10C14 localization_boundary_repair_sha256=dbf69478fcb1e2e9b789141305084f30be54ccf6ebb1a4d3bf218b74b4030dca release0_kds_commit_readiness_replay=GKE-001-COORDINATION-20260813-081-A10C15 release0_kds_commit_readiness_replay_sha256=510e490f2ec5cebb6c236c017c9c94e490043999ca46082a90e69e84d593b224 mmc_release0_policy_freshness_replay=GKE-001-COORDINATION-20260813-082-A10C16 mmc_release0_policy_freshness_replay_sha256=5b43ecdd0ab7b7df6a9919bf283880cd344cfb4f6cf8ac8d8031043ed03d8ac4 release0_consumer_freshness_replay=GKE-001-COORDINATION-20260813-083-A10C17 release0_consumer_freshness_replay_sha256=faac8e0e5840b3abcbc702d16e7dca5d71e50ba20381f1dcfe66a6ad9490dbd3 status=active/partial/not_complete dispatch_status=studio_frozen_brain_a10p1t4_passed_mmc_h1r3_verified_kds_stageb_four_commits_pushed_postpush_review_passed
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
gfis_real_fact_entry_gate=pass strong_block=true read_only_verified=true development_lane=continue_allowed real_business_validation_lane=pending_source_of_record real_source_records_zero_is_not_dev_blocker=true real_business_validation_block=true status_promotion_block=true real_source_records=0 valid_source_records=0 formal_confirmation_files=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 wame_review=0 verified=0 manual_business_verification_pending=true real_business_lane=repair_required status_ceiling=repair_required next_required_input=real_source_record_or_equivalent_formal_confirmation accepted=false integrated=false production_ready=false customer_accepted=false
```

### gfis_real_fact_entry_coverage

```text
gfis_real_fact_entry_coverage=pass covered_entries=8 real_source_record=0 equivalent_formal_confirmation_file=0 manual_business_verification=pending runtime_primary_key=0 review_queue=0 runtime_intake=0 wame_review=0 verified_artifact=0 status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false
```

### gfis_real_fact_no_status_promotion

```text
gfis_real_fact_no_status_promotion=pass checked_docs=9 positive_status_claims=0 gfis_status_ceiling=repair_required accepted=false integrated=false production_ready=false customer_accepted=false strong_block=true
```

### loop_document_gate_gfis_coverage

```text
loop_document_gate_gfis_coverage=pass status_related_direct_validators=34 gfis_guarded_direct_validators=34 gfis_status_ceiling=repair_required customer_accepted_guard=covered
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
  "review_boundary": [
    "GlobalCloud AAAS",
    "GlobalCloud KDS",
    "GlobalCloud PQC",
    "GlobalCloud SOP",
    "GlobalCloud SpaceAI Platform",
    "GlobalCloud WAE",
    "GlobalCoud GPCF"
  ],
  "observed_dirty": [
    "GlobalCloud AAAS",
    "GlobalCoud GPCF",
    "GlobalCloud KDS",
    "GlobalCloud SOP",
    "GlobalCloud PQC",
    "GlobalCloud SpaceAI Platform",
    "GlobalCloud WAE"
  ],
  "observed_ahead": [
    "GlobalCloud AAAS",
    "WAS世界资产体系",
    "GlobalCloud Studio",
    "GlobalCloud PVAOS",
    "GlobalCloud PQC",
    "GlobalCloud World",
    "GlobalCloud WAE"
  ],
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
    "wame_review": "0",
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
    "wame_review": "0",
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
  "current_project_count": 24,
  "historical_expected_project_count": 17,
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
    "wame_review": "0",
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
  "status": "pass",
  "checked_repo_count": 24,
  "dirty_repo_count": 7,
  "dirty_repos": [
    "GlobalCloud AAAS",
    "GlobalCoud GPCF",
    "GlobalCloud KDS",
    "GlobalCloud SOP",
    "GlobalCloud PQC",
    "GlobalCloud SpaceAI Platform",
    "GlobalCloud WAE"
  ],
  "observed_ahead": [
    "GlobalCloud AAAS",
    "WAS世界资产体系",
    "GlobalCloud Studio",
    "GlobalCloud PVAOS",
    "GlobalCloud PQC",
    "GlobalCloud World",
    "GlobalCloud WAE"
  ],
  "stable_dirty_repos": [
    "GlobalCloud AAAS",
    "GlobalCloud KDS",
    "GlobalCloud PQC",
    "GlobalCloud SOP",
    "GlobalCloud SpaceAI Platform",
    "GlobalCloud WAE",
    "GlobalCoud GPCF"
  ],
  "stable_ahead_repos": [
    "GlobalCloud AAAS",
    "GlobalCloud PQC",
    "GlobalCloud PVAOS",
    "GlobalCloud Studio",
    "GlobalCloud WAE",
    "GlobalCloud World",
    "WAS世界资产体系"
  ],
  "optional_volatile_dirty_repos": [
    "GlobalCoud GPCF"
  ],
  "review_boundary": [
    "GlobalCloud AAAS",
    "GlobalCloud KDS",
    "GlobalCloud PQC",
    "GlobalCloud SOP",
    "GlobalCloud SpaceAI Platform",
    "GlobalCloud WAE",
    "GlobalCoud GPCF"
  ],
  "live_dirty_counts": {
    "GlobalCloud AAAS": 7,
    "GlobalCloud Brain": 0,
    "WAS世界资产体系": 0,
    "GlobalCloud XiaoC": 0,
    "GlobalCloud WAME": 0,
    "GlobalCloud GPC": 0,
    "GlobalCloud Studio": 0,
    "GlobalCoud GPCF": 248,
    "GlobalCloud XWAIL": 0,
    "GlobalCloud GFIS": 0,
    "GlobalCloud MMC": 0,
    "GlobalCloud KDS": 52,
    "GlobalCloud XiaoG": 0,
    "GlobalCloud PVAOS": 0,
    "GlobalCloud SOP": 14,
    "GlobalCloud PKC": 0,
    "GlobalCloud XGD": 0,
    "GlobalCloud ICP": 0,
    "GlobalCloud PQC": 5,
    "GlobalCloud SpaceAI Platform": 2,
    "GlobalCloud SpaceAI Studio": 0,
    "GlobalCloud World": 0,
    "GlobalCloud Mem": 0,
    "GlobalCloud WAE": 91
  },
  "current_snapshot": "docs/harness/evidence/project_group_live_status_current.json",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
    "wame_review": "0",
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
docs_checked=1146
software_files_checked=240
findings=0
```

### delegated_project_chinese_localization

```text
delegated_project_localization=not_requested
```

### kds_token

```text
kds_token=pass fingerprint=bfd9553d
```
