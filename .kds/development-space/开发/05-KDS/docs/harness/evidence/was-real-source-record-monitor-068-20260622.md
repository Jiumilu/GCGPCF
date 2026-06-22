---
doc_id: GPCF-DOC-6C0AA90068
title: WAS Real Source Record Monitor 068 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-068-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-068-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 068 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-068` 将绿色供应链覆盖扩展到碳资产、产品碳足迹、生命周期核算、Scope 3 供应商活动数据和 CBAM 监管映射链：产品碳足迹报告、生命周期核算边界、主要排放因子来源、供应商 Scope 3 活动数据、CBAM 嵌入排放申报、碳核查声明、碳信用或碳配额注销记录。只有补齐这些证据，Ontology 才能安全地把产品碳足迹、碳核算边界、排放因子、供应商活动数据、CBAM 申报、第三方核查和碳资产注销绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| product_carbon_footprint_report_gaps | `0` |
| lifecycle_assessment_boundary_gaps | `0` |
| primary_emission_factor_source_gaps | `0` |
| supplier_scope3_activity_data_gaps | `0` |
| cbam_embedded_emissions_declaration_gaps | `0` |
| carbon_verification_statement_gaps | `0` |
| carbon_credit_or_allowance_retirement_record_gaps | `0` |
| accepted_for_carbon_asset_profile | `0` |
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

- `product_carbon_footprint_report`
- `lifecycle_assessment_boundary`
- `primary_emission_factor_source`
- `supplier_scope3_activity_data`
- `cbam_embedded_emissions_declaration`
- `carbon_verification_statement`
- `carbon_credit_or_allowance_retirement_record`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_068.py
```

## 非声明

- 本证据不创建也不推断产品碳足迹报告、生命周期核算边界、主要排放因子来源、供应商 Scope 3 活动数据、CBAM 嵌入排放申报、碳核查声明或碳信用/碳配额注销记录。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-069`
