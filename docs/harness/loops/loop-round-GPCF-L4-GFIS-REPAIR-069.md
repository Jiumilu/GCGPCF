---
doc_id: GPCF-DOC-F91705E737
title: GPCF-L4-GFIS-REPAIR-069 GFIS 辽宁远航原始凭证优先级队列
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-069.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-069.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-069 GFIS 辽宁远航原始凭证优先级队列

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：接收 GFIS `GFIS-RUNTIME-SOP-E2E-062` 的运行层改动，把辽宁远航四项原始凭证采集清单转成机器可排序优先级队列，并纳入 GPCF 总控状态。

## 输入

- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-original-proof-collection-checklist.json`
- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-proof-priority-queue.json`
- GFIS `scripts/validate_gfis_liaoning_yuanhang_proof_priority_queue.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`

## 本轮动作

- GFIS 新增辽宁远航原始凭证优先级队列。
- GFIS runtime SOP validator 接入 priority queue validator。
- GPCF 总控记录 top priority 为 `liaoning_yuanhang_project_quotation`，下一步优先补收辽宁远航客户确认函或等效确认原件。
- GPCF 保持 `repair_required`，不把优先级队列、KDS 候选或报价 PDF 计为 verified live artifact。

## 验证结果

```text
liaoning_yuanhang_proof_priority_queue=pass items=4 top=liaoning_yuanhang_project_quotation verified=0 runtime_sop_e2e=repair_required
liaoning_yuanhang_original_proof_collection_checklist=pass items=4 open=4 verified=0 runtime_sop_e2e=repair_required
liaoning_yuanhang_verified_artifact_intake_submission=pass real_submissions=0 structure_valid=0 rejected_real_submissions=0 rejected_examples=1 pending_business_verification_examples=1 verified_artifacts=0 runtime_sop_e2e=repair_required
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_proof_priority_queue=open_original_proof_priority_queue:top=liaoning_yuanhang_project_quotation:items=4
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
runtime_sop_e2e_master=failed_or_repair_required
gfis_checks_exit=0 runtime_exit=2 diff_check_exit=0
```

## 真实性边界

- proof priority queue 只排序采集动作，不证明业务事实完成。
- top priority 报价项仍缺 `客户确认函`，不计 real submission。
- `real_submissions=0`、`verified_artifacts=0`、`missing_live_business_inputs=5` 保持不变。
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
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

优先接收辽宁远航客户确认函或等效确认原件的脱敏索引，形成第一条 quotation real submission 候选；在业务/WAES/KDS 复核前继续保持 GFIS/GPCF `repair_required`。
