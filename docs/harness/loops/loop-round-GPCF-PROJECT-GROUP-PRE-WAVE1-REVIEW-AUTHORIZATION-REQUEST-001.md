---
doc_id: GPCF-DOC-LOOP-ROUND-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001
title: loop-round-GPCF-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# loop-round-GPCF-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001

## run

- 输入：当前 6 仓 post-scheme review 授权请求、授权回执总账、预执行命令包、delegated wrapper baseline、运行门禁阻塞矩阵、Wave 1 授权请求。
- 动作：把 6 仓 review 边界收口成 Wave 1 之前的统一桥接入口。
- 单仓锚点：KDS 复用 `5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要`；AAAS/XWAIL/SOP 分别复用 `5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要`、`5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要`、`5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要`。
- 输出：`docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 和 `tools/kds-sync/validate_project_group_pre_wave1_review_authorization_request_20260627.py`。

## stop

- 不新增任何真实授权。
- 不执行 6 仓 review 命令包，不登记任何回执，不进入 Wave 1 执行。

## verify

- `python3 tools/kds-sync/validate_project_group_pre_wave1_review_authorization_request_20260627.py`
- `python3 tools/kds-sync/validate_project_group_post_scheme_recognition_review_authorization_request_20260626.py`
- `python3 tools/kds-sync/validate_project_group_post_scheme_recognition_authorization_receipt_ledger_20260626.py`
- `python3 tools/kds-sync/validate_project_group_post_scheme_recognition_pre_execution_command_pack_20260626.py`
- `python3 tools/kds-sync/validate_project_group_wave1_authorization_request_20260626.py`
- `python3 tools/kds-sync/loop_document_gate.py`

## recover

- 若 6 仓 review 边界集合、auth_id、pre-execution gate 或下游解锁对象变化，回滚本文并重新生成桥接包。

## debug

- 当前真正阻塞 Wave 1 的是 `AUTH-KDS-SCHEME-REVIEW-20260626`、`AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627`、`AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627`、`AUTH-GPCF-SCHEME-REVIEW-20260626`、`AUTH-GFIS-SCHEME-REVIEW-20260626`、`AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627` 仍全部 `pending_confirmation`。
