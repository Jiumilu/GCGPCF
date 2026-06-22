---
doc_id: GPCF-DOC-89108DD154
title: ODF Phase 7 小批量样本执行方案
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase7-small-batch-execution-plan.md
source_path: 09-status/odf-phase7-small-batch-execution-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# ODF Phase 7 小批量样本执行方案

日期：2026-06-19

## 目标

在 Phase 6 人工确认后，创建 3 个小批量 ODF metadata envelope，并通过 schema、变更申请、人工确认、污染、KDS TOKEN、KDS 冲突和定向同步门禁。

## 输入

| input | path |
| --- | --- |
| 人工确认工作台 | `docs/harness/evidence/odf-phase6-manual-confirmation-workbench-20260618.json` |
| Phase 7 ledger | `docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.json` |

## 输出

| artifact | path |
| --- | --- |
| ODF envelope 1 | `docs/harness/evidence/odf-samples/phase6/odf-phase6-kds-md-okf-closure-plan.json` |
| ODF envelope 2 | `docs/harness/evidence/odf-samples/phase6/odf-phase6-kds-sync-register.json` |
| ODF envelope 3 | `docs/harness/evidence/odf-samples/phase6/odf-phase6-kds-security-policy.json` |
| Phase 7 ledger | `docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.md` |
| Phase 7 closure | `docs/harness/evidence/odf-phase7-small-batch-closure-20260619.md` |

## 门禁

```bash
python3 tools/kds-sync/validate_odf_schema_gate.py
python3 tools/kds-sync/validate_odf_change_request_gate.py
python3 tools/kds-sync/validate_odf_manual_confirmation_workbench.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/kds_conflict_guard.py
```

## 非范围

- 不复制源 Markdown 正文。
- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不写生产系统或真实外部 API。
- 不做业务状态升级。
