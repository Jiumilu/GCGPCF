---
doc_id: GPCF-DOC-408248DB31
title: WAS Real Source Record Monitor 006 Evidence
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/was-real-source-record-monitor-006-20260621.md
source_path: docs/harness/evidence/was-real-source-record-monitor-006-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 006 Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-006` 已建立候选目录卫生监控。

当前仍没有真实 P4 candidate 文件。隐藏文件、临时文件、LLM-only 文件不得绕过 `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001`，也不得触发 WAES review、runtime intake、review queue 或 runtime primary key。

## 监控指标

| 指标 | 值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| disallowed_hidden_files | `0` |
| disallowed_temporary_files | `0` |
| disallowed_llm_only_files | `0` |
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

- hidden_file：隐藏候选文件不得绕过目录扫描。
- temporary_file：临时/草稿候选文件不得进入 P4 gate。
- llm_only_file：LLM-only 文件不得成为 source-of-record。

## 必跑命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_006.py
```

## 边界

本 evidence 不创建或标记 WAES review、runtime intake、review queue、runtime primary key、verified artifact、accepted、integrated 或 production_ready。
