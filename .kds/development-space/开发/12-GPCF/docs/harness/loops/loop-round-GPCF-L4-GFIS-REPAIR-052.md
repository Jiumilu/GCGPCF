---
doc_id: GPCF-DOC-57CC84A9C1
title: GPCF L4 GFIS Repair 052
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-052.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-052.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 052

## Round Control

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

把 GFIS `live_sample_signoff_release` 的 9 条 KDS 候选从“只知道未通过”推进为“每条都有机器可读拒绝原因”，防止候选数量、治理引用或业务线索被误读为原始签样/转量产 live proof。

## Real Change

- GFIS scanner 不再截断 live proof candidates，`candidate_count` 必须等于 candidate rows。
- GFIS scanner 为未通过候选输出 `missing_verifiers`。
- GFIS 运行层 `get_runtime_sample_signoff_release_evidence_gate` 返回完整 9 条 `candidate_refs`。
- GFIS runner 和 validator 要求每条 rejected candidate 均有 `missing_verifiers` 或 `exclusion_reason`。
- GPCF 控制板、loop-state、状态矩阵、evidence index 和本轮记录回写 REPAIR-052。

## Evidence

| 检查 | 结果 |
|---|---|
| GFIS `python3 -m py_compile ...` | pass |
| GFIS `python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=1`；`live_sample_signoff_release candidate_count=9 rows=9` |
| GFIS `python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=45 created=19 cleanup_deleted=19 runtime_gaps=32` |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_sample_signoff_release_gate=missing_sample_signoff_release_evidence` |
| GFIS `npm run test:e2e` | pass；`26 passed`；Demo-only regression |
| GFIS `git diff --check -- .` | pass |

## Current State

KDS 检索命中的 9 条样品签样/转量产候选仍不能成为 verified live artifact。当前缺失的是原始 proof anchors，不是检索不到关键词：需要真实样品申请、客户签样附件或豁免记录、项目报价单、转量产批准、WAES evidence ref、KDS backlink path 与 source record hash。

## Boundaries

未执行 Git push、生产写入、真实外部 API 写入、物流 API、WAES/KDS/POD 写入、数据库迁移、schema sync、权限变更、部署、accepted 或 integrated 升级。

## Next

下一轮应基于 9 条 rejected candidate 的 `missing_verifiers`，定向采集 `客户签样已通过`、`转量产批准`、`签样附件已归档` 或等效 `verified_live_artifact` 原始凭证；找不到则继续保持 `missing_input`。
