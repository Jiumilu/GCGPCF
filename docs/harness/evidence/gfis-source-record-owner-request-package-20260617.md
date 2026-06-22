---
doc_id: GPCF-DOC-7607A76253
title: GFIS 来源记录负责人请求包
project: GPCF
related_projects: [GFIS, GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md
source_path: docs/harness/evidence/gfis-source-record-owner-request-package-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS 来源记录负责人请求包

- package_id: `GPCF-GFIS-SOURCE-RECORD-OWNER-REQUEST-20260617`
- round_id: `GPCF-L4-GFIS-REPAIR-214`
- request_owner: `GPC_or_Liaoning_Yuanhang_order_owner`
- request_state: `ready_to_request_owner_response_not_submitted`
- expected_submission_path: `docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/*.customer-requirement-platform-order.source-record.json`

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

## 当前计数

| metric | value |
|---|---:|
| `submitted_files_found` | 0 |
| `valid_source_records` | 0 |
| `structure_valid_records` | 0 |
| `runtime_primary_key_ready` | 0 |
| `runtime_primary_key_missing` | 1 |
| `review_queue` | 0 |
| `runtime_intake` | 0 |
| `waes_review` | 0 |
| `verified` | 0 |

## 不声明事项

- `request_package_is_source_record`: `false`
- `owner_response_received`: `false`
- `source_of_record_received`: `false`
- `structure_valid_source_record`: `false`
- `runtime_primary_key_created`: `false`
- `review_queue_created`: `false`
- `runtime_intake_created`: `false`
- `waes_review_created`: `false`
- `verified_artifact_created`: `false`
- `production_write`: `false`
- `real_external_api_write`: `false`
- `real_kds_write`: `false`
- `real_waes_write`: `false`
- `bench_migrate`: `false`
- `schema_sync`: `false`
- `permission_change`: `false`
- `accepted_integrated`: `false`

## 下一步

`obtain_real_customer_order_original_or_platform_order_receipt_json_from_owner`
