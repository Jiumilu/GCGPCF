---
doc_id: GPCF-DOC-42F84B1E32
title: WAS Real Source Record Monitor 032 Evidence
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-032-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-032-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 032 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-032` 已建立销售发票、付款回执、贷项/折让调整、税务申报、绿色补贴/碳资产收益和保险理赔证据边界。

当前仍没有真实 P4 candidate 文件。任何发票、付款、折让、税务、补贴/碳资产收益或保险理赔事实，都不得由 Ontology、LLM 或 RAG 推断生成，也不得替代 KDS source-of-record。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| sales_invoice_gaps | `0` |
| payment_receipt_gaps | `0` |
| credit_note_or_adjustment_gaps | `0` |
| tax_filing_record_gaps | `0` |
| green_subsidy_or_carbon_credit_revenue_record_gaps | `0` |
| insurance_claim_record_gaps | `0` |
| accepted_for_financial_settlement_profile | `0` |
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

- sales_invoice_gap：销售发票缺失不得提升。
- payment_receipt_gap：付款回执缺失不得提升。
- credit_note_or_adjustment_gap：贷项/折让调整缺失不得提升。
- tax_filing_record_gap：税务申报记录缺失不得提升。
- green_subsidy_or_carbon_credit_revenue_record_gap：绿色补贴或碳资产收益记录缺失不得提升。
- insurance_claim_record_gap：保险理赔记录缺失不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
```

## 边界

本 evidence 不接受无真实 source record 的财税/结算/资金流画像，不推断销售发票、付款回执、贷项/折让、税务申报、绿色补贴/碳资产收益或保险理赔，不创建 runtime intake、review queue、WAES review、verified artifact、accepted、integrated 或 production_ready。
