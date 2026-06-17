---
doc_id: GPCF-DOC-255B06AF2A
title: GPCF-L4-GFIS-REPAIR-013 GFIS Runtime Reload And WorkOrder BOM Closure
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-013.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-013.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-013 GFIS Runtime Reload And WorkOrder BOM Closure

## 本轮目标

在不执行 `bench migrate`、schema sync、生产写入或真实外部 API 写入的边界内，受控重载 GFIS 本机运行服务，修复 WorkOrder `bom_no` 必填字段缺口，并复测 GFIS 运行层 SOP E2E runner。

## 真实缺口判断

`GPCF-L4-GFIS-REPAIR-012` 已把样品段纳入 runner，但运行态仍显示 API 未加载。受控重载后，Loop 需要判断真实阻塞到底是旧代码、标准 WorkOrder 必填字段、候选 DocType schema，还是 KDS 葛化业务输入缺失。

## 实施内容

| 仓库 | 文件/动作 | 动作 |
|---|---|---|
| GFIS | 本机 Docker compose restart | 仅重启 backend/frontend/queue/scheduler/websocket；未执行 migrate/schema sync |
| GFIS | `gcfis_custom/gcfis_custom/api.py` | `get_shipment_evidence` 改为字段安全只读；WorkOrder API 增加 `bom_no` 必填和持久化 |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 从 fixture 传入 BOM，并把候选 DocType 缺口归类为 schema gap |
| GFIS | `scripts/validate_gfis_work_order_api_contract.py` | 增加 BOM 与发货只读字段安全契约 |
| GFIS | `docs/harness/sop-e2e/*` | 回写运行态 evidence map 和 README |
| GPCF | 控制板、状态矩阵、loop-state、评分矩阵、evidence index、完整性 validator | 回写 REPAIR-013 当前事实，保持 repair_required |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass；`created_docs=11 commits=11` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=17 created=3 cleanup_deleted=3 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=11` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`gfis_runtime_sop_e2e=repair_required`；`runtime_contract_status=loaded_current_contract`；`work_order_runtime=runtime_api_passed_temp_created_cleanup_required` |
| `npm run test:e2e` in GFIS | pass；26 passed；Demo-only regression, not runtime SOP evidence |

## 当前结论

GFIS 运行层已经从“服务未加载新 API”推进为“合同已加载，WorkOrder 可 dry-run 创建并清理”。这是真实运行层进展。

完整 SOP E2E 仍保持 `repair_required`，原因是：

- 5 项 KDS 葛化真实业务输入仍为 missing_input。
- `GCFIS SOP Runtime Sample Candidate`、`GCFIS SOP Runtime Evidence Candidate`、`GCFIS SOP Runtime Handoff Candidate` 当前均为 schema gap，需要明确授权后执行 schema sync / migrate。
- POD、WAES/KDS 回执和真实 UAT evidence 仍未闭合。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未执行 `bench migrate`、schema sync、数据库迁移、生产写入、真实外部 API 写入、权限变更、部署、Git push 或 accepted/integrated 状态升级。
- 本轮 dry-run 临时创建 3 个对象并全部清理。
- 项目群评分保持 79/100 repair，不恢复 100/100。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | schema_sync_authorization_boundary |
