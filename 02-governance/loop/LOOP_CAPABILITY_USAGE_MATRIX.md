---
doc_id: GPCF-DOC-2830FAF6E4
title: LOOP 能力使用矩阵
project: GPCF
related_projects: [GPCF, GFIS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CAPABILITY_USAGE_MATRIX.md
source_path: 02-governance/loop/LOOP_CAPABILITY_USAGE_MATRIX.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP 能力使用矩阵

本矩阵把 LOOP v1.1 的能力启用规则从“默认能力堆叠”收口为“任务界面驱动的按需启用”。工具、技能、方法只有在 `current_mainline`、`task_interface`、`risk_gate`、`autonomy_level` 和 `lifecycle` 同时允许时，才可进入当前任务切片。

## 能力选择公式

```text
EnabledCapabilities =
  RequiredByTaskInterface
  ∩ AllowedByLifecycle
  ∩ AllowedByRiskGate
  ∩ AllowedByAutonomyLevel
  ∩ NotForbiddenByTask
  ∩ NotForbiddenByCurrentGate
```

## 默认使用矩阵

```yaml
capability_usage_matrix:
  development_completion:
    default_skills:
      - globalcloud-loop-orchestrator
      - globalcloud-collaborative-dev
    default_methods:
      - Delivery Loop
      - controlled_multi_agent
      - local dry-run
      - controlled sample
    default_tools:
      - classify_git_risk.py
      - loop_document_gate.py
      - parse_loop_task_interface.py
      - build_loop_multi_agent_execution_plan.py
    forbidden_by_default:
      - kds_sync_apply.py
      - real_kds_api_write
      - real_external_api_write
      - schema_migrate
      - bench_migrate
      - commit
      - push
      - deploy
      - production_token_tools
      - automatic_status_promotion

  real_business_validation:
    allowed_tools:
      - gfis_real_fact_entry_guard.py
      - source_owner_confirmation_checker
      - agent_reach_limited_live_search_dry_run
    requires:
      - real_source_of_record
      - source_owner_confirmation
      - Governance Loop

  governance_audit:
    allowed_tools:
      - document_control.py
      - loop_document_gate.py
      - check_document_pollution.py
      - project_loop_maturity.py
      - build_loop_document_gate_repair_queue.py
    readonly_only:
      - parse_loop_task_interface.py
      - build_loop_multi_agent_execution_plan.py

  production_readiness:
    guarded_tools:
      - headroom_real_measurement
      - lcx_production_token_gate
      - waes_final_receipt_decision
    requires:
      - explicit_human_authorization
      - rollback_plan
      - production_window
```

## GFIS 当前主线能力界面

当前主线：

```text
GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001
```

当前任务界面由 `docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.md` 中的 `task_interface` 控制，当前能力启用结果如下。

### 白名单

```text
build_gfis_dev_completion_controlled_sample.py
run_gfis_runtime_sop_dev_completion_dry_run.py
validate_loop_v11_delivery_boundary.py
classify_git_risk.py
loop_document_gate.py
check_document_pollution.py
parse_loop_task_interface.py
build_loop_multi_agent_execution_plan.py
```

### 只读灰名单

```text
document_control.py
check_frontmatter_gate.py
project_loop_maturity.py
kds_readonly_probe.py
kds_conflict_guard.py
```

### 黑名单

```text
kds_sync_apply.py
real_kds_api_write
real_external_api_write
schema_migrate
bench_migrate
deploy
push
production_token_tools
headroom_real_measurement
agent_reach_live_closure
waes_final_receipt_decision
automatic_status_promotion
```

## 任务界面驱动约束

- 没有 `task_interface` 的任务，不得进入 `controlled_multi_agent`。
- `parse_loop_task_interface.py` 只负责读取、校验和暴露任务界面，不授予任何执行权限。
- `build_loop_multi_agent_execution_plan.py` 只负责根据任务界面生成阶段计划、文件锁计划和交接计划，不得替代 Orchestrator 的人工边界判断。
- `LOOP_CONTROL_BOARD.md`、`09-status/gpcf-project-status-matrix.md`、主 evidence 和 Governance Summary 仍只能由 Orchestrator 修改。

## 当前边界

```text
accepted=false
integrated=false
production_ready=false
customer_accepted=false
authorization_granted=false
stage_allowed=false
commit_allowed=false
push_allowed=false
```
