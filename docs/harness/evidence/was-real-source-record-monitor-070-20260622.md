---
doc_id: GPCF-DOC-6C0AA90070
title: WAS Real Source Record Monitor 070 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-070-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-070-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 070 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-070` 将绿色供应链覆盖扩展到生物多样性、土地使用与生态影响证据链：生物多样性基线调查、土地使用合规许可、保护地筛查记录、生态影响评估、栖息地恢复计划、利益相关方咨询记录、自然正向 KPI 监测。只有补齐这些证据，Ontology 才能安全地把生态影响、土地合规、保护地风险、恢复承诺、社区参与和自然正向指标绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| biodiversity_baseline_survey_gaps | `0` |
| land_use_compliance_permit_gaps | `0` |
| protected_area_screening_record_gaps | `0` |
| ecological_impact_assessment_gaps | `0` |
| habitat_restoration_plan_gaps | `0` |
| stakeholder_consultation_record_gaps | `0` |
| nature_positive_kpi_monitoring_gaps | `0` |
| accepted_for_biodiversity_profile | `0` |
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

- `biodiversity_baseline_survey`
- `land_use_compliance_permit`
- `protected_area_screening_record`
- `ecological_impact_assessment`
- `habitat_restoration_plan`
- `stakeholder_consultation_record`
- `nature_positive_kpi_monitoring`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_070.py
```

## 非声明

- 本证据不创建也不推断生物多样性基线调查、土地使用合规许可、保护地筛查记录、生态影响评估、栖息地恢复计划、利益相关方咨询记录或自然正向 KPI 监测。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-071`
