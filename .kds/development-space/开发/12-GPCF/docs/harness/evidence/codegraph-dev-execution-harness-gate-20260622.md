---
doc_id: GPCF-DOC-D2709494C0
title: CodeGraph 业务开发执行 Harness 门禁证据
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph 业务开发执行 Harness 门禁证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003`。本轮只建立 Harness/Loop 阻断链，不进入业务实现。

## 接入内容

Harness/Loop gate 必须检查未来业务开发 evidence 是否包含：

- `pre_change_analysis`
- `implementation_constraints`
- `test_selection`
- `codegraph_evidence`
- `efficiency_metrics`
- `status_boundaries`

## 阻断规则

- 缺少 `codegraph_evidence`：blocked。
- 缺少 `target_nodes`：blocked。
- 缺少 `affected_scope`：blocked。
- `affected.affectedTests=[]` 且 `fallback_reason` 为空：blocked。
- `changed_files` 超出 `files_allowed_to_change`：blocked。
- `accepted`、`integrated`、`production_ready` 为 true：blocked。
- `production_write` 或 `external_api_write` 为 true：blocked。
- 声明 CodeGraph 替代 WAES/Harness/人工验收裁决：blocked。

## Dry-run 结果

```text
positive_fixture=pass
negative_fixture=blocked
negative_block_reason=empty_affected_tests_without_fallback_reason
```

## 边界

本轮不代表业务完成，不代表 WAES 通过，不代表 Harness 最终验收，不执行提交、推送、部署、生产写入或外部 API 写入。

## 下一轮输入

`GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004`

下一轮可以选择一个低风险真实业务开发候选；只有用户明确授权进入业务实现时，才可修改业务代码。否则只能生成候选任务的 CodeGraph 前置分析和 Harness gate dry-run。
