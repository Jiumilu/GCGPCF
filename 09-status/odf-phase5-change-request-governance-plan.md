---
doc_id: GPCF-DOC-1DC15FD42D
title: ODF Phase 5 准入变更申请治理方案
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase5-change-request-governance-plan.md
source_path: 09-status/odf-phase5-change-request-governance-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF Phase 5 准入变更申请治理方案

日期：2026-06-17

## 目标

在 Phase 4 `phase4_small_batch_closed` 的基础上，建立 ODF 准入变更申请机制，保证后续任何样本扩展都先经过申请、边界确认、回滚声明、KDS 定向同步清单和门禁验证。

当前阶段目标：`phase5_change_request_closed`。

## 受控对象

| artifact | path |
| --- | --- |
| change request ledger Markdown | `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` |
| change request ledger JSON | `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.json` |
| change request validator | `tools/kds-sync/validate_odf_change_request_gate.py` |
| closure report | `docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` |

## 门禁

1. 申请必须具备 `request_id`、`request_type`、`status`、`requested_by`、`manual_confirmation`。
2. 小批量样本上限为 5。
3. 每个样本必须具备 source path、ODF path 和 rollback hint。
4. 必须列出 KDS 定向同步路径。
5. 必须声明不全量推广、不 accepted、不 integrated、不生产写、不外部 API 写。
6. `validate_odf_change_request_gate.py` 必须通过。
7. `validate_odf_schema_gate.py` 必须继续通过。
8. 文档污染、KDS TOKEN、Loop 文档门禁、KDS conflict guard、KDS sync plan 必须通过。
9. Phase 5 相关 KDS 待同步项必须为 0。

## 非范围

- 不新增 Phase 5 ODF 样本。
- 不全量导入 ODF。
- 不替代 Git、KDS、OKF 或 Loop evidence。
- 不把文档验证写成业务完成。
- 不自动升级 `accepted` 或 `integrated`。
