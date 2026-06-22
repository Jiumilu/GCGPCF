---
doc_id: GPCF-DOC-0F1C7DEBD8
title: GPCF-L4-GFIS-REPAIR-214
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-214.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-214.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-214

## 轮次定位

本轮执行用户指定推荐顺序中的第一项实质补证任务：优先补 `CustomerRequirementOrPlatformOrder` 的真实 source-of-record。

由于当前未收到真实客户订单原件或平台订单回执，本轮不伪造业务凭证，只把缺口转成可提交、可校验、可审计的责任方请求包。

## 输入

- 上一轮：`GPCF-L4-GFIS-REPAIR-213`，已提取 5 类责任方回执任务。
- GFIS source-of-record structure readiness：
  `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-structure-readiness.json`
- GFIS source-of-record receiving directory：
  `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/README.md`
- GPCF owner receipt task ledger：
  `docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.json`

## 产出

| 类型 | 路径 | 说明 |
|---|---|---|
| builder | `tools/kds-sync/build_gfis_source_record_owner_request_package.py` | 读取 GFIS readiness 与接收目录，生成 source-record 责任方请求包 |
| validator | `tools/kds-sync/validate_gfis_source_record_owner_request_package.py` | 防止请求包被误标为真实 source-of-record 或运行层主键 |
| JSON package | `docs/harness/evidence/gfis-source-record-owner-request-package-20260617.json` | 机器可读请求包 |
| Markdown package | `docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md` | 人工审阅请求包 |
| evidence index | `docs/harness/evidence/evidence-index.md` | 登记本轮证据 |
| loop state / control board / status matrix | `docs/harness/loop-state.md` / `02-governance/loop/LOOP_CONTROL_BOARD.md` / `09-status/gpcf-project-status-matrix.md` | 回写总控状态 |

## 请求对象

| 字段 | 值 |
|---|---|
| request_owner | `GPC_or_Liaoning_Yuanhang_order_owner` |
| request_state | `ready_to_request_owner_response_not_submitted` |
| expected_submission_path | `docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/*.customer-requirement-platform-order.source-record.json` |
| allowed source_kind | `customer_order_original` / `platform_order_receipt` |
| required_fields | 12 |

## 必填字段

- `object_family`
- `sop_stage`
- `source_kind`
- `customer_order_original_or_platform_order_receipt`
- `customer_confirmed_product_spec`
- `delivery_requirement`
- `source_of_record_backlink`
- `source_record_hash`
- `issuing_party`
- `owner_confirmation`
- `received_at`
- `runtime_site_context`

## 禁止替代材料

- `formal_quotation`
- `contract_review_draft`
- `kds_candidate`
- `user_statement`
- `loop_document`
- `gfis_demo`

## 验证

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile tools/kds-sync/build_gfis_source_record_owner_request_package.py tools/kds-sync/validate_gfis_source_record_owner_request_package.py` | pass |
| `python3 tools/kds-sync/build_gfis_source_record_owner_request_package.py` | `gfis_source_record_owner_request_package=pass submitted_files_found=0 valid_source_records=0 runtime_primary_key_ready=0 runtime_sop_e2e=repair_required` |
| `python3 tools/kds-sync/validate_gfis_source_record_owner_request_package.py` | `gfis_source_record_owner_request_package=pass required_fields=12 submitted_files_found=0 valid_source_records=0 runtime_intake=0 runtime_sop_e2e=repair_required` |

## 非声明

- 请求包不是客户订单。
- 请求包不是平台订单回执。
- 请求包不是 source-of-record。
- 本轮没有收到 owner response。
- 本轮没有创建 runtime primary key。
- 本轮没有创建 review queue、runtime intake、WAES review 或 verified artifact。
- 本轮没有执行生产写入、真实外部 API 写入、真实 KDS/WAES 写入、数据库迁移、权限变更、部署、提交、推送或 accepted/integrated 升级。

## 真实性计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 下一步

从 `GPC_or_Liaoning_Yuanhang_order_owner` 取得真实客户订单原件或平台订单回执 JSON，放入 GFIS 指定 source-of-record 接收目录并运行 GFIS source-of-record validators。通过后再推进 dispatch confirmation、WAES confirmation、KDS write receipt 与 runtime primary key。
