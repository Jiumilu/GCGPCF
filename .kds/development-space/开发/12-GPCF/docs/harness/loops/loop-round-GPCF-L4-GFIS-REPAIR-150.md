---
doc_id: GPCF-DOC-65C3B89F08
title: GPCF-L4-GFIS-REPAIR-150 GFIS 合同链真实回执接收目录结构
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-150.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-150.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-150 GFIS 合同链真实回执接收目录结构

## 运行计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 12
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 输入

- GFIS `AGENTS.md`
- GFIS `README.md`
- GFIS `PROJECT_HARNESS_MANIFEST.md`
- GFIS `docs/harness/loop-state.md`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-collection-handoff-package.json`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-owner-response-file-landing-scan.json`
- GFIS `git status`
- GPCF `02-governance/loop/LOOP_CONTROL_BOARD.md`
- GPCF `docs/harness/loop-state.md`
- GPCF `09-status/gpcf-project-status-matrix.md`

## 本轮目标

把 GFIS 运行层辽宁远航合同链 5 类真实回执的接收目录结构落地，并纳入 GPCF 总控。目录结构只解决“真实文件提交到哪里”的问题，不代表真实业务凭证已取得。

## GFIS 实施结果

GFIS 新增：

- 5 个接收目录 README：
  - `docs/harness/sop-e2e/intake-submissions/contract-chain/signed-completion/README.md`
  - `docs/harness/sop-e2e/intake-submissions/contract-chain/customer-confirmation/README.md`
  - `docs/harness/sop-e2e/intake-submissions/contract-chain/purchase-order-or-contract/README.md`
  - `docs/harness/sop-e2e/intake-submissions/contract-chain/kds-write-receipt/README.md`
  - `docs/harness/sop-e2e/intake-submissions/contract-chain/waes-confirmation/README.md`
- `scripts/build_gfis_liaoning_yuanhang_contract_chain_real_receipt_receiving_directory_structure.py`
- `scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_receiving_directory_structure.py`
- `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-receiving-directory-structure.json`
- `docs/harness/sop-e2e/liaoning-yuanhang-contract-chain-real-receipt-receiving-directory-structure.md`
- `get_runtime_liaoning_yuanhang_contract_chain_real_receipt_receiving_directory_structure`
- 主 runtime SOP validator 接入点。

核心输出：

```text
liaoning_yuanhang_contract_chain_real_receipt_receiving_directory_structure=pass handoff_items=5 receiving_directories_expected=5 receiving_directories_existing=5 directory_readmes=5 owner_responses=0 submitted_files=0 valid_receipts=0 completed_handoffs=0 open_handoffs=5 structure_valid=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=receiving_directory_structure_ready_no_real_receipts runtime_sop_e2e=repair_required
```

主 runtime SOP validator expected exit 2：

```text
runtime_liaoning_yuanhang_contract_chain_real_receipt_receiving_directory_structure=receiving_directory_structure_ready_no_real_receipts:handoff_items=5:receiving_directories_expected=5:receiving_directories_existing=5:directory_readmes=5:owner_responses=0:submitted_files=0:valid_receipts=0:completed_handoffs=0:open_handoffs=5:structure_valid=0:review_queue=0:runtime_intake=0:waes_review=0:verified=0
RUNTIME_EXIT_CODE:2
```

## GPCF 回写

- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `docs/harness/loop-state.md`
- `docs/harness/evidence/evidence-index.md`
- `09-status/gpcf-project-status-matrix.md`
- `docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-150.md`

## 验证

- GFIS py_compile: pass
- GFIS receiving directory builder: pass
- GFIS receiving directory validator: pass
- GFIS runtime SOP validator: expected exit 2 / repair_required
- GFIS `npm run test:e2e`: 26 passed / pass_demo_only
- GFIS `git diff --check -- .`: pass

## 真实性结论

- receiving_directories_existing: 5
- directory_readmes: 5
- owner_responses: 0
- submitted_files: 0
- valid_receipts: 0
- completed_handoffs: 0
- structure_valid: 0
- review_queue: 0
- runtime_intake: 0
- waes_review: 0
- verified: 0
- runtime_sop_e2e: repair_required

本轮未写真实 KDS、WAES、生产系统或外部 API，未创建真实业务回执，未执行 bench migrate、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更，未升级 accepted 或 integrated。

## 下一轮

`GFIS-RUNTIME-SOP-E2E-144`：扫描 5 个真实回执接收目录是否已有责任方真实提交文件；若仍无真实文件，继续保持 `submitted_files=0 valid_receipts=0 review_queue=0 runtime_intake=0 verified=0 repair_required`。
