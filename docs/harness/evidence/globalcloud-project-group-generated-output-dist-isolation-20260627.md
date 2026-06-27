---
doc_id: GPCF-DOC-GENERATED-OUTPUT-DIST-ISOLATION-20260627
title: GlobalCloud 项目群 SOP/PKC generated-output-dist 提交前隔离重放判定
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-generated-output-dist-isolation-20260627.md
source_path: docs/harness/evidence/globalcloud-project-group-generated-output-dist-isolation-20260627.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 SOP/PKC generated-output-dist 提交前隔离重放判定

## 授权边界

- 输入：承接项目群开发态 P0 队列，执行 `P0-C：SOP/PKC generated/output/dist 提交前隔离判断`。
- 范围：只判断 `GlobalCloud SOP` 与 `GlobalCloud PKC` 当前是否仍存在 generated/output/dist 类提交候选。
- 允许动作：只读 Git 状态、只读 diff-check、生成本地 evidence、生成只读 validator、更新 GPCF 队列文档。
- 禁止动作：删除、清理、提交、推送、部署、生产写入、schema migrate、真实外部 API 写入、触发 PKC build 重新生成 `dist`、把 SOP `output` 写成生产指令、标记 accepted/integrated/production_ready/customer_accepted。
- 判定边界：本轮按 2026-06-28 当前工作树重新重放 SOP/PKC generated/output/dist 隔离状态，只说明当前是否仍有待隔离对象，不证明历史构建产物策略已永久关闭，也不证明项目群 Git 全量 clean。

## 当前只读快照（2026-06-28 重放）

| 项目 | branch/upstream | git status | diff-check | generated/output/dist 隔离判定 |
|---|---|---|---|---|
| GlobalCloud SOP | `main...origin/main` | dirty | pass | `output/.DS_Store` 仍为 dirty candidate，且另有 `tools/` 未跟踪目录；当前不能登记为“无 generated/output/dist 候选” |
| GlobalCloud PKC | `codex/pkc-l4-task-notification...origin/codex/pkc-l4-task-notification` | clean | pass | `dist/` 当前无 dirty/untracked 提交候选；本轮未触发 build，避免重新生成产物 |

## 17 仓 Git Gate 快照

本轮运行：

```bash
python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --allow-non-pass-exit-zero
```

结果摘要：

| 字段 | 结果 |
|---|---|
| checked_repo_count | 17 |
| gate | blocked |
| pass repos | 10 |
| dirty repos | GlobalCloud AAAS、WAS世界资产体系、GlobalCoud GPCF、GlobalCloud XWAIL、GlobalCloud GFIS、GlobalCloud KDS、GlobalCloud SOP |
| sensitive repos | GlobalCloud KDS(`.env.production.example`) |
| missing/ahead/behind | none |
| diff-check | 17/17 pass |

当前 Git gate 已不是旧的 “only GPCF dirty / partial” 快照，而是 7 仓 dirty + KDS sensitive_path 的 `blocked` 基线。其中 SOP 还新增了 `output/.DS_Store` dirty candidate，因此本证据必须降级为 recheck/rework 结论。

## 隔离决策

| 决策项 | 判定 |
|---|---|
| SOP `output/` 是否需要本轮隔离 | recheck_required |
| SOP `generated/` 是否需要本轮隔离 | no_current_candidate |
| PKC `dist/` 是否需要本轮隔离 | no_current_candidate |
| 是否删除或清理任何文件 | false |
| 是否触发 build 重新生成产物 | false |
| 是否进入提交候选 | false |

## 下一轮建议

1. P0-C-recheck：先确认 `GlobalCloud SOP/output/.DS_Store` 是否沿 noise cleanup、忽略规则或 review 边界单独治理，不得直接删除。
2. P0-D：继续把 GPCF 当前大工作区变更维持在 review 包边界中，但不得再写成“唯一 dirty 仓”。
3. P0-E：复跑 17 仓 Git gate，目标先收口为“7 仓真实基线受控”，再讨论是否能从 `blocked` 收敛。
4. 提交/推送仍需单独授权；本轮不做。

## 状态声明

- generated_output_dist_isolation = recheck_required
- sop_generated_output_dist_candidates = 1
- pkc_generated_output_dist_candidates = 0
- sop_status_clean = false
- pkc_status_clean = true
- project_group_git_gate = blocked
- dirty_repo_count = 7
- dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP
- sensitive_repos = GlobalCloud KDS(.env.production.example)
- development_start_allowed = true
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
