---
doc_id: GPCF-DOC-C21E66324C
title: Ontology/WAS 真实 Source Record Intake Package
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/ontology-was-real-source-record-intake-pack-20260621.md
source_path: docs/harness/evidence/ontology-was-real-source-record-intake-pack-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Ontology/WAS 真实 Source Record Intake Package

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001` 已建立真实 `CustomerRequirementOrPlatformOrder` source-record 的业务责任方 intake package。

本 package 用于指导 `GPC_or_Liaoning_Yuanhang_order_owner` 提交真实客户订单原件或平台订单回执。它不写入 GFIS 接收目录，不创建真实 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact，不升级 accepted、integrated 或 production_ready。

## 当前边界

| 指标 | 当前值 |
|---|---:|
| gfis_real_source_record_files | `0` |
| submitted_files_found | `0` |
| accepted_for_next_gate | `0` |
| hold_required | `1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| gfis_real_business_lane | `repair_required` |

## 必交原件

| item_id | 原件 | 可接受形式 | 拒收条件 |
|---|---|---|---|
| IP-001 | 真实客户订单原件或平台订单回执 | 客户签发订单、系统订单原件、带平台标识的订单回执 | 仅报价单、仅合同审阅稿、仅用户口述、仅 Loop 文档、仅 GFIS demo |
| IP-002 | 客户确认产品规格 | 客户确认规格、签样/封样引用、平台附属规格 | 内部估算、未确认草稿规格 |
| IP-003 | 交付要求 | 订单交付日期/窗口、平台交付要求、客户确认交付指令 | 销售假设、缺少目的地或时间 |
| IP-004 | 签发方与责任方确认 | 签发方身份、业务 owner confirmation、源记录归属授权 | 签发方不明、owner confirmation 缺失 |
| IP-005 | KDS source backlink | `kds://` 或 `开发/01-GFIS` 受控源记录 backlink | KDS candidate 未经 owner 确认、backlink 不匹配 |
| IP-006 | runtime site context | 工厂/运行现场上下文、GFIS intake 场景上下文 | runtime context 缺失 |

## 必填字段

GFIS 原生字段 12 个：

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

WAS 字段 12 个：

- `objectFamily`
- `sourceRecordId`
- `assetDimension`
- `flowType`
- `lifecycle`
- `trustLevel`
- `sourceRefs`
- `evidenceRefs`
- `waesGateRefs`
- `promotionBlockers`
- `nextAction`
- `kdsBacklink`

## 提交前自检

- `source_kind` 必须是 `customer_order_original` 或 `platform_order_receipt`。
- `source_record_hash` 必须是 64 位 SHA-256 hex。
- `objectFamily` 必须等于 `CustomerRequirementOrPlatformOrder`。
- `assetDimension` 必须等于 `data_asset`。
- `flowType` 必须等于 `commerce_flow`。
- `lifecycle` 必须等于 `pending_business_verification`。
- `trustLevel` 必须等于 `T4`。
- `kdsBacklink` 必须匹配 `source_of_record_backlink`。
- `waesGateRefs` 必须包含 `waes://gate/customer-order-source-record-review`。
- `promotionBlockers` 必须包含 `valid_source_record_missing` 和 `customer_confirmation_missing`。

## 禁止自动提升

未取得真实 owner 提交并通过下一轮 precheck 前，不得创建或标记：

- runtime primary key
- review queue
- runtime intake
- WAES review
- verified artifact
- accepted
- integrated
- production_ready

## 下一轮门禁

真实候选出现后，下一轮为 `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001`。

必须运行：

- `python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py`
- `python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py`
- `python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py`
- `python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py`
