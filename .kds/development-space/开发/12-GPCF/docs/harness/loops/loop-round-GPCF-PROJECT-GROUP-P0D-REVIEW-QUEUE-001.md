---
doc_id: GPCF-LOOP-PROJECT-GROUP-P0D-REVIEW-QUEUE-001
title: Loop Round GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001
project: GPCF
related_projects: [GPC, WAES, KDS, PKC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001

## run

- 输入：用户要求“下一步”，承接 P0-C。
- 范围：项目群开发态 review queue 拆分。
- 执行：
  1. 读取 P0-C 轮次和文档健康报告。
  2. 采样 GPCF、KDS、PKC、SOP、WAS、Studio 的 dirty 路径族。
  3. 建立 P0-D review queue。
  4. 生成 P0-D evidence、Loop round 和只读 validator。

## stop

| 字段 | 值 |
|---|---|
| stop_type | review_queue_ready |
| stop_reason | 开发态 dirty 已拆为 7 个 review queue；仍为 Git partial，不允许提交/推送/验收 |

## verify

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_p0d_review_queue_20260626.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/kds_conflict_guard.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1" --allow-non-pass-exit-zero
```

## recover

- 本轮只新增 P0-D evidence、Loop round 和 validator；恢复时删除这些新增文件并重跑文档控制。
- 本轮未删除 `.DS_Store`、未清理 `dist`、未清理 `output`、未提交、未推送、未部署。
- GPCF/KDS 本地镜像只作为 KDS 开发空间镜像，不声明真实 KDS API 已同步。

## debug

- 如果 Git gate blocked，优先检查 sensitive path、behind、diff-check failed。
- 如果 review queue 被误当成 accepted/integrated，需要回退为 `review_required`。
- PKC `dist`、SOP `output`、WAS `.DS_Store` 都需要显式 review，不在本轮自动处理。

## 输出

- `docs/harness/evidence/globalcloud-project-group-p0d-review-queue-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001.md`
- `tools/kds-sync/validate_project_group_p0d_review_queue_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | evidence_candidate |
| review_queue_count | 7 |
| 项目群 Git gate | partial |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
