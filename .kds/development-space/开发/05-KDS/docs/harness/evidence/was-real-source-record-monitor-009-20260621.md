---
doc_id: GPCF-DOC-283E587802
title: WAS Real Source Record Monitor 009 Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-009-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-009-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 009 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-009` 已建立多候选批次冲突监控。

当前仍没有真实 P4 candidate 文件。多候选并发、同一订单多个版本、跨客户混合候选、候选字段冲突，均不得被自动合并、自动进入 WAES gate 或自动写入 GFIS/KWE runtime。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| parallel_candidate_files | `0` |
| same_order_multiple_versions | `0` |
| cross_customer_mixed_candidates | `0` |
| conflicting_candidate_fields | `0` |
| missing_attachment_evidence_refs | `0` |
| source_record_hash_mismatch | `0` |
| source_refs_evidence_refs_mismatch | `0` |
| kds_backlink_source_refs_mismatch | `0` |
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

- parallel_candidate_files：多候选并发不得自动合并。
- same_order_multiple_versions：同一订单多个版本不得自动取最新版提升。
- cross_customer_mixed_candidates：跨客户混合候选不得进入同一 source-record gate。
- conflicting_candidate_fields：字段冲突不得由 LLM 自动裁决。
- missing_attachment_evidence_ref：缺附件 evidence ref 不得提升。
- source_record_hash_mismatch：source hash 不一致不得提升。
- source_evidence_ref_mismatch：sourceRefs 与 evidenceRefs 不一致不得提升。
- kds_backlink_source_ref_mismatch：KDS 反链与 sourceRefs 不一致不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_009.py
```

## 边界

本 evidence 不合并候选，不创建或标记 WAES review、runtime intake、review queue、runtime primary key、verified artifact、accepted、integrated 或 production_ready。
