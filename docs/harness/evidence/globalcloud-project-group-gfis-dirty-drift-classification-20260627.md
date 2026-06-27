---
doc_id: GPCF-DOC-GFIS-DIRTY-DRIFT-CLASSIFICATION-20260627
title: GlobalCloud 项目群 GFIS Dirty 漂移分类证据 2026-06-27
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-gfis-dirty-drift-classification-20260627.md
source_path: docs/harness/evidence/globalcloud-project-group-gfis-dirty-drift-classification-20260627.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 GFIS Dirty 漂移分类证据 2026-06-27

## 目标

承接 `GPCF-RP7` review 结论中的堵点：17 仓 Git gate 从 only_dirty_repo=`GlobalCoud GPCF` 漂移为 dirty repos=`GlobalCoud GPCF`,`GlobalCloud GFIS`。

本轮只处理 `GlobalCloud GFIS` 的 51 项 dirty 漂移分类，不对 GFIS 仓库执行 stage、commit、push、stash、reset、checkout、clean、delete、deploy、生产写入、schema migrate、真实 API 写入或状态提升。

## 只读采样

在 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` 执行：

```text
git -c core.quotePath=false status --short --branch
git diff --check -- .
git diff --shortstat -- .
git diff --stat -- docs/harness/sop-e2e/evidence
git diff -U0 -- docs/harness/sop-e2e/evidence
git rev-parse --abbrev-ref HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

## 采样结果

| 项 | 结果 |
|---|---|
| gfis_branch | `main` |
| gfis_upstream | `origin/main` |
| gfis_dirty_file_count | `51` |
| gfis_untracked_file_count | `0` |
| gfis_diff_check | `pass` |
| gfis_shortstat | `51 files changed, 51 insertions(+), 51 deletions(-)` |
| gfis_dirty_path_prefix | `docs/harness/sop-e2e/evidence/` |
| gfis_dirty_file_type | `json` |
| gfis_changed_field_set | `generated_at` |
| gfis_changed_line_pattern | `timestamp_only` |

## 路径族分类

| 路径族 | 数量 | 定性 |
|---|---:|---|
| `source-*` | 39 | GFIS source-record / release / owner-response 相关 evidence 时间戳漂移 |
| `valid-*` | 4 | valid-source-record index / eligibility evidence 时间戳漂移 |
| `owner-*` | 3 | owner reminder dispatch evidence 时间戳漂移 |
| `runtime-*` | 2 | runtime primary-key evidence 时间戳漂移 |
| `gfis-runtime-*` | 2 | runtime dry-run / convergence queue evidence 时间戳漂移 |
| `kds-*` | 1 | KDS candidate source-record mapping evidence 时间戳漂移 |

## Diff 判读

51 个文件均为已跟踪 JSON evidence 文件，每个文件仅 1 行删除、1 行新增；变更字段均为 `generated_at`，示例形态：

```text
-  "generated_at": "2026-06-24T..."
+  "generated_at": "2026-06-27T..."
```

未观察到业务字段、schema 字段、runtime primary key、source-of-record 内容、owner 决策、release 状态、授权字段或真实 API 写入结果发生 diff。

## 结论

| 项 | 结论 |
|---|---|
| gfis_dirty_drift_classification | `timestamp_only_evidence_drift` |
| gfis_dirty_drift_review_result | `classified` |
| gfis_dirty_drift_hard_blocker | `false` |
| gfis_dirty_drift_stage_candidate | `false` |
| gfis_dirty_drift_commit_candidate | `false` |
| gfis_dirty_drift_push_candidate | `false` |
| gfis_runtime_write_detected | `false` |
| gfis_schema_migrate_detected | `false` |
| gfis_real_api_write_detected | `false` |
| gfis_status_promotion_detected | `false` |

本轮将 `GlobalCloud GFIS` 的 51 项 dirty 漂移处理为：已分类的 timestamp-only evidence drift。它不再作为未知漂移阻塞项，但项目群 Git gate 仍为 `partial`，因为 GFIS 工作区仍存在未提交变更。

## 后续边界

- 若目标是恢复 17 仓全量 clean，需要 GFIS owner 或用户另行授权 GFIS 仓内处理策略：保留并 review、提交候选、或恢复这些 timestamp-only evidence drift。
- 当前授权不允许在 GFIS 仓库执行任何 stage、commit、push、reset、checkout、clean 或删除。
- 当前结论不提升 GFIS、GPCF、WAES、KDS 或项目群状态。

## 状态声明

- gfis_dirty_drift_classification = timestamp_only_evidence_drift
- gfis_dirty_drift_review_result = classified
- gfis_dirty_file_count = 51
- gfis_untracked_file_count = 0
- gfis_diff_check = pass
- gfis_changed_field_set = generated_at
- gfis_dirty_drift_hard_blocker = false
- gfis_dirty_drift_stage_candidate = false
- gfis_dirty_drift_commit_candidate = false
- gfis_dirty_drift_push_candidate = false
- stage_allowed = false
- commit_allowed = false
- push_allowed = false
- delete_allowed = false
- deploy_allowed = false
- runtime_write_allowed = false
- schema_migrate_allowed = false
- real_api_write_allowed = false
- status_promotion_allowed = false
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
