---
doc_id: GPCF-DOC-B9037CAE15
title: GPCF L4 GFIS Repair 036 Verified Live Artifact Gate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-036.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-036.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 036 Verified Live Artifact Gate

## Round Control

| Field | Value |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-036 |
| gfis_round_id | GFIS-RUNTIME-SOP-E2E-030 |
| mode | L4 controlled repair |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

把 GFIS 运行层 `live_proof` 审计从“受控引用是否存在”推进到“是否存在 verified live artifact”。本轮只新增只读门禁，不执行生产写入、真实外部 API、POD 确认、WAES 最终裁决、KDS 真实写入、数据库迁移、schema sync、权限变更或 accepted/integrated 升级。

## Implementation

GFIS 真实项目仓新增 `get_runtime_verified_artifact_gate`，由 GFIS runtime 自身读取 KDS live proof 审计结果，并按 5 类真实凭证判断：

- `live_platform_order`
- `live_sample_signoff_release`
- `live_material_batch`
- `live_runtime_records`
- `live_pod_waes_kds_receipt`

只有状态达到 `verified_live_artifact` 才能计入 verified。当前 KDS 受控引用、候选 ID、预检文本、Demo 片段和待签收说明均不得替代真实业务发生凭证。

## Evidence

| Evidence | Result |
|---|---|
| GFIS contract validator | `gfis work-order API contract validation passed`; `created_docs=18 commits=18` |
| KDS Gehua scanner | `kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5` |
| GFIS runtime app check | `gcfis runtime app check passed` after controlled local service restart; no migrate/schema sync |
| GFIS runtime runner | `gfis_runtime_sop_e2e_dry_run=partial`; `runtime_calls=35 created=18 cleanup_deleted=18 runtime_gaps=23` |
| Verified artifact gate | `runtime_verified_artifact_gate=missing_verified_live_artifacts`; `verified_artifact_count=0`; `missing_verified_artifact_count=5` |
| GFIS runtime validator | expected exit 2; `gfis_runtime_sop_e2e=repair_required`; `runtime_verified_artifact_gate=missing_verified_live_artifacts` |
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

本轮通过。它让 GFIS runtime 能明确证明：当前 5 类真实业务凭证仍缺，`verified_artifact_count=0`。这是一条真实性门禁，不是业务完成门禁。完整 GFIS SOP E2E 继续保持 `repair_required`，项目群评分保持 79/100 repair。

## Next

下一轮真实工作应转向收集或接入至少一类 verified live artifact，优先级建议：

1. `live_pod_waes_kds_receipt`
2. `live_runtime_records`
3. `live_material_batch`
