---
doc_id: GPCF-DOC-BCB0F95687
title: GPCF CodeGraph Watchlist Sync Plan Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-watchlist-sync-plan-20260621.md
source_path: docs/harness/evidence/loop-codegraph-watchlist-sync-plan-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Watchlist Sync Plan Evidence

## 结论

本轮状态为 `watchlist_sync_plan_defined`。

本轮未执行 `codegraph sync`。本轮只固化 Brain、Studio、GPCF 的 watchlist 同步授权门，并保持 GFIS policy exception 不变。

## 范围

- 输入轮次：`GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001`
- 来源证据：`docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.json`
- CodeGraph 版本：`1.0.1`
- 模式：只读检查与计划固化
- 项目内部开发：未进入

## Watchlist 决策

| 项目 | 当前索引 | 当前 pending notice | `.codegraph` Git 状态 | 决策 |
| --- | --- | --- | --- | --- |
| GlobalCloud Brain | 152 files / 2415 nodes / 5733 edges | Modified: 5 files | 0 | defer_sync_until_explicit_authorization |
| GlobalCloud Studio | 787 files / 14326 nodes / 46805 edges | Added: 5 files; Modified: 6 files | 0 | defer_sync_until_explicit_authorization |
| GlobalCoud GPCF | 808 files / 9096 nodes / 20915 edges | Added: 3 files; Modified: 5 files | 0 | defer_sync_until_watchlist_sync_authorized |

## Policy Exception

| 项目 | 当前索引 | 当前 pending notice | `.codegraph` Git 状态 | 决策 |
| --- | --- | --- | --- | --- |
| GlobalCloud GFIS | 1022 files / 13152 nodes / 38142 edges | Added: 1 files | 0 | keep_policy_exception_no_sync |

GFIS 保持 `large_generated_validator_exception_candidate` 策略例外。本轮不重构、不删除、不排除、不同步 GFIS 的大文件 validator candidate。

## 授权门

下一轮如需执行 sync，必须明确进入 `GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-001`，并只允许：

- Brain：`codegraph sync`
- Studio：`codegraph sync`
- GPCF：`codegraph sync`
- 执行后重新运行项目群 monitor
- 在 GPCF 中记录 sync evidence 与 Loop 下一轮输入

下一轮仍禁止：

- 项目业务代码修改
- GFIS validator refactor
- GFIS `codegraph sync`
- 删除 generated validator
- commit / push / deploy
- accepted / integrated / production_ready 状态升级

## 风险边界

`codegraph sync` 是本地 `.codegraph/` 索引刷新。Brain、Studio、GPCF 当前均存在 dirty worktree 漂移，因此任何 sync 只能解释为“索引当前本机状态的快照”，不能解释为项目完成、验收通过或生产就绪。

## Loop 下一轮输入

`GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-001`

目标：如果用户明确授权，则仅对 Brain、Studio、GPCF 执行 CodeGraph sync，然后重新运行项目群 monitor。GFIS 保持 policy exception，不进入任何项目内部开发任务。
