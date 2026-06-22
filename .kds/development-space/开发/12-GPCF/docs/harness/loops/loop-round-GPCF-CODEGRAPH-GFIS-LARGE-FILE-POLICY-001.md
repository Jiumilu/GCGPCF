---
doc_id: GPCF-DOC-794D90A6F1
title: GPCF CodeGraph GFIS Large File Policy
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph GFIS Large File Policy

## 输入

- 上一轮 `GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001` 已将 GFIS residual notice 定位到 `scripts/validate_gfis_runtime_sop_e2e.py`。
- 该文件约 1,589,665 bytes / 17,784 行，不在 CodeGraph `files` 表中，且 `.codegraph/` Git 状态为 0 entries。
- 用户要求主线仍是 CodeGraph 项目群与 Loop 集成，不进入项目内部开发任务。

## 动作

- 新增项目群 CodeGraph 超大/生成型文件策略。
- 将 GFIS 个案分类为 `large_generated_validator_exception_candidate`。
- 固化默认决策 `keep_residual_pending_notice_explained`。
- 新增本轮 evidence 与 validator。
- 不修改 GFIS，不拆分 validator，不新增 GFIS 排除规则。

## 输出

- 新增 `02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md`。
- 新增 `docs/harness/evidence/loop-codegraph-large-file-policy-20260621.json`。
- 新增 `docs/harness/evidence/loop-codegraph-large-file-policy-20260621.md`。
- 新增 `tools/kds-sync/validate_loop_codegraph_large_file_policy.py`。

## 检查

- `python3 tools/kds-sync/validate_loop_codegraph_large_file_policy.py`
- `python3 tools/kds-sync/validate_loop_codegraph_gfis_residual_notice.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

CodeGraph 项目群集成现在具备对超大/生成型 validator 的受控解释策略。GFIS 保持 `residual_pending_notice_explained`，不作为覆盖失败，不进入 GFIS 业务开发。下一轮输入为 `GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001`。
