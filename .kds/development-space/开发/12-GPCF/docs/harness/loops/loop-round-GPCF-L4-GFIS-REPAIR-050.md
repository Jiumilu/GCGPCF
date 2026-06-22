---
doc_id: GPCF-DOC-42172F1051
title: GPCF L4 GFIS Repair 050
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-050.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-050.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 050

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

把 KDS 检索中发现的循环污染风险转为机器门禁：GPCF/Loop 自己生成的治理追踪文档，即使包含辽宁远航、样箱、报价单、量产计划等业务线索，也不能反向成为 GFIS `verified_live_artifact`。

## Real Change

- GFIS KDS scanner 新增 path/text disqualifier，识别 GPCF 轮次、evidence、loop-state、治理控制板、状态矩阵和 self-correction 文档。
- GFIS runtime validator 新增反循环检查，禁止带有 `loop_generated_trace_not_business_artifact`、`loop_trace_text_not_business_artifact` 或 `governance_document_not_business_artifact` 的候选成为 `verified_live_artifact`。
- GPCF `validate_loop_engineering_integrity.py` 读取 GFIS KDS coverage evidence，并在总控侧执行同样的反循环门禁。
- GFIS SOP E2E 文档和失败分析补充该规则，防止后续把 Loop 自己写出的线索误当成真实业务凭证。
- GPCF 控制板、loop-state、状态矩阵、evidence index 和本轮记录回写 REPAIR-050。

## Evidence

| 检查 | 结果 |
|---|---|
| GFIS `python3 -m py_compile scripts/harvest_gfis_kds_gehu_inputs.py scripts/validate_gfis_runtime_sop_e2e.py` | pass |
| GFIS `python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=1` |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GPCF `python3 -m py_compile tools/kds-sync/validate_loop_engineering_integrity.py` | pass |
| GPCF `python3 tools/kds-sync/validate_loop_engineering_integrity.py` | pass；`runtime_sop_e2e=repair_required project_group_score=79` |

## Current State

GFIS 已能区分三层材料：真实业务凭证、KDS 受控引用、Loop/GPCF 治理追踪文档。`live_sample_signoff_release` 仍是唯一开放缺口；用户提供的辽宁远航 23 个样箱、江西代工、5 月报价单和 6 月现代精工产线量产计划仍是待核验线索，不是 verified live artifact。

## Boundaries

未执行 Git push、生产写入、真实外部 API 写入、物流 API、WAES/KDS/POD 写入、数据库迁移、权限变更、部署、accepted 或 integrated 升级。

## Next

采集并校验 `live_sample_signoff_release` 的原始样品申请、客户签样附件或豁免记录、项目报价单、转量产批准、WAES evidence ref、KDS backlink path 与 source record hash；采集前继续把 Loop/GPCF 追踪文档排除在 live proof 之外。
