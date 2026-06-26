---
doc_id: GPCF-DOC-ED57C64A4C
title: Cognee 全量场景矩阵模板 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-full-scenario-matrix-template-20260626.md
source_path: docs/harness/evidence/cognee-full-scenario-matrix-template-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 全量场景矩阵模板 2026-06-26

## 1. 当前结论

`cognee_full_scenario_matrix_template = prepared`

本文为 `COGNEE-FULL-RUN-GAP-003` 建立全量场景矩阵模板。当前矩阵状态为 `template_only`，不表示全量场景已经执行或通过。

## 2. 模板文件

- JSON: `fixtures/cognee/cognee-full-scenario-matrix-template.json`
- validator: `tools/kds-sync/validate_cognee_full_scenario_matrix_template.py`
- source admission package: `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- source full-run ledger: `fixtures/cognee/cognee-full-run-ledger-template.json`
- source object coverage: `fixtures/cognee/cognee-full-object-coverage-template.json`

## 3. 场景字段

| field | current_value |
|---|---|
| `scenario_matrix_id` | `COGNEE-FULL-SCENARIO-MATRIX-YYYYMMDD-NNN` |
| `scenario_scope` | `cognee_full_run_candidate_scenarios` |
| `scenario_inventory_source` | `REQUIRED_FULL_SCENARIO_INVENTORY_SOURCE` |
| `total_scenario_count` | `0` |
| `in_scope_scenario_count` | `0` |
| `excluded_scenario_count` | `0` |
| `passed_scenario_count` | `0` |
| `failed_scenario_count` | `0` |
| `untested_scenario_count` | `0` |
| `pass_rate` | `0.0` |
| `scenario_matrix_status` | `template_only` |

## 4. 场景矩阵成立条件

| item | requirement |
|---|---|
| scenario inventory | 必须有真实全量场景清单来源 |
| scenario groups | 必须按业务场景、异常场景、回滚场景或运营场景分组 |
| failure records | 失败场景必须记录原因、责任方和处置入口 |
| exclusion records | 排除场景必须有原因和审批边界 |
| pass rate | 必须由 `passed_scenario_count / in_scope_scenario_count` 得出 |
| ledger linkage | 必须能回链 full-run ledger |
| object coverage linkage | 必须能回链 full object coverage |

## 5. 状态边界

| field | value |
|---|---|
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 6. 非声明

- 不声明全量场景已执行
- 不声明全量场景已通过
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
