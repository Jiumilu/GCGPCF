---
doc_id: GPCF-DOC-6C0AA90075
title: WAS Real Source Record Monitor 075 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-075-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-075-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 075 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-075` 将绿色供应链覆盖扩展到取水计量、水压力区域评估、废水排放许可、出水水质检测、雨水污染预防、水循环复用和供应商水资源管理承诺证据链。只有补齐这些证据，Ontology 才能安全地把水资源、水污染和水风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| water_withdrawal_metering_record_gaps | `0` |
| water_stress_area_assessment_gaps | `0` |
| wastewater_discharge_permit_gaps | `0` |
| effluent_quality_test_report_gaps | `0` |
| stormwater_pollution_prevention_plan_gaps | `0` |
| water_recycling_reuse_record_gaps | `0` |
| supplier_water_stewardship_commitment_gaps | `0` |
| accepted_for_water_stewardship_profile | `0` |
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

- `water_withdrawal_metering_record`
- `water_stress_area_assessment`
- `wastewater_discharge_permit`
- `effluent_quality_test_report`
- `stormwater_pollution_prevention_plan`
- `water_recycling_reuse_record`
- `supplier_water_stewardship_commitment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_075.py
```

## 非声明

- 本证据不创建也不推断取水计量记录、水压力区域评估、废水排放许可、出水水质检测报告、雨水污染预防计划、水循环复用记录或供应商水资源管理承诺。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-076`
