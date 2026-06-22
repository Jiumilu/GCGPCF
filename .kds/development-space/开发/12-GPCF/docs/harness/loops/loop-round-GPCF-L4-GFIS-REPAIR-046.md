---
doc_id: GPCF-DOC-B2B2AA6E07
title: GPCF L4 GFIS Repair 046
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-046.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-046.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 046

## Round Control

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |

## Objective

将 GFIS 运行层 verified artifact intake proof anchors 纳入 GPCF 总控门禁，确保 Loop 不再把结构化弱凭证误判为真实业务凭证。

## Real Change

- GFIS `get_runtime_verified_artifact_intake_gate` 新增 `source_record_uri`、`source_record_hash`、`verification_actor`、`verification_method`、`kds_backlink_path` 必填证明锚点。
- GFIS intake gate 新增类别来源匹配、hash、URI、Demo 来源和验证方式白名单校验。
- GFIS contract validator 新增 weak verified artifact 反例，缺 proof anchors 时必须 blocked。
- GFIS runtime validator 纳入 proof anchor 关键短语检查。
- GPCF 控制板、loop-state、状态矩阵和 evidence index 回写 REPAIR-046。

## Evidence

| 检查 | 结果 |
|---|---|
| GFIS `python3 -m py_compile ...` | pass |
| GFIS `python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `bash scripts/check_gcfis_runtime_app.sh` | pass |
| GFIS `python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=42 created=19 cleanup_deleted=19 runtime_gaps=30` |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required`；`missing_inputs=5` |
| GFIS `npm run test:e2e` | pass；`26 passed`；Demo-only regression |

## Current State

GFIS 运行层仍为 `repair_required`。本轮不是 SOP E2E 完成，而是把 Loop Engineering 的真实性规则落实为运行层机器门禁：无外部 proof anchors 的结构化凭证不得污染 ready 状态。

## Boundaries

未执行 Git push、生产写入、真实外部 API 写入、物流 API、WAES/KDS/POD 写入、数据库迁移、权限变更、部署、accepted 或 integrated 升级。

## Next

下一轮从 collection dossier 中选择 1 类真实 verified artifact 做受控采集输入设计；优先 `live_pod_waes_kds_receipt` 或 `live_runtime_records`。
