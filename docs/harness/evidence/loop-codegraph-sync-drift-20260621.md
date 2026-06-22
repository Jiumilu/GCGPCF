---
doc_id: GPCF-DOC-2DAF142553
title: Loop CodeGraph Sync Drift Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-sync-drift-20260621.md
source_path: docs/harness/evidence/loop-codegraph-sync-drift-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Sync Drift Evidence

## Evidence ID

`LOOP-CODEGRAPH-SYNC-DRIFT-20260621`

## 结论

本轮执行 `GPCF-CODEGRAPH-SYNC-DRIFT-001`，先对上一轮登记的 pending-sync 仓运行 `codegraph sync`：Brain、GFIS、KDS、Studio；随后对新增 GPCF 证据与 validator 产生的 GPCF 本仓 CodeGraph drift 执行同步收口。

同步后 Brain、KDS、Studio、GPCF 已恢复 up-to-date。GFIS 重复同步后仍保留 CodeGraph 内部提示：`Added: 1 files`，但每次 sync 输出均为 `Added: 1 - 0 nodes`，且 `.codegraph/` 未进入 Git 状态。本轮将 GFIS 记为 `residual_pending_notice`，不作为 CodeGraph 部署失败，也不进入 GFIS 项目开发修复。

## 同步结果

| 项目 | 同步结果 |
|---|---|
| GlobalCloud Brain | up_to_date |
| GlobalCloud GFIS | residual_pending_notice |
| GlobalCloud KDS | up_to_date |
| GlobalCloud Studio | up_to_date |
| GlobalCoud GPCF | up_to_date |

## 项目群状态

| 指标 | 数值 |
|---|---:|
| repo_count | 13 |
| indexed_repo_count | 13 |
| git_protected_repo_count | 13 |
| codegraph_git_status_entries_total | 0 |
| up_to_date_repo_count | 12 |
| residual_pending_notice_repo_count | 1 |
| pending_sync_repo_count | 0 |

## 下一轮输入

| 字段 | 内容 |
|---|---|
| Round | `GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001` |
| Objective | 只在集成层调查 GFIS CodeGraph `Added: 1 files / 0 nodes` 残留提示 |
| Allowed | `codegraph status`、CodeGraph 缓存/忽略规则检查、GPCF evidence 更新 |
| Forbidden | GFIS 业务代码修改、测试/构建修复、提交、推送、部署、状态升级 |

## 非声明

- 本轮未修改 Brain、GFIS、KDS、Studio 的业务代码。
- 本轮未运行项目测试或构建。
- 本轮未提交、未推送、未部署。
- 本轮不升级 `accepted`、`integrated` 或 `production_ready`。
- 下一轮只调查 CodeGraph 集成层残留提示，不进入 GFIS 业务开发。
