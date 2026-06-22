---
doc_id: GPCF-DOC-07988FA674
title: CodeGraph 首个真实业务候选 Dry-run 证据
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph 首个真实业务候选 Dry-run 证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004`。本轮只选择低风险真实业务候选并生成 CodeGraph 前置分析和 Harness gate dry-run，不进入业务实现。

## 候选任务

候选：GFIS 辽宁远航合同链真实回执空目录 hold register。

目标节点：

```text
scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py
```

选择原因：

- 该候选对应 GFIS 当前真实业务阻塞点。
- 当前动作只读，不写入 GFIS 接收目录、不触发 runtime intake、不触发 WAES review。
- 可验证真实业务候选在 `affectedTests=[]` 时是否被 Harness gate 要求记录 fallback。

## CodeGraph 前置分析

执行命令：

```bash
codegraph query "GFIS runtime gap hold register source record receipt fallback_reason codegraph evidence" --json
codegraph node "scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py"
codegraph affected "scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py" --json
```

结果：

- `node` 显示目标 validator 为 211 行、20 个符号、没有其他索引文件依赖它。
- `affected` 返回 `affectedTests=[]`、`totalDependentsTraversed=0`。
- GFIS CodeGraph 当前存在既有 `pendingChanges.added=1`，本轮只登记，不执行 GFIS sync。

## Harness Gate Dry-run

```text
gate=pass
codegraph_evidence_present=true
target_nodes_present=true
affected_scope_present=true
affected_tests_empty_with_fallback_reason=true
changed_files_empty=true
status_boundaries_false=true
```

fallback 原因：

```text
codegraph affected returned affectedTests=[] and totalDependentsTraversed=0; fallback tests are selected from the target GFIS validator and the GPCF Harness gate validators.
```

## 只读验证

GFIS 候选 validator 输出：

```text
liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register=pass hold_items=5 open_holds=5 closed_holds=0 owner_responses=0 submitted_files=0 valid_receipts=0 completed_handoffs=0 structure_valid=0 release_allowed=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=empty_directory_holds_open_waiting_real_receipts runtime_sop_e2e=repair_required
```

该输出继续证明 GFIS 真实业务链仍为 `repair_required`，不得升级 accepted、integrated 或 production_ready。

## 状态边界

本轮未修改 GFIS 业务文件，未运行 GFIS sync，未提交、未推送、未部署，未生产写入，未外部 API 写入。

## 下一轮输入

`GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005`

下一轮应形成授权包：是否允许围绕该 GFIS 候选进入业务实现、允许改哪些文件、禁止触碰哪些目录、允许运行哪些测试、是否允许 GFIS CodeGraph sync。未授权前继续保持 dry-run only。
