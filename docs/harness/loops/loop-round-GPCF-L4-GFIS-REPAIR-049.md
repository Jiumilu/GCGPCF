---
doc_id: GPCF-DOC-36CF236EFA
title: GPCF L4 GFIS Repair 049
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-049.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-049.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 049

## Round Control

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

把用户补充的业务线索纳入 GFIS 运行层 `live_sample_signoff_release` 采集请求，并通过 GPCF 总控门禁检查，确保 Loop 不再把样品签样/转量产缺口停留在泛化描述。

## Real Change

- GFIS 运行层 `get_runtime_verified_artifact_request_package`、`get_runtime_verified_artifact_collection_dossier`、`get_runtime_verified_artifact_collection_priority` 输出 `business_trace_hints`。
- GFIS KDS scanner 已把辽宁远航、23 个样箱、样箱、江西代工、项目报价单、现代精工产线和量产计划纳入 `live_sample_signoff_release` 检索词；当前样品类候选 8 条，仍没有 verified live artifact。
- 业务线索包括：2026 年 1 月辽宁远航 23 个样箱测试、江西代工厂生产、2026 年 5 月辽宁远航项目报价单、2026 年 6 月现代精工产线量产计划。
- GFIS contract validator、runtime runner、runtime validator 和 GPCF `validate_loop_engineering_integrity.py` 均增加该线索检查。
- GPCF 控制板、loop-state、状态矩阵、evidence index 回写 REPAIR-049。

## Evidence

| 检查 | 结果 |
|---|---|
| GFIS `python3 -m py_compile ...` | pass |
| GFIS `python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `docker compose ... restart ...` | pass；运行层受控重载 |
| GFIS `bash scripts/check_gcfis_runtime_app.sh` | pass |
| GFIS `python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`missing_live_business_inputs=1`；`live_sample_signoff_release` 候选 8 条，含 `样箱` 线索但仍缺 runtime verifier |
| GFIS `python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=44 created=19 cleanup_deleted=19 runtime_gaps=31`；业务线索已输出 |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GFIS `npm run test:e2e` | pass；`26 passed`；Demo-only regression |

## Current State

`live_sample_signoff_release` 仍是唯一开放缺口。用户业务线索已进入运行层请求和总控门禁，但仍不是 verified live artifact。完整 SOP E2E 仍为 `repair_required`，项目群评分保持 79/100，不得恢复 100/100。

## Boundaries

未执行 Git push、生产写入、真实外部 API 写入、物流 API、WAES/KDS/POD 写入、数据库迁移、权限变更、部署、accepted 或 integrated 升级。用户线索只作为待核验采集线索。

## Next

围绕辽宁远航 23 个样箱测试、江西代工、5 月项目报价单和 6 月现代精工量产计划，采集真实样品申请、客户签样附件或豁免记录、项目报价单、转量产批准、WAES evidence ref、KDS backlink path 与 source record hash。
