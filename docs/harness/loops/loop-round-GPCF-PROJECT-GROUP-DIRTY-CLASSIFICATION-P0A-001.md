---
doc_id: GPCF-LOOP-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001
title: Loop Round GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001

## run

- 输入：用户要求“下一步”，承接项目群开发态 P0 阻点消减。
- 范围：17 仓 dirty 分类；不提交、不推送、不部署、不生产写入、不 schema migrate、不状态提升。
- 执行：
  1. 重跑 17 仓 Git gate，确认 remaining blocker 为普通 dirty/untracked。
  2. 采集每仓 `git status --porcelain=v1` 文件族，区分方案传导、工程变更、治理 evidence、KDS mirror、知识导入、本地产物。
  3. 生成 P0-A dirty 分类证据和只读 validator。
  4. 通过文档控制 scoped 同步把 evidence 和 Loop round 纳入 KDS 开发空间本地镜像。

## stop

| 字段 | 值 |
|---|---|
| stop_type | development_dirty_classified |
| stop_reason | 17 仓 dirty 已分类为开发态处理队列；剩余阻点不阻断正常开发启动，但继续阻断提交、推送、验收和状态提升 |

## verify

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_dirty_classification_p0a_20260626.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/kds_conflict_guard.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/check_document_pollution.py
```

## recover

- 本轮只新增 P0-A evidence、Loop round 和 validator；恢复时删除这些新增文件并重跑 scoped 文档控制。
- 本轮未提交、未推送、未部署、未生产写入、未 schema migrate。
- 本轮未修改业务 schema、生产配置或真实外部系统。

## debug

- 如果 17 仓 Git gate 从 partial 回到 blocked，优先检查 `sensitive_paths`、`diff_check`、`behind_repos`。
- 如果 KDS conflict guard blocked，优先重跑 scoped `document_control.py`，确认 source 与 `.kds/development-space` 镜像哈希一致。
- 如果某项目 dirty 变为 clean，不视为失败；P0-A 分类证据仍保留为当轮开发态审计记录。

## 输出

- `docs/harness/evidence/globalcloud-project-group-dirty-classification-p0a-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001.md`
- `tools/kds-sync/validate_project_group_dirty_classification_p0a_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | evidence_candidate |
| 开发态是否可推进 | yes |
| 项目群 Git gate | partial |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
