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
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 文档健康报告

生成时间：2026-06-22T16:12:10.355400+00:00

Loop 文档门禁：`rework_required`

## 总览

- 仓库 Markdown：2662
- KDS 镜像 Markdown：2676
- KDS 本地镜像流水：2662
- KDS 本地镜像唯一文档：2662
- KDS API 同步流水：141
- 元数据缺失：0
- README 缺失目录：0
- 中文本地化债务：False
- 固定 doc_id 漂移：False
- 门禁原因：hard_failure:loop_engineering_five_direction, hard_failure:loop_engineering_master_plan, hard_failure:loop_capability_registry, hard_failure:loop_ui_quality_baseline

## 状态分布

- archive: 85
- controlled: 2406
- draft: 13
- okf_derived: 99
- operational_controlled: 54

## 项目分布

- Brain: 6
- GFIS: 83
- GPC: 40
- GPCF: 1566
- KDS: 737
- MMC: 8
- PKC: 6
- PVAOS: 7
- WAES: 149
- XGD: 6
- XiaoC: 42
- XiaoG: 7

## 命令结果

### loop_engineering_five_direction

```text
FAIL validate_loop_engineering_five_direction_implementation: autonomy policy missing standing adoption phrase: LOOP 运行控制闭环常驻接入规则
```

### loop_engineering_master_plan

```text
FAIL validate_loop_engineering_master_plan: loop README missing capability registry entry
```

### loop_capability_registry

```text
FAIL validate_loop_capability_registry: registry missing governance phrase: LOOP 能力注册表
```

### loop_ui_quality_baseline

```text
LOOP_CAPABILITY_REGISTRY.md must promote skill.globalcloud-ui-quality-gate to pilot
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
loop_session_registry=pass repo_recorded_loop_rounds=1092 orphan_session_family=0 live_codex_threads_covered=false auto_takeover_allowed=false GFIS_L4_repair_and_test_sync=296,KDS___DKS_governance=446,Ontology___WAS_governance=131,CodeGraph_governance=46,Agent-Reach_governance=49,Headroom___LCX_governance=50,OKF___ODF_governance=4,GPCF_CF___governance_rounds=47,XiaoG_evidence_repair=1,Project_group_phase_goals=1,LOOP_localization_governance=3,UI_governance_and_validation=13,Session_declaration_and_mainline=5
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
docs_checked=2330
software_files_checked=240
findings=0
```

### kds_token

```text
kds_token=pass fingerprint=bfd9553d
```
