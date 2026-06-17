---
doc_id: GPCF-DOC-82AC5DFB29
title: GFIS-RUNTIME-SOP-E2E-223
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-223.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-223.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-223

## 基本信息

| 字段 | 值 |
|---|---|
| round_id | GFIS-RUNTIME-SOP-E2E-223 |
| date | 2026-06-17 |
| project | GlobalCloud GFIS |
| subject | GFIS 运行层 |
| object_family | CustomerRequirementOrPlatformOrder |
| stage | pending_business_verification_manual_completion_hold_release_precheck |
| status | partial |

## 输入

- `GFIS-RUNTIME-SOP-E2E-222` manual completion receiving hold gate evidence。
- `docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/pending-business-verification/` 真实接收目录。
- `scripts/validate_gfis_runtime_sop_e2e.py` 主 runtime SOP E2E validator。

## 本轮目标

建立人工业务核验完成 open hold 的 release precheck。若真实人工核验完成文件、source hash、KDS backlink、责任人、release authorization 或运行层主键缺失，必须继续阻断 review queue、runtime intake、WAES review 和 verified artifact。

## 执行动作

- 新增 hold release precheck builder。
- 新增 hold release precheck validator。
- 生成 JSON/Markdown evidence。
- 新增只读 API：`get_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_hold_release_precheck`。
- 将本轮门禁接入 `scripts/validate_gfis_runtime_sop_e2e.py`。

## 输出

- `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-pending-business-verification-manual-completion-hold-release-precheck.json`
- `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-source-record-pending-business-verification-manual-completion-hold-release-precheck.md`
- `scripts/build_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_hold_release_precheck.py`
- `scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_hold_release_precheck.py`
- `gcfis_custom/gcfis_custom/api.py`
- `scripts/validate_gfis_runtime_sop_e2e.py`
- `docs/harness/loop-state.md`
- `docs/harness/evidence/evidence-index.md`
- `docs/harness/loops/README.md`

## 关键计数

```text
source_hold_gate_items=1
source_open_holds=1
release_precheck_items=1
blocked=1
release_allowed_items=0
release_requirements=8
unsatisfied_release_requirements=8
manual_business_verification_completion_files_found=0
schema_valid_manual_completion_files=0
manual_business_verification_completed=0
valid_source_records=0
structure_valid_records=0
hold_items=1
open_holds=1
hold_release_allowed=0
manual_completion_release_allowed=0
runtime_primary_key_ready=0
runtime_primary_key_missing=1
review_queue=0
runtime_intake=0
waes_review=0
verified=0
runtime_sop_e2e=repair_required
```

## 验证

- `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_hold_release_precheck.py`
- `python3 scripts/validate_gfis_runtime_sop_e2e.py`
- `npm run test:e2e`
- `git diff --check -- .`

## 非声明

本轮不创建、不确认、不替代客户订单、平台订单回执、pending submission、合规人工核验完成文件、有效 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact 或 accepted/integrated 状态。

## 真实性计数

```text
declared_rounds=1/15
substantive_rounds=1/15
generated_items=7
batch_generated=false
substance_gate=pass
stop_type=authorization_boundary
```

## 下一轮建议

`GFIS-RUNTIME-SOP-E2E-224`：建立人工核验完成 hold release negative fixture guard，防止 GFIS Demo、KDS 候选、用户口述、Loop 文档、缺 hash/KDS backlink/责任人/release authorization 的弱 release attempt 绕过 open hold。
