---
doc_id: GPCF-DOC-D2A947A430
title: GPCF-L4-GFIS-REPAIR-088 GFIS 辽宁远航业务事实链索引
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-088.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-088.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-088 GFIS 辽宁远航业务事实链索引

## 轮次元数据

| 字段 | 值 |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-088 |
| gfis_round_id | GFIS-RUNTIME-SOP-E2E-081 |
| date | 2026-06-14 |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 输入

用户再次确认辽宁远航业务事实链：

- 2026-01 向辽宁远航提供 23 个样箱用于测试。
- 样箱委托江西一家工厂进行生产。
- 2026-05 辽宁远航计划采购，并提交项目报价单。
- 2026-06 计划使用现代精工产线组织量产。

## 输出

GFIS 已新增：

- `docs/harness/sop-e2e/evidence/liaoning-yuanhang-business-fact-chain-index.json`
- `docs/harness/sop-e2e/liaoning-yuanhang-business-fact-chain-index.md`
- `scripts/validate_gfis_liaoning_yuanhang_business_fact_chain.py`
- `scripts/validate_gfis_runtime_sop_e2e.py` 主 validator 接入
- `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-081.md`

## 验证

```text
liaoning_yuanhang_business_fact_chain=pass facts=4 open_original_proofs=4 verified=0 customer_confirmation_candidates=0 runtime_sop_e2e=repair_required
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_business_fact_chain=pass:facts=4:open_original_proofs=4:verified=0:customer_confirmation_candidates=0
runtime_liaoning_yuanhang_customer_confirmation_intake_precheck=blocked_missing_customer_confirmation:candidates=0:ready=false:verified=0
runtime_verified_artifact_submission=missing_verified_artifact_submission
validator_exit=2
```

## 结论

本轮只把用户一手业务线索固化为 GFIS 运行层 KDS targeted search 与原始凭证采集输入。它不满足客户确认函、样箱测试记录、江西委托生产记录、现代精工转量产批准或 WAES evidence ref，也不允许升级 `accepted` / `integrated`。
