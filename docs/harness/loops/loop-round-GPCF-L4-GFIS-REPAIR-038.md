---
doc_id: GPCF-DOC-CB718E4EA2
title: GPCF L4 GFIS Repair 038 Verified Artifact Request Package
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-038.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-038.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 038 Verified Artifact Request Package

## Round Control

| Field | Value |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-038 |
| gfis_round_id | GFIS-RUNTIME-SOP-E2E-032 |
| mode | L4 controlled repair |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

把 GFIS 运行层从“能接收外部 verified artifact intake”推进到“能把 5 类缺失真实凭证转为可执行采集请求包”。本轮不接入真实凭证，不执行生产写入、真实外部 API、POD 确认、WAES 最终裁决、KDS 真实写入、数据库迁移、schema sync、权限变更或 accepted/integrated 升级。

## Implementation

GFIS 真实项目仓新增 `get_runtime_verified_artifact_request_package`。该 API 读取 KDS `live_proof` 审计结果，并为 `live_platform_order`、`live_sample_signoff_release`、`live_material_batch`、`live_runtime_records` 和 `live_pod_waes_kds_receipt` 生成只读请求项。

每个请求项包含目标系统、最小字段、候选来源、候选状态和禁止越界声明。请求包本身不是业务凭证，也不能替代 WAES/KDS/POD 回执或人工验收。

## Evidence

| Evidence | Result |
|---|---|
| GFIS py_compile | `python3 -m py_compile ...` pass |
| GFIS contract validator | `gfis work-order API contract validation passed`; `created_docs=18 commits=18` |
| GFIS runtime app check | `gcfis runtime app check passed` after controlled local service restart; no migrate/schema sync |
| GFIS runtime runner | `gfis_runtime_sop_e2e_dry_run=partial`; `runtime_calls=37 created=18 cleanup_deleted=18 runtime_gaps=25` |
| Verified artifact request package | `runtime_verified_artifact_request_package=verified_artifact_requests_open`; `request_count=5`; `open_request_count=5` |
| GFIS runtime validator | expected exit 2; `gfis_runtime_sop_e2e=repair_required`; `runtime_verified_artifact_request_package=verified_artifact_requests_open` |
| GFIS Demo E2E | `26 passed`; `pass_demo_only` |
| GFIS diff check | `git diff --check -- .` pass |

## Boundary

- `demo_substitution=false`
- `production_write=false`
- `real_external_api_write=false`
- `accepted_integrated=false`
- `bench_migrate=false`
- `schema_sync=false`
- `permission_change=false`
- `kds_token_leak=false`

## Result

本轮通过真实性门禁，但业务闭环仍是 partial repair。GFIS runtime 现在能把 5 类缺失真实凭证转为明确采集请求；但 `verified_artifact_count=0`，真实 intake 仍为空，完整 GFIS SOP E2E 继续保持 `repair_required`，项目群评分保持 79/100 repair。

## Next

按 request package 收集至少一类真实 verified artifact，并优先选择：

1. `live_pod_waes_kds_receipt`
2. `live_runtime_records`
3. `live_material_batch`
