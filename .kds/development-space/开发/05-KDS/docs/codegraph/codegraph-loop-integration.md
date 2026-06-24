---
doc_id: GPCF-DOC-F7ADE9DF11
title: CodeGraph Loop 集成规范
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-loop-integration.md
source_path: docs/codegraph/codegraph-loop-integration.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Loop 集成规范

Loop 任务必须把 CodeGraph 结果从临时上下文提升为 evidence。

## 标准流程

```text
Task Intake
  -> Task Intake Gate
  -> CodeGraph Context
  -> Impact Analysis
  -> Patch Plan
  -> Implementation
  -> Test Mapping
  -> Evidence Capture
  -> WAES Gate
  -> KDS / OKF Candidate Record
  -> Loop Feedback
```

## Loop evidence 字段

```yaml
karpathy:
  assumptions:
  tradeoff_options:
  simpler_path:
  minimal_scope:
  acceptance_criteria:
  execution_plan:
    steps:
      - step:
        verify:
  assumptions_log:
    clarifying_questions:
      - "<清单>"
    resolved_before_run: false
codegraph:
  required: true
  snapshot_id:
  context_queries:
  explored_symbols:
  impact_paths:
  impacted_tests:
  risk_flags:
  evidence_ref:
task_intake:
  query:
  query_results:
  target_nodes:
  node_inspection:
  affected:
  affected_scope:
  files_allowed_to_change:
  files_not_to_touch:
  expected_tests:
  affected_tests:
  fallback_tests:
  fallback_reason:
  codegraph_evidence:
  efficiency_metrics:
    manual_scan_files:
    codegraph_candidate_files:
    actual_changed_files:
    affected_tests:
    missed_impact_count:
    time_to_first_target:
    review_rework_count:
```

Task Intake 的默认硬门禁是：先做 `codegraph query / node / affected`，再固化 `target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`expected_tests`，测试选择必须带 `affected_tests` 或 `fallback_reason`，验收证据必须包含 `codegraph_evidence`。

Harness / WAES 不把 CodeGraph 当参考材料，而是把它当作验收输入之一。

## Karpathy 行为门禁（Loop 真实运行）

在 Task Intake / Planning 阶段，必须明确提交以下条目，否则任务不进入 `Implementation`：

- `assumptions`：不确定项、假设边界、排除范围。
- `tradeoff_options`：至少两个可行解释/路径（含推荐项与取舍理由）。
- `simpler_path`：本轮是否有更简单实现；有则给出。
- `minimal_scope`：本轮最小改动边界，禁止超范围 touch 。
- `acceptance_criteria`：可复核验收清单，需对应 `verify` 步骤。
- `clarifying_questions`：在实现前必须已回答的澄清问题。
- `resolved_before_run`：若存在不确定，须为 `true` 并在 run 前补齐。

Review 阶段需要给出 `karpathy_gate` 字段中：

- assumptions 是否完整披露；
- 是否给出替代路径与 tradeoff；
- 是否确认非侵入性最小改动；
- 孤悬清理是否完成；
- 每条验收标准是否有证据映射（脚本输出、日志、diff、测试）。

## 阶段边界

- intake：仓库概览、符号检索、架构上下文。
- intake gate：任务必须先具备 `query`、`target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`affected_tests` / `fallback_reason` 和 `codegraph_evidence`。
- planning：影响分析、依赖追踪、风险区域识别。
- implementation：符号探索、调用链追踪、相关文件定位。
- validation：影响测试、覆盖映射、架构规则检查。
- evidence：快照、查询日志、受影响符号、变更路径。
- closure：文档候选、KDS candidate。

Loop 不得把 CodeGraph 结果直接升级成 accepted、integrated 或 production_ready。
