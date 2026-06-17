---
doc_id: GPCF-DOC-6913FD52DB
title: L4 Minimum Closed Loop Closure Score Matrix
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/l4-closure-score-matrix.md
source_path: docs/harness/minimum-closed-loop/l4-closure-score-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# L4 Minimum Closed Loop Closure Score Matrix

## Current Correction Status

2026-06-17 最新修正：GFIS 已推进到 `GFIS-RUNTIME-SOP-E2E-204` / `GPCF-L4-GFIS-REPAIR-211`。本轮先复核 GFIS 203 总控同步，再在第一个运行对象族 `CustomerRequirementOrPlatformOrder` 的 owner/manual request dispatch confirmation hold release negative fixture guard 之后，新增 dispatch confirmation release-ready schema。用户确认 GFIS 是葛化工厂建设期由现代精工 OEM 代加工生产时使用、以及葛化自建工厂投产后继续使用的同一运行时系统；本轮只定义真实派发确认释放 hold 前必须具备的 18 个字段和 10 项 readiness 条件，不能替代 GFIS 运行层主键、source-of-record、有效授权信封、派发动作、有效派发确认或业务完成。项目级 validator 输出 `release_ready_schema_items=1 required_fields=18 readiness_requirements=10 submitted_confirmation_files=0 valid_confirmation_files=0 release_ready_confirmations=0 missing_required_fields=18 missing_readiness_requirements=10 hold_release_allowed=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 runtime_primary_key_missing=1 runtime_sop_e2e=repair_required`；主 runtime SOP validator 仍 expected exit 2 并输出 `gfis_runtime_sop_e2e=repair_required`。因此矩阵继续保持 `79/100` 与 `repair_required`，不得恢复 closed、accepted 或 integrated。

运行层定位修正：辽宁远航合同链发生在葛化工厂建设阶段，现代精工工厂承担 OEM 代加工生产；GFIS 在当前阶段服务于现代精工代加工生产运行，在葛化自建工厂投产后继续作为同一 GFIS 运行时系统承接葛化自有工厂运行。此定位不允许 GFIS Demo、KDS 候选、用户口述、README、弱授权邮件或未核验 accepted/integrated 声明替代运行层事实。

2026-06-14 自我纠错结论：本矩阵原 `100/100` 和 `L4 closure achieved` 结论失效。原因是 GFIS 证据错误使用 `gcfis_demo` 作为工厂运行事实主体，而正确主体应为 GFIS 运行层。

最新修正：GFIS Demo E2E 已从 failed 修复为 `26 passed`，但这只能证明展示层回归通过，必须标记为 `pass_demo_only`。GFIS 运行层 SOP E2E validator 当前仍输出 `gfis_runtime_sop_e2e=repair_required`；4 项 GFIS 运行层 KDS 镜像源已补齐，`missing_kds_source_paths=0`，源码契约已补齐 `create_runtime_sop_sample_candidate`、`create_runtime_sop_evidence_candidate` 与 `create_runtime_sop_handoff_candidate`，validator 输出 `runtime_sample_candidate_contract=available`、`runtime_evidence_candidate_contract=available` 和 `runtime_handoff_candidate_contract=available`。新增 KDS 葛化受控资料扫描后，17 个 KDS 受控来源覆盖 8/8 类预检资料，validator 输出 `kds_controlled_coverage=available missing_live_business_inputs=5`。受控重载后只读运行态合同状态已输出 `runtime_contract_status=loaded_current_contract`，WorkOrder 已通过 `bom_no` 修复进入 `runtime_api_passed_temp_created_cleanup_required`，ShipmentEvidenceRead 为 `shipment_evidence_read_passed`；三类样品候选、四类运行层证据候选和 handoff candidate 已通过既有 `GCFIS Sync Event` fallback 临时创建并清理。最新 live proof 审计显示 5 类缺口均有 KDS 候选引用，但均被标记为 `controlled_reference_not_live_proof` 或 `unverified_reference`，不是 verified live artifact；GFIS 运行层新增只读 `get_runtime_verified_artifact_intake_summary` 后，validator 输出 `runtime_verified_artifact_intake_summary=missing_verified_artifact_intake`，并确认 `ready_category_count=0`、`missing_category_count=5`、`blocked_artifact_count=0`。GFIS contract validator 已证明 partial-good intake 仍保持 `missing_verified_artifact_intake`，只有五类 `运行层真实输入门禁` 全部有效且无阻断时才允许 `verified_artifact_intake_ready_for_review`。本轮新增只读 `get_runtime_verified_artifact_collection_dossier`，validator 输出 `runtime_verified_artifact_collection_dossier=verified_artifact_collection_dossier_open`、`open_request_count=5`、`collected_artifact_count=0`、`dossier_item_count=5`；runner 输出 `runtime_calls=42 created=19 cleanup_deleted=19 runtime_gaps=30`。当前状态继续保持 `L4 repair required`，项目群评分暂定 `79/100`。

