---
doc_id: GPCF-DOC-19A55BF909
title: GPCF-L4-GFIS-REPAIR-057 GFIS KDS 原始凭证字段缺口矩阵
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-057.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-057.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-057 GFIS KDS 原始凭证字段缺口矩阵

## Objective

结合用户补充的辽宁远航业务事实，从真实 KDS 仓检索候选资料，并把候选线索转成 GFIS 运行层可复测的字段级 proof anchor 缺口。目标是让 Loop 自己发现“为什么 E2E 仍失败”，而不是只记录“还缺资料”。

## Real Change

本轮落地在 GFIS 真实项目仓和 GPCF 总控仓：

- GFIS scanner 纳入 KDS canonical read-only 辽宁远航报价、成本测算、行动台账、现代精工/辽宁远航实体页候选。
- GFIS scanner 输出 `required_anchor_fields`、`present_anchor_fields`、`missing_anchor_fields`、`candidate_field_gap_summary`、`top_candidate_refs`。
- GFIS 运行态 API `get_runtime_liaoning_yuanhang_sample_release_gate` 与 `get_runtime_liaoning_yuanhang_proof_collection_package` 透传字段缺口。
- GFIS runner、runtime validator、contract validator 和 GPCF integrity validator 均要求字段级缺口存在。
- GPCF 控制板、状态矩阵、loop-state 与 evidence-index 回写本轮真实结果。

## KDS Findings

| proof_key | 当前候选 | 字段级缺口 |
|---|---|---|
| `liaoning_yuanhang_sample_test_record` | 29 条候选，未验真 | 测试记录编号、测试签收附件、客户反馈原件、客户签收单号 |
| `jiangxi_subcontract_sample_production_record` | 6 条候选，未验真 | 委托生产单号、完工记录编号、生产批次号、代工签收附件 |
| `liaoning_yuanhang_project_quotation` | 强候选 `报价单_Rev.01.md`，含报价编号与报价正文，未验真 | 报价附件URI、客户确认函 |
| `modern_jinggong_mass_production_release` | 36 条候选，未验真 | 转量产批准单号、放行批准附件、量产计划编号、WAES evidence ref |

## Evidence

| Check | Result |
|---|---|
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ...` | pass |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=1`；4 项 proof item 均为 `candidate_found_not_verified` |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `docker compose ... restart backend frontend` | pass；仅本机运行态重载，无 migrate/schema sync |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GFIS `npm run test:e2e` | 26 passed；Demo only / `pass_demo_only` |
| GFIS `git diff --check -- .` | pass |

## Current State

GFIS/GPCF 仍为 `repair_required` / `partial_repair`，项目群评分继续保持 79/100。

本轮没有完成样箱测试验真、江西委托生产验真、报价客户确认、现代精工转量产放行、生产写入、真实外部 API、物流 API、`bench migrate`、schema sync、权限/Token/生产配置变更或 accepted/integrated 状态升级。

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

优先补齐报价 PDF/报价附件 URI 与客户确认函；同时继续寻找 2026-01 样箱测试签收/反馈、江西委托生产单或完工记录、2026-06 转量产批准或 WAES evidence ref。
