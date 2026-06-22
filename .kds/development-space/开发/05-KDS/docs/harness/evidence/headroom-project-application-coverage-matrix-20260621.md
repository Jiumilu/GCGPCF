---
doc_id: GPCF-DOC-5FD034A1C2
title: Headroom Project Application Coverage Matrix
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md
source_path: docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Project Application Coverage Matrix

## Evidence ID

`HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-20260621`

## 结论

本矩阵把 Headroom dry-run-only 应用路由落到 15 个项目/域，形成项目级应用覆盖、成本来源和阻断边界。

`project_application_coverage_gate | true`，`dry_run_application_gate | true`，`production_admission_gate | false`，`measured_production_tokens | false`。

## 项目覆盖

| project | source_path | dry_run_routes | blocked_routes | l2_saving_rate | production_admission_gate |
|---|---|---:|---:|---:|---|
| GPCF | 02-governance/loop/LOOP_CONTROL_BOARD.md | 3 | 3 | 0.9659 | false |
| KDS | docs/harness/KDS/loop-state.md | 3 | 3 | 0.777273 | false |
| Brain | 09-status/gpcf-project-status-matrix.md | 3 | 3 | 0.994427 | false |
| WAES | 09-status/gpcf-project-status-matrix.md | 3 | 3 | 0.99473 | false |
| GFIS | 08-evidence-samples/GFIS/loop-state.md | 3 | 3 | 0.998611 | false |
| GPC | 09-status/gpcf-project-status-matrix.md | 3 | 3 | 0.996846 | false |
| PVAOS | docs/harness/PVAOS/loop-state.md | 3 | 3 | 0.734615 | false |
| Edge | 03-data-ai-knowledge/GlobalCloud绿色供应链体系Edge接入与安全模型.md | 3 | 3 | 0.899306 | false |
| PKC | docs/harness/PKC/loop-state.md | 3 | 3 | 0.683258 | false |
| XiaoC | docs/harness/XiaoC/loop-state.md | 3 | 3 | 0.69333 | false |
| XGD | docs/harness/XGD/loop-state.md | 3 | 3 | 0.69532 | false |
| XiaoG | docs/harness/XiaoG/loop-state.md | 3 | 3 | 0.678029 | false |
| MMC | docs/harness/MMC/loop-state.md | 3 | 3 | 0.682464 | false |
| Studio | 02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md | 3 | 3 | 0.869509 | false |
| WAS | docs/harness/evidence/was-project-group-admission-20260621.md | 3 | 3 | 0.745947 | false |

## 汇总

- `project_count`: 15
- `projects_with_l2_measurement`: 15
- `projects_with_dry_run_routes`: 15
- `projects_with_production_routes`: 0
- `authorization_action_queue_gate`: false
