---
doc_id: GPCF-DOC-8B82DFE880
title: GPCF CodeGraph GFIS Residual Notice Investigation
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF CodeGraph GFIS Residual Notice Investigation

## 输入

- 上一轮 `GPCF-CODEGRAPH-SYNC-DRIFT-001` 将项目群 CodeGraph drift 收敛到 GFIS 单点 `residual_pending_notice`。
- 用户要求当前主线是 CodeGraph 在项目群和 Loop 中的部署集成，不进入各项目内部开发任务。

## 动作

- 执行 GFIS `codegraph status`。
- 检查 GFIS `.codegraph/` Git 状态。
- 检查 GFIS `.git/info/exclude` 是否保护 `.codegraph/`。
- 读取 GFIS `.codegraph/codegraph.db` 的 `files` 与 `project_metadata`。
- 用 GFIS Git 跟踪文件清单与 CodeGraph DB `files.path` 做差集。
- 对残留候选执行文件类型、行数、大小、Git 状态和 CodeGraph node lookup 复核。
- 新增 GPCF evidence 与 validator 后，对 GPCF 治理仓执行 CodeGraph evidence sync，保持 GPCF 本仓图谱收口。

## 输出

- GFIS `.codegraph/` 未进入 Git 状态。
- GFIS `.git/info/exclude` 已包含 `.codegraph/`。
- GFIS CodeGraph status 仍显示 `Pending Changes: Added: 1 files`。
- 残留候选定位为 `scripts/validate_gfis_runtime_sop_e2e.py`。
- 该候选是 Git 已跟踪 modified 文件，约 1,589,665 bytes / 17,784 行，不存在于 CodeGraph `files` 表，`codegraph node` 返回 `No indexed file matches`。
- 新增 `docs/harness/evidence/loop-codegraph-gfis-residual-notice-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-gfis-residual-notice-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_gfis_residual_notice.py`。
- GPCF 治理仓 CodeGraph 已同步到 `Files=805`、`Nodes=9,038`、`Edges=20,746`，且 `.codegraph/` 未进入 Git 状态。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_gfis_residual_notice.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git status --short -- .codegraph`

## 反馈

GFIS CodeGraph 残留提示已解释为超大生成 validator 与 CodeGraph 索引策略之间的集成层 notice，不是 13 仓覆盖失败，也不是 `.codegraph` Git 保护失败。本轮不进入 GFIS 业务开发。下一轮输入为 `GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001`，用于决定是否在项目群层面固化大文件/生成 validator 的 CodeGraph 策略。
