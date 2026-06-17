---
doc_id: GPCF-DOC-AB61A7E360
title: GPCF-L4-GFIS-REPAIR-056 GFIS 辽宁远航原始凭证采集包
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-056.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-056.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-056 GFIS 辽宁远航原始凭证采集包

## Objective

把用户补充的辽宁远航业务线索纳入 GFIS 运行层可治理采集包：2026 年 1 月向辽宁远航提供 23 个样箱测试，样箱委托江西工厂生产；2026 年 5 月辽宁远航计划采购并提交项目报价单；2026 年 6 月计划用现代精工产线组织量产。

本轮只把这些信息转成原始凭证采集请求，不把口述线索、KDS 候选、治理文档或 Loop 记录升级为 `verified_live_artifact`。

## Real Change

本轮落地在 GFIS 真实项目仓和 GPCF 总控仓：

- GFIS 新增 `get_runtime_liaoning_yuanhang_proof_collection_package` 只读 API。
- GFIS runner 真实调用该 API，并写入 `LiaoningYuanhangProofCollectionPackage` gap register。
- GFIS runtime validator 与 contract validator 强制 4 项请求仍为 open、0 verified、4 missing。
- GPCF `validate_loop_engineering_integrity.py` 纳入采集包完整性检查。
- GPCF 控制板、状态矩阵、loop-state 与 evidence-index 回写本轮真实结果。

## Evidence

| Check | Result |
|---|---|
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ...` | pass |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=1` |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `docker compose ... restart backend frontend` | pass；仅本机运行态重载，无 migrate/schema sync |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_liaoning_yuanhang_proof_collection_package=liaoning_yuanhang_original_proof_collection_open` |
| GFIS `npm run test:e2e` | 26 passed；Demo only / `pass_demo_only` |

## Collection Package Result

| proof_key | target_system | collection_status | verified |
|---|---|---|---:|
| `liaoning_yuanhang_sample_test_record` | GPC | original_proof_collection_open | 0 |
| `jiangxi_subcontract_sample_production_record` | GFIS | original_proof_collection_open | 0 |
| `liaoning_yuanhang_project_quotation` | GPC | original_proof_collection_open | 0 |
| `modern_jinggong_mass_production_release` | WAES | original_proof_collection_open | 0 |

合计：`request_count=4`、`open_request_count=4`、`verified_proof_item_count=0`、`missing_proof_item_count=4`。

## Current State

GFIS/GPCF 仍为 `repair_required` / `partial_repair`，项目群评分继续保持 79/100。

本轮没有完成：

- GFIS SOP E2E Master。
- 样品签样/转量产放行。
- 辽宁远航样箱测试验真。
- 江西委托工厂生产验真。
- 辽宁远航项目报价验真。
- 现代精工产线量产批准验真。
- 生产写入、真实外部 API、物流 API。
- `bench migrate`、schema sync、数据库迁移。
- 权限、Token 或生产配置变更。
- accepted/integrated 状态升级。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Next

继续收集 4 项原始凭证 proof anchors：测试记录或客户反馈附件、江西委托工厂生产/完工记录、辽宁远航项目报价单原件、现代精工转量产批准或 WAES release evidence。
