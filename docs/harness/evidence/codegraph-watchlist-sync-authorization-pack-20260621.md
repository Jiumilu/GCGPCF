---
doc_id: GPCF-DOC-89B4FED3DA
title: CodeGraph Watchlist Sync Authorization Pack Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-watchlist-sync-authorization-pack-20260621.md
source_path: docs/harness/evidence/codegraph-watchlist-sync-authorization-pack-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Watchlist Sync Authorization Pack Evidence

本轮执行 `GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002`。目标是为 Brain/Studio 的 CodeGraph watchlist active drift 生成 sync-only 授权包。

本轮不执行 Brain/Studio `codegraph sync`，不进入任何项目业务开发，不提交、不推送、不部署，不升级 accepted / integrated / production_ready。

## Required Authorization Phrase

`授权执行 Brain/Studio CodeGraph watchlist sync-only closure`

未收到该口令前，状态为 `authorization_pack_ready`，决策为 `do_not_execute_brain_or_studio_codegraph_sync`。

## Preflight

| repo | pending | classification | `.codegraph` Git status |
|---|---|---|---|
| GlobalCloud Brain | added=0 / modified=11 / removed=0 | active_drift_action_required | empty |
| GlobalCloud Studio | added=0 / modified=5 / removed=0 | active_drift_action_required | empty |
| GlobalCloud GFIS | added=1 / modified=0 / removed=0 | policy_exception_watch | empty |
| GlobalCoud GPCF | added=0 / modified=0 / removed=0 | self_sync_clear | empty |

## Allowed Before Authorization

- `codegraph status --json .`
- `git status --short -- .codegraph`
- GPCF evidence / validator / 文档治理
- GPCF governance evidence 生成后的本仓 CodeGraph self-sync

## Forbidden Before Authorization

- Brain `codegraph sync`
- Studio `codegraph sync`
- Brain/Studio 业务代码编辑
- GFIS policy exception repair
- `git add`、commit、push、deploy
- accepted / integrated / production_ready 升级

## 下一轮

收到授权口令后，才进入：

`GPCF-CODEGRAPH-WATCHLIST-SYNC-ONLY-CLOSURE-003-AUTHORIZED`
