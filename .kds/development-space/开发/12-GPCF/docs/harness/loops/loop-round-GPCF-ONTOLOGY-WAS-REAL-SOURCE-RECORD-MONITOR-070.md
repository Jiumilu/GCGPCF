---
doc_id: GPCF-DOC-B1974D0070
title: "Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-070"
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-070.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-070.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-070

## 输入

- `docs/harness/evidence/was-real-source-record-monitor-069-20260622.json`
- `tools/kds-sync/validate_was_real_source_record_monitor_069.py`
- `docs/harness/intake/was-real-source-record-candidate-template.yaml`

## 动作

- 建立第七十次真实 P4 输入 monitor。
- 增加绿色供应链生物多样性与生态影响负例：生物多样性基线调查缺失、土地使用合规许可缺失、保护地筛查记录缺失、生态影响评估缺失、栖息地恢复计划缺失、利益相关方咨询记录缺失、自然正向 KPI 监测缺失。
- 复跑当前 P4 必跑门禁和 candidate precheck。
- 保持无真实 source-record 时的 hold 状态。

## 输出

- `docs/harness/evidence/was-real-source-record-monitor-070-20260622.json`
- `docs/harness/evidence/was-real-source-record-monitor-070-20260622.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_070.py`
- `fixtures/was/real-source-record-monitor-070-*.json`

## 检查

```bash
python3 tools/kds-sync/validate_was_real_source_record_monitor_070.py
```

## 反馈

真实 P4 输入 monitor 070 已建立。当前 `accepted_for_biodiversity_profile=0`、`accepted_for_next_gate=0`、`hold_required=1`，生物多样性基线调查、土地使用合规许可、保护地筛查记录、生态影响评估、栖息地恢复计划、利益相关方咨询记录和自然正向 KPI 监测均不得替代 KDS source-of-record。

## loop_was_context

```yaml
loop_was_context:
  project_group_scope:
    - GFIS
    - GPC
    - PVAOS
    - WAES
    - KDS
    - Brain
    - PKC
    - XiaoC
    - XGD
    - XiaoG
    - MMC
    - GPCF
    - Studio
    - WAS
  asset_dimension: natural_asset
  flow_type: compliance_flow
  object_family: BiodiversityLandUseAndEcologicalImpactEvidence
  source_of_record: KDS
  ontology_role: real_source_record_monitor_070
  scenario_scope: biodiversity_baseline_survey_land_use_compliance_permit_protected_area_screening_record_ecological_impact_assessment_habitat_restoration_plan_stakeholder_consultation_record_nature_positive_kpi_monitoring
  biodiversity_requirements:
    - biodiversity_baseline_survey
    - land_use_compliance_permit
    - protected_area_screening_record
    - ecological_impact_assessment
    - habitat_restoration_plan
    - stakeholder_consultation_record
    - nature_positive_kpi_monitoring
  waes_gate: blocked_until_real_source_record_and_biodiversity_proofs_exist
  loop_role: evidence_closure
  llm_role: candidate_generation_only
  rag_role: controlled_reference_only
  runtime_writeback: blocked_without_kds_bound_biodiversity_evidence
  rejected_biodiversity_cases:
    - biodiversity_baseline_survey_gap
    - land_use_compliance_permit_gap
    - protected_area_screening_record_gap
    - ecological_impact_assessment_gap
    - habitat_restoration_plan_gap
    - stakeholder_consultation_record_gap
    - nature_positive_kpi_monitoring_gap
  promotion_boundary:
    real_source_records: 0
    valid_source_records: 0
    runtime_primary_key_ready: 0
    review_queue: 0
    runtime_intake: 0
    waes_review: 0
    verified: 0
    accepted: false
    integrated: false
    production_ready: false
  next_round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-071
```
