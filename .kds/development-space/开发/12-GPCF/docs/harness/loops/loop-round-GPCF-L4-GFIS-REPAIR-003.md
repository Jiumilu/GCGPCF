---
doc_id: GPCF-DOC-98EB05CB36
title: GPCF-L4-GFIS-REPAIR-003 GFIS WorkOrder Runtime API Blocker Isolation
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-003.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-003 GFIS WorkOrder Runtime API Blocker Isolation

## Trigger

`GPCF-L4-GFIS-REPAIR-002` 已验证部分 GFIS 运行层 API，但 WorkOrder 未进入运行态调用。本轮只做一个真实实质目标：修复并验证 `create_work_order_from_production_demand` 的源码契约，同时让 runtime runner 真实调用该 API 并登记阻塞。

## Scope

| 项 | 说明 |
|---|---|
| 真实项目仓 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` |
| 正确主体 | GFIS 运行层 |
| 本轮目标 | 修复 WorkOrder API 对 Frappe RPC JSON 字符串入参的处理，并把运行态 blocker 写入 evidence |
| 非目标 | 不执行生产写入、真实外部 API、`bench migrate`、schema sync、数据库迁移、权限变更、生产配置变更、服务重启或 accepted/integrated 升级 |

## Changes

| 路径 | 变更 |
|---|---|
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/gcfis_custom/gcfis_custom/api.py` | `create_work_order_from_production_demand` 入口改为可解析 JSON 字符串/对象，并去除 whitelisted 入口附近复杂类型注解 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_work_order_api_contract.py` | 增加 JSON 字符串 demand 与 invalid JSON 契约覆盖 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/run_gfis_runtime_sop_e2e_dry_run.py` | 增加 WorkOrder runtime API 调用与 blocker 分类 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/README.md` | 登记 WorkOrder 源码契约 pass、运行态仍需重载复测 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/gfis-runtime-evidence-map.md` | 更新 WorkOrder evidence 状态 |

## Evidence

| 类型 | 命令或路径 | 结论 |
|---|---|---|
| GFIS WorkOrder contract | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` | pass；JSON 字符串入参、幂等、越界字段、非法 JSON 和状态流转均覆盖 |
| GFIS SOP precheck | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | pass；仍只是 precheck，不代表完整运行层 SOP E2E |
| GFIS runtime runner | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；runtime_calls=8，created=2，cleanup_deleted=2，runtime_gaps=5 |
| GFIS runtime evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dry-run-result.json` | WorkOrder blocker=`runtime_api_stale_code_or_reload_required` |

## Findings

| 发现 | 判断 |
|---|---|
| GFIS WorkOrder API 源码契约问题 | 已修复；本地 fake-Frappe contract validator 通过 |
| 本机 GFIS 运行态 WorkOrder 调用 | 仍失败；返回旧实现的 `AttributeError: 'str' object has no attribute 'get'` |
| 最可能原因 | GFIS 本机运行服务仍加载旧导入实现，需要受控重载后复测 |
| 是否完成完整 SOP E2E | 否 |
| 是否可恢复 `accepted/integrated/L4 closed` | 否 |

## Round Accounting

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | runtime_reload_required |
| stop_evidence | 源码 contract validator 通过，但本机 runtime 仍返回旧实现错误；未获服务重载/重启授权，本轮不擅自重启 |

## Next Input

下一轮优先做受控 GFIS 服务重载/重启复测，或在不重启的情况下建立可证明新代码已被运行态加载的 endpoint/version evidence。重载后复测 `create_work_order_from_production_demand`，再继续 `ProductionExecution -> QualityInspection -> InventoryBatch -> DeliveryNote` runner。
