---
doc_id: GPCF-DOC-2E7C6F89D0
title: Cognee 生产状态提升证据模板 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-production-state-promotion-evidence-template-20260626.md
source_path: docs/harness/evidence/cognee-production-state-promotion-evidence-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 生产状态提升证据模板 2026-06-26

## 1. 当前结论

`cognee_production_state_promotion_template = prepared`

本文为 `COGNEE-FULL-RUN-GAP-004` 建立生产状态提升证据模板。当前状态为 `template_only`，不表示任何生产状态已经提升。

## 2. 模板文件

- JSON: `fixtures/cognee/cognee-production-state-promotion-evidence-template.json`
- validator: `tools/kds-sync/validate_cognee_production_state_promotion_template.py`
- source admission package: `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- source full-run ledger: `fixtures/cognee/cognee-full-run-ledger-template.json`
- source object coverage: `fixtures/cognee/cognee-full-object-coverage-template.json`
- source scenario matrix: `fixtures/cognee/cognee-full-scenario-matrix-template.json`

## 3. 提升字段

| field | current_value |
|---|---|
| `promotion_evidence_id` | `COGNEE-PRODUCTION-STATE-PROMOTION-YYYYMMDD-NNN` |
| `promotion_scope` | `cognee_full_run_candidate_state_promotion` |
| `waes_decision.decision` | `pending` |
| `harness_decision.decision` | `pending` |
| `rollback_entry` | `return_to_cognee_full_run_admission_not_admitted` |
| `promotion_status` | `template_only` |

## 4. 状态提升成立条件

| item | requirement |
|---|---|
| external execution receipt | 必须是真实外部执行回执，不接受样例回执 |
| full-run ledger | 必须是真实账本，不接受 `template_only` |
| object coverage | 必须是真实全量对象覆盖，不接受 `template_only` |
| scenario matrix | 必须是真实全量场景矩阵，不接受 `template_only` |
| WAES decision | 必须有明确 `pass` 或 `approved` evidence |
| Harness decision | 必须有明确 `pass`、`approved` 或 `accepted` evidence |
| rollback plan | 必须有回退入口、责任人和触发条件 |

## 5. 状态边界

| field | value |
|---|---|
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 6. 非声明

- 不声明生产状态已经提升
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
