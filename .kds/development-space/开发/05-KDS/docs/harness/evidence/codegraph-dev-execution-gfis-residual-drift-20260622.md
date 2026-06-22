---
doc_id: GPCF-DOC-68559C2B7E
title: CodeGraph GFIS 残余漂移复核证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph GFIS 残余漂移复核证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007`。

## 结论

GFIS CodeGraph sync 已执行过，但当前不能声明 sync-only closure 完成。

```text
pendingChanges.added=1
pendingChanges.modified=0
pendingChanges.removed=0
codegraph_sync_only_closure=false
```

## 工作区背景

GFIS 当前存在大量既有未跟踪文件：

```text
untracked_files_total=226
untracked_codegraph_scannable_files=73
```

本轮不清理、不删除、不 stage、不 commit、不 push。

## 授权候选范围状态

上一轮授权候选四文件仍在范围内：

- `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-empty-directory-hold-register.json`
- `docs/harness/sop-e2e/liaoning-yuanhang-contract-chain-real-receipt-empty-directory-hold-register.md`
- `scripts/build_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py`
- `scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py`

候选 validator 仍为 pass。全量 GFIS runtime SOP validator 仍不能作为通过证据，因为既有缺口为：

```text
FAIL: KDS coverage must not have missing controlled sources
```

## 禁止声明

不得声明：

- GFIS CodeGraph sync-only closure 已完成。
- GFIS 业务实现已完成。
- accepted。
- integrated。
- production_ready。
- 已提交、已推送或已部署。

## 下一轮

`GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008`
