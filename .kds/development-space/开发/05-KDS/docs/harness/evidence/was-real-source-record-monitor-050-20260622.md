---
doc_id: GPCF-DOC-6C0AA90050
title: WAS Real Source Record Monitor 050 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-050-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-050-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 050 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-050` 将绿色供应链覆盖扩展到供应商资质档案、供应商审核报告、供应商行为准则确认、尽职调查记录、整改跟踪、分包商披露和供应商绩效复盘证据层。只有补齐这些证据，Ontology 才能安全地把供应商准入、审核、尽调、整改、分包披露或绩效复盘状态绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| supplier_qualification_file_gaps | `0` |
| supplier_audit_report_gaps | `0` |
| supplier_code_of_conduct_acknowledgement_gaps | `0` |
| supplier_due_diligence_record_gaps | `0` |
| corrective_action_followup_gaps | `0` |
| subcontractor_disclosure_gaps | `0` |
| supplier_performance_review_gaps | `0` |
| accepted_for_supplier_governance_profile | `0` |
| accepted_for_next_gate | `0` |
| hold_required | `1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 必需证据类别

- `supplier_qualification_file`
- `supplier_audit_report`
- `supplier_code_of_conduct_acknowledgement`
- `supplier_due_diligence_record`
- `corrective_action_followup`
- `subcontractor_disclosure`
- `supplier_performance_review`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_050.py
```

## 非声明

- 本证据不创建也不推断供应商资质档案、供应商审核报告、供应商行为准则确认、尽职调查记录、整改跟踪、分包商披露或供应商绩效复盘证据。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-051`
