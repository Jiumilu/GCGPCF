---
doc_id: GPCF-DOC-D5A774D7ED
title: GPCF-L4-GFIS-REPAIR-270
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-270.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-270.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-270

- round_id: `GPCF-L4-GFIS-REPAIR-270`
- gfis_round_id: `GFIS-RUNTIME-SOP-E2E-260`
- subject: GFIS 运行层
- stage: `01_customer_requirement_platform_order` / `CustomerRequirementOrPlatformOrder`
- declared_rounds: `1`
- substantive_rounds: `1`
- generated_items: `4`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`

## 本轮目标

总控同步 GFIS 260：判断辽宁远航正式报价单与 KDS 葛化受控数据是否足以让 `CustomerRequirementOrPlatformOrder` 升级为 valid source record。

## 输入

- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`
- GFIS `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-kds-candidate-source-record-mapping-gate.json`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-formal-quotation-source-intake.json`

## 输出

- GFIS `scripts/build_gfis_sop_e2e_260.py`
- GFIS `scripts/validate_gfis_sop_e2e_260.py`
- GFIS `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-valid-source-record-eligibility-gate.json`
- GFIS `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-valid-source-record-eligibility-gate.md`

## 真实结果

- pending_business_verification_candidates: `1`
- formal_quotation_candidates: `1`
- customer_confirmations: `0`
- purchase_orders: `0`
- valid_source_records: `0`
- runtime_primary_key_ready: `0`
- review_queue: `0`
- runtime_intake: `0`
- waes_review: `0`
- verified: `0`
- runtime_sop_e2e: `repair_required`

## 验证

- `python3 scripts/validate_gfis_sop_e2e_260.py` in GFIS: pass
- `python3 scripts/harvest_gfis_kds_gehu_inputs.py` in GFIS: refreshed coverage, categories `8/8`, missing live business inputs `5`
- `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS: failed as expected on `KDS coverage must not have missing controlled sources`; current `missing_sources=4`
- `npm run test:e2e` in GFIS: `26 passed`，仅作 Demo/frontend 回归
- `git diff --check -- .` in GFIS: pass

## 结论

报价单与 KDS 受控数据只能进入 pending_business_verification。当前不能生成 valid source record，不能进入 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。

## 下一轮

`GFIS-RUNTIME-SOP-E2E-261`：接收辽宁远航客户确认、平台订单回执、采购订单或等效正式确认原件的脱敏索引；若仍无真实文件，继续保持 repair_required。
