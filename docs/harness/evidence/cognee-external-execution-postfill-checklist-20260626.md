---
doc_id: GPCF-DOC-0A73F98BE4
title: Cognee 外部执行回填检查清单 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-external-execution-postfill-checklist-20260626.md
source_path: docs/harness/evidence/cognee-external-execution-postfill-checklist-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 外部执行回填检查清单 2026-06-26

## 1. 当前结论

`cognee_external_execution_postfill_checklist = ready`

本文把真实外部执行后的回填动作压缩成受控检查清单，确保回执、evidence 和状态边界同步，不因回填而误升级 full-run 结论。

## 2. 回填前检查

| step | requirement |
|---|---|
| 1 | 再次确认 `validate_cognee_p4_live_authorization_signoff.py --require-complete-signoff` 为 `pass_complete` |
| 2 | 再次确认 `validate-cognee-p4-real-writeback-live.py --input ...` 为 `pass` |
| 3 | 再次确认 `validate_cognee_external_execution_integration_intake.py --require-complete-intake` 为 `pass_complete` |
| 4 | 取得唯一 `receipt_id` |
| 5 | 取得真实 `executed_at`、`execution_count`、`error_count`、`rollback_triggered` |

## 3. 回填动作

| step | action |
|---|---|
| 1 | 按正式模板填写真实执行回执 |
| 2 | 在 postfill evidence 草稿中回填 preflight 结果 |
| 3 | 在 postfill evidence 草稿中回填执行结果 |
| 4 | 若 `rollback_triggered=true`，补 `rollback_evidence` |
| 5 | 将本轮结论限定为 `external_execution_validation_recorded`，不得直接提升到 `full_run_complete` |

## 4. 回填后必须复核

| item | expected_state |
|---|---|
| `production_write` | `false`，除非另有独立 production receipt |
| `accepted` | `false`，除非 Harness 单独裁决 |
| `integrated` | `false`，除非 WAES 单独裁决 |
| `production_ready` | `false`，除非 full-run gap 全部关闭 |
| `full_run_claim` | `false`，除非全量运行链路另行完成 |

## 5. 非声明

- 不把外部执行验证回执等同于 full-run 回执
- 不把 postfill 完成等同于 `accepted`
- 不把 postfill 完成等同于 `integrated`
- 不把 postfill 完成等同于 `production_ready`
