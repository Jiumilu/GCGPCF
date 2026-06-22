---
doc_id: GPCF-DOC-4BCB989BD4
title: GPCF-L4-GFIS-REPAIR-011 GFIS Runtime Handoff Candidate Control
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoG, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-011.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-011.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-011 GFIS Runtime Handoff Candidate Control

## 本轮目标

把 GFIS 运行层 SOP E2E 后半段从文档链推进到运行态 runner 覆盖：DeliveryNote/POD 之后的 WAES evidence review、KDS backlink write、Brain read-only query、PKC notification candidate、XiaoG audit candidate 必须有 GFIS 运行层 handoff candidate API 和 gap register。

## 真实缺口判断

上一轮已经覆盖 ProductionExecution、QualityInspection、InventoryBatch、DeliveryNote 四类 runtime evidence candidate，但 EvidenceRecord、KnowledgeBacklink 和 AI 协作面仍可能被文档或 fixture 冒充闭环。本轮必须补 handoff candidate，且不允许写成 WAES/KDS/POD/AI 完成。

## 实施内容

| 仓库 | 文件 | 动作 |
|---|---|---|
| GFIS | `gcfis_custom/gcfis_custom/api.py` | 新增 `create_runtime_sop_handoff_candidate`，只生成 `runtime_handoff_candidate_only` |
| GFIS | `gcfis_custom/gcfis_custom/install/doctypes.py` | 新增 `GCFIS SOP Runtime Handoff Candidate` |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 调用数增至 14，并新增 `EvidenceHandoffCandidate` gap |
| GFIS | `scripts/validate_gfis_runtime_sop_e2e.py` | validator 要求 `runtime_handoff_candidate=` 与 `runtime_handoff_candidate_contract=available` |
| GFIS | `scripts/validate_gfis_work_order_api_contract.py` | contract validator 覆盖 handoff candidate 和越界字段拒绝 |
| GPCF | `tools/kds-sync/validate_loop_engineering_integrity.py` | 总控完整性门禁要求 handoff 输出，防止后半段假闭环 |
| GPCF | `02-governance/loop/LOOP_CONTROL_BOARD.md`、`09-status/gpcf-project-status-matrix.md`、`docs/harness/loop-state.md`、`docs/harness/evidence/evidence-index.md`、`docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` | 回写 repair-011 状态，不升级完成态 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass；`created_docs=8 commits=8` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=14 created=2 cleanup_deleted=2 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=7` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`gfis_runtime_sop_e2e=repair_required`；`runtime_handoff_candidate=runtime_handoff_candidate_api_missing_reload_required` |
| `npm run test:e2e` in GFIS | pass；26 passed；Demo-only regression, not runtime SOP evidence |
| `git diff --check -- .` in GFIS | pass |

## 当前结论

GFIS 源码层已具备后半段 handoff candidate contract，但当前本机 GFIS 运行服务仍未加载新 API，所以完整 SOP E2E 保持 `repair_required`。这轮修复的是 Loop Engineering 的真实闭环检测能力：让运行态未加载、POD/WAES/KDS/AI 未真实交接的事实不会再被文档链掩盖。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未写 WAES 最终裁决、KDS 真实提交、POD、资金事实、外部 API 或真实通知。
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
