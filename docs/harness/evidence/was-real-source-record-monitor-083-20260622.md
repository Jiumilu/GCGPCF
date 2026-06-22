---
doc_id: GPCF-DOC-6C0AA90083
title: WAS Real Source Record Monitor 083 证据
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: ontology-governance
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-083-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-083-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 083 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-083` 将绿色供应链覆盖扩展到限制物质声明、RoHS 合规证书、REACH SVHC 声明、材料安全数据表、化学品清单记录、物质检测报告和供应商化学合规承诺证据链。只有补齐这些证据，Ontology 才能安全地把限制物质、RoHS、REACH、MSDS、化学品清单和供应商化学合规风险绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| restricted_substance_declaration_gaps | `0` |
| rohs_compliance_certificate_gaps | `0` |
| reach_svhc_statement_gaps | `0` |
| material_safety_data_sheet_gaps | `0` |
| chemical_inventory_record_gaps | `0` |
| substance_test_report_gaps | `0` |
| supplier_chemical_compliance_commitment_gaps | `0` |
| accepted_for_chemical_compliance_profile | `0` |
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

- `restricted_substance_declaration`
- `rohs_compliance_certificate`
- `reach_svhc_statement`
- `material_safety_data_sheet`
- `chemical_inventory_record`
- `substance_test_report`
- `supplier_chemical_compliance_commitment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_083.py
```

## 非声明

- 本证据不创建也不推断限制物质声明、RoHS 合规证书、REACH SVHC 声明、材料安全数据表、化学品清单记录、物质检测报告或供应商化学合规承诺。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-084`
