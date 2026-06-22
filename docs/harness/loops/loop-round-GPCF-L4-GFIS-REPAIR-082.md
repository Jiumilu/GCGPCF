---
doc_id: GPCF-DOC-A5B22DA133
title: GPCF-L4-GFIS-REPAIR-082 GFIS 辽宁远航候选锚点缺口矩阵
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-082.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-082.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-082 GFIS 辽宁远航候选锚点缺口矩阵

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：推动 GFIS 运行层新增辽宁远航四项原始凭证候选锚点缺口矩阵，使 KDS 候选、缺失正式锚点和下一步提交要求可由运行层只读 API 输出。

## 输入

- KDS 候选：辽宁远航报价 PDF、行动台账、沟通纪要、葛化/现代精工预运营材料。
- 用户业务事实线索：2026-01 23 个样箱测试、江西工厂代工、2026-05 报价、2026-06 现代精工产线量产计划。
- GFIS `gcfis_custom/gcfis_custom/api.py`
- GFIS `scripts/run_gfis_runtime_sop_e2e_dry_run.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-075.md`

## 本轮动作

- GFIS 新增只读 API `get_runtime_liaoning_yuanhang_original_proof_candidate_gap_matrix`，并接入 runtime contract。
- GFIS dry-run 调用该 API，输出候选索引可用但不可 runtime intake。
- GFIS runtime validator 增加候选矩阵输出，要求 `items=4`、`ready=false`。
- GPCF 回写 loop-state、状态矩阵、控制板和 evidence index，继续保持 `repair_required`。

## 验证结果

```text
python3 -m py_compile gcfis_custom/gcfis_custom/api.py scripts/run_gfis_runtime_sop_e2e_dry_run.py scripts/validate_gfis_runtime_sop_e2e.py
pass

python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=53 created=21 cleanup_deleted=21 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=40 next=collect_verified_live_artifacts_or_runtime_reload

python3 scripts/validate_gfis_runtime_sop_e2e.py => expected exit 2
runtime_liaoning_yuanhang_original_proof_candidate_gap_matrix=candidate_gap_matrix_ready:items=4:ready=false
runtime_liaoning_yuanhang_original_proof_source_gate=liaoning_yuanhang_original_proof_sources_missing:items=4:ready=false:verified=0
runtime_sop_e2e_master=failed_or_repair_required

npm run test:e2e
26 passed

git diff --check -- .
pass
```

## 总控结论

| 项 | GPCF 判定 |
|---|---|
| GFIS 运行层主体 | 正确，未使用 Demo 作为 SOP 主体 |
| 候选锚点缺口矩阵 | 已进入 dry-run 和 validator |
| candidate_index_ready | true |
| ready_for_runtime_intake | false |
| verified_artifact_count | 0 |
| real_submissions | 0 |
| GFIS SOP E2E | `repair_required` |

## 真实性边界

- 候选矩阵不是正式原始凭证。
- KDS 候选、报价 PDF、行动台账、沟通纪要、预运营材料和用户业务线索不能单独成为 verified live artifact。
- GFIS Demo E2E `26 passed` 只登记为展示层回归，不作为 SOP Master 通过证据。
- 本轮不升级 accepted/integrated。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 4
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

选择一个 proof key，按矩阵中缺字段提交正式原件脱敏索引候选；优先补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件。
