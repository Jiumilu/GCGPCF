---
doc_id: GPCF-DOC-LOOP-ROUND-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001
title: loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001

## run

- 输入：`review-auth worktree confirmation`、`review-auth RP7 conclusion`、`pre-wave1 review authorization request`、`wave1 authorization request`。
- 动作：把 GPCF worktree review、Pre-Wave1 和 Wave 1 request 的先后关系与阻断关系收成一份桥接审计。
- 输出：`docs/harness/evidence/globalcloud-project-group-review-auth-pre-wave1-wave1-bridge-audit-20260627.md` 和对应只读 validator。

## stop

- 不生成任何真实授权回执。
- 不进入 post-scheme、execution 或 Wave 1 receipt ledger。
- 不执行 review、cleanup、命令包、stage、commit、push、deploy、release 或真实 KDS API 同步。

## verify

- `python3 tools/kds-sync/validate_project_group_review_auth_gpcf_worktree_confirmation_20260627.py`
- `python3 tools/kds-sync/validate_project_group_review_auth_gpcf_rp7_conclusion_20260627.py`
- `python3 tools/kds-sync/validate_project_group_pre_wave1_review_authorization_request_20260627.py`
- `python3 tools/kds-sync/validate_project_group_wave1_authorization_request_20260626.py`
- `python3 tools/kds-sync/validate_project_group_review_auth_pre_wave1_wave1_bridge_audit_20260627.py`
- `python3 tools/kds-sync/loop_document_gate.py`

## recover

- 若 `review-auth -> pre-wave1 -> wave1` 顺序、阻断关系、或默认边界漂移，回滚本回合并重新收口。

## debug

- 当前真正阻断 Wave 1 的不是 request 缺失，而是 Pre-Wave1 六仓 review 边界仍全部 `pending_confirmation`。
- `GPCF-RP7` 当前为 `rework_required`，只能证明 drift 已登记，不足以解除 Pre-Wave1 或 Wave 1 阻断。
