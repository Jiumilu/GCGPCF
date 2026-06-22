---
doc_id: GPCF-DOC-60058E8559
title: GFIS-RUNTIME-SOP-E2E-260
project: GFIS
related_projects: [GFIS, GPC, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-260.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-260.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-260

- round_id: `GFIS-RUNTIME-SOP-E2E-260`
- subject: GFIS 运行层
- stage: `01_customer_requirement_platform_order` / `CustomerRequirementOrPlatformOrder`
- declared_rounds: `1`
- substantive_rounds: `1`
- generated_items: `4`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`

## 本轮目标

只推进一个真实阶段：判断辽宁远航正式报价单与 KDS 葛化受控数据能否让 `CustomerRequirementOrPlatformOrder` 从 pending_business_verification 升级为 valid_source_record。

## 输入

- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`
- GFIS `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-kds-candidate-source-record-mapping-gate.json`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-formal-quotation-source-intake.json`

## 输出

- GFIS `scripts/build_gfis_sop_e2e_260.py`
- GFIS `scripts/validate_gfis_sop_e2e_260.py`
- GFIS `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-valid-source-record-eligibility-gate.json`
- GFIS `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-valid-source-record-eligibility-gate.md`

## 真实结论

- pending_business_verification_candidates: `1`
- formal_quotation_candidates: `1`
- customer_confirmations: `0`
- purchase_orders: `0`
- valid_source_records: `0`
- source_record_to_runtime_primary_key_ready: `0`
- runtime_primary_key_ready: `0`
- review_queue: `0`
- runtime_intake: `0`
- waes_review: `0`
- verified: `0`
- runtime_sop_e2e: `repair_required`

## 阻塞原因

报价单与 KDS 受控数据只能作为 pending 候选。当前仍缺辽宁远航客户正式确认、平台订单回执、采购订单或等效正式确认原件的脱敏索引，因此不得生成运行层主键。

## 验证

- `python3 scripts/validate_gfis_sop_e2e_260.py`：pass
- `python3 scripts/validate_gfis_runtime_sop_e2e.py`：failed as expected on `KDS coverage must not have missing controlled sources`
- `npm run test:e2e`：26 passed；仅作 Demo/frontend 回归，不替代运行层 SOP E2E

## 禁止声明

- 不使用 GFIS Demo 作为 SOP 主体。
- 不用 mock、fixture 或文档冒充业务完成。
- 不标记 accepted/integrated。
- 不生产写入。
- 不真实外部 API 写入。
- 不 bench migrate、schema sync 或权限变更。
