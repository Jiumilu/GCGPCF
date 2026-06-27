---
doc_id: GPCF-LOOP-PROJECT-GROUP-AUTHORIZATION-LAYER-MATRIX-001
title: GPCF PROJECT GROUP AUTHORIZATION LAYER MATRIX 001
project: GPCF
related_projects: [GPC, WAES, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-AUTHORIZATION-LAYER-MATRIX-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-AUTHORIZATION-LAYER-MATRIX-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GPCF PROJECT GROUP AUTHORIZATION LAYER MATRIX 001

## run

- 输入：用户要求“按建议执行”。
- 执行：将开发过程授权拆成 DEV-AUTH、REVIEW-AUTH、RUNTIME-AUTH、ACCEPTANCE-AUTH 四层，并把第一执行入口绑定为 `REVIEW-AUTH-GPCF-WORKTREE-20260627`。
- 输出：新增 evidence `docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md` 和 validator `tools/kds-sync/validate_project_group_authorization_layer_matrix_20260627.py`。

## stop

- stop_type：authorization_boundary。
- stop_evidence：本轮只生成授权入口与口令模板，没有获得用户逐包 review/stage/commit/push/runtime/acceptance 授权。
- 禁止动作：未 review、未 stage、未 commit、未 push、未删除文件、未 deploy、未 release、未生产写入、未 schema migrate、未真实 API 写入、未状态提升。

## verify

- 17 仓 Git gate：`partial`，唯一 dirty 仓为 GPCF，无 hard blocker。
- GPCF worktree review packages validator：pass。
- SOP/PKC generated-output-dist isolation validator：pass。
- 授权矩阵 validator：待本轮执行。

## recover

- 若任一默认授权字段变为 true，回退本文并标记 `partial/rework`。
- 若用户后续授权范围不含具体包 ID、文件清单、动作和禁止边界，不得执行 stage/commit/push/runtime/acceptance。
- 若 Git gate 出现 sensitive、behind、diff-check failed，REVIEW-AUTH 降级为 blocked。

## debug

- 当前建议已经从“授权堵点评估”落为可执行层级：开发态继续由 DEV-AUTH 支持；GPCF dirty review 由 REVIEW-AUTH 第一入口承接；runtime 与 acceptance 继续保持阻断，等待真实业务输入和人工确认。
