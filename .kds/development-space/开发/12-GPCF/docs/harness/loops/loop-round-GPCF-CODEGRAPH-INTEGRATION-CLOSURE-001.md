---
doc_id: GPCF-DOC-28984FE940
title: GPCF CodeGraph Integration Closure Audit
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-INTEGRATION-CLOSURE-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-INTEGRATION-CLOSURE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Integration Closure Audit

## 输入

- 当前主目标是完成 CodeGraph 在项目群和 Loop 工程中的部署集成。
- 用户明确要求只检查并固化 13 仓覆盖、同步命令、状态证据、GPCF validator、Loop 下一轮输入。
- 本轮不得进入各项目具体开发工作。

## 动作

- 只读执行 13 仓 `codegraph status`。
- 只读检查 13 仓 `.codegraph/` 是否存在。
- 只读检查 13 仓 `.git/info/exclude` 是否保护 `.codegraph/`。
- 只读检查 13 仓 `git status --short -- .codegraph`。
- 新增 GPCF 层收口审计 evidence 和 validator。

## 输出

- `docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.json`
- `docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.md`
- `tools/kds-sync/validate_loop_codegraph_integration_closure.py`

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_integration_closure.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

13 仓 CodeGraph 部署集成已收口为 `project_group_codegraph_integrated_with_sync_drift`：13 仓均有 `.codegraph/`，13 仓均保护 `.codegraph/` 不入 Git，`.codegraph` Git 状态总计为 0。Brain、GFIS、KDS、Studio 有待同步提示。

下一轮输入为 `GPCF-CODEGRAPH-SYNC-DRIFT-001`：只对 Brain、GFIS、KDS、Studio 执行 `codegraph sync`，随后更新 GPCF 覆盖证据。禁止业务代码修改、CI/workflow 修复、项目测试/构建修复、提交、推送、部署或状态升级。
