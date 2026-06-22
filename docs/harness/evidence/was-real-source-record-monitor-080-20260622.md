---
doc_id: GPCF-DOC-6C0AA90080
title: WAS Real Source Record Monitor 080 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-080-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-080-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 080 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-080` 将绿色供应链覆盖扩展到可再生能源采购合同、绿电证书、购电协议、用电排放因子、能源属性证书注销记录、碳抵消项目证明和供应商绿电承诺证据链。只有补齐这些证据，Ontology 才能安全地把能源采购、绿电属性、碳抵消和供应商能源承诺风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| renewable_energy_purchase_contract_gaps | `0` |
| green_electricity_certificate_gaps | `0` |
| power_purchase_agreement_gaps | `0` |
| electricity_emission_factor_record_gaps | `0` |
| energy_attribute_certificate_retirement_gaps | `0` |
| carbon_offset_project_certificate_gaps | `0` |
| supplier_renewable_energy_commitment_gaps | `0` |
| accepted_for_renewable_energy_profile | `0` |
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

- `renewable_energy_purchase_contract`
- `green_electricity_certificate`
- `power_purchase_agreement`
- `electricity_emission_factor_record`
- `energy_attribute_certificate_retirement`
- `carbon_offset_project_certificate`
- `supplier_renewable_energy_commitment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_080.py
```

## 非声明

- 本证据不创建也不推断可再生能源采购合同、绿电证书、购电协议、用电排放因子、能源属性证书注销记录、碳抵消项目证明或供应商绿电承诺。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-081`
