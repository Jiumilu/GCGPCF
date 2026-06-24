---
doc_id: GPCF-DOC-6C0AA90095
title: WAS Real Source Record Monitor 095 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-095-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-095-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 095 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-095` 将绿色供应链覆盖扩展到第三方保证执行层：核验机构资质、核验人员能力矩阵、保证取样计划、现场访问到场记录、证据抽样轨迹、保证例外日志和最终保证意见。该边界用于约束外部核验执行证据进入 WAES/KDS/GFIS/RAG/Pool 之前必须具备可追溯、可复核、不可由 LLM 或治理文档替代的来源链。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| verifier_accreditation_certificate_gaps | `0` |
| verifier_competence_matrix_gaps | `0` |
| assurance_sampling_plan_gaps | `0` |
| site_visit_attendance_record_gaps | `0` |
| evidence_sampling_trace_gaps | `0` |
| assurance_exception_log_gaps | `0` |
| assurance_final_opinion_statement_gaps | `0` |
| accepted_for_external_assurance_execution_profile | `0` |
| accepted_for_next_gate | `0` |
| hold_required | `1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `False` |
| integrated | `False` |
| production_ready | `False` |

## 必需证据类别

- `verifier_accreditation_certificate`
- `verifier_competence_matrix`
- `assurance_sampling_plan`
- `site_visit_attendance_record`
- `evidence_sampling_trace`
- `assurance_exception_log`
- `assurance_final_opinion_statement`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_095.py
```

## 非声明

- 本证据不创建也不推断核验机构资质、核验人员能力矩阵、保证取样计划、现场访问到场记录、证据抽样轨迹、保证例外日志或最终保证意见。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-096`
