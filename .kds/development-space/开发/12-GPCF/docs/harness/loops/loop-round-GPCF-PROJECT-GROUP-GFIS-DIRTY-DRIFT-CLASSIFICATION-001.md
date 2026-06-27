---
doc_id: GPCF-LOOP-PROJECT-GROUP-GFIS-DIRTY-DRIFT-CLASSIFICATION-001
title: GPCF PROJECT GROUP GFIS DIRTY DRIFT CLASSIFICATION 001
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GFIS-DIRTY-DRIFT-CLASSIFICATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GFIS-DIRTY-DRIFT-CLASSIFICATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP GFIS DIRTY DRIFT CLASSIFICATION 001

## run

- 输入：继续处理 `GPCF-RP7` 的前置堵点，先处理或授权审查 `GlobalCloud GFIS` 的 51 项 dirty 漂移。
- 执行：只读采样 GFIS Git 状态、diff-check、shortstat、diff 内容和路径族分布。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-gfis-dirty-drift-classification-20260627.md` 和 validator `tools/kds-sync/validate_project_group_gfis_dirty_drift_classification_20260627.py`。

## stop

- stop_type：authorization_boundary。
- stop_evidence：GFIS 51 项 dirty 已分类为 timestamp-only evidence drift，但未获得 GFIS 仓内 stage/commit/push/reset/checkout/clean/delete 授权。
- 禁止动作：未修改 GFIS 仓库、未 stage、未 commit、未 push、未删除文件、未 deploy、未生产写入、未 schema migrate、未真实 API 写入、未状态提升。

## verify

- GFIS dirty drift classification validator：必须 pass。
- GFIS `git diff --check -- .`：必须 pass。
- GFIS dirty 文件：必须为 51 个已跟踪 JSON evidence 文件。
- GFIS diff 内容：必须只包含 `generated_at` 时间戳变更。

## recover

- 若 GFIS dirty 文件数、路径、字段或 diff-check 发生变化，重新分类，不沿用本轮 timestamp-only 结论。
- 若用户授权 GFIS 提交候选或恢复策略，先重新运行 GFIS validator 和 17 仓 Git gate。
- 若出现 sensitive、behind、diff-check failed 或非 evidence 业务字段变化，立即停止并标记 blocked。

## debug

- 本轮消除了 GFIS dirty 的未知性，但没有让项目群 Git gate 变为 pass。
- 17 仓 Git gate 仍为 partial，直到 GPCF 与 GFIS 工作区均按授权收口。
