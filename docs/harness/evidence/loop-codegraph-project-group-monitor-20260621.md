---
doc_id: GPCF-DOC-D83747FB28
title: Loop CodeGraph Project Group Monitor Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.md
source_path: docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Project Group Monitor Evidence

## Evidence ID

`LOOP-CODEGRAPH-PROJECT-GROUP-MONITOR-20260621`

## 结论

本轮执行 `GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001` 后追加受控 `.codegraph` 同步复核，只维护 CodeGraph 本地索引，不进入任何项目内部开发。

14 个仓库仍全部有 `.codegraph/` 本地索引，全部通过 `.git/info/exclude` 保护，`.codegraph/` Git 状态总数为 `0`。

当前监控结果为 `project_group_codegraph_monitor_pass_with_active_watchlist`：11 仓 up-to-date，2 仓 Brain 与 Studio 活动 pending sync watchlist，1 仓 GFIS controlled residual。

## 项目群状态

| 指标 | 数值 |
|---|---:|
| repo_count | 14 |
| indexed_repo_count | 14 |
| git_protected_repo_count | 14 |
| codegraph_git_status_entries_total | 0 |
| up_to_date_repo_count | 11 |
| pending_sync_repo_count | 2 |
| policy_exception_repo_count | 1 |

## 当前 watchlist 与 residual

| 项目 | 状态 | 说明 |
|---|---|---|
| GlobalCloud Brain | pending_sync | 受控 `.codegraph` 同步复核后出现 `Modified: 32 files`，登记为活动仓漂移，不进入 Brain 业务开发 |
| GlobalCloud Studio | pending_sync | 受控 `.codegraph` 同步复核后再次出现 `Added: 2 files; Modified: 2 files`，登记为活动仓漂移，不进入 Studio 业务开发 |
| GlobalCloud GFIS | policy_exception | `Added: 1 files`，按 `LOOP_CODEGRAPH_LARGE_FILE_POLICY.md` 解释为 `large_generated_validator_exception_candidate` |

GFIS policy exception 保持受控，不作为项目群图谱覆盖失败处理。

Brain 活动漂移与 Studio 活动漂移均已进入下一轮 watchlist。

## 已清空 watchlist

| 项目 | 当前状态 | 说明 |
|---|---|---|
| GlobalCoud GPCF | up_to_date | 已完成受控 `.codegraph` 同步复核 |

## 非声明

- 本轮只执行受控 `.codegraph` 同步复核。
- 本轮未修改 Brain、GFIS、Studio 或其他项目业务代码。
- 本轮未重构、拆分或删除 GFIS validator。
- 本轮未提交、未推送、未部署。
- 本轮不升级 `accepted`、`integrated` 或 `production_ready`。

## 下一轮输入

`GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`：持续监控 Brain 与 Studio 活动 CodeGraph drift，GFIS 继续保持 policy exception；不进入项目业务开发。
