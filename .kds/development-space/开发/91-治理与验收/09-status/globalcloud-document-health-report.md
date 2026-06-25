---
doc_id: GPCF-DOC-C436DDB0F6
title: GlobalCloud 文档健康报告
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
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

生成时间：2026-06-25T01:19:33.431403+00:00

Loop 文档门禁：`pass`

## 总览

- 仓库 Markdown：2809
- KDS 镜像 Markdown：2823
- KDS 本地镜像流水：2809
- KDS 本地镜像唯一文档：2809
- KDS API 同步流水：141
- 元数据缺失：0
- README 缺失目录：0
- 中文本地化债务：False
- 固定 doc_id 漂移：False
- 门禁原因：无

## 状态分布

- archive: 85
- controlled: 2553
- draft: 13
- okf_derived: 99

## 项目分布

- Brain: 11
- GFIS: 90
- GPC: 45
- GPCF: 1604
- KDS: 760
- MMC: 8
- PKC: 6
- PVAOS: 8
- WAES: 163
- XGD: 6
- XiaoC: 42
- XiaoG: 7

## 命令结果

### loop_engineering_five_direction

```text
loop_engineering_five_direction_implementation=pass run=implemented stop=implemented verify=implemented recover=implemented debug=implemented status_ceiling=partial_repair real_business_lane=repair_required runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_allowed=false integrated_allowed=false production_ready_allowed=false
```

### loop_engineering_master_plan

```text
loop_engineering_master_plan=pass baseline=v1.0 authority=master_implementation_plan roadmap=P0,P1,P2,P3,P4,P5 status_ceiling=repair_required accepted_allowed=false integrated_allowed=false runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0
```

### loop_capability_registry

```text
loop_capability_registry=pass pools=skill,tool,method statuses=fast_admitted,candidate,pilot,controlled,default_enabled,downgraded,disabled,deprecated,superseded default_enable=risk_tiered pilot_plus_evidence=required core_methods=CodeGraph,external_search,RAG,multi_agent_parallel capability_families=CodeGraph,Agent-Reach,Ontology,WAS,Headroom,OKF_ODF,LCX,WAES_KDS_RAG_writeback
```

### codegraph_loop_schema

```text
codegraph_loop_schema=pass templates=3 required_fields=38 automatic_status_upgrade=false karpathy_gate=enabled
```

### loop_ui_quality_baseline

```text
loop_ui_quality_baseline=pass template_ui_section=present master_spec=present capability_status=pilot explicit_ui_scope_rounds=22 explicit_ui_scope_valid=22 historical_ui_signal_rounds_without_explicit_scope=594 baseline_evidence=present
```

### loop_session_mainline_control

```text
loop_session_mainline_control=pass session_mainline=required handoff_evidence=required mainline_drift_detected=hard_pause write_without_handoff=false commit_push_deploy_status_promotion_allowed=false
```

### current_session_mainline_declaration

```text
current_session_mainline_declaration=pass session_mainline=session-mainline-control-rollout handoff_required=false mainline_drift_detected=false status_ceiling=partial accepted=false integrated=false production_ready=false
```

### loop_session_registry

```text
loop_session_registry=pass repo_recorded_loop_rounds=1135 orphan_session_family=0 live_codex_threads_covered=false auto_takeover_allowed=false GFIS_L4_repair_and_test_sync=296,KDS___DKS_governance=446,Ontology___WAS_governance=131,CodeGraph_governance=53,COGNEE_pilot___writeback=7,Agent-Reach_governance=49,Headroom___LCX_governance=68,OKF___ODF_governance=4,GPCF_CF___governance_rounds=47,XiaoG_evidence_repair=1,Project_group_phase_goals=1,LOOP_localization_governance=5,UI_governance_and_validation=22,Session_declaration_and_mainline=5
```

### session_mainline_preflight_enforcement

```text
session_mainline_preflight_enforcement=pass preflight_decision=continue_current_mainline_only mainline_drift_detected=false handoff_required=false authorization_required=false live_codex_threads_covered=false auto_takeover_allowed=false
```

### session_mainline_drift_watch

```text
session_mainline_drift_watch=pass watch_mode=repo_recorded_governance_only positive_fixtures=2 negative_fixtures=4 live_codex_threads_covered=false auto_takeover_allowed=false
```

### session_mainline_handoff_request_gate

```text
session_mainline_handoff_request_gate=pass gate_mode=explicit_user_confirmation_required proposal_only_for_other_sessions=true live_codex_threads_covered=false auto_takeover_allowed=false
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
docs_checked=828
software_files_checked=240
findings=0
```

### kds_token

```text
kds_token=pass fingerprint=bfd9553d
```

### project_group_gate_readiness

```text
project_group_gate_readiness=pass checked_repos=13 passed=13 failed=0 reasons=none
```
