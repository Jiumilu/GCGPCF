---
doc_id: GPCF-LOOP-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001
title: Loop Round GPCF-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001
project: GPCF
related_projects: [GPC, WAES, KDS, Brain, PKC, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001

## run

- 输入：用户要求“下一步”，承接 `P0-A dirty 分类`。
- 范围：Brain、MMC、KDS、PKC、Studio 的本地项目级验证复跑。
- 执行：
  1. 读取 Loop 控制面、自治边界、状态矩阵和文档健康报告。
  2. 复跑 Brain build、MMC runtime pytest、KDS API smoke、PKC build、Studio harness check。
  3. 生成 P0-B evidence、Loop round 和只读 validator。
  4. 同步 KDS 本地镜像并复跑文档/Git 门禁。

## stop

| 字段 | 值 |
|---|---|
| stop_type | development_validation_passed_with_dirty_gate_partial |
| stop_reason | 5 个项目级验证入口均通过；项目群 Git gate 仍 partial，阻断提交/推送/验收，不阻断继续开发 |

## verify

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_p0b_project_validation_20260626.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/kds_conflict_guard.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1" --allow-non-pass-exit-zero
```

## recover

- 本轮新增 P0-B evidence、Loop round 和 validator；恢复时删除这些新增文件并重跑文档控制。
- 构建/测试不触发提交、推送、部署、生产写入或 schema migrate。
- 若 PKC build artifact 后续被判定为派生物不入库，只能在 review queue 中处理，不在本轮删除。

## debug

- Brain/PKC 的 Node `DEP0205` 是 warning，未导致构建失败。
- PKC 的 npm `onlyBuiltDependencies` 是 warning，未导致构建失败。
- KDS smoke 只证明本地 API smoke 测试可运行，不代表真实 KDS API 写入。
- Studio `harness:check` 通过仍不等于 release workflow 执行或发布。

## 输出

- `docs/harness/evidence/globalcloud-project-group-p0b-project-validation-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0B-PROJECT-VALIDATION-001.md`
- `tools/kds-sync/validate_project_group_p0b_project_validation_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | evidence_candidate |
| 5 项项目级验证 | pass |
| 项目群 Git gate | partial |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
