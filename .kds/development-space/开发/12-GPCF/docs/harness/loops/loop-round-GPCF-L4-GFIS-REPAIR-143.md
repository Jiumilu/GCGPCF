---
doc_id: GPCF-DOC-55875D9017
title: GPCF-L4-GFIS-REPAIR-143
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-143.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-143.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-143

## 本轮目标

按 Loop 新真实性规则，只完成 1 个真实实质轮次：把 GFIS 辽宁远航合同链从签章完成件接收门禁推进到真实回执接收目录扫描，防止把合同审阅稿、用户口述、KDS 候选或 Demo 数据冒充为签章完成、客户确认、采购订单、KDS write receipt、WAES confirmation 或运行层完成。

## 输入

- GFIS `AGENTS.md`、`README.md`、`PROJECT_HARNESS_MANIFEST.md`
- GFIS `docs/harness/loop-state.md`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-completion-gate.json`
- 用户澄清：葛化工厂建设期使用现代精工 OEM 代加工；GFIS 是现代精工代加工生产时和葛化工厂投产后共同使用的运行时系统。

## 实质变更

- GFIS 新增合同链真实回执接收目录扫描 JSON/Markdown。
- GFIS 新增 builder 与 validator。
- GFIS 运行层 API 新增只读真实回执目录扫描门禁。
- GFIS 主 `scripts/validate_gfis_runtime_sop_e2e.py` 接入真实回执目录扫描输出。
- GPCF 总控只记录 partial/repair_required，不升级 accepted/integrated。

## 关键结果

```text
liaoning_yuanhang_contract_chain_real_receipt_directory_scan=pass scanned_roles=8 signed_completion_files_found=0 kds_write_receipt_files_found=0 waes_confirmation_files_found=0 customer_confirmation=false purchase_order_or_contract=false runtime_ready=0 verified=0 state=contract_chain_real_receipt_directory_scan_no_real_receipts runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_contract_chain_real_receipt_directory_scan=contract_chain_real_receipt_directory_scan_no_real_receipts:scanned_roles=8:signed_completion_files_found=0:kds_write_receipt_files_found=0:waes_confirmation_files_found=0:customer_confirmation=false:purchase_order_or_contract=false:runtime_ready=0:verified=0
RUNTIME_EXIT_CODE:2
```

## 状态判定

- GFIS Demo E2E 仍只能作为 `pass_demo_only`。
- GFIS 运行层 SOP E2E 仍为 `repair_required`。
- 现代精工 OEM 是当前 GFIS 运行层。
- 葛化自建工厂投产后是未来 GFIS 运行层。
- `signed_completion_files_found=0`、`kds_write_receipt_files_found=0`、`waes_confirmation_files_found=0`。
- `customer_confirmation=false`、`purchase_order_or_contract=false`。

## 真实计数

- declared_rounds=1/15
- substantive_rounds=1/15
- generated_items=6
- batch_generated=false
- substance_gate=pass
- stop_type=authorization_boundary

## 禁止事项确认

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行真实 KDS 写入。
- 未执行真实 WAES 写入。
- 未执行数据库迁移、bench migrate 或 schema sync。
- 未执行权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 配置变更。
- 未将状态升级为 accepted 或 integrated。
