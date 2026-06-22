---
doc_id: GPCF-DOC-0D6920E7D2
title: CodeGraph 项目群稳态验证证据
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-project-group-steady-state-verify-20260621.md
source_path: docs/harness/evidence/codegraph-project-group-steady-state-verify-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph 项目群稳态验证证据

本轮执行 `GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004`。范围仅限 CodeGraph 项目群稳态验证与实际作用评估，不进入任何项目业务开发，不提交、不推送、不部署。

## 稳态汇总

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
| GlobalCloud Brain | pending_sync | 153 | 2594 | 6071 | 5 | 0 |
| GlobalCloud PKC | up_to_date | 110 | 1034 | 2685 | 0 | 0 |
| GlobalCloud XiaoC | up_to_date | 1176 | 15520 | 64515 | 0 | 0 |
| GlobalCloud XGD | up_to_date | 181 | 3645 | 9914 | 0 | 0 |
| GlobalCloud XiaoG | up_to_date | 752 | 13943 | 45987 | 0 | 0 |
| GlobalCloud MMC | up_to_date | 84 | 522 | 1083 | 0 | 0 |
| GlobalCoud GPCF | up_to_date | 961 | 10718 | 25469 | 0 | 0 |
| GlobalCloud Studio | up_to_date | 799 | 14513 | 47053 | 0 | 0 |
| WAS世界资产体系 | up_to_date | 30 | 70 | 209 | 0 | 0 |

## 实际作用评估

| 能力 | 本轮证据 | 判定 |
|---|---|---|
| 项目群覆盖 | 14 仓均可 `codegraph status --json .`，且 `.codegraph` 未进入 Git | pass |
| 漂移可见性 | Brain 活动漂移被识别为 watchlist；GFIS residual 被保留为 policy exception | pass |
| Loop 接入 | Loop schema 已要求 snapshot、query、impact、test、risk 和 evidence 字段 | pass |
| Harness 接入 | impact report 与 evidence bundle 模板已存在 | pass |
| WAES 接入 | 高风险权限、租户、资金、KDS、Ontology、API、Harness、Loop 变更需要 CodeGraph 输入 | pass |
| KDS/OKF 接入 | CodeGraph 输出仅作为 candidate，升格需要 Harness evidence、WAES gate 和 human review | pass |
| 成本与质量改进 | 已具备低风险 impact-report dry-run 条件，但尚未形成量化成本 delta | next_round_required |

## 保留边界

- 本轮不进入项目业务开发。
- 本轮不提交、不推送、不部署。
- 本轮不把 CodeGraph 输出直接升级为 KDS accepted fact。
- 本轮不声明 accepted、integrated 或 production_ready。
- Brain 活动漂移进入下一轮 watchlist。
- GFIS policy exception 继续受控，不作为项目群覆盖失败。

## 下一轮输入

`GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005`
