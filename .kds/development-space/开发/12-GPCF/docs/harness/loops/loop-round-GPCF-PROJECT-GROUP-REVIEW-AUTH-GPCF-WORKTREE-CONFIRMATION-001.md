---
doc_id: GPCF-LOOP-PROJECT-GROUP-REVIEW-AUTH-GPCF-WORKTREE-CONFIRMATION-001
title: GPCF PROJECT GROUP REVIEW AUTH GPCF WORKTREE CONFIRMATION 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-WORKTREE-CONFIRMATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-WORKTREE-CONFIRMATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP REVIEW AUTH GPCF WORKTREE CONFIRMATION 001

## run

- 输入：用户要求“下一步”，承接 `REVIEW-AUTH-GPCF-WORKTREE-20260627`。
- 执行：将 GPCF 7 个 review 包转为逐项人工确认请求，并列出每包执行前必须复核的 validator。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-worktree-confirmation-20260627.md` 和 validator `tools/kds-sync/validate_project_group_review_auth_gpcf_worktree_confirmation_20260627.py`。

## stop

- stop_type：authorization_boundary。
- stop_evidence：本轮只准备确认请求，未获得用户对任何 GPCF-RP 包的 review/stage/commit/push 授权。
- 禁止动作：未 review、未 stage、未 commit、未 push、未删除文件、未 deploy、未生产写入、未 schema migrate、未真实 API 写入、未状态提升。

## verify

- authorization layer matrix validator：待本轮执行。
- review confirmation validator：待本轮执行。
- 17 仓 Git gate：必须保持 partial/pass 且无 sensitive、behind、diff-check failed。
- Loop document gate：必须 pass。

## recover

- 若任一默认授权字段变为 true，回退确认请求并标记 `partial/rework`。
- 若用户后续只说“下一步”而未包含 GPCF-RP 包编号，不得执行 review/stage/commit/push。
- 若专项 Agent-Reach validator 不存在或失败，RP5/RP6 保持 pending，不影响 RP7/RP3/RP4/RP1/RP2 的确认请求。

## debug

- 当前最小可执行授权是按包确认 review；stage/commit/push/delete/runtime/acceptance 仍必须另行授权。
