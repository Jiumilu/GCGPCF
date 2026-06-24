---
doc_id: GPCF-DOC-9B884D2365
title: OKF v0.1 关系图谱证据
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-relationship-graph-20260620.md
source_path: docs/harness/evidence/okf-v01-relationship-graph-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# OKF v0.1 关系图谱证据

generated_at: 2026-06-21T00:41:44.528518+00:00

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| bundles | 3 |
| concepts | 81 |
| nodes | 186 |
| edges | 303 |
| duplicate_source_count | 30 |
| json | `docs/harness/evidence/okf-v01-relationship-graph-20260620.json` |

## Bundle 覆盖

| bundle | concepts |
| --- | ---: |
| architecture | 6 |
| governance | 39 |
| kds | 36 |

## 边类型

| edge_type | count |
| --- | ---: |
| bundle_contains_concept | 81 |
| concept_derives_from_source | 81 |
| concept_targets_kds_path | 81 |
| same_source_multi_bundle_view | 60 |

## 多 bundle 来源视图

以下来源文档会按设计同时出现在多个 bundle 中，作为限定范围视图使用。该做法成立的前提是 KDS/Git 始终保持 source of record 地位。

| source_path |
| --- |
| `09-status/kds-phase10-governance-sustainment-plan.md` |
| `09-status/odf-introduction-governance-plan.md` |
| `09-status/odf-phase2-expansion-plan.md` |
| `09-status/odf-phase3-schema-gate-plan.md` |
| `09-status/odf-phase4-small-batch-admission-plan.md` |
| `09-status/odf-phase5-change-request-governance-plan.md` |
| `09-status/odf-phase6-manual-confirmation-workbench-plan.md` |
| `09-status/odf-phase7-small-batch-execution-plan.md` |
| `09-status/odf-phase8-drift-monitoring-plan.md` |
| `09-status/odf-phase9-dynamic-source-stabilization-plan.md` |
| `docs/harness/evidence/kds-md-okf-odf-full-closure-report-20260619.md` |
| `docs/harness/evidence/kds-phase10-backlog-triage-20260619.md` |
| `docs/harness/evidence/kds-phase10-self-refresh-stabilization-workpack-20260619.md` |
| `docs/harness/evidence/odf-phase2-closure-report-20260617.md` |
| `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` |
| `docs/harness/evidence/odf-phase3-schema-gate-20260617.md` |
| `docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` |
| `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` |
| `docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` |
| `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` |

## 边界

- 本 graph 是派生 evidence，不是 source of record。
- 在作出事实判断前，OKF nodes 必须回溯到 `source_path` 与 `kds_path`。
- 本 evidence 不升级业务、验收或集成状态。
