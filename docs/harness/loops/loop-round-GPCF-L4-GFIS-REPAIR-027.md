---
doc_id: GPCF-DOC-DDF4235DF5
title: GPCF L4 GFIS Repair 027 Runtime Gap Resolution Plan
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-027.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-027.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 027 Runtime Gap Resolution Plan

## 输入

上一轮已将 GFIS `FinanceBoundary` 缺口落到运行层金融边界只读门禁。本轮继续处理 Loop Engineering 的自我发现能力：GFIS 运行层必须把所有 blocked gate 汇总为机器可读修复计划，使下一轮能自动选择 GFIS 可行动缺口，而不是依赖人工口头指出问题。

## 动作

| 文件 | 动作 |
|---|---|
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/gcfis_custom/gcfis_custom/api.py` | 新增 GFIS 运行层只读 `get_runtime_sop_gap_resolution_plan` API |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 纳入 gap resolution plan，运行态调用数增至 27 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py` | validator 强制输出并检查 `runtime_gap_resolution_plan=repair_required` |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_work_order_api_contract.py` | 源码级 contract test 覆盖自诊断 API、forbidden writes 和 repair_required 分类 |
| GPCF 控制文档 | 更新控制板、状态矩阵、loop-state、evidence index 和 L4 closure matrix |

## 输出

- GFIS runtime validator 输出 `runtime_gap_resolution_plan=repair_required`。
- GFIS runner 输出 `runtime_calls=27 created=11 cleanup_deleted=11 runtime_gaps=21`。
- `RuntimeGapResolutionPlan` 输出 `gap_count=28`、`gfis_runtime_actionable_count=7`、`external_dependency_count=21`。
- GPCF/GFIS 继续保持 `repair_required`，项目群评分继续冻结 `79/100`。

## 验证

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass |
| `docker compose ... restart backend frontend queue-short queue-long scheduler websocket` in GFIS | pass；未 migrate/schema sync |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/harvest_gfis_kds_gehu_inputs.py` in GFIS | `categories=8/8 missing_live_business_inputs=5` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`; `runtime_calls=27 runtime_gaps=21` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`runtime_gap_resolution_plan=repair_required` |
| `npm run test:e2e` in GFIS | 26 passed；仅作为 `pass_demo_only` 展示层回归 |
| `git diff --check -- .` in GFIS | pass |

## 边界

- 未使用 GFIS Demo 作为业务主体。
- 未将自诊断修复计划写成 SOP 完成、业务验收、accepted 或 integrated。
- 未写 WAES 最终裁决、未提交 KDS 真实回指、未创建或确认 POD、未创建 Payment Entry、未创建 Sales Invoice、未执行 Stock Entry、未确认资金事实。
- 未执行 Git push、生产写入、真实外部 API 写入、数据库迁移、schema sync、`bench migrate`、权限变更、生产配置修改、部署或 accepted/integrated 状态升级。

## 真实计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | completed_single_substantive_round |
