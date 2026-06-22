---
doc_id: GPCF-DOC-6C0AA90060
title: WAS Real Source Record Monitor 060 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-060-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-060-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 060 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-061` 将绿色供应链覆盖扩展到绿色电力与能源属性链：绿色电力采购合同、能源消耗计量记录、绿电证书、可再生能源证书注销证明、现场发电计量记录、能源结构分摊记录和电网排放因子来源。只有补齐这些证据，Ontology 才能安全地把绿色电力采购、能源属性、证书注销、现场发电计量、能源结构分摊和电网排放因子绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| renewable_energy_contract_gaps | `0` |
| energy_consumption_meter_record_gaps | `0` |
| green_power_certificate_gaps | `0` |
| renewable_energy_certificate_retirement_gaps | `0` |
| onsite_generation_meter_record_gaps | `0` |
| energy_mix_allocation_record_gaps | `0` |
| grid_emission_factor_source_gaps | `0` |
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

- `renewable_energy_contract`
- `energy_consumption_meter_record`
- `green_power_certificate`
- `renewable_energy_certificate_retirement`
- `onsite_generation_meter_record`
- `energy_mix_allocation_record`
- `grid_emission_factor_source`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_060.py
```

## 非声明

- 本证据不创建也不推断绿色电力采购合同、能源消耗计量记录、绿电证书、可再生能源证书注销证明、现场发电计量记录、能源结构分摊记录或电网排放因子来源。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-061`
