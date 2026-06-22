---
doc_id: GPCF-DOC-6C0AA90082
title: WAS Real Source Record Monitor 082 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-082-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-082-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 082 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-082` 将绿色供应链覆盖扩展到土地使用权证明、生物多样性影响评估、零毁林声明、保护区筛查记录、生态系统修复计划、供应商土地使用承诺和栖息地转换风险评估证据链。只有补齐这些证据，Ontology 才能安全地把土地利用、生物多样性、零毁林、保护区、生态修复和栖息地转换风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| land_use_right_certificate_gaps | `0` |
| biodiversity_impact_assessment_gaps | `0` |
| deforestation_free_declaration_gaps | `0` |
| protected_area_screening_record_gaps | `0` |
| ecosystem_restoration_plan_gaps | `0` |
| supplier_land_use_commitment_gaps | `0` |
| habitat_conversion_risk_assessment_gaps | `0` |
| accepted_for_biodiversity_land_use_profile | `0` |
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

- `land_use_right_certificate`
- `biodiversity_impact_assessment`
- `deforestation_free_declaration`
- `protected_area_screening_record`
- `ecosystem_restoration_plan`
- `supplier_land_use_commitment`
- `habitat_conversion_risk_assessment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_082.py
```

## 非声明

- 本证据不创建也不推断土地使用权证明、生物多样性影响评估、零毁林声明、保护区筛查记录、生态系统修复计划、供应商土地使用承诺或栖息地转换风险评估。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-083`
