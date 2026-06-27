---
doc_id: GPCF-LOOP-PROJECT-GROUP-GPCF-WORKTREE-REVIEW-PACKAGES-001
title: GPCF PROJECT GROUP GPCF WORKTREE REVIEW PACKAGES 001
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GPCF-WORKTREE-REVIEW-PACKAGES-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GPCF-WORKTREE-REVIEW-PACKAGES-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP GPCF WORKTREE REVIEW PACKAGES 001

## run

- 输入：项目群开发态任务队列中的 `P0-D：GPCF 大工作区 review 包拆分`。
- 执行：复跑 17 仓 Git gate，采样 GPCF dirty 路径族，将 GPCF 本仓剩余工作区拆成 7 个 review 包。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md` 和 validator `tools/kds-sync/validate_project_group_gpcf_worktree_review_packages_20260627.py`。

## stop

- stop_type：authorization_boundary。
- stop_evidence：GPCF 工作区只完成 review 包拆分，未 stage、commit、push；提交候选仍需下一轮人工授权或更细 review。
- 禁止动作：未提交、未推送、未部署、未生产写入、未 schema migrate、未删除文件、未升级 accepted/integrated/production_ready/customer_accepted。

## verify

- 17 仓 Git gate：`partial`。
- 16/17 仓 clean，唯一 dirty 仓为 `GlobalCoud GPCF`。
- missing/ahead/behind/sensitive 为空。
- 17/17 diff-check pass。
- GPCF review_package_count：7。

## recover

- 如果后续 GPCF 出现 sensitive path、behind upstream 或 diff-check failed，本包失效并回退到 hard blocker 修复。
- 如果文档控制同步后 `.kds` mirror 漂移，先跑 conflict guard，再只按 source 到 local mirror 的受控方向修复。
- 如果 Agent-Reach 专项包 validator 失败，不得把 Agent-Reach 包并入项目群 P0 提交候选。

## debug

- GPCF 当前 dirty 已从“不可执行大块”拆成 7 个 review 包：KDS mirror、mirror ledger、status registers、docs indexes、Agent-Reach evidence、Agent-Reach tooling/fixture、project-group P0 evidence。
- 本轮不把拆分等同于 review 完成；只降低下一步 stage/commit 前的不确定性。
