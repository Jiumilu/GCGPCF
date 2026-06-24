---
doc_id: GPCF-DOC-A1E6C5C544
title: CodeGraph 业务开发执行层准入证据
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-dev-execution-admission-20260621.md
source_path: docs/harness/evidence/codegraph-dev-execution-admission-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 业务开发执行层准入证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001`。本轮只建立准入规则、模板和 validator，不进入任何业务项目内部开发。

## 准入状态

`dev_execution_admission_ready`

未来业务开发任务如果缺少 CodeGraph 前置分析，应判定为 `dev_execution_admission=blocked`，除非存在受控的 `codegraph_unavailable_exception`。

## 必跑命令

```bash
codegraph query "<功能/模块/接口关键词>" --json
codegraph node "<候选文件>"
codegraph affected "<候选文件>" --json
```

这些命令用于回答入口文件、相关函数/组件/接口、影响文件/测试、跨项目依赖风险。没有这一步，任务不能进入实现。

## 五层规则

- 变更前：记录 `query`、`target_nodes`、`node_inspection`、`affected`。
- 实现中：固化 `affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`expected_tests`。
- 测试选择：优先使用 `affected_tests`；为空时记录 `fallback_tests` 和 `fallback_reason`。
- 验收证据：必须包含 `codegraph_evidence`，字段为 `query`、`target_nodes`、`affected`、`changed_files`、`test_selection_reason`、`post_change_status`。
- 持续评估：记录 `manual_scan_files`、`codegraph_candidate_files`、`actual_changed_files`、`affected_tests`、`missed_impact_count`、`time_to_first_target`、`review_rework_count`。

## 模板

模板位置：`templates/CODEGRAPH_DEV_EXECUTION_EVIDENCE_TEMPLATE.json`

模板默认状态为 `draft`，且 `accepted`、`integrated`、`production_ready`、`production_write`、`external_api_write` 全部为 `false`。

## 边界

本证据不代表业务完成，不代表 WAES 通过，不代表 Harness 最终验收，不授予生产写入或外部 API 写入权限。

## 下一轮输入

`GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002`

下一轮应选择一个低风险业务变更候选，仅生成 CodeGraph 前置分析、改动边界、测试选择和验收 evidence 样例；是否进入业务实现需另行授权。
