---
doc_id: GPCF-DOC-1AD952153C
title: WAS Real Source Record Monitor 026 Evidence
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-026-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-026-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 026 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-026` 已建立能源计量、GHG scope 1/2/3、可再生能源证书和排放因子计算方法证据边界。

当前仍没有真实 P4 candidate 文件。任何能耗、碳排、绿电、运输排放、原料排放或碳因子计算结论，都不得由 Ontology、LLM 或 RAG 推断生成，也不得替代 KDS source-of-record。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| energy_meter_record_gaps | `0` |
| scope1_fuel_record_gaps | `0` |
| scope2_electricity_invoice_gaps | `0` |
| scope3_transport_material_record_gaps | `0` |
| renewable_certificate_gaps | `0` |
| emission_factor_method_gaps | `0` |
| accepted_for_energy_carbon_profile | `0` |
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

## 负例

- energy_meter_record_gap：能源计量记录缺失不得提升。
- scope1_fuel_record_gap：Scope 1 燃料记录缺失不得提升。
- scope2_electricity_invoice_gap：Scope 2 电费/电量发票缺失不得提升。
- scope3_transport_material_record_gap：Scope 3 运输或物料记录缺失不得提升。
- renewable_certificate_gap：绿电/可再生能源证书缺失不得提升。
- emission_factor_method_gap：排放因子和计算方法缺失不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck_execution.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_026.py
```

## 边界

本 evidence 不接受无真实 source record 的能源/碳/GHG 画像，不推断能源计量、Scope 1/2/3 排放、绿电证书、排放因子或计算方法，不创建 runtime intake、review queue、WAES review、verified artifact、accepted、integrated 或 production_ready。
