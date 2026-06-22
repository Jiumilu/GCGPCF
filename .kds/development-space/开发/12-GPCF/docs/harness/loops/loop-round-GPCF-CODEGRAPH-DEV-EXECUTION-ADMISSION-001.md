---
doc_id: GPCF-DOC-DE30AB91D7
title: Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001

## 输入

用户要求将 CodeGraph 深度进入业务开发执行层，但本轮不进入业务开发，只建立准入规则、模板和 validator。

## 动作

- 建立 `docs/codegraph/codegraph-dev-execution-admission.md`。
- 建立 `templates/CODEGRAPH_DEV_EXECUTION_EVIDENCE_TEMPLATE.json`。
- 建立 `docs/harness/evidence/codegraph-dev-execution-admission-20260621.json`。
- 建立 `docs/harness/evidence/codegraph-dev-execution-admission-20260621.md`。
- 建立 `tools/kds-sync/validate_codegraph_dev_execution_admission.py`。

## 输出

输出准入规则：

- 业务开发任务进入实现前必须运行 CodeGraph query/node/affected。
- Loop 必须记录 `target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`、`expected_tests`。
- 测试选择必须使用 `affected_tests` 或记录 `fallback_tests` 与 `fallback_reason`。
- 验收 evidence 必须包含 `codegraph_evidence`。
- 效率评估必须记录候选文件、实际改动文件、漏影响数量和定位时间。

## 检查

- validator：`python3 tools/kds-sync/validate_codegraph_dev_execution_admission.py`
- 文档治理：`document_control.py`、`check_document_pollution.py`、`validate_kds_token.py`、`loop_document_gate.py --check-only`
- CodeGraph 自身：`codegraph sync && codegraph status --json . && git status --short -- .codegraph`

## 反馈

下一轮输入：`GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002`。

下一轮只应选择低风险候选任务生成 pilot pack；是否进入业务实现必须另行授权。