2026-06-14 追加修正：GFIS 已将辽宁远航 4 项原始凭证采集清单推进为 verified artifact intake 前置校验，4 个 slot 均为 `awaiting_original_proof`、`ready_for_runtime_intake=false`、`verified_artifact_count=0`。`python3 scripts/validate_gfis_verified_artifact_intake_precheck.py` 通过，但 `python3 scripts/validate_gfis_runtime_sop_e2e.py` 仍按预期 exit 2；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34`。该前置校验只防止报价 PDF、会议纪要、计划文字和用户口述污染 ready 状态，不构成 GFIS SOP E2E 完成证据，项目群评分继续冻结为 `79/100`。

2026-06-14 再追加修正：GFIS 已将用户补充的 2026-01 辽宁远航 23 个样箱、江西委托生产、2026-05 报价、2026-06 现代精工量产计划写入 verified artifact intake packet 模板。4 个 packet slot 均为 `blank_pending_original_proof`、`ready_for_runtime_intake=false`、`verified_artifact_count=0`，业务时间线只作为 `unverified_trace_hint`，不构成 verified live artifact。`python3 scripts/validate_gfis_verified_artifact_intake_packet_template.py` 通过，`python3 scripts/validate_gfis_runtime_sop_e2e.py` 仍按预期 exit 2；项目群评分继续冻结为 `79/100`。

Loop Engineering 当前结论：项目群不能只依赖人类指出问题。主体漂移必须被自动标记为 `subject_drift_detected`；Demo 通过但 runtime 失败必须以 runtime failed 为主状态；controlled reference、候选 ID 和说明文本不得冒充 verified live artifact；任何 `repair_required` 存在时不得恢复 100/100、closed、accepted 或 integrated。

本文件保留 L4 原始链路结构，但所有 GFIS/GPCF 收口判定以 `GPCF-L4-CORR-001` 和 `docs/harness/evidence/loop_self_correction_assessment.json` 为准。

## Closure Boundary

This matrix closes L4 only. It proves that all 12 GlobalCloud projects participate in the same minimum closed loop with controlled roles, evidence and validators. It does not mark any project accepted, integrated, deployed, production-written or customer-signed.

## Project Coverage

| Project | L4 round | Role in minimum loop | Evidence status | Validator status | Boundary |
|---|---|---|---|---|---|
| GPCF | GPCF-L4-001 / GPCF-L4-012 / GPCF-L4-CORR-001 | Project-group governance, score matrix, evidence intake and self-correction | repair_required | pass via correction gate | Does not replace business systems |
| MMC | MMC-L4-002 | Policy templates, resource gate fields and strategy boundary | ready_for_review | pass | Does not own factory facts |
| KDS | KDS-L4-003 | Knowledge source, SOP/case index and evidence backlinks | ready_for_review | pass | Does not replace current business facts |
| Brain | Brain-L4-004 | SOP/case retrieval UI and explanation surface | ready_for_review | pass | Consumes KDS, does not become KDS |
| PKC | PKC-L4-005 | Personal task, notification and todo-state intake | ready_for_review | pass | Workbench only, no business fact ownership |
| PVAOS | PVAOS-L4-006 | Tenant, organization, partner and permission baseline | ready_for_review | pass | Entry/portal layer only |
| GPC | GPC-L4-007 | Platform order, sample approval, production release and POD contract | ready_for_review | pass | Does not write GFIS factory facts |
| GFIS | GFIS-L4-008 / GFIS-RUNTIME-SOP-E2E-001..202 | Factory-side formula, sample, order, work-order, quality, inventory, shipment and handoff candidate facts | repair_required | Demo E2E passed but is `pass_demo_only`; KDS controlled references cover 12 SOP stages and 12 runtime object families, and first object dispatch confirmation hold release precheck reports `request_package_items=1`, `prepared_requests=1`, `dispatch_preflight_items=1`, `dispatch_preflight_blocked=1`, `dispatch_authorizations=0`, `recipients_confirmed=0`, `manual_channels_confirmed=0`, `dispatch_allowed=0`, `dispatched_requests=0`, `confirmation_slots=1`, `receiving_directory_exists=1`, `receiving_readme_exists=1`, `expected_confirmation_files=1`, `confirmation_files_found=0`, `structure_valid_confirmations=0`, `valid_confirmations=0`, `invalid_confirmations=0`, `missing_confirmations=1`, `unexpected_files=0`, `acknowledgement_allowed=0`, `acknowledged_requests=0`, `review_queue=0`, `manual_review=0`, `waes_review=0`, `runtime_intake=0`, `verified=0`, `runtime_primary_key_ready=0`, `runtime_primary_key_missing=1`, `hold_items=1`, `open_holds=1`, `hold_release_allowed=0`, `precheck_items=1`, `blocked=1`, `blocked_reasons=6`, `release_allowed_items=0`; runtime SOP E2E still returns repair_required | GFIS runtime layer must be the subject |
| XiaoC | XiaoC-L4-009 | Ant queen task decomposition, model routing and dispatch plan | ready_for_review | pass | Does not write business facts or bypass WAES |
| XGD | XGD-L4-010 | Elephant risk analysis, reliability assessment and recommendation packet | ready_for_review | pass | Analysis only, no final approval |
| XiaoG | XiaoG-L4-011 | Ant execution terminal read-only query, PKC notice candidate and WAES audit mock | ready_for_review | pass | No production write, no device OTA, no real API write |
| WAES | GPCF-L4-001..012 | Governance center, evidence gate and audit status owner | ready_for_review | pass via contracts/mock evidence | Does not become business master data |

## P0 Chain Reconstruction

| Chain node | Project evidence |
|---|---|
| Project initialization | PVAOS-L4-006, MMC-L4-002 |
| Organization and partner onboarding | PVAOS-L4-006 |
| Platform order | GPC-L4-007 |
| Quote review and contract | GPC-L4-007 |
| Formula R&D and sample work order | GFIS-L4-008 requires runtime-layer repair |
| Customer sample approval | GPC-L4-007, WAES evidence gate contract |
| Production release gate | GPC-L4-007, MMC-L4-002, WAES evidence gate contract |
| Factory order and work order | GFIS-L4-008 requires runtime-layer repair |
| Quality, inventory and batch | GFIS-L4-008 requires runtime-layer repair |
| Shipment and POD boundary | GFIS-L4-008 requires runtime-layer repair, GPC-L4-007 |
| Exception and risk | XGD-L4-010, KDS-L4-003 |
| WAES evidence and audit | XiaoG-L4-011, GPCF-L4-012 |
| Daily review and knowledge deposition | Brain-L4-004, PKC-L4-005, KDS-L4-003 |
| Project-group closure | GPCF-L4-012 |

## Project Group 100 Point Score

| Metric | Max | Score | Evidence |
|---|---:|---:|---|
| 12 project coverage | 15 | 15 | All 12 projects have role, input, output, validation and evidence entry |
| P0 business chain continuity | 20 | 12 | GFIS runtime-layer SOP/E2E is blocked; Demo cannot carry factory runtime facts |
| Real repository code/config/test closure | 20 | 13 | GFIS Demo E2E is passed, KDS source path gaps are closed, runtime sample/evidence/handoff candidate contract validators pass, and the latest `CustomerRequirementOrPlatformOrder` dispatch confirmation post-scan hold gate is executable. It keeps `dispatch_authorizations=0`, `dispatch_allowed=0`, `dispatched_requests=0`, `expected_confirmation_files=1`, `confirmation_files_found=0`, `structure_valid_confirmations=0`, `valid_confirmations=0`, `invalid_confirmations=0`, `missing_confirmations=1`, `unexpected_files=0`, `acknowledged_requests=0`, `owner_response_allowed=0`, `submission_package_allowed=0`, `review_queue=0`, `manual_review=0`, `waes_review=0`, `runtime_intake=0`, `verified=0`, `runtime_primary_key_ready=0`, `runtime_primary_key_missing=1`, `hold_items=1`, `open_holds=1` and `hold_release_allowed=0`; runtime SOP E2E validator remains repair_required, so project-group score remains frozen |
| KDS retrieval and knowledge backlink completeness | 10 | 10 | L4-002 through L4-011 include KDS retrieval or controlled evidence backlinks |
| Evidence and audit completeness | 15 | 15 | Project-level evidence and GPCF evidence index cross-reference each other; WAES audit remains controlled mock for L4 |
| Cross-project contract consistency | 10 | 10 | Object contracts preserve GFIS/GPC/MMC/WAES/KDS/AI boundaries |
| User reproducibility and L5 readiness | 10 | 0 | L5 preparation is blocked until GFIS runtime repair and SOP E2E pass |
| Total | 100 | 79/100 | GFIS runtime repair required; previous 100/100 is invalidated |

## Required Non-Claims

- GFIS Demo is not a SOP implementation subject.
- GFIS Demo is not a business acceptance subject.
- GFIS Demo is not a substitute for GFIS runtime-layer DocTypes, workflows, permissions, reports, attachments or runtime APIs.
- No project is marked accepted.
- No project is marked integrated.
- No production deployment occurred.
- No production write occurred.
- No real external API write occurred.
- No permission or token change occurred.
- No device OTA occurred.
- L5 remains a separate, stronger authorization stage.

## Repair Requirement

L4 may not close at 100/100. The next stage is `GFIS-runtime-repair`: replace Demo-backed GFIS evidence with GFIS runtime-layer evidence, collect the KDS Gehua missing inputs, repair and pass SOP E2E, then rerun `validate_loop_self_correction_gate.py` and `validate_l4_minimum_closed_loop.py`.
