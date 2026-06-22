---
doc_id: GPCF-DOC-DA0B8578AF
title: CodeGraph 项目群全量覆盖证据
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-project-group-full-coverage-20260621.md
source_path: docs/harness/evidence/codegraph-project-group-full-coverage-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph 项目群全量覆盖证据

本轮执行 `GPCF-CODEGRAPH-PROJECT-GROUP-FULL-FABRIC-001`，将 CodeGraph 定位为 GlobalCloud 项目群 `Code Intelligence Fabric`，覆盖 14 个项目，并固化 Loop/Harness/WAES/KDS/OKF 接入边界。

## 项目群汇总

| 指标 | 值 |
|---|---:|
| repo_count | 14 |
| indexed_repo_count | 14 |
| git_protected_repo_count | 14 |
| up_to_date_repo_count | 12 |
| pending_sync_repo_count | 1 |
| policy_exception_repo_count | 1 |
| codegraph_git_status_entries_total | 0 |
| GlobalCloud Studio included | true |
| WAS included | true |
| status | review_required |

## 仓库状态

| 项目 | index_status | files | nodes | edges | pending_total | .codegraph git entries |
|---|---|---:|---:|---:|---:|---:|
| GlobalCloud GFIS | policy_exception | 1022 | 13152 | 38142 | 1 | 0 |
| GlobalCloud GPC | up_to_date | 70 | 705 | 1995 | 0 | 0 |
| GlobalCloud PVAOS | up_to_date | 604 | 8899 | 28838 | 0 | 0 |
| GlobalCloud WAES | up_to_date | 281 | 3511 | 11298 | 0 | 0 |
| GlobalCloud KDS | up_to_date | 518 | 3499 | 7115 | 0 | 0 |
| GlobalCloud Brain | pending_sync | 153 | 2594 | 6071 | 2 | 0 |
| GlobalCloud PKC | up_to_date | 110 | 1034 | 2685 | 0 | 0 |
| GlobalCloud XiaoC | up_to_date | 1176 | 15520 | 64515 | 0 | 0 |
| GlobalCloud XGD | up_to_date | 181 | 3645 | 9914 | 0 | 0 |
| GlobalCloud XiaoG | up_to_date | 752 | 13943 | 45987 | 0 | 0 |
| GlobalCloud MMC | up_to_date | 84 | 522 | 1083 | 0 | 0 |
| GlobalCoud GPCF | up_to_date | 936 | 10624 | 25210 | 0 | 0 |
| GlobalCloud Studio | up_to_date | 799 | 14513 | 47053 | 0 | 0 |
| WAS世界资产体系 | up_to_date | 30 | 70 | 209 | 0 | 0 |

## 治理产物

- `governance/codegraph/repo-codegraph-registry.yaml`
- `governance/codegraph/agent-codegraph-permissions.yaml`
- `governance/codegraph/waes-codegraph-gates.yaml`
- `governance/codegraph/kds-codegraph-mapping.yaml`
- `docs/codegraph/codegraph-positioning.md`
- `docs/codegraph/codegraph-authorization-model.md`
- `docs/codegraph/codegraph-loop-integration.md`
- `docs/codegraph/codegraph-waes-gate.md`
- `docs/codegraph/codegraph-kds-okf-mapping.md`
- `harness/templates/codegraph-impact-report.yaml`
- `harness/templates/codegraph-evidence-bundle.yaml`
- `loop/templates/loop-task-with-codegraph.yaml`
- `loop/templates/loop-review-with-codegraph.yaml`
- `loop/templates/loop-retrospective-with-codegraph.yaml`

## 边界声明

- CodeGraph 输出只进入 candidate，不直接成为 KDS accepted fact。
- WAES 使用 CodeGraph impact report 作为门禁输入，不把 CodeGraph 当成裁决者。
- 本轮不进入项目内部业务开发。
- 本轮不提交、不推送、不部署。
- 本轮不声明 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004`
