---
doc_id: GPCF-DOC-7C6A2D0D31
title: CodeGraph 任务 Intake 门禁
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/codegraph/codegraph-task-intake-gate.md
source_path: docs/codegraph/codegraph-task-intake-gate.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 任务 Intake 门禁

这个门禁把 CodeGraph 前置分析变成任务开工前的硬条件。它的作用是阻断任务进入实现，而不是证明任务已经完成。

状态枚举：`blocked` / `ready` / `exception_recorded`。

## 固定顺序

```text
Task Intake
  -> codegraph query
  -> codegraph node
  -> codegraph affected
  -> target_nodes / affected_scope / files_allowed_to_change / files_not_to_touch
  -> expected_tests
  -> affected_tests / fallback_tests / fallback_reason
  -> codegraph_evidence
  -> Harness / WAES
```

## 必填字段

### 前置分析

- `query`
- `query_results`
- `target_nodes`
- `node_inspection`
- `affected`

### 实现约束

- `target_nodes`
- `affected_scope`
- `files_allowed_to_change`
- `files_not_to_touch`
- `expected_tests`

### 测试选择

- `affected_tests`
- `fallback_tests`
- `fallback_reason`

### 验收证据

- `codegraph_evidence`
- `query`
- `target_nodes`
- `affected`
- `changed_files`
- `test_selection_reason`
- `post_change_status`

### 效率指标

- `manual_scan_files`
- `codegraph_candidate_files`
- `actual_changed_files`
- `affected_tests`
- `missed_impact_count`
- `time_to_first_target`
- `review_rework_count`

## 阻断规则

- 缺少 `codegraph_evidence`，直接阻断进入实现。
- `affected_tests=[]` 且没有 `fallback_tests` 或 `fallback_reason`，直接阻断。
- `changed_files` 超出 `files_allowed_to_change`，直接阻断。
- `accepted`、`integrated` 或 `production_ready` 不能在这个门禁里被声明为 true。
- `production_write`、`external_api_write`、`git_commit`、`git_push`、`deploy` 不属于这个门禁的允许动作。

## 例外规则

只有在 CodeGraph CLI 不可用、仓库未初始化，或者图谱被独立 validator 判定不可用时，才允许记录 `codegraph_unavailable_exception`。

例外不能跳过测试，不能跳过 Harness / WAES，不能把任务升级为已完成。

## 与现有门禁的关系

- `docs/codegraph/codegraph-dev-execution-admission.md` 定义进入实现前必须具备什么。
- `docs/codegraph/codegraph-dev-execution-harness-gate.md` 定义 Harness/Loop 如何阻断缺失证据。
- 这个门禁把同一套字段前移到任务开工点。

## 非声明

- 本门禁不证明业务功能完成。
- 本门禁不证明 accepted、integrated 或 production_ready。
- 本门禁不授权生产写入、外部 API 写入、commit、push 或 deploy。
- 本门禁不替代源码复核、测试、WAES、Harness 或人工判断。
