---
doc_id: GPCF-DOC-6301C8DAB8
title: WAS Real Source Record Monitor 008 Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-008-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-008-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 008 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-008` 已建立签发方、责任方、KDS 反链与 runtime site context 一致性监控。

当前仍没有真实 P4 candidate 文件。即使候选字段齐全，缺责任方确认、缺签发方确认、责任方与 runtime site context 不一致、KDS 反链与 runtime site context 不一致，均不得进入 WAES gate 或 GFIS/KWE runtime。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| owner_confirmation_missing | `0` |
| issuer_confirmation_missing | `0` |
| owner_runtime_context_mismatch | `0` |
| kds_backlink_runtime_context_mismatch | `0` |
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

- owner_confirmation_missing：责任方未确认不得提升。
- issuer_confirmation_missing：签发方未确认不得提升。
- owner_runtime_context_mismatch：责任方与 runtime site context 不一致不得提升。
- kds_backlink_runtime_context_mismatch：KDS 反链与 runtime site context 不一致不得提升。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_008.py
```

## 边界

本 evidence 不创建或标记 WAES review、runtime intake、review queue、runtime primary key、verified artifact、accepted、integrated 或 production_ready。
