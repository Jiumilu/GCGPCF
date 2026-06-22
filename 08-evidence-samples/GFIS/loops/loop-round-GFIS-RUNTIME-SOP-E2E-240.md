---
doc_id: GPCF-DOC-611E16E9CD
title: GFIS-RUNTIME-SOP-E2E-240
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-240.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-240.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-240

## 输入

- 上一轮 `GFIS-RUNTIME-SOP-E2E-239` 已将 dispatch confirmation 接收目录无真实确认文件的事实登记为 open hold。
- 当前真实缺口仍为：真实派发确认文件 0、人工派发授权 0、收件方身份确认 0、人工通道确认 0、KDS backlink 0、WAES evidence candidate 0。
- GFIS 运行层是现代精工 OEM 代加工生产期间和葛化自建工厂投产后的同一运行时系统；GFIS Demo 不得替代运行层事实。

## 执行动作

- 新增 hold release precheck builder 与 validator。
- 新增 machine-readable evidence 与 Markdown evidence。
- 在 `gcfis_custom/gcfis_custom/api.py` 新增只读 API。
- 在 `scripts/validate_gfis_runtime_sop_e2e.py` 接入主 runtime SOP validator。

## 输出摘要

- `source_post_scan_hold_gate_items=1`
- `source_open_holds=1`
- `source_hold_release_allowed=0`
- `precheck_items=1`
- `blocked=1`
- `blocked_reasons=6`
- `release_candidates=1`
- `release_allowed_items=0`
- `confirmation_files_found=0`
- `valid_confirmations=0`
- `missing_confirmations=1`
- `owner_response_allowed=0`
- `submission_package_allowed=0`
- `dispatch_allowed=0`
- `request_items_dispatched=0`
- `release_override_allowed=0`
- `hold_items=1`
- `open_holds=1`
- `hold_release_allowed=0`
- `runtime_primary_key_ready=0`
- `review_queue=0`
- `runtime_intake=0`
- `waes_review=0`
- `verified=0`
- `runtime_sop_e2e=repair_required`

## 验证

- `python3 -m py_compile scripts/build_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_hold_release_precheck.py scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_hold_release_precheck.py scripts/validate_gfis_runtime_sop_e2e.py gcfis_custom/gcfis_custom/api.py`：pass。
- `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_hold_release_precheck.py`：pass。
- `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_pending_business_verification_manual_completion_release_ready_package_release_override_approval_request_dispatch_confirmation_post_scan_hold_gate.py`：pass。
- `python3 scripts/validate_gfis_runtime_sop_e2e.py`：expected exit 2，输出 `gfis_runtime_sop_e2e=repair_required`。
- `npm run test:e2e`：26 passed，仅作为 demo/frontend 回归。
- `git diff --check -- .`：pass。

## 反馈

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 7
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary
- 本轮只建立 hold release precheck，不创建客户订单、平台订单、pending submission、合规人工核验完成文件、有效 release-ready package、source-of-record、运行层主键、dispatch confirmation、review queue、runtime intake、WAES review、verified artifact 或 accepted/integrated 状态。
- 下一轮建议：`GFIS-RUNTIME-SOP-E2E-241` 建立 dispatch confirmation hold release negative fixture guard，拒收 GFIS Demo、KDS candidate-only、用户口述、Loop 文档、缺 hash/KDS backlink/WAES candidate 等弱放行声明。
