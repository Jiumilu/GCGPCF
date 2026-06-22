---
doc_id: GPCF-DOC-1149753675
title: GPCF-L4-GFIS-REPAIR-159
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-159.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-159.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-159

## 输入

- 用户确认：辽宁远航首笔订单合同链当前因葛化工厂仍在建设，使用现代精工工厂进行 OEM 代加工；葛化投产后继续使用 GFIS 作为运行时系统。
- GFIS `GFIS-RUNTIME-SOP-E2E-151` 已证明 KDS 受控资料覆盖 12/12 SOP 阶段，但 live proof 仍为 0。
- GFIS 合同链 intake 已证明 8 个 Word 源文件存在、hash 有效、合同编号可识别，但仍为审阅/修订稿，不是签章完成件。

## 本轮目标

在真实 GFIS 项目仓落地一个实质门禁：把辽宁远航合同链源文件映射到 GFIS SOP 12 个阶段，形成“合同链输入边界”，并保持签章完成、KDS write receipt、WAES confirmation、GFIS 运行层单据事实、review/runtime/WAES/verified 全部为 0。

## 动作

- GFIS 新增 `scripts/build_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py`。
- GFIS 新增 `scripts/validate_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py`。
- GFIS 新增 `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-sop-stage-input-map.json`。
- GFIS 新增 `docs/harness/sop-e2e/liaoning-yuanhang-contract-chain-sop-stage-input-map.md`。
- GFIS 新增只读 API `get_runtime_liaoning_yuanhang_contract_chain_sop_stage_input_map`。
- GFIS 主 runtime SOP validator 已接入 `runtime_liaoning_yuanhang_contract_chain_sop_stage_input_map`。
- GPCF 回写控制板、项目状态矩阵、loop-state、evidence index。

## 验证

| 命令 | 结果 |
|---|---|
| `python3 scripts/build_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py` in GFIS | pass |
| `python3 -m py_compile scripts/build_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py scripts/validate_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | pass |
| `python3 scripts/validate_gfis_liaoning_yuanhang_contract_chain_sop_stage_input_map.py` in GFIS | pass |
| `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增 `runtime_liaoning_yuanhang_contract_chain_sop_stage_input_map`，总体仍为 `repair_required` |
| `npm run test:e2e` in GFIS | pass；26 passed；仅为 GFIS Demo 前端回归 |

## 输出

```text
liaoning_yuanhang_contract_chain_sop_stage_input_map=pass source_files=8 hash_valid=8 sop_stages=12 mapped_sop_stages=12 signed_completion_files=0 kds_backlink_write_receipts=0 waes_confirmations=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=contract_chain_sop_stage_input_mapped_waiting_signed_receipts runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_contract_chain_sop_stage_input_map=contract_chain_sop_stage_input_mapped_waiting_signed_receipts:source_files=8:hash_valid=8:sop_stages=12:mapped_sop_stages=12:signed_completion_files=0:kds_backlink_write_receipts=0:waes_confirmations=0:review_queue=0:runtime_intake=0:waes_review=0:verified=0
```

## 边界

- 未写真实 KDS、WAES、生产系统或外部 API。
- 未执行 `bench migrate`、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更。
- 未创建签章完成件、KDS write receipt、WAES confirmation、GFIS FactoryOrder、WorkOrder、QualityInspection、InventoryBatch、DeliveryNote、POD、review queue、runtime intake、verified artifact、accepted 或 integrated。
- 合同链源文件只作为 SOP 阶段输入边界，不替代真实运行层 evidence。

## 本轮真实计数

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `7`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`
