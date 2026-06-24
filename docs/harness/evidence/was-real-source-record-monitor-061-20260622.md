---
doc_id: GPCF-DOC-6C0AA90061
title: WAS Real Source Record Monitor 061 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-061-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-061-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 061 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-061` 将绿色供应链覆盖扩展到生态设计与材料效率链：设计减量记录、可拆解设计记录、可维修性评估、产品寿命延长计划、材料效率核算、替代材料评估和设计变更环境评审。只有补齐这些证据，Ontology 才能安全地把生态设计、材料减量、可拆解、可维修、寿命延长、材料效率和设计变更环境评审绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| design_material_reduction_record_gaps | `0` |
| design_for_disassembly_record_gaps | `0` |
| repairability_assessment_gaps | `0` |
| product_lifetime_extension_plan_gaps | `0` |
| material_efficiency_calculation_gaps | `0` |
| substitute_material_assessment_gaps | `0` |
| design_change_environmental_review_gaps | `0` |
| accepted_for_eco_design_profile | `0` |
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

- `design_material_reduction_record`
- `design_for_disassembly_record`
- `repairability_assessment`
- `product_lifetime_extension_plan`
- `material_efficiency_calculation`
- `substitute_material_assessment`
- `design_change_environmental_review`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_061.py
```

## 非声明

- 本证据不创建也不推断设计减量记录、可拆解设计记录、可维修性评估、产品寿命延长计划、材料效率核算、替代材料评估或设计变更环境评审。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-062`
