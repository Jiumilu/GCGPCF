---
doc_id: GPCF-DOC-751B5CF916
title: GFIS-RUNTIME-SOP-E2E-262
project: GFIS
related_projects: [GFIS, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-262.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-262.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-262

## 本轮目标

建立 `CustomerRequirementOrPlatformOrder` runtime primary key gate。

本轮不创建运行层主键，只证明在 `valid_source_records=0` 时主键门禁必须阻断。

## 输入

- `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-valid-source-record-index-receiving-scan.json`
- `GFIS-RUNTIME-SOP-E2E-261`

## 产出

- `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-runtime-primary-key-gate.json`
- `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-runtime-primary-key-gate.md`
- `scripts/build_gfis_sop_e2e_262.py`
- `scripts/validate_gfis_sop_e2e_262.py`
- `scripts/validate_gfis_runtime_sop_e2e.py`

## 验证结果

`python3 scripts/validate_gfis_sop_e2e_262.py`：

```text
gfis_customer_requirement_platform_order_runtime_primary_key_gate=pass source_record_index_files_found=0 valid_source_records=0 source_record_to_runtime_primary_key_ready=0 runtime_primary_key_gate_items=1 runtime_primary_key_gate_blocked=1 runtime_primary_key_created=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 blocked=1 state=customer_requirement_platform_order_runtime_primary_key_gate_blocked_missing_valid_source_record runtime_sop_e2e=repair_required
```

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 结论

当前仍没有通过校验的 `CustomerRequirementOrPlatformOrder` valid source record。

因此：

- runtime_primary_key_gate_blocked=1
- runtime_primary_key_created=0
- runtime_primary_key_ready=0
- review_queue=0
- runtime_intake=0
- waes_review=0
- verified=0
- runtime_sop_e2e=repair_required

不得创建 GFIS 运行层主键，不得进入 review queue、runtime intake、WAES review、verified artifact，不得升级 accepted/integrated。

## 下一轮建议

`GFIS-RUNTIME-SOP-E2E-263`：建立 runtime primary key gate 的负例/污染拒收，确保 Demo、KDS candidate-only、报价单、Loop 文档或口述不能打开主键门禁。
