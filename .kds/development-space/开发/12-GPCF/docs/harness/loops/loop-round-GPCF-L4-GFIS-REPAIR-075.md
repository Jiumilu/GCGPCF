---
doc_id: GPCF-DOC-0FE0AB07DD
title: GPCF-L4-GFIS-REPAIR-075 GFIS 辽宁远航 discovery 原始凭证请求包
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-075.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-075.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-075 GFIS 辽宁远航 discovery 原始凭证请求包

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：接收 GFIS 将 37 条 KDS discovery context 候选转为 4 类辽宁远航原始凭证采集请求的证据，并在 GPCF 总控中保持 `repair_required`。

## 输入

- GFIS `docs/harness/sop-e2e/evidence/liaoning-yuanhang-discovery-intake-requests.json`
- GFIS `scripts/build_gfis_liaoning_yuanhang_discovery_intake_requests.py`
- GFIS `scripts/validate_gfis_liaoning_yuanhang_discovery_intake_requests.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-068.md`

## 本轮动作

- GFIS 新增 discovery intake request builder/validator。
- GFIS 将 discovery context 分配到 4 个采集请求：报价客户确认、样箱测试/签收、江西委托生产、现代精工转量产放行。
- GFIS 主 validator 新增 `runtime_liaoning_yuanhang_discovery_intake_requests` 输出。
- GPCF 回写 loop-state、控制板、状态矩阵、evidence index 和 loops README。

## 验证结果

```text
liaoning_yuanhang_discovery_intake_requests=pass requests=4 with_context=4 discovered=37 verified=0 runtime_sop_e2e=repair_required
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_discovery_intake_requests=open_original_proof_intake_requests:requests=4:with_context=4:discovered=37:verified=0
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
git diff --check -- . => pass
```

## 真实性边界

- 本轮证明 GFIS 已能把 KDS discovery context 转成原始凭证采集请求。
- 本轮不证明任何原始凭证已经收到。
- `verified=0`、`real_submissions=0`、`verified_artifacts=0`、`runtime_sop_e2e=repair_required` 保持不变。
- 不恢复 100/100，不升级 accepted/integrated。

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
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

继续围绕 `LY-QUOTE-CONFIRMATION-ORIGINAL` 补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件脱敏索引。若仍只有 KDS 上下文、报价 PDF、口头认可、计划采购或会议纪要，则继续保持 `repair_required`。
