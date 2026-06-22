---
doc_id: GPCF-DOC-9306DE5D41
title: GFIS-RUNTIME-SOP-E2E-263
project: GFIS
related_projects: [GFIS, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-263.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-263.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-263

## 本轮目标

建立 `CustomerRequirementOrPlatformOrder` runtime primary key gate 的负例/污染拒收。

本轮不创建运行层主键，只证明 GFIS Demo、KDS candidate-only、报价单、Loop 文档、口述事实、mock/fixture/培训资料不能打开主键门禁。

## 输入

- `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-runtime-primary-key-gate.json`
- `GFIS-RUNTIME-SOP-E2E-262`

## 产出

- `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-runtime-primary-key-negative-pollution-guard.json`
- `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-runtime-primary-key-negative-pollution-guard.md`
- `scripts/build_gfis_sop_e2e_263.py`
- `scripts/validate_gfis_sop_e2e_263.py`
- `scripts/validate_gfis_runtime_sop_e2e.py`

## 验证结果

`python3 scripts/validate_gfis_sop_e2e_263.py`：

```text
gfis_customer_requirement_platform_order_runtime_primary_key_negative_pollution_guard=pass source_runtime_primary_key_gate_items=1 source_runtime_primary_key_gate_blocked=1 source_valid_source_records=0 weak_primary_key_open_attempts=6 rejected_primary_key_open_attempts=6 accepted_primary_key_open_attempts=0 demo_substitution_attempts=1 kds_candidate_only_attempts=1 quotation_only_attempts=1 loop_document_claim_attempts=1 oral_statement_attempts=1 mock_fixture_attempts=1 runtime_primary_key_created=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 blocked=1 state=customer_requirement_platform_order_runtime_primary_key_negative_pollution_guard_rejected_all_weak_attempts runtime_sop_e2e=repair_required
```

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 结论

6 类弱主键打开声明全部被拒收：

- GFIS Demo
- KDS candidate-only
- 报价单无客户确认
- Loop 文档完成声明
- 口述事实
- mock/fixture/培训资料

因此：

- runtime_primary_key_created=0
- runtime_primary_key_ready=0
- review_queue=0
- runtime_intake=0
- waes_review=0
- verified=0
- runtime_sop_e2e=repair_required

不得创建 GFIS 运行层主键，不得进入 review queue、runtime intake、WAES review、verified artifact，不得升级 accepted/integrated。

## 下一轮建议

`GFIS-RUNTIME-SOP-E2E-264`：建立 CustomerRequirementOrPlatformOrder valid source-record 接收目录的下一轮监听/变更检测，只有真实 source-record index 到达时才允许重新评估 runtime primary key gate。
