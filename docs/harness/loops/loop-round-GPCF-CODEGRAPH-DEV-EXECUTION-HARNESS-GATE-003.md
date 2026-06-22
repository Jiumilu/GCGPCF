---
doc_id: GPCF-DOC-16936490ED
title: Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003

## 输入

上一轮 `GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002` 要求把 `codegraph_evidence`、`target_nodes`、`affected_scope`、`fallback_reason` 和效率指标接入 Harness/Loop 检查链，使未来业务开发任务缺少 CodeGraph 影响分析时被阻断。

## 动作

- 建立 `docs/codegraph/codegraph-dev-execution-harness-gate.md`。
- 建立 positive/negative dry-run fixtures。
- 建立 `docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.json`。
- 建立 `docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.md`。
- 建立 `tools/kds-sync/validate_codegraph_dev_execution_harness_gate.py`。

## 输出

Harness/Loop gate 已定义以下阻断条件：

- 缺少 `codegraph_evidence`。
- 缺少 `target_nodes`。
- 缺少 `affected_scope`。
- `affectedTests=[]` 但没有 `fallback_reason`。
- `changed_files` 超出 `files_allowed_to_change`。
- 状态边界误升级为 accepted/integrated/production_ready。
- 出现生产写入、外部 API 写入或 CodeGraph 替代验收裁决声明。

## 检查

- `python3 tools/kds-sync/validate_codegraph_dev_execution_harness_gate.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_admission.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_pilot_pack.py`
- `python3 tools/kds-sync/validate_codegraph_session_declaration_boundary.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `codegraph sync && codegraph status --json . && git status --short -- .codegraph`

## 反馈

下一轮输入：`GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004`。

下一轮是否进入业务实现，必须由用户明确授权；未授权时只允许候选任务的 CodeGraph 前置分析和 Harness gate dry-run。
