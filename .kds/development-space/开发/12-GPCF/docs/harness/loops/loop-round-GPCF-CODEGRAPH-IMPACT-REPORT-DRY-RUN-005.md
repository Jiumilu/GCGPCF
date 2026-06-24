---
doc_id: GPCF-DOC-B9144A4914
title: GPCF CodeGraph Impact Report Dry-run 005
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Impact Report Dry-run 005

## 输入

- 上一轮输出：`GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005`。
- 用户要求继续下一轮。
- 本轮只验证 CodeGraph impact report 对低风险治理变更的实际作用。

## 动作

- 选择 GPCF CodeGraph steady-state validator 作为低风险 dry-run 对象。
- 执行 `codegraph query` 定位目标文件与证据常量。
- 执行 `codegraph node` 读取目标 validator 和 indexed dependents。
- 执行 `codegraph affected` 选择受影响测试。
- 执行 `codegraph explore` 查找相邻 validator 模式。
- 执行宽泛 `codegraph impact main` 作为噪声负例。
- 与 `rg` 文本扫描基线对照。
- 生成 impact report evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-impact-report-dry-run-20260621.json`
- `docs/harness/evidence/codegraph-impact-report-dry-run-20260621.md`
- `tools/kds-sync/validate_codegraph_impact_report_dry_run.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_impact_report_dry_run.py`
- `python3 tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py`
- `python3 tools/kds-sync/validate_codegraph_project_group_full_coverage.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

CodeGraph dry-run 已把影响分析从文本匹配提升为符号、依赖、测试和噪声控制证据。当前结论为 `impact_report_dry_run_pass`，仍不进入业务开发、不提交、不推送、不部署、不升级 accepted/integrated/production_ready。下一轮进入 `GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006`，建立可持续的成本与质量指标基线。
