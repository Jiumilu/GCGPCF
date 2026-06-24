---
doc_id: GPCF-DOC-2AF01CCB7C
title: CodeGraph 任务 Intake 门禁证据
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-task-intake-gate-20260623.md
source_path: docs/harness/evidence/codegraph-task-intake-gate-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 任务 Intake 门禁证据

## 证据 ID

`CODEGRAPH-TASK-INTAKE-GATE-20260623`

## 结论

任务 Intake 门禁已建立，并通过正负例 dry-run。
status: task_intake_gate_ready
positive_fixture=pass
negative_missing_codegraph_evidence=blocked
negative_empty_affected_tests_no_fallback=blocked
negative_missing_expected_tests=blocked

## 门禁输入

- `docs/codegraph/codegraph-task-intake-gate.md`
- `tools/kds-sync/validate_codegraph_task_intake_gate.py`
- `fixtures/codegraph/task-intake-gate/positive-task-intake.json`
- `fixtures/codegraph/task-intake-gate/negative-missing-codegraph-evidence.json`
- `fixtures/codegraph/task-intake-gate/negative-empty-affected-tests-no-fallback.json`
- `fixtures/codegraph/task-intake-gate/negative-missing-expected-tests.json`

## 固定字段

- 前置分析：`query`、`query_results`、`target_nodes`、`node_inspection`、`affected`
- 实现约束：`target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`expected_tests`
- 测试选择：`affected_tests`、`fallback_tests`、`fallback_reason`
- 验收证据：`codegraph_evidence`、`query`、`target_nodes`、`affected`、`changed_files`、`test_selection_reason`、`post_change_status`
- 效率指标：`manual_scan_files`、`codegraph_candidate_files`、`actual_changed_files`、`affected_tests`、`missed_impact_count`、`time_to_first_target`、`review_rework_count`

## 阻断结果

- 缺少 `codegraph_evidence` 时阻断。
- `affected_tests=[]` 且缺少 `fallback_reason` 时阻断。
- `changed_files` 超出 `files_allowed_to_change` 时阻断。
- `accepted`、`integrated`、`production_ready`、`production_write`、`external_api_write` 保持 false。

## 非声明

- 本证据不证明业务功能完成。
- 本证据不证明 accepted、integrated 或 production_ready。
- 本证据不授权生产写入、外部 API 写入、commit、push 或 deploy。
