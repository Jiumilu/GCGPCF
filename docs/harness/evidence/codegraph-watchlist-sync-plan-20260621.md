---
doc_id: GPCF-DOC-481D44CB8A
title: CodeGraph Watchlist Sync Plan Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.md
source_path: docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph Watchlist Sync Plan Evidence

本轮执行 `GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001`，目标是把上一轮 `pass_with_watch` 的 CodeGraph watch 项转成 owner / threshold / action 计划。

本轮不执行 Brain/Studio `codegraph sync`，不进入任何项目业务开发，不提交、不推送、不部署，不升级 accepted / integrated / production_ready。

## Watchlist Matrix

| repo | owner | current pending | classification | action |
|---|---|---|---|---|
| GlobalCloud Brain | Brain repo owner + GPCF CodeGraph steward | added=0 / modified=12 / removed=0 | active_drift_action_required | prepare_sync_authorization_pack |
| GlobalCloud Studio | Studio repo owner + GPCF CodeGraph steward | added=0 / modified=5 / removed=0 | active_drift_action_required | prepare_sync_authorization_pack |
| GlobalCloud GFIS | GFIS runtime owner + GPCF CodeGraph steward | added=1 / modified=0 / removed=0 | policy_exception_watch | keep_policy_exception_watch |
| GlobalCoud GPCF | GPCF governance owner | added=0 / modified=0 / removed=0 | self_sync_clear | continue_self_sync_after_each_governance_round |

## Authorization Boundary

Brain/Studio 再次 sync 需要新的明确授权口令：

`授权执行 Brain/Studio CodeGraph watchlist sync-only closure`

未收到该口令前，只允许：

- `codegraph status --json .`
- `git status --short -- .codegraph`
- GPCF evidence / validator / 文档治理

## 非声明

- 本轮不证明任何业务功能完成。
- 本轮不修复 GFIS runtime 或 policy exception。
- 本轮不执行生产写入、真实外部 API 或部署。
- 本轮不执行 `git add`、commit、push。

## 下一轮

进入 `GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002`。
