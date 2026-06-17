---
doc_id: GPCF-DOC-83CA73C4BE
title: GPCF-L4-GFIS-REPAIR-081 GFIS 辽宁远航四项原始凭证正式来源总门禁
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-081.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-081.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-081 GFIS 辽宁远航四项原始凭证正式来源总门禁

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：推动 GFIS 运行层新增辽宁远航四项原始凭证正式来源总门禁，防止只校验客户确认函而遗漏样箱测试、江西委托生产和现代精工量产放行原始凭证。

## 输入

- 用户业务事实线索：2026 年 1 月向辽宁远航提供 23 个样箱测试；样箱委托江西工厂生产；2026 年 5 月辽宁远航计划采购并提交项目报价单；2026 年 6 月计划使用现代精工产线组织量产。
- GFIS `gcfis_custom/gcfis_custom/api.py`
- GFIS `scripts/run_gfis_runtime_sop_e2e_dry_run.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dry-run-result.json`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-074.md`

## 本轮动作

- GFIS 新增只读 API `get_runtime_liaoning_yuanhang_original_proof_source_gate`，并接入 runtime contract。
- GFIS dry-run 真实调用该门禁 API，输出 `liaoning_yuanhang_original_proof_sources_missing`。
- GFIS runtime validator 增加四项原始凭证正式来源门禁输出，要求 `items=4`、`ready=false`、`verified=0`、`formal_original_candidate_count=0`。
- GPCF 回写 loop-state、状态矩阵、控制板和 evidence index，继续保持 `repair_required`。

## 验证结果

```text
python3 -m py_compile gcfis_custom/gcfis_custom/api.py scripts/run_gfis_runtime_sop_e2e_dry_run.py scripts/validate_gfis_runtime_sop_e2e.py
pass

python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=52 created=21 cleanup_deleted=21 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=39 next=collect_verified_live_artifacts_or_runtime_reload

python3 scripts/validate_gfis_runtime_sop_e2e.py => expected exit 2
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_original_proof_source_gate=liaoning_yuanhang_original_proof_sources_missing:items=4:ready=false:verified=0
runtime_liaoning_yuanhang_customer_confirmation_formal_source_gate=formal_customer_confirmation_source_missing:ready=false:verified=0
runtime_liaoning_yuanhang_customer_confirmation_submission=isolated_pending_business_verification:ready=false:verified=0
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
| 四项正式来源总门禁 | 已进入 dry-run 和 validator |
| proof_item_count | 4 |
| missing_proof_count | 4 |
| formal_source_ready | false |
| ready_for_runtime_intake | false |
| verified_artifact_count | 0 |
| formal_original_candidate_count | 0 |
| GFIS SOP E2E | `repair_required` |

## 真实性边界

- 用户业务线索可帮助定位凭证，但不能作为正式原始凭证。
- KDS discovery、报价 PDF、弱确认、业务口述、Loop 记录或采集请求不得替代样箱测试记录、江西委托生产记录、辽宁远航项目报价/采购确认原件和现代精工量产放行记录。
- GFIS Demo E2E `26 passed` 只登记为展示层回归，不作为 SOP Master 通过证据。
- 本轮不确认 GFIS runtime SOP E2E 通过。
- 本轮不升级 accepted/integrated。

## 禁止动作

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行数据库迁移、bench migrate 或 schema sync。
- 未执行权限、Token 或生产配置变更。
- 未部署。
- 未升级 accepted/integrated。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 4
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

优先接收 4 项原始凭证中任一项的正式原件脱敏索引，再在 GFIS 提交 formal source type real submission 候选，并保持人工/WAES/KDS 复核。GPCF 在这些原件进入复核前继续保持 GFIS/GPCF `repair_required`。
