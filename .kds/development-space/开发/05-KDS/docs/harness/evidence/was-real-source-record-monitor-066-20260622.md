---
doc_id: GPCF-DOC-6C0AA90066
title: WAS Real Source Record Monitor 066 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-066-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-066-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 066 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-066` 将绿色供应链覆盖扩展到绿色采购与生态标签市场准入链：绿色采购资格、生态标签证书、产品环境声明、公共招标绿色准则映射、绿色采购合同条款、生命周期成本与环境评分、供应商绿色承诺。只有补齐这些证据，Ontology 才能安全地把绿色采购准入、生态标签、环境声明、招标准则、合同承诺、生命周期评分和供应商责任绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| green_procurement_eligibility_gaps | `0` |
| ecolabel_certificate_gaps | `0` |
| product_environmental_declaration_gaps | `0` |
| public_tender_green_criteria_mapping_gaps | `0` |
| green_procurement_contract_clause_gaps | `0` |
| lifecycle_cost_environmental_score_gaps | `0` |
| supplier_green_commitment_gaps | `0` |
| accepted_for_green_procurement_profile | `0` |
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

- `green_procurement_eligibility`
- `ecolabel_certificate`
- `product_environmental_declaration`
- `public_tender_green_criteria_mapping`
- `green_procurement_contract_clause`
- `lifecycle_cost_environmental_score`
- `supplier_green_commitment`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_066.py
```

## 非声明

- 本证据不创建也不推断绿色采购资格、生态标签证书、产品环境声明、公共招标绿色准则映射、绿色采购合同条款、生命周期成本与环境评分或供应商绿色承诺。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-067`
