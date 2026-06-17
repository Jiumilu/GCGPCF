---
doc_id: GPCF-DOC-139C007EDA
title: GPCF L4 GFIS Repair 039 Verified Artifact Request Candidate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-039.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-039.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 039 Verified Artifact Request Candidate

## Round Control

| Field | Value |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-039 |
| gfis_round_id | GFIS-RUNTIME-SOP-E2E-033 |
| mode | L4 controlled repair |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

把上一轮 GFIS 运行层生成的 5 类 verified artifact request package 承载为可清理的本地 request candidate。该 candidate 只能表达“需要采集真实凭证”，不能表达凭证已接收、WAES 已裁决、KDS 已写入、POD 已确认、生产事实已完成或业务已验收。

## Implementation

GFIS 真实项目仓新增 `create_runtime_verified_artifact_request_candidate`。该 API 通过既有 `GCFIS Sync Event` fallback 临时创建并清理请求候选，强制校验：

- `request_count=5`
- `open_request_count=5`
- `kds_backlink_path` 必须在 `开发/` 空间内
- `open_categories` 只能来自 GFIS 运行层真实输入门禁
- `target_systems` 只能来自 GPC、GPC_POD、WAES、KDS、GFIS
- 越界字段如 `artifact_status`、`verified_live_artifact`、`waes_final_decision`、`kds_write_committed`、`pod_confirmed`、`business_fact_written` 必须拒绝

## Evidence

| Evidence | Result |
|---|---|
| GFIS py_compile | `python3 -m py_compile ...` pass |
| GFIS contract validator | `gfis work-order API contract validation passed`; `created_docs=19 commits=19` |
| GFIS runtime app check | `gcfis runtime app check passed` after controlled local service restart; no migrate/schema sync |
| GFIS runtime runner | `gfis_runtime_sop_e2e_dry_run=partial`; `runtime_calls=38 created=19 cleanup_deleted=19 runtime_gaps=26` |
| Verified artifact request candidate | `runtime_verified_artifact_request_candidate=runtime_verified_artifact_request_candidate_passed_temp_created_cleanup_required`; `request_count=5`; `open_request_count=5` |
| GFIS runtime validator | expected exit 2; `gfis_runtime_sop_e2e=repair_required`; `runtime_verified_artifact_request_candidate=runtime_verified_artifact_request_candidate_passed_temp_created_cleanup_required` |
| GFIS Demo E2E | `26 passed`; `pass_demo_only` |
| GFIS diff check | `git diff --check -- .` pass |

## Boundary

- `artifact_received=false`
- `verified_artifact_count=0`
- `demo_substitution=false`
- `production_write=false`
- `real_external_api_write=false`
- `accepted_integrated=false`
- `bench_migrate=false`
- `schema_sync=false`
- `permission_change=false`
- `kds_token_leak=false`

## Result

本轮通过真实性门禁，但业务闭环仍是 partial repair。GFIS runtime 现在能把 5 类缺失真实凭证请求承载为本地 candidate-only 请求候选；但 `verified_artifact_count=0`，真实 intake 仍为空，完整 GFIS SOP E2E 继续保持 `repair_required`，项目群评分保持 79/100 repair。

## Next

按 request package 和 request candidate 收集至少一类真实 verified artifact，并优先选择：

1. `live_pod_waes_kds_receipt`
2. `live_runtime_records`
3. `live_material_batch`
