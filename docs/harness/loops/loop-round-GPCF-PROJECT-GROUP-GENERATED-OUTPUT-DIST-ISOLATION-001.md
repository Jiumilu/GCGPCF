---
doc_id: GPCF-LOOP-PROJECT-GROUP-GENERATED-OUTPUT-DIST-ISOLATION-001
title: GPCF PROJECT GROUP GENERATED OUTPUT DIST ISOLATION 001
project: GPCF
related_projects: [GPC, WAES, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GENERATED-OUTPUT-DIST-ISOLATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GENERATED-OUTPUT-DIST-ISOLATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP GENERATED OUTPUT DIST ISOLATION 001

## run

- 输入：项目群开发态任务队列中的 `P0-C：SOP/PKC generated/output/dist 提交前隔离判断`。
- 执行：只读检查 SOP 与 PKC 的 Git 状态和 diff-check，并复跑项目群 17 仓 Git gate。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-generated-output-dist-isolation-20260627.md` 和 validator `tools/kds-sync/validate_project_group_generated_output_dist_isolation_20260627.py`。

## stop

- stop_type：authorization_boundary。
- stop_evidence：SOP/PKC 当前 clean，隔离对象归零；下一步涉及 GPCF 大工作区拆分和任何提交/推送均需继续保持显式边界。
- 禁止动作：未提交、未推送、未部署、未生产写入、未 schema migrate、未清理 generated/output/dist、未升级 accepted/integrated/production_ready/customer_accepted。

## verify

- `git -C GlobalCloud SOP status --short --branch`：clean。
- `git -C GlobalCloud PKC status --short --branch`：clean。
- `git -C GlobalCloud SOP diff --check -- .`：pass。
- `git -C GlobalCloud PKC diff --check -- .`：pass。
- `project_group_git_clean_gate.py --allow-non-pass-exit-zero`：`gate=partial`，16/17 仓 pass，唯一 dirty 仓为 GPCF，missing/ahead/behind/sensitive 为空，17/17 diff-check pass。

## recover

- 若 SOP 后续再次出现 `output/` 或 generated 类变更，必须先区分草案、模板、执行输出和生产指令，不得直接提交。
- 若 PKC 后续 build 重新生成 `dist/`，必须先确认当前 build 输出与源码版本一致，再决定提交或排除策略。
- 若 17 仓 gate 出现 sensitive、behind 或 diff-check failed，状态上限回退到 blocked/repair_required。

## debug

- 旧队列中的 SOP `output` 与 PKC `dist` 是 2026-06-26 快照；当前 2026-06-27 快照显示二者已经 clean。
- 当前项目群开发态剩余 Git 阻点收敛为 GPCF 本仓治理工作区，不再是 SOP/PKC generated/output/dist。
- 下一轮应进入 GPCF 大工作区 review 包拆分，而不是重复处理已归零的 SOP/PKC 隔离项。
