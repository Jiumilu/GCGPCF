---
doc_id: GPCF-DOC-B1974D0080
title: "Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-080"
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-080.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-080.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-080

## 输入

- `docs/harness/evidence/was-real-source-record-monitor-079-20260622.json`
- `tools/kds-sync/validate_was_real_source_record_monitor_079.py`
- `docs/harness/intake/was-real-source-record-candidate-template.yaml`

## 动作

- 建立第八十次真实 P4 输入 monitor。
- 增加绿色供应链可再生能源与碳抵消负例：可再生能源采购合同缺失、绿电证书缺失、购电协议缺失、用电排放因子记录缺失、能源属性证书注销记录缺失、碳抵消项目证明缺失、供应商绿电承诺缺失。
- 负例 case key：`renewable_energy_purchase_contract_gap`、`green_electricity_certificate_gap`、`power_purchase_agreement_gap`、`electricity_emission_factor_record_gap`、`energy_attribute_certificate_retirement_gap`、`carbon_offset_project_certificate_gap`、`supplier_renewable_energy_commitment_gap`。
- 复跑当前 P4 必跑门禁和 candidate precheck。
- 保持无真实 source-record 时的 hold 状态。

## 输出

- `docs/harness/evidence/was-real-source-record-monitor-080-20260622.json`
- `docs/harness/evidence/was-real-source-record-monitor-080-20260622.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_080.py`
- `fixtures/was/real-source-record-monitor-080-*.json`

## 检查

```bash
python3 tools/kds-sync/validate_was_real_source_record_monitor_080.py
```

## 反馈

真实 P4 输入 monitor 080 已建立。当前 `accepted_for_renewable_energy_profile=0`、`accepted_for_next_gate=0`、`hold_required=1`，可再生能源采购合同、绿电证书、购电协议、用电排放因子、能源属性证书注销记录、碳抵消项目证明和供应商绿电承诺均不得替代 KDS source-of-record。

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
  flow_type: energy_flow
  object_family: RenewableEnergyCarbonOffsetEvidence
  source_of_record: KDS
  ontology_role: real_source_record_monitor_080
  scenario_scope: renewable_energy_purchase_contract_green_electricity_certificate_power_purchase_agreement_electricity_emission_factor_record_energy_attribute_certificate_retirement_carbon_offset_project_certificate_supplier_renewable_energy_commitment
  renewable_energy_requirements:
    - renewable_energy_purchase_contract
    - green_electricity_certificate
    - power_purchase_agreement
    - electricity_emission_factor_record
    - energy_attribute_certificate_retirement
    - carbon_offset_project_certificate
    - supplier_renewable_energy_commitment
  source_refs:
    - docs/harness/evidence/was-real-source-record-monitor-080-20260622.json
    - docs/harness/intake/was-real-source-record-candidate-template.yaml
  validator_refs:
    - tools/kds-sync/validate_was_real_source_record_monitor_080.py
  waes_gate: blocked_without_kds_bound_renewable_energy_evidence
  loop_role: evidence_boundary_monitor
  llm_role: candidate_generation_only
  rag_role: controlled_reference_only
  runtime_writeback: blocked_without_kds_bound_renewable_energy_evidence
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
  next_round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-081
  no_write_declaration: no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready
```
