---
doc_id: GPCF-DOC-B1974D0082
title: "Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-082"
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-082.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-082.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-082

## 输入

- `docs/harness/evidence/was-real-source-record-monitor-080-20260622.json`
- `tools/kds-sync/validate_was_real_source_record_monitor_080.py`
- `docs/harness/intake/was-real-source-record-candidate-template.yaml`

## 动作

- 建立第八十二次真实 P4 输入 monitor。
- 增加绿色供应链土地利用与生物多样性负例：土地使用权证明缺失、生物多样性影响评估缺失、零毁林声明缺失、保护区筛查记录缺失、生态系统修复计划缺失、供应商土地使用承诺缺失、栖息地转换风险评估缺失。
- 负例 case key：`land_use_right_certificate_gap`、`biodiversity_impact_assessment_gap`、`deforestation_free_declaration_gap`、`protected_area_screening_record_gap`、`ecosystem_restoration_plan_gap`、`supplier_land_use_commitment_gap`、`habitat_conversion_risk_assessment_gap`。
- 复跑当前 P4 必跑门禁和 candidate precheck。
- 保持无真实 source-record 时的 hold 状态。

## 输出

- `docs/harness/evidence/was-real-source-record-monitor-082-20260622.json`
- `docs/harness/evidence/was-real-source-record-monitor-082-20260622.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_082.py`
- `fixtures/was/real-source-record-monitor-082-*.json`

## 检查

```bash
python3 tools/kds-sync/validate_was_real_source_record_monitor_082.py
```

## 反馈

真实 P4 输入 monitor 082 已建立。当前 `accepted_for_biodiversity_land_use_profile=0`、`accepted_for_next_gate=0`、`hold_required=1`，土地使用权证明、生物多样性影响评估、零毁林声明、保护区筛查记录、生态系统修复计划、供应商土地使用承诺和栖息地转换风险评估均不得替代 KDS source-of-record。

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
  asset_dimension: environmental_asset
  flow_type: biodiversity_flow
  object_family: BiodiversityLandUseEvidence
  source_of_record: KDS
  ontology_role: real_source_record_monitor_082
  scenario_scope: land_use_right_certificate_biodiversity_impact_assessment_deforestation_free_declaration_protected_area_screening_record_ecosystem_restoration_plan_supplier_land_use_commitment_habitat_conversion_risk_assessment
  biodiversity_land_use_requirements:
    - land_use_right_certificate
    - biodiversity_impact_assessment
    - deforestation_free_declaration
    - protected_area_screening_record
    - ecosystem_restoration_plan
    - supplier_land_use_commitment
    - habitat_conversion_risk_assessment
  source_refs:
    - docs/harness/evidence/was-real-source-record-monitor-082-20260622.json
    - docs/harness/intake/was-real-source-record-candidate-template.yaml
  validator_refs:
    - tools/kds-sync/validate_was_real_source_record_monitor_082.py
  waes_gate: blocked_without_kds_bound_biodiversity_land_use_evidence
  loop_role: evidence_boundary_monitor
  llm_role: candidate_generation_only
  rag_role: controlled_reference_only
  runtime_writeback: blocked_without_kds_bound_biodiversity_land_use_evidence
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
  next_round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-083
  no_write_declaration: no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready
```
