---
doc_id: GPCF-DOC-CB7C953B3A
title: Loop CodeGraph Integration Closure Audit Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.md
source_path: docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Integration Closure Audit Evidence

## Evidence ID

`LOOP-CODEGRAPH-INTEGRATION-CLOSURE-AUDIT-20260621`

## 结论

本轮只做 CodeGraph 项目群集成收口审计，不进入任何项目内部开发任务。

当前 13 个本机 Git 仓均已具备 `.codegraph/` 本地索引，且 `.codegraph/` 均写入各仓 `.git/info/exclude`，`git status --short -- .codegraph` 均为空。CodeGraph 在项目群和 Loop 工程中的部署集成可以判定为 `integrated_with_sync_drift`。

## 覆盖统计

| 指标 | 数值 |
|---|---:|
| repo_count | 13 |
| indexed_repo_count | 13 |
| git_protected_repo_count | 13 |
| codegraph_git_status_entries_total | 0 |
| up_to_date_repo_count | 9 |
| pending_sync_repo_count | 4 |

## 待同步项目

| 项目 | Pending changes |
|---|---|
| GlobalCloud Brain | Added: 2 files; Modified: 77 files |
| GlobalCloud GFIS | Added: 1 files |
| GlobalCloud KDS | Added: 2 files |
| GlobalCloud Studio | Added: 9 files; Modified: 2 files |

## 受控同步命令

```bash
codegraph sync "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"
codegraph sync "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"
codegraph sync "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"
codegraph sync "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"
```

同步后只允许执行：

```bash
codegraph status "<repo_path>"
git -C "<repo_path>" status --short -- .codegraph
```

## Loop 下一轮输入

| 字段 | 内容 |
|---|---|
| Round | `GPCF-CODEGRAPH-SYNC-DRIFT-001` |
| Objective | 只对 Brain、GFIS、KDS、Studio 运行 CodeGraph sync，并回写 GPCF 覆盖 evidence |
| Allowed | `codegraph sync`、`codegraph status`、`.codegraph` Git 保护检查、GPCF evidence 更新 |
| Forbidden | 业务代码修改、CI/workflow 修复、项目测试/构建修复、提交、推送、部署、状态升级 |

## 非声明

- 本轮未运行 `codegraph sync`。
- 本轮未修改任何项目内部业务代码。
- 本轮未执行测试、构建、发布、部署、提交或推送。
- 本轮不把任何项目升级为 `accepted`、`integrated` 或 `production_ready`。
