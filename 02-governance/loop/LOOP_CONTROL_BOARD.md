---
doc_id: GPCF-DOC-0DF6AA8647
title: LOOP Control Board
project: WAES
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CONTROL_BOARD.md
source_path: 02-governance/loop/LOOP_CONTROL_BOARD.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP Control Board

## Current Standing Control

LOOP 运行控制闭环常驻能力 = active / all Loop work.

后续所有非只读 Loop 工作必须按 `run / stop / verify / recover / debug` 记录。未登记运行控制闭环的轮次不得升级 accepted/integrated/production_ready。

当前状态边界：

```text
GPCF-PROJECT-STATUS-MATRIX-17-SCOPE-001
validate_gpcf_project_status_matrix_17_project_scope.py
ready_for_review=12
partial_verified=1
repair_required=3
owner_review_required=1
project_group_git_gate = partial
current_live_dirty_repos = GlobalCoud GPCF, GlobalCloud GFIS, GlobalCloud SOP
current_live_sensitive_repos = none
current_live_kds_blocker = resolved_not_in_git_status
current_live_kds_status = clean / ahead=0 / behind=0 / diff_check=pass
development_queue_ready = true
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
real_business_lane=repair_required
development_lane=continue_allowed
real_business_validation_lane=pending_source_of_record
real_source_records_zero_is_not_dev_blocker=true
runtime_primary_key_ready=0
review_queue=0
runtime_intake=0
waes_review=0
verified=0
authorization_granted = false
action_executed = false
stage_allowed = false
commit_allowed = false
push_allowed = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## Standing Decision: Development vs Real Business Validation

```yaml
decision:
  id: GLOBALCLOUD-DEV-VS-REAL-BUSINESS-VALIDATION-SEPARATION
  conclusion: real_source_records_zero_is_not_development_blocker
  principle: 真实业务输入是验收门，不是开发门
  applies_to:
    - GFIS
    - GPCF
    - KDS
    - WAES
    - all_project_group
  development_lane:
    status: continue_allowed
    allowed:
      - local_development
      - fixture_e2e
      - controlled_sample_e2e
      - dry_run
      - contract_validator
      - runtime_intake_development
      - review_queue_development
      - waes_review_candidate_development
      - verified_artifact_candidate_development
      - development_ready_for_real_business_validation
  real_business_validation_lane:
    status: pending_source_of_record
    blocked_until:
      - real_source_record
      - source_owner_confirmation
      - real_runtime_intake
      - real_review_queue
      - real_waes_review
      - real_verified_artifact_candidate
  forbidden_claims:
    - real_business_verified
    - accepted
    - integrated
    - production_ready
    - customer_accepted
```

控制面引用：

- `globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `globalcloud-project-group-dev-task-queue-20260626.md`
- `02-governance/loop/LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md`
- `registry/project-state-matrix.yaml`

项目词表锚点：XWAIL / AaaS / AAAS / SOP / WAES / GPC / GFIS / KDS / GPCF。

历史口径说明：`dirty_repo_count = 7` 只作为 2026-06-26/2026-06-27 replay 口径保留；当前 live 判断以三仓 dirty 和 KDS blocker 已解除为准，不得恢复 KDS sensitive_path blocked。

## GFIS Development Blocker Reclassification

```yaml
decision:
  id: LOOP-GFIS-DEV-BLOCKER-RECLASSIFICATION
  conclusion: real_source_records_zero_is_not_dev_blocker
  reason: 真实业务 source-of-record 是真实业务验证和验收条件，不是 GFIS 开发完成前置条件。

gfis_state:
  previous:
    development_lane: blocked_by_real_source_missing
  updated:
    development_lane: continue_allowed
    real_business_validation_lane: pending_source_of_record
    progress_policy: may_continue_to_development_ready_for_real_business_validation

still_forbidden:
  - real_business_verified
  - accepted
  - integrated
  - production_ready
  - customer_accepted
  - production_write
  - real_external_api_write
  - schema_migrate_without_authorization
  - commit_push_deploy_without_authorization
```

本裁决不改变 GFIS 真实业务链路门禁：`real_business_lane=repair_required`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0` 仍阻断真实业务验证、状态提升和客户验收。
