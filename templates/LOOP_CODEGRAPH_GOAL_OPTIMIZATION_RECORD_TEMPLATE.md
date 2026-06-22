---
doc_id: GPCF-DOC-4C34AF960B
title: Loop CodeGraph Goal Optimization Record Template
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md
source_path: templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop CodeGraph Goal Optimization Record Template

用途：每个启用 CodeGraph 的 Loop 轮次，必须用本模板或等价字段记录目标优化过程。未启用 CodeGraph 时，也应记录 `codegraph_enabled=false` 和原因，防止把未使用工具写成效率提升。

## 1. 目标声明

| 字段 | 值 |
|---|---|
| target_id |  |
| target_source |  |
| target_success_criteria |  |
| target_non_scope |  |
| authorization_level | L0/L1/L2/L3/L3.5/L4/L5 |
| status_upgrade_requested | false |

## 2. CodeGraph 预检

| 字段 | 值 |
|---|---|
| codegraph_enabled | false |
| codegraph_cli_available | false |
| codegraph_scope_query |  |
| codegraph_tool_calls | 0 |
| codegraph_index_status | not_checked / available / stale / unavailable |
| fallback_reason |  |

## 3. 影响面收敛

| 字段 | 值 |
|---|---|
| impacted_symbols |  |
| impacted_files |  |
| impacted_routes_or_commands |  |
| risk_paths |  |
| manual_source_check | required |
| manual_source_check_result | pending |

## 4. 最小动作计划

| 字段 | 值 |
|---|---|
| planned_change_set |  |
| files_allowed_to_touch |  |
| files_not_allowed_to_touch |  |
| rollback_path |  |
| dirty_worktree_notes |  |

## 5. 验证选择

| 字段 | 值 |
|---|---|
| related_validators |  |
| related_tests |  |
| document_gates |  |
| expected_evidence |  |

## 6. 执行后度量

| 字段 | 值 |
|---|---|
| exploration_tool_calls_before | baseline_pending |
| exploration_tool_calls_after | pending |
| file_reads_before | baseline_pending |
| file_reads_after | pending |
| round_duration_before | baseline_pending |
| round_duration_after | pending |
| validator_first_pass | pending |
| wrong_scope_change_count | 0 |
| impact_miss_count | 0 |
| rework_count | 0 |
| scope_precision_result | pending |

## 7. 反馈沉淀

| 字段 | 值 |
|---|---|
| optimization_feedback |  |
| reusable_query_template |  |
| skill_or_checklist_update_candidate |  |
| next_round_constraint |  |

## 8. 非声明

- 本记录不证明业务完成。
- 本记录不替代源码复核、测试、文档门禁、KDS TOKEN 门禁、Harness/WAES 判定或人工确认。
- 本记录不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、推送或合并。
