---
doc_id: GPCF-DOC-0D35D7BC63
title: Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004
project: GPCF
related_projects: [GFIS, GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004

## 输入

上一轮 `GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003` 要求选择一个低风险真实业务开发候选；未获授权时只生成 CodeGraph 前置分析和 Harness gate dry-run。

## 动作

- 在 GFIS 仓执行 CodeGraph query/node/affected。
- 选择 `scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py` 作为目标节点。
- 运行只读 GFIS validator，确认候选仍为 hold/open 与 repair_required。
- 建立 `docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.json`。
- 建立 `docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.md`。
- 建立 `tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate.py`。

## 输出

- `target_nodes=1`
- `affectedTests=[]`
- `fallback_reason` 已记录。
- `changed_files=[]`
- `business_implementation_completed=false`
- GFIS `runtime_sop_e2e=repair_required`

## 检查

- `python3 scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate.py`
- `python3 tools/kds-sync/validate_codegraph_dev_execution_harness_gate.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `codegraph sync && codegraph status --json . && git status --short -- .codegraph` in GPCF only

## 反馈

下一轮输入：`GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005`。

下一轮需明确是否授权进入该 GFIS 候选的业务实现；未授权前不得修改 GFIS 业务文件，不得写入真实回执目录，不得运行 GFIS sync，不得升级 accepted/integrated/production_ready。
