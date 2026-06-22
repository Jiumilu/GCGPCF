---
doc_id: GPCF-DOC-4F21C4151F
title: GPCF-L4-GFIS-REPAIR-085 GFIS 辽宁远航报价正式原件候选复核前隔离
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-085.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-085.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-085 GFIS 辽宁远航报价正式原件候选复核前隔离

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：把 GFIS 对辽宁远航的 KDS 报价 pending submission 样例纳入运行层 dry-run，让报价正式原件字段从“缺失”收敛为“可人工/WAES/KDS 复核但不可 runtime intake”，同时保持客户确认函缺失和 SOP E2E `repair_required`。

## 输入

- 用户补充业务事实：2026 年 1 月向辽宁远航提供 23 个样箱测试，样箱委托江西工厂生产；2026 年 5 月辽宁远航计划采购并提交项目报价单；2026 年 6 月计划使用现代精工产线组织量产。
- GFIS KDS 报价 pending submission 样例：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/intake-submissions/examples/kds-quotation-pending-customer-confirmation.submission.json`。
- GFIS runtime dry-run：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/run_gfis_runtime_sop_e2e_dry_run.py`。
- GFIS runtime SOP validator：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py`。
- GFIS loop record：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-078.md`。

## 本轮动作

- GFIS dry-run 读取 KDS 报价 pending submission 样例，并把 source uri/hash/backlink 和报价字段带入 formal original submission candidate。
- GFIS 主 validator 更新 formal submission candidate 摘要为 `review_ready_without_runtime_intake`。
- GPCF 回写 loop-state、项目状态矩阵、evidence index 和本轮记录。

## 验证结果

```text
python3 -m py_compile scripts/run_gfis_runtime_sop_e2e_dry_run.py scripts/validate_gfis_runtime_sop_e2e.py
pass

python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=55 created=22 cleanup_deleted=22 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=42 next=collect_verified_live_artifacts_or_runtime_reload

python3 scripts/validate_gfis_runtime_sop_e2e.py => expected exit 2
runtime_liaoning_yuanhang_formal_original_submission_candidate=review_ready_without_runtime_intake:top=liaoning_yuanhang_project_quotation:ready_for_manual_or_waes_review=true:ready_for_runtime_intake=false:verified=0
runtime_liaoning_yuanhang_quote_original_intake_preflight=awaiting_customer_confirmation_original:required=客户确认函:ready=false:verified=0
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
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
| proof_key | `liaoning_yuanhang_project_quotation` |
| formal candidate | `review_ready_without_runtime_intake` |
| ready_for_manual_or_waes_review | true |
| ready_for_runtime_intake | false |
| customer confirmation | missing |
| verified_artifact_count | 0 |
| real_submissions | 0 |
| GFIS SOP E2E | `repair_required` |

## 真实性边界

- KDS 报价 PDF/source hash/backlink 只能支持报价正式原件候选复核，不能替代客户确认函。
- 用户业务事实、KDS context、弱确认、报价 PDF 和 Loop 文档均不得升级为 verified live artifact。
- GFIS Demo E2E `26 passed` 只登记为展示层回归，不作为 SOP Master 通过证据。
- 本轮没有生产写入、真实外部 API 写入、KDS 写入、WAES 写入、bench migrate、schema sync、权限变更、部署、Git push 或 accepted/integrated 升级。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 4
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

进入 `GFIS-RUNTIME-SOP-E2E-079` / `GPCF-L4-GFIS-REPAIR-086`：围绕 `客户确认函` 或等效正式确认原件脱敏索引建立运行层补证包与校验，继续保持 candidate-only，禁止把报价 PDF 或业务线索升级为客户确认。
