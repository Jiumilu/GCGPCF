---
doc_id: GPCF-DOC-8AB30F85DB
title: GPCF-L4-GFIS-REPAIR-014 GFIS Sync Event Candidate Fallback
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoG, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-014.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-014.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-014 GFIS Sync Event Candidate Fallback

## 本轮目标

在不执行 `bench migrate`、schema sync、生产写入或真实外部 API 写入的边界内，修复 GFIS 运行层候选证据因专用候选 DocType 未同步而不能落地的问题，并回写 GPCF 总控状态。

## 真实缺口判断

`GPCF-L4-GFIS-REPAIR-013` 已证明 GFIS 运行层合同已加载、WorkOrder 可 dry-run 创建并清理，但样品候选、运行层证据候选和交接候选仍为 schema gap。本轮不能把 schema sync/migrate 当作默认动作，因此改用既有运行层 DocType `GCFIS Sync Event` 作为 fallback carrier。

## 实施内容

| 仓库 | 文件/动作 | 动作 |
|---|---|---|
| GFIS | `gcfis_custom/gcfis_custom/api.py` | 新增候选写入 fallback：专用候选 DocType 存在时写专用对象；不存在时写 `GCFIS Sync Event` |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 按 API 返回的真实 doctype 记录和清理临时对象，并记录 `candidate_storage` / `fallback_carrier` |
| GFIS | `scripts/validate_gfis_work_order_api_contract.py` | 增加 fallback contract 断言 |
| GFIS | `docs/harness/sop-e2e/*` 与 `loop-round-GFIS-RUNTIME-SOP-E2E-011.md` | 回写 GFIS 运行层证据事实 |
| GPCF | 控制板、状态矩阵、loop-state、评分矩阵、evidence index、完整性 validator | 回写 REPAIR-014 当前事实，保持 repair_required 和 79/100 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass；`created_docs=11 commits=11` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=17 created=11 cleanup_deleted=11 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=11` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`gfis_runtime_sop_e2e=repair_required`；8 个候选节点均为 `passed_temp_created_cleanup_required` |
| `npm run test:e2e` in GFIS | pass；26 passed；Demo-only regression, not runtime SOP evidence |
| `git diff --check -- .` in GFIS | pass |

## 当前结论

GFIS 运行层现在可以在未授权 schema sync/migrate 的情况下，通过既有 `GCFIS Sync Event` 临时承载并清理：

- 3 个样品段候选。
- 4 个运行层证据候选。
- 1 个 WAES/KDS/Brain/PKC/XiaoG 交接候选。

完整 SOP E2E 仍保持 `repair_required`，原因是 5 项 KDS 葛化真实业务输入、POD、WAES/KDS 回执和运行层 UAT evidence 仍缺。项目群评分保持 79/100 repair，不恢复 100/100。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未执行 `bench migrate`、schema sync、数据库迁移、生产写入、真实外部 API 写入、权限变更、部署、Git push 或 accepted/integrated 状态升级。
- 本轮 dry-run 临时创建 11 个对象并全部清理。
- Demo E2E 只作为展示层回归，不作为 SOP 完成证据。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | completed_single_substantive_round |
