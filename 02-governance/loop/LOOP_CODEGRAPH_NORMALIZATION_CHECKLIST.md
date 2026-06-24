---
doc_id: GPCF-DOC-4C7D46A1B3
title: LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST
project: WAES
related_projects: [GFIS, GPC, WAES, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md
source_path: 02-governance/loop/LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST

## 已完成

- 14 仓 CodeGraph 全覆盖已建立。
- `.codegraph/` 已保持 Git 隔离。
- 开发前置分析字段已建立：`target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`expected_tests`。
- 测试选择约束已建立：`affected_tests`、`fallback_tests`、`fallback_reason`。
- 验收证据字段已建立：`codegraph_evidence`、`changed_files`、`test_selection_reason`、`post_change_status`。
- 影响度量基线已建立：`manual_scan_files`、`codegraph_candidate_files`、`actual_changed_files`、`affected_tests`、`missed_impact_count`、`time_to_first_target`。
- 返工趋势字段已建立：`rework_count=trend_down`。
- 项目群稳态监控已建立：`pass_with_watch`、`review_required`、`active drift watchlist`、`GFIS policy exception`。

## 常驻门禁

- 所有开发任务开工前强制执行 `codegraph query / node / affected`。
- 任务单必须固定写 `target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`。
- `affected_tests=[]` 时必须带 `fallback_tests` 和 `fallback_reason`。
- 缺少 `codegraph_evidence` 的任务，直接阻断进入实现。
- 每个业务变更的 evidence 固定包含 `codegraph_evidence`。
- 证据里必须有 `query`、`target_nodes`、`affected`、`changed_files`、`test_selection_reason`、`post_change_status`。
- 任务开工前先过 `CodeGraph 任务 Intake 门禁`，再进入实现。
- Harness / WAES 不把 CodeGraph 当参考材料，而是当验收输入之一。
- 每轮 Loop 都要看 14 仓 `codegraph status`。
- `.codegraph/` 始终保持 Git 隔离。
- 有 drift 先 watch，不直接 sync。
- `sync / reindex` 继续走授权边界。

## 还缺什么

- 把这些字段变成每个真实业务任务的默认必填项，而不是只存在于模板和样例证据里。
- 把 `docs/codegraph/codegraph-task-intake-gate.md` 变成每个任务的开工入口。
- 把 `codegraph query / node / affected` 变成真正的任务开工前门禁。
- 把 `codegraph_evidence` 变成 Harness / WAES evidence 的固定输入，而不是可选附录。
- 把 `manual_scan_files`、`time_to_first_target`、`missed_impact_count`、`rework_count` 变成每轮常规采集项。
- 把 Studio / GPCF 之类的 watchlist 漂移，继续维持在 monitor_only，不误判为已闭合。
- 把 CodeGraph 准入、pilot pack、Harness gate、impact metrics baseline 变成长期受控文档，并固定挂在目录入口。

## 下一轮

- 每个真实业务任务进入实现前，先采集 CodeGraph 影响分析。
- 每个任务的测试计划优先由 affected 结果驱动。
- 每个验收 evidence 固定附带 CodeGraph 证据块。
- 每轮 Loop 先看项目群稳态，再决定是否允许进入实现。

## 边界

- CodeGraph 不替代源码审查。
- CodeGraph 不替代测试、WAES、Harness 或人工验收。
- CodeGraph 不授权生产写入、外部 API 写入、commit、push 或 deploy。

## 验证

- `python3 tools/kds-sync/validate_codegraph_normalization_checklist.py`
- `python3 tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_admission.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_pilot_pack.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_harness_gate.py`
- `python3 tools/kds-sync/validate_codegraph_impact_metrics_baseline.py`
- `python3 tools/kds-sync/validate_codegraph_impact_report_dry_run.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_steady_state_monitor.py`
