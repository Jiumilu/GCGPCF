---
doc_id: GPCF-DOC-07B7044CD3
title: WAS Real Source Record Monitor 021 Evidence
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-021-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-021-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 021 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-021` 已建立质量检验、批次/批号追溯、校准证书、不合格记录、CAPA 闭环和放行授权证据边界。

当前仍没有真实 P4 candidate 文件。质量检验、批次追溯、校准、不合格处置、CAPA 和放行授权证据均不得由 Ontology、LLM 或 RAG 推断生成，也不得替代 KDS source-of-record。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| quality_inspection_report_gaps | `0` |
| batch_lot_traceability_gaps | `0` |
| calibration_certificate_gaps | `0` |
| nonconformance_record_gaps | `0` |
| capa_closure_evidence_gaps | `0` |
| release_authorization_gaps | `0` |
| accepted_for_quality_profile | `0` |
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

## 负例

- quality_inspection_report_gap：质量检验报告缺失不得提升。
- batch_lot_traceability_gap：批次/批号追溯缺失不得提升。
- calibration_certificate_gap：校准证书缺失不得提升。
- nonconformance_record_gap：不合格记录缺失不得提升。
- capa_closure_evidence_gap：CAPA 闭环证据缺失不得提升。
- release_authorization_gap：放行授权缺失不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_021.py
```

## 边界

本 evidence 不接受无真实 source record 的质量画像，不推断质量检验、批次追溯、校准证书、不合格记录、CAPA 闭环或放行授权证据，不创建 runtime intake、review queue、WAES review、verified artifact、accepted、integrated 或 production_ready。
