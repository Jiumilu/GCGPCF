---
doc_id: GPCF-DOC-CGNC20260623
title: CodeGraph 常态化归一清单证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-normalization-checklist-20260623.md
source_path: docs/harness/evidence/codegraph-normalization-checklist-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 常态化归一清单证据

本证据对应 `GPCF-CODEGRAPH-NORMALIZATION-CHECKLIST-001`。

## 结论

CodeGraph 常态化清单已固化为受控文档，并连接到现有项目群门禁、影响度量基线和稳态监控链。

当前状态为 `normalization_checklist_ready_with_watch`。

## 已覆盖的常态化要求

- 开工前 `query / node / affected`
- 任务单固定字段
- `affected_tests=[]` fallback 约束
- `codegraph_evidence` 固定入验收
- `manual_scan_files`、`codegraph_candidate_files`、`actual_changed_files`、`affected_tests`、`missed_impact_count`、`time_to_first_target`、`review_rework_count`
- 14 仓稳态监控
- `.codegraph/` Git 隔离
- drift watch，不直接 sync
- 准入、pilot pack、Harness gate、impact metrics baseline 常设

## 当前状态

| 项 | 值 |
| --- | --- |
| repo_count | 14 |
| all_repo_codegraph_initialized | true |
| all_codegraph_git_isolated | true |
| codegraph_reindex_recommended | false |
| watchlist_mode | monitor_only |
| watchlist_repos | Studio |
| gpcf_pending | 0 |
| studio_pending | 18 |

## 下一轮

`GPCF-CODEGRAPH-NORMALIZATION-WATCH-002`
