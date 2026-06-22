---
doc_id: GPCF-DOC-102515B96D
title: WAS Real Source Record Monitor 013 Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/was-real-source-record-monitor-013-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-013-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 013 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-013` 已建立绿色供应链全链路证据门禁。

当前仍没有真实 P4 candidate 文件。碳足迹、材料来源、合规证书、绿色金融、供应商-运输-交付追踪和跨链一致性证据均不得由 Ontology、LLM 或 RAG 推断生成，也不得在缺真实 source record 时推进 WAES/GFIS/KWE。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| carbon_evidence_gaps | `0` |
| material_origin_gaps | `0` |
| compliance_certificate_gaps | `0` |
| green_finance_evidence_gaps | `0` |
| supplier_route_delivery_trace_gaps | `0` |
| cross_chain_consistency_gaps | `0` |
| accepted_for_green_supply_chain_profile | `0` |
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

- carbon_evidence_gap：碳足迹证据缺失不得提升。
- material_origin_gap：材料来源证据缺失不得提升。
- compliance_certificate_gap：合规证书证据缺失不得提升。
- green_finance_evidence_gap：绿色金融凭证缺失不得提升。
- supplier_route_delivery_trace_gap：供应商-运输-交付不可追踪不得提升。
- cross_chain_consistency_gap：碳、材料、合规、金融链路不一致不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_013.py
```

## 边界

本 evidence 不接受无真实 source record 的绿色供应链画像，不推断碳足迹、材料来源、合规证书或绿色金融证据，不创建 runtime intake、review queue、WAES review、verified artifact、accepted、integrated 或 production_ready。
