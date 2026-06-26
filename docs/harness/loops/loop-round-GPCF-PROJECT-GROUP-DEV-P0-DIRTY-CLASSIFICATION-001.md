---
doc_id: GPCF-LOOP-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001
title: Loop Round GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001
project: GPCF
related_projects: [GPC, WAES, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001

## run

- 输入：用户要求继续下一步，目标是在项目群全项目开发态启动前消减剩余阻点。
- 范围：GlobalCloud 项目群 17 仓 dirty/untracked 分类。
- 执行：
  1. 读取 Loop 控制板、自治策略、项目状态矩阵、文档健康报告和文档台账。
  2. 运行 17 仓 Git clean gate，确认当前 gate 为 partial，且无 missing、ahead、behind、sensitive path 或 diff-check failed。
  3. 逐仓只读扫描 `git status --porcelain=v1` 和 `git diff --check -- .`。
  4. 将 dirty/untracked 按 governance_doc、evidence_or_fixture、harness_tooling、kds_mirror_or_wiki、test、config_or_workflow、generated_or_cache、other 分类。
  5. 生成 P0-A dirty 分类 evidence 和 validator。

## stop

| 字段 | 值 |
|---|---|
| stop_type | development_gate_classified |
| stop_reason | 17 仓 dirty/untracked 已拆为开发态任务类别；剩余阻点限制提交/推送/验收，不阻断开发态启动 |

## verify

本轮验证命令：

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_dev_p0_dirty_classification_20260626.py
```

验证标准：

- 17 仓存在且可检查。
- `missing_repos=[]`、`ahead_repos=[]`、`behind_repos=[]`、`sensitive_repos=[]`。
- `diff_check=17/17 pass`。
- evidence 包含 17 仓分类动作和明确状态边界。
- `accepted=false`、`integrated=false`、`production_ready=false`、`customer_accepted=false`。

## recover

- 本轮只新增 GPCF 侧 evidence、Loop round 和 validator。
- 可恢复点：删除本轮 3 个新增文件并复跑 validator。
- 本轮未提交、未推送、未部署、未生产写入、未 schema migrate。

## debug

- WAES 授权仍是验收/发布/状态提升边界，但不再是本轮开发态唯一硬阻点。
- GPC 触及测试文件，需要项目级测试闭环。
- SOP/PKC 含 generated/output/dist 类路径，提交前必须隔离或 owner 明确确认。
- GPCF 工作区规模大，必须按路径族拆分提交候选，禁止整包处理。

## 输出

- `docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001.md`
- `tools/kds-sync/validate_project_group_dev_p0_dirty_classification_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| dirty_classification_ready | true |
| 开发态是否可推进 | yes |
| 项目群 Git gate | partial |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
