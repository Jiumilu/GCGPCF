---
doc_id: GPCF-LOOP-PROJECT-GROUP-REVIEW-AUTH-GPCF-RP7-CONCLUSION-001
title: GPCF PROJECT GROUP REVIEW AUTH GPCF RP7 CONCLUSION 001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-RP7-CONCLUSION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-RP7-CONCLUSION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP REVIEW AUTH GPCF RP7 CONCLUSION 001

## run

- 输入：用户授权 `REVIEW-AUTH-GPCF-WORKTREE-20260627` 的 `GPCF-RP7`，只允许人工 review 和结论登记。
- 执行：复核 RP7 前置 validator、17 仓 Git gate 与 RP7 diff-check，登记 review 结论。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-rp7-review-conclusion-20260627.md` 和 validator `tools/kds-sync/validate_project_group_review_auth_gpcf_rp7_conclusion_20260627.py`。

## stop

- stop_type：project_group_git_gate_drift。
- stop_evidence：17 仓 Git gate 当前 dirty repos 为 `GlobalCoud GPCF`、`GlobalCloud GFIS`，不再满足 RP7 原前提 only_dirty_repo=`GlobalCoud GPCF`。
- 禁止动作：未 stage、未 commit、未 push、未删除文件、未 deploy、未生产写入、未 schema migrate、未真实 API 写入、未状态提升。

## verify

- RP7 conclusion validator：必须 pass，且只能证明 `rework_required` 结论登记真实。
- generated/output/dist isolation validator：pass。
- 17 仓 Git gate：partial；无 missing/ahead/behind/sensitive；17/17 diff-check pass。
- 原 RP7 前置 validator：因 GFIS dirty 漂移保持 fail，不得据此升级为 pass。

## recover

- 若 `GlobalCloud GFIS` 恢复 clean 或完成 GFIS dirty 分类证据，可重新运行 RP7 前置 validator。
- 若用户后续授权 stage/commit/push，必须另起授权口令，并重新复跑 Git gate、Loop document gate、KDS conflict guard 和 RP7 专项 validator。
- 若出现 sensitive、behind、diff-check failed 或 missing repo，立即停止并标记 blocked。

## debug

- 本轮只把用户授权消费为 `review_conclusion_registered`。
- `rp7_review_result = rework_required` 不等同于 review pass，也不产生 stage/commit/push 候选。
