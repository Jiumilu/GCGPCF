---
doc_id: GPCF-DOC-B067D96D82
title: WAS Real Source Record Monitor 007 Evidence
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-007-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-007-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 007 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-007` 已建立候选重放与 KDS 反链范围监控。

当前仍没有真实 P4 candidate 文件。重复 source record、陈旧 `received_at`、错误 KDS 反链范围的候选不得进入 WAES gate，也不得触发 runtime intake、review queue 或 runtime primary key。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| replayed_source_record_ids | `0` |
| stale_received_at_candidates | `0` |
| wrong_kds_backlink_scope_candidates | `0` |
| nested_candidate_files | `0` |
| sidecar_only_files | `0` |
| unsupported_extension_files | `0` |
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

- replayed_source_record_id：重复 source record 不得作为新事实进入下一门禁。
- stale_received_at：陈旧候选不得绕过人工/业务 owner 复核。
- wrong_kds_backlink_scope：非 `开发/` 受控 KDS 反链不得成为 source-of-record。
- nested_candidate：嵌套目录候选不得绕过 intake 根目录扫描。
- sidecar_only：旁挂说明文件不得替代真实 P4 source-record。
- unsupported_extension：非 JSON/YAML 候选不得进入 P4 gate。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_007.py
```

## 边界

本 evidence 不创建或标记 WAES review、runtime intake、review queue、runtime primary key、verified artifact、accepted、integrated 或 production_ready。
