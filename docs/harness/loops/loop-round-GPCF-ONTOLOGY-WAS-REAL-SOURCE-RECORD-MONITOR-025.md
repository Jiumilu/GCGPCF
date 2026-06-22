---
doc_id: GPCF-DOC-8D92531407
title: "Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-025"
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-025.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-025.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-025

## 输入

- `docs/harness/evidence/was-real-source-record-monitor-024-20260621.json`
- `tools/kds-sync/validate_was_real_source_record_monitor_024.py`
- `tools/kds-sync/validate_was_real_source_record_candidate_precheck.py`
- `docs/harness/intake/was-real-source-record-candidate-template.yaml`

## 动作

- 建立第二十五次真实 P4 输入 monitor。
- 增加用地/生态/环评边界负例：用地许可缺失、环境影响评价缺失、生态/生物多样性基线缺失、保护区筛查缺失、土壤/地下水评估缺失、修复缓解方案缺失。
- 复跑 P4 candidate precheck 与 GFIS/WAS source-record 必跑门禁。
- 保持无真实 source-record 时的 hold 状态。

## 输出

- `docs/harness/evidence/was-real-source-record-monitor-025-20260621.json`
- `docs/harness/evidence/was-real-source-record-monitor-025-20260621.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_025.py`
- `fixtures/was/real-source-record-monitor-025-positive.json`
- `fixtures/was/real-source-record-monitor-025-negative-land-use-permit-gap.json`
- `fixtures/was/real-source-record-monitor-025-negative-environmental-impact-assessment-gap.json`
- `fixtures/was/real-source-record-monitor-025-negative-biodiversity-baseline-gap.json`
- `fixtures/was/real-source-record-monitor-025-negative-protected-area-screening-gap.json`
- `fixtures/was/real-source-record-monitor-025-negative-soil-groundwater-assessment-gap.json`
- `fixtures/was/real-source-record-monitor-025-negative-restoration-mitigation-plan-gap.json`

## 检查

```bash
python3 tools/kds-sync/validate_was_real_source_record_monitor_025.py
```

## 反馈

真实 P4 输入 monitor 025 已建立。当前 `accepted_for_land_ecology_profile=0`、`accepted_for_next_gate=0`、`hold_required=1`，用地许可、环境影响评价、生态基线、保护区筛查、土壤/地下水评估和修复缓解方案均不得替代 KDS source-of-record。

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
  asset_dimension: spacetime_asset
  flow_type: rule_flow
  object_family: SiteLandEcologyCompliance
  source_of_record: KDS
  ontology_role: real_source_record_monitor_025
  scenario_scope: land_use_eia_biodiversity_protected_area_soil_groundwater_restoration
  land_ecology_requirements:
    - land_use_permit
    - environmental_impact_assessment
    - biodiversity_baseline
    - protected_area_screening
    - soil_groundwater_assessment
    - restoration_mitigation_plan
  waes_gate: blocked_until_real_source_record_and_land_ecology_proofs_exist
  loop_role: evidence_closure
  llm_role: candidate_generation_only
  rag_role: controlled_reference_only
  runtime_writeback: blocked_without_kds_bound_land_ecology_evidence
  rejected_land_ecology_cases:
    - land_use_permit_gap
    - environmental_impact_assessment_gap
    - biodiversity_baseline_gap
    - protected_area_screening_gap
    - soil_groundwater_assessment_gap
    - restoration_mitigation_plan_gap
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
```
