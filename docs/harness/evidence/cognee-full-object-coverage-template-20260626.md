---
doc_id: GPCF-DOC-5BB0B82415
title: Cognee 全量对象覆盖模板 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-full-object-coverage-template-20260626.md
source_path: docs/harness/evidence/cognee-full-object-coverage-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 全量对象覆盖模板 2026-06-26

## 1. 当前结论

`cognee_full_object_coverage_template = prepared`

本文为 `COGNEE-FULL-RUN-GAP-002` 建立全量对象覆盖模板。当前覆盖状态为 `template_only`，不表示全量对象已经覆盖。

## 2. 模板文件

- JSON: `fixtures/cognee/cognee-full-object-coverage-template.json`
- validator: `tools/kds-sync/validate_cognee_full_object_coverage_template.py`
- source admission package: `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- source full-run ledger: `fixtures/cognee/cognee-full-run-ledger-template.json`

## 3. 覆盖字段

| field | current_value |
|---|---|
| `coverage_id` | `COGNEE-FULL-OBJECT-COVERAGE-YYYYMMDD-NNN` |
| `coverage_scope` | `cognee_full_run_candidate_objects` |
| `object_inventory_source` | `REQUIRED_FULL_OBJECT_INVENTORY_SOURCE` |
| `total_object_count` | `0` |
| `in_scope_object_count` | `0` |
| `excluded_object_count` | `0` |
| `covered_object_count` | `0` |
| `uncovered_object_count` | `0` |
| `coverage_rate` | `0.0` |
| `coverage_status` | `template_only` |

## 4. 覆盖成立条件

| item | requirement |
|---|---|
| object inventory | 必须有真实全量对象清单来源 |
| object groups | 必须按项目、域、对象类型或业务边界分组 |
| exclusion records | 排除对象必须有原因和责任人 |
| coverage rate | 必须由 `covered_object_count / in_scope_object_count` 得出 |
| ledger linkage | 必须能回链 full-run ledger |

## 5. 状态边界

| field | value |
|---|---|
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 6. 非声明

- 不声明全量对象已覆盖
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
