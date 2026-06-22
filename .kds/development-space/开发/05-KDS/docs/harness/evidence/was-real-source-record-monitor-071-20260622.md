---
doc_id: GPCF-DOC-6C0AA90071
title: WAS Real Source Record Monitor 071 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-071-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-071-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 071 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-071` 将绿色供应链覆盖扩展到劳工、人权与社会责任证据链：劳工标准审核报告、工时与工资记录、职业健康安全记录、员工申诉机制记录、人权尽调记录、强迫劳动筛查记录、社区影响咨询记录。只有补齐这些证据，Ontology 才能安全地把劳工合规、工资工时、职业健康安全、申诉机制、人权尽调、强迫劳动风险和社区影响绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| labor_standard_audit_report_gaps | `0` |
| working_hours_wage_record_gaps | `0` |
| occupational_health_safety_record_gaps | `0` |
| worker_grievance_mechanism_record_gaps | `0` |
| human_rights_due_diligence_record_gaps | `0` |
| forced_labor_screening_record_gaps | `0` |
| community_impact_consultation_record_gaps | `0` |
| accepted_for_social_responsibility_profile | `0` |
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

- `labor_standard_audit_report`
- `working_hours_wage_record`
- `occupational_health_safety_record`
- `worker_grievance_mechanism_record`
- `human_rights_due_diligence_record`
- `forced_labor_screening_record`
- `community_impact_consultation_record`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_071.py
```

## 非声明

- 本证据不创建也不推断劳工标准审核报告、工时工资记录、职业健康安全记录、员工申诉机制记录、人权尽调记录、强迫劳动筛查记录或社区影响咨询记录。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-072`
