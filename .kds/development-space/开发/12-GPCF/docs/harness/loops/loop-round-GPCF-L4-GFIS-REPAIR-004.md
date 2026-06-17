---
doc_id: GPCF-DOC-8429F70096
title: GPCF-L4-GFIS-REPAIR-004 GFIS Runtime KDS Gehua Input Gate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-004.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-004 GFIS Runtime KDS Gehua Input Gate

## Trigger

用户指出两个关键问题：

- GFIS 当前开发主体曾错误落到 `GFIS Demo`，正确主体必须是 `GFIS 运行层`。
- SOP E2E 大师测试失败不能被前端 Demo 回归通过掩盖。

本轮只做一个真实实质目标：把 GFIS Demo 与 GFIS 运行层的证据边界写入机器门禁，并让 GPCF 总控以后读取 GFIS 运行层 SOP validator，而不是只读取 Demo E2E last-run。

## Scope

| 项 | 说明 |
|---|---|
| 真实项目仓 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` |
| 总控项目仓 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF` |
| 正确主体 | GFIS 运行层 |
| 本轮目标 | 纠正 Demo pass 与运行层 pass 的边界；登记 KDS 葛化 missing_input；更新 GPCF 自我纠偏和 L4 validator |
| 非目标 | 不执行生产写入、真实外部 API、`bench migrate`、schema sync、数据库迁移、权限变更、生产配置变更、服务重启、推送或 accepted/integrated 升级 |

## Changes

| 路径 | 变更 |
|---|---|
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/e2e-failure-analysis.md` | 将 Demo E2E 状态更新为 `passed`，同时明确它不能证明运行层 SOP E2E |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/kds-gehu-data-input-register.md` | 登记 KDS 葛化受控源、缺失镜像源和 5 项真实业务 missing_input |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py` | 输出 `repair_required`，并暴露完整 SOP 链、missing_input 与 KDS source path 缺口 |
| `tools/kds-sync/validate_loop_self_correction_gate.py` | 新增 GFIS 运行层 SOP validator 调用，防止 Demo pass 恢复 100/100 |
| `tools/kds-sync/validate_l4_minimum_closed_loop.py` | 新增 GFIS 运行层 SOP validator 调用，L4 收口必须同时满足运行层通过 |
| `02-governance/loop/LOOP_CONTROL_BOARD.md`、`09-status/gpcf-project-status-matrix.md`、`docs/harness/loop-state.md`、`docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` | 回写当前状态、评分、下一轮任务和 evidence 边界 |

## Evidence

| 类型 | 命令或路径 | 结论 |
|---|---|---|
| GFIS runtime SOP validator | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | `gfis_runtime_sop_e2e=repair_required`；missing_inputs=5；missing_kds_source_paths=4 |
| GFIS WorkOrder API contract | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass |
| GFIS JS check | `npm run check:js` in GFIS | pass |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | 26 passed |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass |
| GPCF self-correction gate | `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | must remain repair/block until runtime SOP validator passes |
| GPCF L4 gate | `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | must remain repair until runtime SOP validator passes |

## Findings

| 发现 | 判断 |
|---|---|
| Demo E2E 通过 | 只证明展示层回归；不能作为 SOP 实现主体 |
| GFIS 运行层 SOP E2E | 仍为 `repair_required` |
| KDS 葛化真实输入 | 缺 5 项，包括真实客户订单、样品申请/签样、转量产批准、原料/采购/入库、作业卡/质检/库存/发货/POD/WAES/KDS 回执 |
| KDS 镜像源 | 缺 4 项 GFIS 运行层文档镜像 |
| L4 评分 | 继续保持 78/100，不得恢复 100/100 |
| Loop Engineering 改进 | 自我发现结果已转为机器门禁，后续 Demo pass 不会掩盖运行层 repair |

## Round Accounting

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | missing_input_and_runtime_retest_required |
| stop_evidence | GFIS runtime SOP validator 输出 `repair_required`；KDS 葛化真实输入与运行层 evidence 未补齐；未获生产写入、真实外部 API、数据库迁移、权限变更或 accepted/integrated 授权 |

## Next Input

下一轮优先补齐 KDS 葛化受控输入和 GFIS 运行层 KDS 镜像源；随后在受控边界内重载/复测 WorkOrder API，并继续推进 `ProductionExecution -> QualityInspection -> InventoryBatch -> DeliveryNote -> ProofOfDelivery -> WAES/KDS backlink` 的运行层 runner。
