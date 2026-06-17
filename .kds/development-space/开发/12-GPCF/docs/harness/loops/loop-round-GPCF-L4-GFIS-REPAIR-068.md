---
doc_id: GPCF-DOC-72AB13D2C2
title: GPCF-L4-GFIS-REPAIR-068 GFIS pending business verification submission
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-068.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-068.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-068 GFIS pending business verification submission

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：让 GFIS 运行层 submission validator 能表达 KDS 强候选进入业务复核队列的中间态，而不是把所有非 verified 材料都混为 rejected 或 missing。

## 输入

- GFIS `scripts/validate_gfis_verified_artifact_intake_submission.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`
- GFIS `docs/harness/sop-e2e/intake-submissions/examples/kds-quotation-pending-customer-confirmation.submission.json`

## 本轮动作

- GFIS 新增 KDS 报价 PDF pending submission 样例。
- GFIS submission validator 新增 `pending_business_verification_examples` 计数。
- GFIS runtime SOP validator 强制检查 pending 样例存在，并在 repair 输出中展示 pending 计数。
- GPCF 总控记录该中间态不会降低 repair_required，也不构成 verified live artifact。

## 验证结果

```text
python3 -m py_compile scripts/validate_gfis_verified_artifact_intake_submission.py scripts/validate_gfis_runtime_sop_e2e.py: pass
liaoning_yuanhang_verified_artifact_intake_submission=pass real_submissions=0 structure_valid=0 rejected_real_submissions=0 rejected_examples=1 pending_business_verification_examples=1 verified_artifacts=0 runtime_sop_e2e=repair_required
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=47 created=19 cleanup_deleted=19 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=34
gfis_runtime_sop_e2e=repair_required
runtime_verified_artifact_submission=missing_verified_artifact_submission
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
runtime_sop_e2e_master=failed_or_repair_required
validate_exit=2
git diff --check -- .: pass
```

## 真实性边界

- pending 样例来自 KDS canonical read-only 报价 PDF 候选，缺 `客户确认函`。
- pending 样例不计入 real submission。
- pending 样例不计入 verified artifact。
- GFIS SOP E2E 继续 `repair_required`。
- 不恢复 100/100，不升级 accepted/integrated。

## 禁止动作

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行数据库迁移、`bench migrate` 或 schema sync。
- 未执行权限变更、部署或生产配置修改。
- 未升级 `accepted` 或 `integrated`。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 3
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

接收客户确认函或 2026-01 样箱测试签收/反馈原件的脱敏索引，形成第一条 real submission；在业务/WAES/KDS 复核前继续保持 GFIS/GPCF `repair_required`。
