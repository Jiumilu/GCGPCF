---
doc_id: GPCF-DOC-990EE0035A
title: CodeGraph 业务开发执行层准入规则
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/codegraph/codegraph-dev-execution-admission.md
source_path: docs/codegraph/codegraph-dev-execution-admission.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 业务开发执行层准入规则

本规则把 CodeGraph 从项目群代码图谱工具推进到业务开发执行层。它不代表业务变更完成，也不代表 WAES、Harness 或人工委员会已经验收；它只定义业务开发任务进入实现前必须具备的 CodeGraph 影响分析证据。

## 准入结论

任何项目群业务开发任务，在进入实现前必须先完成 CodeGraph 前置分析。没有这一步，任务不能进入实现。

必须执行并记录：

```bash
codegraph query "<功能/模块/接口关键词>" --json
codegraph node "<候选文件>"
codegraph affected "<候选文件>" --json
```

前置分析必须回答：

- 入口文件在哪里。
- 相关函数、组件、接口有哪些。
- 修改候选文件会影响哪些文件或测试。
- 是否存在跨项目依赖风险。

## 五层执行规则

### 1. 变更前影响定位

任务 intake 必须记录 `query`、`query_results`、`target_nodes`、`node_inspection` 和 `affected`。如果 CodeGraph 查询结果为空，仍需记录空结果，并说明人工 fallback 的原因。

### 2. 实现中改动范围约束

Loop 任务必须在进入实现前固化：

```text
target_nodes:
affected_scope:
files_allowed_to_change:
files_not_to_touch:
expected_tests:
```

`files_allowed_to_change` 是实现边界，不得把 CodeGraph 结果扩展为任意重构许可。`files_not_to_touch` 用于保护跨项目边界、治理文件和无关模块。

### 3. 测试选择

测试计划必须引用：

```bash
codegraph affected <changed-file> --json
```

如果 affected 结果包含测试或依赖，优先纳入 `affected_tests`。如果 affected 返回空，必须记录：

```text
affected_tests=[]
fallback_tests=<手动选择原因>
fallback_reason=<为什么 CodeGraph 结果不足以决定测试范围>
```

### 4. 验收证据

每个业务开发 evidence 必须增加：

```json
{
  "codegraph_evidence": {
    "query": "",
    "target_nodes": [],
    "affected": {},
    "changed_files": [],
    "test_selection_reason": "",
    "post_change_status": ""
  }
}
```

`post_change_status` 只能描述 CodeGraph 相关状态，例如 `synced`、`pending_resync`、`exception_recorded`，不得写成 `accepted`、`integrated` 或 `production_ready`。

### 5. 持续效率评估

每个任务必须记录以下指标，用于判断 CodeGraph 是否实际降低定位成本和漏测风险：

```text
manual_scan_files:
codegraph_candidate_files:
actual_changed_files:
affected_tests:
missed_impact_count:
time_to_first_target:
review_rework_count:
```

评估口径：

- `codegraph_candidate_files` 是否明显小于 `manual_scan_files`。
- `actual_changed_files` 是否落在 `files_allowed_to_change` 内。
- `affected_tests` 是否解释了测试选择。
- `missed_impact_count` 是否持续下降。
- `time_to_first_target` 是否持续下降。
- `review_rework_count` 是否持续下降。

## 例外规则

只有在 CodeGraph CLI 不可用、仓库未初始化或图谱状态被 validator 判定不可用时，才允许创建 `codegraph_unavailable_exception`：

```yaml
codegraph_unavailable_exception:
  reason:
  fallback_scan:
  reviewer:
  expires_at:
```

例外不能跳过测试，也不能把任务升级为已验收。例外任务必须进入下一轮 CodeGraph 修复或重放。

## 状态边界

- `dev_execution_admission=blocked`：缺少 CodeGraph 前置分析，且没有有效例外。
- `dev_execution_admission=ready`：准入证据完整，可以进入实现。
- `dev_execution_admission=exception_recorded`：存在受控例外，可以进入受限实现或等待修复。

本规则不授予生产写入权限，不创建外部 API 写入权限，不代表 accepted、integrated 或 production_ready。

## 下一轮输入

下一轮建议目标：`GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002`。

目标是在不做大规模业务开发的前提下，选择一个低风险业务变更候选，按本规则生成完整 CodeGraph 前置分析、实现边界、测试选择和验收 evidence 样例。
