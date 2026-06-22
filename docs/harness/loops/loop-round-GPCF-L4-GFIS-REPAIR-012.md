---
doc_id: GPCF-DOC-0E0B8A7E4B
title: GPCF-L4-GFIS-REPAIR-012 GFIS Runtime Sample Candidate Control
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoG, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-012.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-012.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-012 GFIS Runtime Sample Candidate Control

## 本轮目标

把完整 SOP 中“样品申请与打样”阶段从文档/fixture 校验推进到 GFIS 运行层 runner 覆盖。SampleWorkOrder、SampleQualityInspection、SampleDispatch 必须进入运行态调用链和 gap register。

## 真实缺口判断

上一轮已覆盖 WAES/KDS/Brain/PKC/XiaoG handoff candidate，但样品段仍没有运行层 API 调用。若样品段不进入 runner，Loop 可能错误地跳过客户签样和转量产前置条件，直接推进正式工厂订单和量产段。

## 实施内容

| 仓库 | 文件 | 动作 |
|---|---|---|
| GFIS | `gcfis_custom/gcfis_custom/api.py` | 新增 `create_runtime_sop_sample_candidate`，只生成 `runtime_sample_candidate_only` |
| GFIS | `gcfis_custom/gcfis_custom/install/doctypes.py` | 新增 `GCFIS SOP Runtime Sample Candidate` |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 调用数增至 17，并新增 SampleWorkOrder、SampleQualityInspection、SampleDispatch gap |
| GFIS | `scripts/validate_gfis_runtime_sop_e2e.py` | validator 要求 `runtime_sample_candidates=` 和 `runtime_sample_candidate_contract=available` |
| GFIS | `scripts/validate_gfis_work_order_api_contract.py` | contract validator 覆盖 sample candidate 与越界字段拒绝 |
| GPCF | `tools/kds-sync/validate_loop_engineering_integrity.py` | 总控完整性门禁要求样品段输出，防止样品段假闭环 |
| GPCF | `02-governance/loop/LOOP_CONTROL_BOARD.md`、`09-status/gpcf-project-status-matrix.md`、`docs/harness/loop-state.md`、`docs/harness/evidence/evidence-index.md`、`docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` | 回写 repair-012 状态，不升级完成态 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass；`created_docs=11 commits=11` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=17 created=2 cleanup_deleted=2 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=10` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`gfis_runtime_sop_e2e=repair_required`；3 类 sample candidates 均为 `runtime_sample_candidate_api_missing_reload_required` |
| `npm run test:e2e` in GFIS | pass；26 passed；Demo-only regression, not runtime SOP evidence |
| `git diff --check -- .` in GFIS | pass |

## 当前结论

GFIS 源码层已具备样品段 sample candidate contract，但当前本机 GFIS 运行服务仍未加载新 API，所以完整 SOP E2E 保持 `repair_required`。这轮修复的是完整链路覆盖能力：样品工单、样品质检、样品发出必须被运行态检测，不允许只靠文档链或 Demo 展示链证明。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未确认客户签样、转量产、正式工厂订单、WAES 最终裁决或 accepted/integrated。
- 未执行 `bench migrate`、schema sync、数据库迁移、权限变更、生产配置修改、Docker/bench 重启、部署、Git push 或 accepted/integrated 状态升级。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | runtime_reload_required |
