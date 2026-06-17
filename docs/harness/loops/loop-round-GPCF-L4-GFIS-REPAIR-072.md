---
doc_id: GPCF-DOC-5B2E774848
title: GPCF-L4-GFIS-REPAIR-072 GFIS 辽宁远航业务原话检索与运行态重载复测
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-072.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-072.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-072 GFIS 辽宁远航业务原话检索与运行态重载复测

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：接收用户补充的辽宁远航业务事实，把自然语言原话纳入 GFIS 运行层 KDS 检索别名和 validator，并验证上一轮 GFIS 报价客户确认请求 candidate-only API 已经在本机运行态生效。

## 输入

- 用户业务线索：今年元月份向辽宁远航提供 23 个样箱测试，样箱委托江西一家工厂生产；2026-05 辽宁远航计划采购并提交项目报价单；2026-06 计划使用现代精工产线组织量产。
- GFIS `gcfis_custom/gcfis_custom/api.py`
- GFIS `scripts/harvest_gfis_kds_gehu_inputs.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `scripts/validate_gfis_work_order_api_contract.py`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-065.md`

## 本轮动作

- GFIS 已把 `今年元月份`、`委托江西一家工厂`、`计划采购`、`提交项目报价单`、`组织量产` 纳入业务线索和 KDS 检索别名。
- GFIS checklist validator、runtime SOP validator、API contract validator 已要求这些原话进入运行态 evidence 链。
- 已受控重启本机 GFIS Docker 开发栈 `backend`、`frontend`、`scheduler`、`queue-short`、`queue-long`。
- 已复跑 GFIS KDS scanner、runtime dry-run、专项 validators、API contract validator、runtime SOP validator、Demo E2E 和 diff check。

## 验证结果

```text
kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=48 created=20 cleanup_deleted=20 runtime_gaps=35
runtime_liaoning_yuanhang_quotation_confirmation_request=runtime_liaoning_yuanhang_quotation_confirmation_request_candidate_passed_temp_created_cleanup_required
runtime_liaoning_yuanhang_quotation_confirmation=formal_customer_confirmation_missing:formal=0:weak=7:attachments=7
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
gfis_runtime_sop_e2e=repair_required
npm run test:e2e -> 26 passed
runner_exit=0 checklist_exit=0 queue_exit=0 contract_exit=0 runtime_exit=2 e2e_exit=0 diff_check_exit=0
```

## 真实性边界

- 运行态重载已验证上一轮 candidate-only API 生效，但这只是收证请求候选能力。
- 正式客户确认候选仍为 0。
- `real_submissions=0`、`verified_artifacts=0`、`missing_live_business_inputs=5` 保持不变。
- 用户业务原话、KDS 候选、报价 PDF、会议纪要、计划文字和采购计划均不得成为 verified live artifact。
- GFIS Demo E2E 26 passed 仅为 `pass_demo_only`。
- 不恢复 100/100，不升级 accepted/integrated。

## 禁止动作

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行数据库迁移、bench migrate 或 schema sync。
- 未执行权限、Token 或生产配置变更。
- 未写 WAES/KDS/POD 真实业务事实。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 7
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

继续围绕 top priority `liaoning_yuanhang_project_quotation` 补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件的脱敏索引。只有形成结构合格且业务可验真的 submission 后，GFIS 才能进入下一步运行层 real submission 复核；当前仍保持 repair。
