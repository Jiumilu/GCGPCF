---
doc_id: GPCF-DOC-7A8497F896
title: GPCF-L4-GFIS-REPAIR-055 GFIS 辽宁远航四项凭证检索分类账
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-055.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-055.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-055 GFIS 辽宁远航四项凭证检索分类账

## Objective

把 GFIS 上一轮拆出的辽宁远航样箱转量产 4 个 proof item 纳入真实 KDS/相关项目只读检索分类账，形成机器可复核的候选、拒绝原因和 verified 计数，防止治理文档术语被误当成原始业务凭证。

## Real Change

本轮落地在 GFIS 真实项目仓和 GPCF 总控仓：

- GFIS scanner 新增 `liaoning_yuanhang_proof_search`。
- GFIS API/runner/validator 透出并校验四项 proof item 搜索账。
- GPCF `validate_loop_engineering_integrity.py` 增加 proof search ledger 检查。
- GPCF 控制板、状态矩阵、loop-state 与 evidence-index 回写本轮真实结果。

## Evidence

| Check | Result |
|---|---|
| GFIS `python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=1` |
| GFIS `python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=46 created=19 cleanup_deleted=19 runtime_gaps=33` |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_liaoning_yuanhang_sample_release_gate=missing_liaoning_yuanhang_sample_release_proofs` |
| GFIS `npm run test:e2e` | 26 passed；Demo only / `pass_demo_only` |
| GFIS `python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |

## Proof Search Result

| proof_key | search_status | candidate_count | verified |
|---|---:|---:|---:|
| `liaoning_yuanhang_sample_test_record` | candidate_found_not_verified | 16 | 0 |
| `jiangxi_subcontract_sample_production_record` | candidate_found_not_verified | 1 | 0 |
| `liaoning_yuanhang_project_quotation` | candidate_found_not_verified | 2 | 0 |
| `modern_jinggong_mass_production_release` | candidate_found_not_verified | 25 | 0 |

合计：`proof_search_candidate_count=44`、`verified_proof_item_count=0`、`missing_proof_item_count=4`。

## Self Correction

本轮首次扫描发现 3 个子项被治理文档里的 `verified_live_artifact` 术语误触发为 verified。已修正为：子凭证 verified 必须依赖原始业务记录字段和 proof anchors，例如测试记录编号、签收/反馈附件、委托生产单号、报价附件 URI、转量产批准单号、WAES evidence ref、source hash 和 KDS backlink。治理文档、Loop 追踪、fixture/mock/local_mirror 只能作为候选或拒绝原因，不得作为 live proof。

## Current State

GFIS/GPCF 仍为 `repair_required` / `partial_repair`。

本轮没有完成：

- GFIS SOP E2E Master。
- 样品签样/转量产放行。
- 生产写入、真实外部 API、物流 API。
- `bench migrate`、schema sync、数据库迁移。
- 权限、Token 或生产配置变更。
- accepted/integrated 状态升级。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Next

继续收集 4 项原始凭证 proof anchors：测试记录或客户反馈附件、江西代工委托生产/完工记录、辽宁远航项目报价单原件、现代精工转量产批准或 WAES release evidence。
