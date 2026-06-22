---
doc_id: GPCF-DOC-6C0AA90076
title: WAS Real Source Record Monitor 076 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-076-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-076-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 076 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-076` 将绿色供应链覆盖扩展到空气排放许可、烟囱排放监测、VOCs 清单、颗粒物控制、厂界噪声、异味投诉响应和环保检查通知证据链。只有补齐这些证据，Ontology 才能安全地把空气排放、噪声、异味和环保监管风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| air_emission_permit_gaps | `0` |
| stack_emission_monitoring_report_gaps | `0` |
| volatile_organic_compound_inventory_gaps | `0` |
| particulate_matter_control_record_gaps | `0` |
| noise_boundary_monitoring_report_gaps | `0` |
| odor_complaint_response_record_gaps | `0` |
| environmental_inspection_notice_record_gaps | `0` |
| accepted_for_air_emission_profile | `0` |
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

- `air_emission_permit`
- `stack_emission_monitoring_report`
- `volatile_organic_compound_inventory`
- `particulate_matter_control_record`
- `noise_boundary_monitoring_report`
- `odor_complaint_response_record`
- `environmental_inspection_notice_record`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_076.py
```

## 非声明

- 本证据不创建也不推断空气排放许可、烟囱排放监测报告、VOCs 清单、颗粒物控制记录、厂界噪声监测报告、异味投诉响应记录或环保检查通知记录。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-077`
