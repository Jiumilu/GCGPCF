---
doc_id: GPCF-DOC-6C0AA90078
title: WAS Real Source Record Monitor 078 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-078-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-078-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 078 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-078` 将绿色供应链覆盖扩展到土地使用许可、生物多样性影响评估、生态敏感区筛查、供应商土地权属声明、复垦恢复计划、社区环境影响记录和零毁林承诺证据链。只有补齐这些证据，Ontology 才能安全地把土地、生物多样性、生态敏感区和社区环境风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| land_use_permit_gaps | `0` |
| biodiversity_impact_assessment_gaps | `0` |
| ecological_sensitive_area_screening_gaps | `0` |
| supplier_land_tenure_declaration_gaps | `0` |
| remediation_restoration_plan_gaps | `0` |
| community_environmental_impact_record_gaps | `0` |
| no_deforestation_commitment_gaps | `0` |
| accepted_for_land_biodiversity_profile | `0` |
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

- `land_use_permit`
- `biodiversity_impact_assessment`
- `ecological_sensitive_area_screening`
- `supplier_land_tenure_declaration`
- `remediation_restoration_plan`
- `community_environmental_impact_record`
- `no_deforestation_commitment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_078.py
```

## 非声明

- 本证据不创建也不推断土地使用许可、生物多样性影响评估、生态敏感区筛查、供应商土地权属声明、复垦恢复计划、社区环境影响记录或零毁林承诺。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-079`
