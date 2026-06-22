---
doc_id: GPCF-DOC-6C0AA90067
title: WAS Real Source Record Monitor 067 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-067-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-067-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 067 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-067` 将绿色供应链覆盖扩展到废弃物与危废合规处置链：废弃物分类记录、危废转移联单、持证处置商许可、废弃物转移收据、处置或回收证明、残余处置确认、监管处置报告。只有补齐这些证据，Ontology 才能安全地把废弃物分类、危废转移、持证处置、转移收据、处理回收、残余处置和监管报告绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| waste_classification_record_gaps | `0` |
| hazardous_waste_manifest_gaps | `0` |
| licensed_disposal_vendor_permit_gaps | `0` |
| waste_transfer_receipt_gaps | `0` |
| treatment_or_recycling_certificate_gaps | `0` |
| residue_disposal_confirmation_gaps | `0` |
| regulator_disposal_report_gaps | `0` |
| accepted_for_waste_disposal_profile | `0` |
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

- `waste_classification_record`
- `hazardous_waste_manifest`
- `licensed_disposal_vendor_permit`
- `waste_transfer_receipt`
- `treatment_or_recycling_certificate`
- `residue_disposal_confirmation`
- `regulator_disposal_report`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_067.py
```

## 非声明

- 本证据不创建也不推断废弃物分类记录、危废转移联单、持证处置商许可、废弃物转移收据、处置或回收证明、残余处置确认或监管处置报告。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-068`
