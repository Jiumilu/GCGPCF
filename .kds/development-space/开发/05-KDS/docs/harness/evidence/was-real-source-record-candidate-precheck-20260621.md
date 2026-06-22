---
doc_id: GPCF-DOC-A1C8A72190
title: WAS Real Source Record Candidate Precheck Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: ontology-governance
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md
source_path: docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Real Source Record Candidate Precheck Evidence

## 结论

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001` 已建立 P4 真实 source-record candidate 预检闭环。

本轮只建立模板、正例夹具、负例拒收夹具、真实 candidate 扫描规则和 validator。当前没有业务 owner 提交的真实客户订单原件或平台订单回执，因此预检结果为 `pass_with_empty_hold`，必须保持 `hold_required=1`。

## 当前边界

| 指标 | 当前值 |
|---|---:|
| submitted_real_candidate_files | `0` |
| candidate_files_checked | `0` |
| accepted_for_next_gate | `0` |
| rejected_candidate_files | `0` |
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

## 项目群范围

本 P4 precheck 面向整个 GlobalCloud 项目群：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF、Studio、WAS。

当前落点仍是 GFIS `CustomerRequirementOrPlatformOrder` 首场景，后续通过 scenario profile 扩展到全绿色供应链链路。

## 已建立文件

- `docs/harness/intake/was-real-source-record-candidate-template.yaml`
- `fixtures/was/p4-real-source-record-candidate-positive.json`
- `fixtures/was/p4-real-source-record-candidate-negative-llm-only.json`
- `fixtures/was/p4-real-source-record-candidate-negative-missing-source.json`
- `fixtures/was/p4-real-source-record-candidate-negative-missing-runtime-site-context.json`
- `fixtures/was/p4-real-source-record-candidate-negative-wrong-dimension.json`
- `tools/kds-sync/validate_was_real_source_record_candidate_precheck.py`

## P4 必交输入

- 真实客户订单原件或平台订单回执
- 客户确认产品规格
- 交付要求
- 签发方与责任方确认
- KDS source backlink
- runtime site context

## 字段门禁

GFIS 原生字段 12 个，WAS/Ontology 字段 12 个。候选必须同时通过：

- `source_kind` 只能是 `customer_order_original` 或 `platform_order_receipt`
- `source_record_hash` 必须是 64 位 SHA-256 hex
- `objectFamily` 必须等于 `CustomerRequirementOrPlatformOrder`
- `assetDimension` 必须等于 `data_asset`
- `flowType` 必须等于 `commerce_flow`
- `lifecycle` 必须等于 `pending_business_verification`
- `trustLevel` 必须等于 `T4`
- `kdsBacklink` 必须等于 `source_of_record_backlink`
- `waesGateRefs` 必须包含 `waes://gate/customer-order-source-record-review`
- `promotionBlockers` 必须包含 `valid_source_record_missing` 和 `customer_confirmation_missing`

## 夹具结果

| 类型 | 数量 | 期望 |
|---|---:|---|
| positive fixture | `1` | accepted_for_next_gate |
| negative fixture | `4` | rejected |

负例覆盖：

- LLM-only fact claim
- missing real source artifact / owner confirmation
- missing runtime site context
- wrong asset dimension and flow type

## 禁止自动提升

本 evidence 不创建或标记：

- runtime primary key
- GFIS runtime write
- verified artifact
- accepted
- integrated
- production_ready

## 下一轮

只有当 `accepted_for_next_gate > 0` 时，才允许进入 `GPCF-ONTOLOGY-WAS-WAES-GATE-INPUT-CANDIDATE-001`。

在真实候选出现前，本轮后续动作仍是等待业务 owner 提交真实 source-record candidate，并保持 `hold_required=1`。
