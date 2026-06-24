---
doc_id: GPCF-DOC-B1974D0060
title: "Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-060"
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-060.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-060.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-060

## 输入

- `docs/harness/evidence/was-real-source-record-monitor-059-20260622.json`
- `tools/kds-sync/validate_was_real_source_record_monitor_059.py`
- `docs/harness/intake/was-real-source-record-candidate-template.yaml`

## 动作

- 建立第五十九次真实 P4 输入 monitor。
- 增加绿色供应链绿色电力与能源属性负例：绿色电力采购合同缺失、能源消耗计量记录缺失、绿电证书缺失、可再生能源证书注销证明缺失、现场发电计量记录缺失、能源结构分摊记录缺失、电网排放因子来源缺失。
- 复跑当前 P4 必跑门禁和 candidate precheck。
- 保持无真实 source-record 时的 hold 状态。

## 输出

- `docs/harness/evidence/was-real-source-record-monitor-060-20260622.json`
- `docs/harness/evidence/was-real-source-record-monitor-060-20260622.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_060.py`
- `fixtures/was/real-source-record-monitor-060-*.json`

## 检查

```bash
python3 tools/kds-sync/validate_was_real_source_record_monitor_060.py
```

## 反馈

真实 P4 输入 monitor 060 已建立。当前 `accepted_for_renewable_energy_profile=0`、`accepted_for_next_gate=0`、`hold_required=1`，绿色电力采购合同、能源消耗计量记录、绿电证书、可再生能源证书注销证明、现场发电计量记录、能源结构分摊记录和电网排放因子来源均不得替代 KDS source-of-record。

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
  asset_dimension: physical_asset
  flow_type: material_flow
  object_family: RenewableEnergyAttributeEvidence
  source_of_record: KDS
  ontology_role: real_source_record_monitor_060
  scenario_scope: renewable_energy_contract_metering_certificate_retirement_generation_allocation_factor
  renewable_energy_requirements:
    - renewable_energy_contract
    - energy_consumption_meter_record
    - green_power_certificate
    - renewable_energy_certificate_retirement
    - onsite_generation_meter_record
    - energy_mix_allocation_record
    - grid_emission_factor_source
  waes_gate: blocked_until_real_source_record_and_renewable_energy_attribute_proofs_exist
  loop_role: evidence_closure
  llm_role: candidate_generation_only
  rag_role: controlled_reference_only
  runtime_writeback: blocked_without_kds_bound_renewable_energy_evidence
  rejected_renewable_energy_cases:
    - renewable_energy_contract_gap
    - energy_consumption_meter_record_gap
    - green_power_certificate_gap
    - renewable_energy_certificate_retirement_gap
    - onsite_generation_meter_record_gap
    - energy_mix_allocation_record_gap
    - grid_emission_factor_source_gap
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
  next_round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-061
```
