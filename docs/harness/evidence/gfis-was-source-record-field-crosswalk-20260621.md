---
doc_id: GPCF-DOC-2C3EE1AAC6
title: GFIS WAS Source Record Field Crosswalk Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.md
source_path: docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS WAS Source Record Field Crosswalk Evidence

## Evidence ID

`GFIS-WAS-SOURCE-RECORD-FIELD-CROSSWALK-20260621`

## 结论

GPCF 已建立 GFIS 原生 source-record 字段与 WAS/Ontology 字段的提交 crosswalk。该 crosswalk 只作为未来真实提交的填写与审核规则，不创建任何真实 source-of-record，也不改变 GFIS 当前 `repair_required` 状态。

## 覆盖

| 字段 | 值 |
|---|---|
| GFIS 原生必填字段 | `12` |
| WAS/Ontology 必填字段 | `12` |
| crosswalk entries | `12` |
| direct_equalities | `2` |
| fixed_was_values | `5` |
| explicit_submission_fields | `5` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |

## Crosswalk 摘要

| WAS 字段 | 规则 |
|---|---|
| `objectFamily` | 必须等于 GFIS `object_family`，且为 `CustomerRequirementOrPlatformOrder` |
| `sourceRecordId` | 必须显式填写，并绑定 `source_record_hash` |
| `assetDimension` | 固定为 WAS S01 的 `data_asset` |
| `flowType` | 固定为 WAS S01 的 `commerce_flow` |
| `lifecycle` | 人工核验前固定为 `pending_business_verification` |
| `trustLevel` | WAES review 前固定为 `T4` |
| `sourceRefs` | 必须包含 WAS S01 source ref |
| `evidenceRefs` | 必须包含 GFIS REAL-001 source-record intake gate |
| `waesGateRefs` | 必须包含 WAES customer-order source-record review gate |
| `promotionBlockers` | 必须保留 `valid_source_record_missing` 和 `customer_confirmation_missing` |
| `nextAction` | 固定为 `collect_customer_order_or_platform_receipt` |
| `kdsBacklink` | 必须等于 GFIS `source_of_record_backlink`，且以 `开发/` 开头 |

## 非声明

- 本 evidence 不向 GFIS 接收目录写入文件。
- 本 evidence 不创建真实 source-of-record。
- 本 evidence 不创建 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本 evidence 不证明 GFIS 真实业务 SOP E2E 完成。
- 本 evidence 不升级 accepted、integrated 或 production_ready。

## 下一步

收到真实客户订单原件或平台订单回执后，业务方应按本 crosswalk 同时填写 GFIS 原生字段与 WAS/Ontology 字段；提交后先运行提交前扫描、负例门禁和 crosswalk validator，再进入 GFIS 人工核验与 runtime primary key 门禁。
