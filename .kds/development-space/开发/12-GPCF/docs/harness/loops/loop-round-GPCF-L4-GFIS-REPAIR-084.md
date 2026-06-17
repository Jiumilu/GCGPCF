---
doc_id: GPCF-DOC-5552A2FBA5
title: GPCF-L4-GFIS-REPAIR-084 GFIS 辽宁远航报价单正式原件 submission 候选隔离
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-084.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-084.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-084 GFIS 辽宁远航报价单正式原件 submission 候选隔离

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：推动 GFIS 运行层新增辽宁远航正式原件 submission 候选隔离 API，让 top priority 报价项可以被运行层接收为 candidate-only，同时保持 `ready=false`、`verified=0` 和 `runtime_sop_e2e=repair_required`。

## 输入

- 用户业务事实线索：2026-01 辽宁远航 23 个样箱测试、江西工厂代工、2026-05 报价、2026-06 现代精工产线量产计划。
- GFIS `get_runtime_liaoning_yuanhang_formal_original_submission_instruction_packet` 输出。
- GFIS `get_runtime_liaoning_yuanhang_original_proof_candidate_gap_matrix` 输出。
- GFIS `gcfis_custom/gcfis_custom/api.py`
- GFIS `scripts/run_gfis_runtime_sop_e2e_dry_run.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-077.md`

## 本轮动作

- GFIS 新增 `create_runtime_liaoning_yuanhang_formal_original_submission_candidate`，并接入 runtime contract。
- GFIS dry-run 调用该 API，临时创建并清理 candidate-only 运行层候选。
- GFIS runtime validator 增加候选隔离输出，要求 `ready=false`、`verified_artifact_count=0`、`runtime_sop_e2e=repair_required`。
- GPCF 回写 loop-state、状态矩阵、控制板和 evidence index，继续保持 `repair_required`。

## 自我纠偏

本轮第一次 dry-run 发现：不能把 `客户确认函` 缺口套到泛化 formal original submission API 上。GFIS 候选锚点缺口矩阵显示，`liaoning_yuanhang_project_quotation` 的泛化正式原件 submission 缺口是报价单正式原件字段；客户确认函仍由报价客户确认专用 API、preflight 和 formal source gate 追踪。

GPCF 本轮记录该纠偏：泛化 API 只隔离报价单正式原件 candidate，不能替代客户确认函，也不能把报价 PDF、弱确认或用户线索升级为 verified artifact。

## 验证结果

```text
python3 -m py_compile gcfis_custom/gcfis_custom/api.py scripts/run_gfis_runtime_sop_e2e_dry_run.py scripts/validate_gfis_runtime_sop_e2e.py
pass

python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=55 created=22 cleanup_deleted=22 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=42 next=collect_verified_live_artifacts_or_runtime_reload

python3 scripts/validate_gfis_runtime_sop_e2e.py => expected exit 2
runtime_liaoning_yuanhang_formal_original_submission_candidate=isolated_pending_anchor:top=liaoning_yuanhang_project_quotation:ready=false:verified=0
runtime_liaoning_yuanhang_formal_original_submission_instruction_packet=formal_original_submission_instruction_ready:top=liaoning_yuanhang_project_quotation:ready=false
runtime_liaoning_yuanhang_quote_original_intake_preflight=awaiting_customer_confirmation_original:required=客户确认函:ready=false:verified=0
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
| 正式原件 submission candidate API | 已进入 dry-run 和 validator |
| proof_key | `liaoning_yuanhang_project_quotation` |
| isolation_status | `pending_formal_anchor_completion` |
| ready_for_runtime_intake | false |
| verified_artifact_count | 0 |
| real_submissions | 0 |
| GFIS SOP E2E | `repair_required` |

## 真实性边界

- formal original submission candidate 不是正式原始凭证。
- candidate-only 临时候选不进入 runtime intake，不进入 WAES final decision，不写 KDS，不升级 SOP E2E。
- 客户确认函仍由报价客户确认专用门禁追踪，不能被泛化 API 冒充。
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

继续补收辽宁远航报价单正式原件字段和客户确认函或等效正式确认原件脱敏索引；提交后仍需人工/WAES/KDS 复核。
