---
doc_id: GPCF-DOC-8AD9ECEAB7
title: GPCF-L4-GFIS-REPAIR-074 GFIS 辽宁远航业务事实 discovery intake
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-074.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-074.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-074 GFIS 辽宁远航业务事实 discovery intake

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：将用户补充的辽宁远航 2026 年 1 月样箱测试、江西委托生产、2026 年 5 月报价和 2026 年 6 月现代精工量产计划，纳入 GFIS 运行层报价客户确认候选扫描，并回写 GPCF 总控，不夸大为正式凭证或 SOP E2E 通过。

## 输入

- 用户补充业务事实：辽宁远航 23 个样箱测试、江西工厂委托生产、5 月项目报价单、6 月现代精工产线量产计划。
- GFIS `scripts/build_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py`
- GFIS `scripts/validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`

## 本轮动作

- GFIS 报价客户确认候选 builder 读取 KDS discovery refs，并按辽宁远航、陈启光、报价、采购、23 个样箱、江西委托生产、现代精工量产等业务词筛选。
- GFIS 新增 `USER_BUSINESS_FACT_TRACE`，把 4 条用户业务事实登记为采集线索，并保留下一步原始凭证要求。
- GFIS 新增 `discovered_context_requires_manual_intake` 分类，确保 discovery 命中只能作为采集上下文，不能自动成为正式客户确认或 verified live artifact。
- GFIS quotation confirmation validator 要求正式确认候选仍为 0，并要求用户事实全部 `may_count_as_verified_live_artifact=false`。
- GPCF 总控状态、状态矩阵、evidence index 和 loop record 回写为 `partial_repair`。

## 验证结果

```text
liaoning_yuanhang_quotation_confirmation_candidates=written candidates=55 formal=0 weak=7 attachments=7 discovered=37 runtime_sop_e2e=repair_required
liaoning_yuanhang_quotation_confirmation_candidates=pass candidates=55 formal=0 weak=7 attachments=7 discovered=37 runtime_sop_e2e=repair_required
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_quotation_confirmation=formal_customer_confirmation_missing:formal=0:weak=7:attachments=7
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
runtime_sop_e2e_master=failed_or_repair_required
npm run test:e2e => 26 passed
git diff --check -- . => pass
```

## 真实性边界

- 本轮证明 GFIS 已能用用户业务线索和 KDS discovery 缩小报价客户确认采集范围。
- 本轮不证明辽宁远航客户确认函、样箱测试签收/反馈、江西委托生产单、现代精工转量产批准或 WAES evidence ref 已取得。
- `formal_confirmation_candidate_count=0`、`real_submissions=0`、`verified_artifacts=0`、`runtime_sop_e2e=repair_required` 均保持不变。
- Demo E2E 26 passed 只登记为展示层回归，不作为 GFIS 运行层 SOP E2E 验收。

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
- generated_items: 6
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

继续围绕 top priority `liaoning_yuanhang_project_quotation`，将 37 条 discovery context 候选转成原始凭证采集请求优先级。优先补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件脱敏索引；若仍只有报价 PDF、计划采购、口头认可、微信发送或 KDS 上下文，GFIS 与 GPCF 均继续保持 `repair_required`。
