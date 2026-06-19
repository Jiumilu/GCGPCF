---
doc_id: GPCF-DOC-7A13C50C93
title: GFIS-RUNTIME-SOP-E2E-247
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-247.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-247.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-247

## 输入

- 上一轮 `GFIS-RUNTIME-SOP-E2E-246` 已建立 owner response / submission package release guard，并确认补证未完成时 release 必须 blocked。
- 当前真实缺口仍为：真实派发确认文件 0、有效责任方响应 0、有效 submission package 0、人工派发授权 0、KDS backlink 0、WAES evidence candidate 0、运行层主键 0。
- 本轮只允许建立 submission package release negative fixture guard；不得把负例门禁当成业务完成。

## 执行动作

- 新增 dispatch confirmation submission package release negative fixture guard builder 与 validator。
- 新增 machine-readable evidence 与 Markdown evidence。
- 在 `gcfis_custom/gcfis_custom/api.py` 新增只读 API。
- 在 `scripts/validate_gfis_runtime_sop_e2e.py` 接入主 runtime SOP validator。

## 输出摘要

- `source_owner_response_release_guard_items=1`
- `source_owner_response_release_allowed=0`
- `source_owner_response_release_blocked=1`
- `source_owner_response_release_block_reasons=9`
- `release_negative_fixture_guard_items=1`
- `release_negative_fixture_count=9`
- `rejected_release_fixture_count=9`
- `accepted_release_fixture_count=0`
- `submission_package_release_allowed=0`
- `submission_package_reopen_allowed=0`
- `submission_package_reopened=0`
- `submission_package_allowed=0`
- `remediation_complete=0`
- `owner_response_release_allowed=0`
- `owner_response_allowed=0`
- `owner_response_reopened=0`
- `confirmation_files_found=0`
- `valid_confirmations=0`
- `missing_confirmations=1`
- `dispatch_allowed=0`
- `request_items_dispatched=0`
- `release_override_allowed=0`
- `hold_release_allowed=0`
- `runtime_primary_key_ready=0`
- `review_queue=0`
- `runtime_intake=0`
- `waes_review=0`
- `verified=0`
- `runtime_sop_e2e=repair_required`

## 验证

- `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_submission_package_release_negative_fixture_guard.py`：使用 bundled Python 执行，pass。
- `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_submission_package_owner_response_release_guard.py`：使用 bundled Python 执行，pass。
- `python3 scripts/validate_gfis_runtime_sop_e2e.py`：expected exit 2，预期输出 `gfis_runtime_sop_e2e=repair_required` 和 `runtime_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_submission_package_release_negative_fixture_guard=manual_business_verification_release_ready_package_release_override_approval_request_dispatch_confirmation_submission_package_release_negative_fixtures_rejected:...`。
- `npm run test:e2e`：`26 passed`，仅作 GFIS Demo / frontend 回归，不作为 SOP 业务完成证据。
- `git diff --check -- .`：pass。

## 反馈

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 7
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary
- 本轮只拒收 9 类弱 release 声明：guard、remediation scan、GFIS Demo、KDS candidate-only、用户口述、Loop 文档、缺 hash/KDS backlink、缺 WAES candidate、未核验 accepted/integrated。
- 本轮不创建客户订单、平台订单、pending submission、合规人工核验完成文件、有效 release-ready package、source-of-record、运行层主键、dispatch confirmation、review queue、runtime intake、WAES review、verified artifact 或 accepted/integrated 状态。
- 下一轮建议：`GFIS-RUNTIME-SOP-E2E-248` 建立 real submission package release intake scanner，仅在补证完成且真实确认链齐备后才允许扫描真实 release 文件。
