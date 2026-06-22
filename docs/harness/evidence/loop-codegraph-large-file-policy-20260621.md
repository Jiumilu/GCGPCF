---
doc_id: GPCF-DOC-657DDCA61A
title: Loop CodeGraph Large File Policy Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/loop-codegraph-large-file-policy-20260621.md
source_path: docs/harness/evidence/loop-codegraph-large-file-policy-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Large File Policy Evidence

## Evidence ID

`LOOP-CODEGRAPH-LARGE-FILE-POLICY-20260621`

## 结论

本轮执行 `GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001`，只在 GPCF 固化 CodeGraph 超大/生成型文件策略，不进入 GFIS 业务开发。

新增 `02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md`。该政策将 GFIS `scripts/validate_gfis_runtime_sop_e2e.py` 分类为 `large_generated_validator_exception_candidate`，当前决策为 `keep_residual_pending_notice_explained`。

## 策略阈值

| 条件 | 阈值 |
|---|---:|
| 文件大小 | `>= 1,000,000` bytes |
| 文件行数 | `>= 15,000` lines |
| 生成型 validator | `scripts/validate_*_sop_e2e.py`、`scripts/build_*_sop_e2e_*.py` 或同类批量生成脚本 |

## GFIS 个案

| 项 | 当前值 |
|---|---|
| Candidate | `scripts/validate_gfis_runtime_sop_e2e.py` |
| Classification | `large_generated_validator_exception_candidate` |
| Size | `1,589,665` bytes |
| Lines | `17,784` |
| Git status | `tracked_modified` |
| CodeGraph DB | not present in `files` table |
| CodeGraph pending notice | `Added: 1 files` |
| `.codegraph` Git entries | `0` |
| Decision | `keep_residual_pending_notice_explained` |

## 授权边界

| 动作 | 本轮是否允许 |
|---|---|
| GPCF policy/evidence 更新 | true |
| GFIS 业务代码修改 | false |
| GFIS validator 重构 | false |
| 删除生成 validator | false |
| GFIS 项目级排除规则修改 | false |
| 提交/推送/部署 | false |
| `accepted` / `integrated` / `production_ready` 升级 | false |

## 下一轮输入

| 字段 | 内容 |
|---|---|
| Round | `GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001` |
| Objective | 建立轻量项目群 CodeGraph monitor 输入，检查 13 仓覆盖、`.codegraph` Git 保护、residual notice 与 policy exception |
| Allowed | GPCF evidence/validator 更新、只读 `codegraph status`、只读 `.codegraph` Git 状态 |
| Forbidden | 项目业务代码修改、GFIS validator 重构、删除生成 validator、提交、推送、部署、状态升级 |

## 非声明

- 本轮未修改 GFIS 业务代码。
- 本轮未重构、拆分或删除 GFIS validator。
- 本轮未修改 GFIS 项目级 CodeGraph 排除规则。
- 本轮未提交、未推送、未部署。
- 本轮不升级 `accepted`、`integrated` 或 `production_ready`。
