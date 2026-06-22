---
doc_id: GPCF-DOC-6C0AA90051
title: WAS Real Source Record Monitor 051 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-051-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-051-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 051 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-051` 将绿色供应链覆盖扩展到供应商主数据批准、供应商合同协议、银行账户核验、税务登记记录、制裁筛查结果、出口管制筛查和供应商准入批准证据层。只有补齐这些证据，Ontology 才能安全地把供应商正式准入、交易开户、合规筛查和采购合作状态绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| supplier_master_data_approval_gaps | `0` |
| supplier_contract_agreement_gaps | `0` |
| bank_account_verification_gaps | `0` |
| tax_registration_record_gaps | `0` |
| sanctions_screening_result_gaps | `0` |
| export_control_screening_gaps | `0` |
| supplier_onboarding_approval_gaps | `0` |
| accepted_for_supplier_onboarding_profile | `0` |
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

- `supplier_master_data_approval`
- `supplier_contract_agreement`
- `bank_account_verification`
- `tax_registration_record`
- `sanctions_screening_result`
- `export_control_screening`
- `supplier_onboarding_approval`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_051.py
```

## 非声明

- 本证据不创建也不推断供应商主数据批准、供应商合同协议、银行账户核验、税务登记记录、制裁筛查结果、出口管制筛查或供应商准入批准证据。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-052`
