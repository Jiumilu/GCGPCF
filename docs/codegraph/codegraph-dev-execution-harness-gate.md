---
doc_id: GPCF-DOC-E1D4339FD6
title: CodeGraph 业务开发执行 Harness 门禁
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/codegraph/codegraph-dev-execution-harness-gate.md
source_path: docs/codegraph/codegraph-dev-execution-harness-gate.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 业务开发执行 Harness 门禁

本门禁把 `GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001` 和 `GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002` 固化为 Harness/Loop 阻断规则。它只检查业务开发任务是否具备 CodeGraph 影响分析证据，不代表业务完成、WAES 通过、Harness 最终验收或人工批准。

## 门禁目标

未来任何业务开发 evidence 进入实现或验收前，必须具备：

- `pre_change_analysis`
- `implementation_constraints`
- `test_selection`
- `codegraph_evidence`
- `efficiency_metrics`
- `status_boundaries`

缺少任一核心字段时，Harness/Loop 应返回：

```text
codegraph_dev_execution_harness_gate=blocked
```

## 必填字段

`pre_change_analysis` 必须包含：

```text
query
target_nodes
affected
```

`implementation_constraints` 必须包含：

```text
target_nodes
affected_scope
files_allowed_to_change
files_not_to_touch
expected_tests
```

`test_selection` 必须包含：

```text
affected_tests
fallback_tests
fallback_reason
```

`codegraph_evidence` 必须包含：

```text
query
target_nodes
affected
changed_files
test_selection_reason
post_change_status
```

`efficiency_metrics` 必须包含：

```text
manual_scan_files
codegraph_candidate_files
actual_changed_files
affected_tests
missed_impact_count
time_to_first_target
review_rework_count
```

## 阻断规则

- 缺少 `codegraph_evidence`：blocked。
- 缺少 `target_nodes`：blocked。
- 缺少 `affected_scope`：blocked。
- `affected.affectedTests=[]` 且 `fallback_reason` 为空：blocked。
- `changed_files` 超出 `files_allowed_to_change`：blocked。
- `status_boundaries.accepted=true`、`integrated=true` 或 `production_ready=true`：blocked。
- 出现 `production_write=true` 或 `external_api_write=true`：blocked。
- 证据声明 CodeGraph 替代 WAES/Harness/人工验收裁决：blocked。

## 允许状态

本门禁只允许输出：

- `pass`
- `blocked`
- `exception_recorded`

其中 `exception_recorded` 必须附带 `codegraph_unavailable_exception`，并登记 `reason`、`fallback_scan`、`reviewer`、`expires_at`。

## 下一轮输入

`GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004`

下一轮可以选择一个低风险真实业务开发候选，但只有在用户明确授权进入业务实现时才可修改业务代码；否则只能生成候选任务的 CodeGraph 前置分析和 Harness gate dry-run。
