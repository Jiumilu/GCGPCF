---
doc_id: GPCF-DOC-D1CB84A7AE
title: GPCF-L4-GFIS-REPAIR-071 GFIS 辽宁远航报价确认请求候选 API
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-071.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-071.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-071 GFIS 辽宁远航报价确认请求候选 API

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：接收 GFIS `GFIS-RUNTIME-SOP-E2E-064` 的运行层改动，把辽宁远航报价客户确认从候选清单推进为 GFIS 运行层 candidate-only 请求 API，并纳入 GPCF 总控状态。

## 输入

- GFIS `gcfis_custom/gcfis_custom/api.py`
- GFIS `scripts/run_gfis_runtime_sop_e2e_dry_run.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dry-run-result.json`
- GFIS `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-064.md`

## 本轮动作

- GFIS 新增 `create_runtime_liaoning_yuanhang_quotation_confirmation_request_candidate`。
- GFIS runner 已调用该 API；当前本机运行态未重载，输出 `runtime_liaoning_yuanhang_quotation_confirmation_request_api_missing_reload_required`。
- GFIS 主 validator 已纳入该状态，并继续保持 `gfis_runtime_sop_e2e=repair_required`。
- GPCF 总控登记：该 API 是 candidate-only 收证请求能力，不是客户正式确认事实。

## 验证结果

```text
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=48 created=19 cleanup_deleted=19 runtime_gaps=35
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_quotation_confirmation=formal_customer_confirmation_missing:formal=0:weak=7:attachments=7
runtime_liaoning_yuanhang_quotation_confirmation_request=runtime_liaoning_yuanhang_quotation_confirmation_request_api_missing_reload_required
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
npm run test:e2e -> 26 passed
runtime_exit=2 test_exit=0 diff_check_exit=0
```

## 真实性边界

- 本轮只增加 GFIS 运行层 candidate-only 请求能力。
- 当前本机 GFIS 运行态服务尚未加载新 API，需要受控重载后复测。
- 正式客户确认候选仍为 0。
- `real_submissions=0`、`verified_artifacts=0`、`missing_live_business_inputs=5` 保持不变。
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
- generated_items: 4
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

受控重载 GFIS 本机运行态服务，复跑 dry-run，确认报价客户确认请求候选可以临时创建并清理；同时继续补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件的脱敏索引。
